#!/usr/bin/env python                                                                                                                                                                                              
import sys, os
import numpy as np
import ROOT  as r
import pickle
from math import log10
from tabulate import tabulate
sys.path.append(os.environ['CMSSW_BASE']+ '/CMGTools/python/plotter/ttH-modules/')

from signalExtractionHarvestingConfigs import processes, signals, procswithdecays, processes_name, process_order



from optparse import OptionParser
parser = OptionParser()

def readNominalAndToys(nominalFile, toyexp, fit='fit_s',readFromPickle=False):
    if readFromPickle:
        results = pickle.load(open('save_%s.p'%fit))
        data = pickle.load(open('data.p'))
        return results, data

    results={}; data={}
    tf = r.TFile.Open(nominalFile)
    cats=[key.GetName() for key in tf.Get('shapes_%s'%fit).GetListOfKeys()]
    for proc in processes:
        results[proc]={}
        results[proc]['nom']={}
        for cat in cats:
            results[proc]['nom'][cat]=None
            for comp in processes[proc]:
                for compwithdecay in ([comp] if comp not in procswithdecays else ['%s_%s'%(comp,x) for x in ["hww", "hzz", "htt"]]):
                    hist = tf.Get('shapes_%s/%s/%s'%(fit,cat,compwithdecay))
                    if not hist: continue
                    thehist=hist.Clone('shapes_%s_%s_%s'%(fit,cat,compwithdecay)); thehist.SetDirectory(None)
                    if not results[proc]['nom'][cat]:
                        results[proc]['nom'][cat]=thehist
                    else:
                        results[proc]['nom'][cat].Add(thehist)

        for toy in range(100):
            results[proc]['toy_%d'%toy]={}
            for cat in cats:
                results[proc]['toy_%d'%toy][cat]=None
    # also take the chance to read data                                                                                                                                                                            
    for cat in cats:
        data_obs=tf.Get('shapes_%s/%s/data'%(fit,cat))
        # get the binning from another random process                                                                                                                                                              
        data_hist=None
        for proc in results:
            if results[proc]['nom'][cat]:
                data_hist=results[proc]['nom'][cat].Clone('data_%s_%s'%(fit,cat)); data_hist.SetDirectory(None)
                data_hist.Reset()
                break
        if not data_hist:
            raise RuntimeError("tried to get that with a category with no process...")
        bin=1
        for y in data_obs.GetY():
            data_hist.SetBinContent(bin, y)
            bin=bin+1
        data[cat]=data_hist

    pickle.dump( data, open('data.p','w'))

    tf.Close()



    for toy in range(100):
        print 'reading toy %d'%toy
        tftoy=r.TFile.Open(toyexp.format(toy=toy,fit=fit))
        for proc in processes:
            for cat in cats:
                for comp in processes[proc]:
                    for compwithdecay in ([comp] if comp not in procswithdecays else ['%s_%s'%(comp,x) for x in ["hww", "hzz", "htt"]]):
                        hist = tftoy.Get('n_exp_final_bin%s_proc_%s'%(cat,compwithdecay))
                        if not hist:
                            hist = tftoy.Get('n_exp_bin%s_proc_%s'%(cat,compwithdecay))
                            if not hist:
                                continue
                        thehist=hist.Clone('shapes_%s_%s_%s_toy%s'%(fit,cat,compwithdecay,toy)); thehist.SetDirectory(None)
                        if not results[proc]['toy_%d'%toy][cat]:
                            results[proc]['toy_%d'%toy][cat]=thehist
                        else:
                            results[proc]['toy_%d'%toy][cat].Add(thehist)
        tftoy.Close()
    results['total_signal']={}
    results['total background']={}
    for what in ['nom']+['toy_%d'%toy for toy in range(100)]:
        results['total_signal'][what]={}
        results['total background'][what]={}

    # build total sums now                                                                                                                                                                                         
    for cat in cats:
        for what in ['nom']+['toy_%d'%toy for toy in range(100)]:
            results['total_signal'][what][cat]=None
            results['total background'][what][cat]=None
            for proc in processes:
                if proc in signals:
                    group='total_signal'
                else:
                    group='total background'
                if not results[group][what][cat]:
                    if results[proc][what][cat]:
                        results[group][what][cat] = results[proc][what][cat].Clone('shapes_%s_%s_%s'%(group, what,cat))
                else:
                    if results[proc][what][cat]:
                        results[group][what][cat].Add( results[proc][what][cat] )

    pickle.dump( results, open('save_%s.p'%fit,'w'))
    print data
    return results, data


