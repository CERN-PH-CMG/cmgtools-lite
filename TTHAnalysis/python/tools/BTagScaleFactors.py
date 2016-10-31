import os

import ROOT
#################################################################
# This is mostly copy pasted from Lorenzo Bianchini:
# https://github.com/bianchini/cmssw/blob/LB_newbtagSF/VHbbAnalysis/Heppy/python/btagSF.py
#
# Load the BTagCalibrationStandalone.cc macro from
# https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration
# and compile it:
# cmsenv
# g++ -c -o BTagCalibrationStandalone.so -L${ROOTSYS}/lib $CMSSW_RELEASE_BASE/src/CondTools/BTau/test/BTagCalibrationStandalone.cpp `root-config --cflags` `root-config --libs`
#
# Get the current scale factor files from: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80X
#################################################################
from ROOT import gSystem

gSystem.Load(os.path.join(os.path.dirname(__file__), 'BTagCalibrationStandalone.so'))
from ROOT import BTagCalibration, BTagCalibrationReader

def get_allowed_ranges(csvfile):
    """Extracts the allowed ranges and systematics from the csv file"""
    from csv import DictReader
    ranges = {}
    with open(csvfile, 'r') as infile:
        # Remove spaces from field headers
        firstline = infile.readline()
        headers = [k.strip() for k in firstline.split(',')]
        if not len(headers) == 11:
            headers = [k.strip() for k in firstline.split(' ')]
        opfield = 'CSVv2;OperatingPoint'
        if not opfield in headers: opfield = 'cMVAv2;OperatingPoint'
        if not opfield in headers: opfield = 'CSV;OperatingPoint'

        reader = DictReader(infile, fieldnames=headers)
        for row in reader:
            key = (int(row[opfield].strip()),
                   row['measurementType'].strip(),
                   row['sysType'].strip(),
                   int(row['jetFlavor'].strip()))
            ranges.setdefault(key, {})
            for var in ['eta', 'pt', 'discr']:
                mini = float(row['%sMin'%var].strip())
                maxi = float(row['%sMax'%var].strip())
                ranges[key]['%sMin'%var] = min(ranges[key].setdefault('%sMin'%var, mini), mini)
                ranges[key]['%sMax'%var] = max(ranges[key].setdefault('%sMax'%var, maxi), maxi)
    return ranges

def relevant_iterative_systs(flavor, syst):
    """Returns true if a flavor/syst combination is relevant"""
    if flavor==0:
        return syst in ["central",
                        "up_jes", "down_jes",
                        "up_lf", "down_lf",
                        "up_hfstats1", "down_hfstats1",
                        "up_hfstats2", "down_hfstats2"]
    elif flavor==1:
        return syst in ["central",
                        "up_cferr1", "down_cferr1",
                        "up_cferr2", "down_cferr2" ]
    elif flavor==2:
        return syst in ["central",
                        "up_jes", "down_jes",
                        "up_hf", "down_hf",
                        "up_lfstats1", "down_lfstats1",
                        "up_lfstats2", "down_lfstats2" ]
    return True

