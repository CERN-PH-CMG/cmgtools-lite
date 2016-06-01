from ROOT import *

# Electrons
if False:
    tf = TFile("eleSF.root","READ")

    h1 = tf.Get("CutBasedTight")
    h2 = tf.Get("MiniIso0p1_vs_AbsEta")

    tf2 = TFile("eleSF_comb.root","RECREATE")

    h = h1.Clone("CBTight_MiniIso0p1_ACDV")
    h.Multiply(h2)

    h.Write()

    tf.Close()
    tf2.Close()

# Muons
if True:
    tf1 = TFile("TnP_MuonID_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta.root","READ")
    tf2 = TFile("TnP_MuonID_NUM_MiniIsoTight_DENOM_LooseID_VAR_map_pt_eta.root","READ")
    tf3 = TFile("TnP_MuonID_NUM_TightIP3D_DENOM_LooseID_VAR_map_pt_eta.root","READ")

    tf1.ls()
    h1 = tf1.Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_tag_IsoMu20_pass")
    h2 = tf2.Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_PF_pass_&_tag_IsoMu20_pass")
    h3 = tf3.Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_PF_pass_&_tag_IsoMu20_pass")

    tf = TFile("muSF_comb.root","RECREATE")
    h = h1.Clone("MediumID_MiniIso0p2_IP3D_ACDV")
    h.Multiply(h2)
    h.Multiply(h3)

    h.Write()

    tf1.Close()
    tf2.Close()
    tf3.Close()
    tf.Close()