def stackByMapping(results, data, regionMapping, picklename, readFromPickle=False):
    if readFromPickle:
        results = pickle.load(open('save_%s.p'%picklename))
        data = pickle.load(open('data_%s.p'%picklename))
        return results, data

    stacked_data={}; stacked_results={}
    for cat in regionMapping:
        print 'doing', cat
        for proc in [x for x in processes] + ['total_signal','total background']:
            if proc not in stacked_results:
                stacked_results[proc]={}
            for what in ['nom']+['toy_%d'%toy for toy in range(100)]:
                if what not in stacked_results[proc]:
                    stacked_results[proc][what]={}
                stacked_results[proc][what][cat]=None
                for year in regionMapping[cat]:
                    if not results[proc][what][year]:
                        continue
                    if not stacked_results[proc][what][cat]:
                        stacked_results[proc][what][cat] = results[proc][what][year].Clone('%s_%s_%s'%(proc, what,cat))
                    else:
                        stacked_results[proc][what][cat].Add(results[proc][what][year])
        stacked_data[cat]=None
        for year in regionMapping[cat]:
            if not stacked_data[cat]:
                stacked_data[cat]=data[year].Clone('data_%s'%cat)
            else:
                stacked_data[cat].Add(data[year].Clone('data_%s'%cat))
    print 'writing'
    pickle.dump( stacked_results, open('save_%s.p'%picklename,'w') )
    pickle.dump( stacked_data   , open('data_%s.p'%picklename,'w') )
    return results,data

def tableToNumbers(results, data, regionMapping):
    for cat in regionMapping:
        for proc in [x for x in processes] +['total_signal','total background']:
            for what in ['nom']+['toy_%d'%toy for toy in range(100)]:
                if results[proc][what][cat]:
                    results[proc][what][cat] = results[proc][what][cat].Integral()
        data[cat]=data[cat].Integral()

def getSoverB(results, data, regionMapping, signals):
    points={}
    for what in ['nom']+['toy_%d'%toy for toy in range(100)]:
        points[what]=[]
        for cat in regionMapping:
            for bin in range(1,data[cat].GetNbinsX()+1):
                bkg=0; sigs={}
                data_obs=data[cat].GetBinContent(bin)
                tot_sig=0
                for proc in [x for x in processes]:
                    if proc in signals:
                        if results[proc][what][cat]:
                            tot_sig+=max(0,results[proc][what][cat].GetBinContent(bin))
                            sigs[proc]=results[proc][what][cat].GetBinContent(bin)
                    else:
                        if results[proc][what][cat]:
                            bkg=bkg+results[proc][what][cat].GetBinContent(bin)
                if bkg>0 and log10(tot_sig/bkg)>0:
                    print what, cat, bin, bkg, tot_sig
                points[what].append((cat,bin, data_obs,bkg,sigs))
    return points

def buildRms(results, data, regionMapping):
    for proc in [x for x in processes]+['total_signal','total background']:
        results[proc]['up']={}; results[proc]['dn']={}
        for cat in regionMapping:
            toyvalues = []
            for what in ['toy_%d'%toy for toy in range(100)]:
                if results[proc][what][cat]:
                    toyvalues.append( results[proc][what][cat] )
            if len(toyvalues) not in [0,100]:
                print 'number of toys are', len(toyvalues), 'for proc cat', proc, cat
                raise RuntimeError("Theres something wrong")
            if not len(toyvalues) and results[proc]['nom'][cat]:
                # theres nominal but not variations...
                print proc, cat, results[proc]['nom'][cat]
                raise RuntimeError("Theres something wrong")
            if len(toyvalues)==100:
                dn = np.percentile(np.array(toyvalues), 16)
                up = np.percentile(np.array(toyvalues), 84)
                
                results[proc]['up'][cat]=(up-dn)/2
                results[proc]['dn'][cat]=(up-dn)/2
            for what in ['toy_%d'%toy for toy in range(100)]:
                del results[proc][what][cat]

def makeTable(regions, results, data):
    header=['Process']
    for cat in regions:
        header.append(cat)
    table=[header]

    for proc in process_order:
        line=[processes_name[proc]]
        for cat in regions:
            nom=results[proc]['nom'][cat]
            if nom and nom >0.1:
                up=results[proc]['up'][cat]
                dn=results[proc]['dn'][cat]
                line.append('$%4.1f \pm %4.1f $'%(nom, up))
            else:
                line.append('$<$0.1')
        table.append(line)
    line=['Data']
    for cat in regions:
        line.append('%d'%data[cat])
    table.append(line)
    print tabulate(table, tablefmt='latex_raw')