class BTagScaleFactors(object):
    """Calculate btagging scale factors
        algo has to be either 'csv' or 'cmva'
    """
    def __init__(self, name,
                 csvfile,
                 csvfastsim=None,
                 eff_rootfile=None,
                 algo='csv',
                 verbose=0):
        self.name = name
        self.csvfile = csvfile
        self.csvfastsim = csvfastsim
        self.eff_rootfile = eff_rootfile
        self.verbose = verbose
        self.algo = algo.lower()

        if not self.algo in ['csv', 'cmva']:
            print "ERROR: Unknown algorithm. Choose either 'csv' or 'cmva'"
            return

        self.working_points = {
            "L" : 0.460,
            "M" : 0.800,
            "T" : 0.935,
        }

        if self.algo == 'cmva':
            self.working_points = {
                "L" : -0.715,
                "M" :  0.185,
                "T" :  0.875,
            }

        self.mtypes = {
            # Measurement type for each flavor
            0 : "comb", # b
            1 : "comb", # c
            2 : "incl", # light
        }
        if self.algo == 'cmva':
            self.mtypes[0] = 'ttbar'
            self.mtypes[1] = 'ttbar'

        self.iterative_systs = ['jes',
                                'lf', 'hf',
                                'hfstats1', 'hfstats2',
                                'lfstats1', 'lfstats2',
                                'cferr1', 'cferr2' ]

        self.init()
        self.create_readers()
        self.not_found = set()

    def init(self):
        if self.verbose>0:
            print "Initializing btag calibrator from %s" % self.csvfile
        self.allowed = get_allowed_ranges(self.csvfile)
        self.calibrator = BTagCalibration(self.name, self.csvfile)

        if self.csvfastsim:
            if self.verbose>0:
                print "Initializing fastsim btag calibrator from %s" % self.csvfastsim
            self.calibrator_fastsim = BTagCalibration("%s_fastsim"%self.name,
                                                      self.csvfastsim)
            self.allowed.update(get_allowed_ranges(self.csvfastsim))

        if self.eff_rootfile:
            if self.verbose>0:
                print "Reading tagging efficiencies from %s" % self.eff_rootfile
            self.load_tagging_efficiencies(self.eff_rootfile)

    def load_tagging_efficiencies(self, filename):
        from ROOT import TFile
        ifile = TFile.Open(filename, "READ")
        self.efficiency_hists = {}
        for wp in ["L", "M", "T"]:
            for flavor in ["b", "c", "udsg"]:
                key = "eff_TT_%s_%s" % (wp, flavor)
                hist = ifile.Get(key)
                try: hist.GetEntries()
                except AttributeError:
                    print "histogram %s not found in %s" % (key, filename)
                self.efficiency_hists[(wp, flavor)] = hist.Clone()
                self.efficiency_hists[(wp, flavor)].SetDirectory(0)

    def get_tagging_efficiency(self, jet, wp="L"):
        flavor = {5:"b", 4:"c"}.get(jet.hadronFlavour, "udsg")
        binno = self.efficiency_hists[(wp, flavor)].FindBin(jet.pt, abs(jet.eta))
        return self.efficiency_hists[(wp, flavor)].GetBinContent(binno)


    def check_range(self, csvop, mtype, stype, flavor, pt, eta, discr):
        """Check if a given pt, eta, and discriminator output are in the allowed range
        Call this inside a try/except KeyError block to check if a given
        wp/mtype/syst/flavor combination exists.

        Eta is changed to abs(eta) for checking the range.

        Note: for fastsim use mtype 'fastsim'
        """
        allowed_range = self.allowed[(csvop, mtype, stype, flavor)]

        eta = abs(eta)
        allowed = all([
                eta   >= allowed_range['etaMin'],   eta   <= allowed_range['etaMax'],
                pt    >= allowed_range['ptMin'],    pt    <= allowed_range['ptMax'],
                discr >= allowed_range['discrMin'], discr <= allowed_range['discrMax'],
            ])

        if not allowed and self.verbose>2:
            print 'pt    %6.1f <? %6.1f <? %6.1f' % (allowed_range['ptMin'],    pt,    allowed_range['ptMax'])
            print 'eta   %4.1f <? %4.1f <? %4.1f' % (allowed_range['etaMin'],   eta,   allowed_range['etaMax'])
            print 'discr %4.1f <? %4.1f <? %4.1f' % (allowed_range['discrMin'], discr, allowed_range['discrMax'])

        return allowed

    def create_readers(self):
        if self.verbose>0:
            print "Setting up btag calibration readers"
        self.readers = {}

        # Create empty vector for systematics.
        # It would be better to create a single reader, as pointed out here https://hypernews.cern.ch/HyperNews/CMS/get/btag/1341.html , but this would mean reworking this whole module. 
        # For now, adopted the quicker solution. Will implement the full one in a longer timescale. P.
        v_sys = getattr(ROOT, 'vector<string>')()

        for wp in [0, 1, 2]:
            for syst in ['central', 'up', 'down', 'up_correlated', 'down_correlated']:
                for flavor in [0, 1, 2]:
                    self.readers[(self.mtypes[flavor], wp, syst, flavor)] = BTagCalibrationReader(
                                                        wp,
                                                        syst,
                                                        v_sys
                                                        )
                    self.readers[(self.mtypes[flavor], wp, syst, flavor)].load(
                                                        self.calibrator,
                                                        flavor,
                                                        self.mtypes[flavor]
                                                        )

                    if self.csvfastsim and 'correlated' not in syst:

                        self.readers[('fastsim', wp, syst, flavor)] = BTagCalibrationReader(
                                                        wp,
                                                        syst,
                                                        v_sys
                                                        )
                        self.readers[('fastsim', wp, syst, flavor)].load(
                                                        self.calibrator_fastsim,
                                                        flavor,
                                                        'fastsim'
                                                        )


        allsysts =  ["up_%s"%s for s in self.iterative_systs]
        allsysts += ["down_%s"%s for s in self.iterative_systs]
        allsysts += ["central"]
        for syst in allsysts:
            v_iterativefit_sys = getattr(ROOT, 'vector<string>')()
            #v_iterativefit_sys.push_back(syst)
            self.readers[('iterative', syst)] = BTagCalibrationReader(
                                                    3,
                                                    syst,
                                                    v_iterativefit_sys
                                                    )
            self.readers[('iterative', syst)].load(
                                                 self.calibrator,
                                                 0 ,#..., #flavour
                                                 'iterativefit'
                                                 )



    def get_SF(self, pt=30., eta=0.0, flavor=5, val=0.0,
               syst="central", wp="M", mtype='auto',
               shape_corr=False):
        """Evaluate the scalefactors.
            Note the flavor convention: hadronFlavor is b=5, c=4, f=0
            Convert them to the btagging group convention of 0,1,2

            Same for working points: input is "L", "M", "T"
            Convert to 0, 1, 2

            Automatically checks if values are in allowed range

            Use mtype='fastsim' for fastsim SFs

            If unknown wp/syst/mtype/flavor, returns -1.0
        """

        raise RuntimeError, 'BTagScaleFactors.py: some weights were observed to be set to zero. This should be fixed before the module can be used.'

        flavor_new = {5:0, 4:1, 0:2}.get(flavor, None)
        if flavor_new == None:
            if self.verbose>0:
                print "Unknown flavor %s, no btagging SF evaluated!" % repr(flavor)
            return -1.0
        flavor = flavor_new

        if shape_corr: wp = "M"
        wp_new = wp.lower()
        wp_new = {"l":0, "m":1, "t":2}.get(wp_new, None)
        if wp_new == None:
            if self.verbose>0:
                print "Unknown working point %s, no btagging SF evaluated!" % repr(wp)
            return -1.0
        wp = wp_new

        syst = syst.lower()

        if mtype == 'auto':
            mtype = self.mtypes[flavor]
        if shape_corr:
            wp = 3
            mtype = 'iterativefit'

        try:
            self.check_range(wp, mtype, syst, flavor, pt, eta, val)
        except KeyError:
            if shape_corr and relevant_iterative_systs(flavor, syst):
                self.not_found.add((wp, mtype, syst, flavor))
                if self.verbose>1:
                    print ("Warning: wp/mtype/syst/flavor combination not in csv file: (%s/%s/%s/%s)"
                           "\n scale factor not evaluated" %
                                     (repr(wp), repr(mtype), repr(syst), repr(flavor)))
                return 1.0


        # no SF for pT<20 GeV or pt>1000 or abs(eta)>2.4
        if abs(eta)>2.4 or pt>1000. or pt<20.:
            return 1.0

        if shape_corr:
            if relevant_iterative_systs(flavor, syst):
                return self.readers[("iterative", syst)].eval_auto_bounds(syst, flavor, eta, pt, val)
            else:
                return self.readers[("iterative", "central")].eval_auto_bounds('central', flavor, eta, pt, val)

        # pt ranges for bc SF: needed to avoid out_of_range exceptions
        pt_max = self.allowed[(wp, mtype, syst, flavor)]['ptMax']
        pt_min = self.allowed[(wp, mtype, syst, flavor)]['ptMin']
        out_of_range = False
        if pt > pt_max or pt < pt_min:
            out_of_range = True
            pt = min(pt, pt_max - 0.01)
            pt = max(pt, pt_min + 0.01)

        # pt_max = 670.-1e-02 if "CSV" in algo else 320.-1e-02
        # pt_min = 30.+1e-02

        if flavor < 2: # b or c jets
            sf = self.readers[(self.mtypes[flavor], wp, syst, flavor)].eval_auto_bounds(syst, flavor, eta, pt)

            # double the error for pt out-of-range
            if out_of_range and syst in ["up","down"]:
                sf = max(2*sf - self.readers[(self.mtypes[flavor], wp, "central", flavor)].eval_auto_bounds('central', flavor, eta, pt), 0.)

            # Fastsim SFs are 0.0 for pt between 20 and 30
            return sf if sf != 0.0 else 1.0

        else: # light jets
            sf = self.readers[(self.mtypes[flavor], wp, syst, flavor)].eval_auto_bounds(syst, flavor, eta, pt)
            return sf if sf != 0.0 else 1.0

#################################################################
def testing():
    csvpath = os.path.join(os.environ['CMSSW_BASE'],"src/CMGTools/TTHAnalysis/data/btag/")
    test_for = [

        #BTagScaleFactors("CSV", os.path.join(csvpath, "CSVv2_ichep.csv"),  algo='csv', verbose=1),
        BTagScaleFactors("CSV", os.path.join(csvpath, "CSVv2_4invfb.csv"),  algo='csv'),
        # BTagScaleFactors("MVA", os.path.join(csvpath, "cMVAv2_4invfb.csv"), algo='cmva')
    ]

    print "POG WP:"
    for sfs in test_for:
        print sfs.name,":"
        for wp in [ "L", "M", "T" ]:
            print wp+":"
            for syst in ["central", "up", "down"]:
                print "\t"+syst+":"
                for pt in [19.,25.,31.,330., 680.]:
                    print ("\t\tB(pt=%.0f, eta=0.0): %.3f" % (pt, sfs.get_SF(pt=pt, eta=0.0, flavor=5, val=0.0,
                                                              syst=syst, wp=wp)))
                    print ("\t\tC(pt=%.0f, eta=0.0): %.3f" % (pt, sfs.get_SF(pt=pt, eta=0.0, flavor=4, val=0.0,
                                                              syst=syst, wp=wp)))
                    print ("\t\tL(pt=%.0f, eta=0.0): %.3f" % (pt, sfs.get_SF(pt=pt, eta=0.0, flavor=0, val=0.0,
                                                              syst=syst, wp=wp)))

    print "Iterative:"
    for sfs in test_for:
        print sfs.name,":"
        for syst in ["central",
                     "up_jes", "down_jes",
                     "up_lf", "down_lf",
                     "up_hf", "down_hf",
                     "up_hfstats1", "down_hfstats1",
                     "up_hfstats2", "down_hfstats2",
                     "up_lfstats1", "down_lfstats1",
                     "up_lfstats2", "down_lfstats2",
                     "up_cferr1", "down_cferr1",
                     "up_cferr2", "down_cferr2"]:
            print "\t"+syst+":"
            for pt in [50.]:
                print ("\t\tB(pt=%.0f, eta=0.0): %.3f" % (pt, sfs.get_SF(pt=pt, eta=0.0, flavor=5, val=0.89,
                                                          syst=syst, shape_corr=True)))
                print ("\t\tC(pt=%.0f, eta=0.0): %.3f" % (pt, sfs.get_SF(pt=pt, eta=0.0, flavor=4, val=0.89,
                                                          syst=syst, shape_corr=True)))
                print ("\t\tL(pt=%.0f, eta=0.0): %.3f" % (pt, sfs.get_SF(pt=pt, eta=0.0, flavor=0, val=0.89,
                                                          syst=syst, shape_corr=True)))

    if len(sfs.not_found):
        from pprint import pprint
        print "The following wp/mtype/syst/flavor combinations were requested but not found:"
        pprint(sfs.not_found)

debug = False
if debug: testing()
