from array import *

class sms():

    def __init__(self, modelname):
        if modelname.find("T1tttt") != -1: self.T1tttt()
        #if modelname.find("T6bbsleptonMET150") != -1: self.T6bbsleptonMET150()
        #if modelname.find("T6bbslepton") != -1: self.T6bbslepton()
        if modelname == "T6bbsleptonMET150": self.T6bbsleptonMET150()
        if modelname == "T6bbslepton": self.T6bbslepton()
        if modelname.find("T5ttttDM175") != -1: self.T5ttttDM175()
        if modelname.find("T1bbbb") != -1: self.T1bbbb()
        if modelname.find("TChiNeuWZ") != -1: self.TChiNeuWZ()
        if modelname.find("T2tt") != -1: self.T2tt()
        if modelname.find("T1qqqq") != -1: self.T1qqqq()


    def T2tt(self):
        # model name
        self.modelname = "T2tt"
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{t} #tilde{t}, #tilde{t} #rightarrow bff #tilde{#chi}^{0}_{1}"
        self.label2= ""
        # scan range to plot
        self.Xmin = 250.
        self.Xmax = 400.
        self.Ymin =  10.
        self.Ymax =  102.#102
        self.Zmin = 1#0.0001
        self.Zmax =100 #0.01   
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{ #tilde{t}}}} [GeV]"
        # LSP
        #self.LSP = "#Delta m#kern[0.1]{_{#tilde{t},#tilde{#chi}^{0}_{1}}} [GeV]"
        self.LSP = "#Delta m ( #tilde{t}, #tilde{#chi}^{0}_{1} ) [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagX = array('d',[100,250])
        self.diagY = array('d',[ 93,243])

    def TChiNeuWZ(self):
        # model name
        self.modelname = "TChiNeuWZ"
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{#chi}_{2}^{0} #tilde{#chi}_{1}^{#pm}, #tilde{#chi}_{2}^{0} #rightarrow Z #tilde{#chi}^{0}_{1}, #tilde{#chi}_{1}^{#pm} #rightarrow W #tilde{#chi}^{0}_{1}"
        self.label2= ""
        # scan range to plot
        self.Xmin = 100.
        self.Xmax = 220.
        self.Ymin =   7.
        self.Ymax =  50.#50
        self.Zmin = 0.1#0.1
        self.Zmax = 10#10.   
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{#chi}^{0}_{2}, #tilde{#chi_{1}}^{#pm}   }}} [GeV]"
        # LSP
        #self.LSP = "m#kern[0.1]{_{#tilde{#chi}^{0}_{1}}} [GeV]"
        self.LSP = "#Delta m ( #tilde{#chi}^{0}_{2},#tilde{#chi}^{0}_{1} ) [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        self.diagX = array('d',[100,250])
        self.diagY = array('d',[ 93,243])

    def T6bbslepton(self):
        # model name
        self.modelname = "T6bbslepton"
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{b} #tilde{b}, #tilde{b} #rightarrow b #tilde{#chi}^{0}_{2}, #tilde{#chi}^{0}_{2} #rightarrow #tilde{l} l, #tilde{l} #rightarrow l #tilde{#chi}^{0}_{1}"
        self.label2= "#tilde{#chi}^{0}_{1} = 100 GeV";
        # scan range to plot
        self.Xmin = 400.
        self.Xmax = 900.
        self.Ymin = 200.
        self.Ymax = 900.
        self.Zmin = 0.1
        self.Zmax = 0.5
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{b}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{#tilde{#chi}^{0}_{2}}} [GeV]"
        # turn off diagonal lines
        self.diagOn = True
        self.diagX = array('d',[400,600,900])
        self.diagY = array('d',[212.5,412.5,712.5])

    def T6bbsleptonMET150(self):
        # model name
        self.modelname = "T6bbsleptonMET150"
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{b} #tilde{b}, #tilde{b} #rightarrow b #tilde{#chi}^{0}_{2}, #tilde{#chi}^{0}_{2} #rightarrow #tilde{l} l, #tilde{l} #rightarrow l #tilde{#chi}^{0}_{1}"
        self.label2= "#tilde{#chi}^{0}_{1} = 100 GeV";
        # scan range to plot
        self.Xmin = 400.
        self.Xmax = 900.
        self.Ymin = 200.
        self.Ymax = 900.
        self.Zmin = 0.05
        self.Zmax = 0.3
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{b}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{#tilde{#chi}^{0}_{2}}} [GeV]"
        # turn off diagonal lines
        self.diagOn = True
        self.diagX = array('d',[400,600,900])
        self.diagY = array('d',[212.5,412.5,712.5])

    def T1tttt(self):
        # model name
        self.modelname = "T1tttt"
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow t #bar{t} "+lsp_s;
        self.label2= "";
        # scan range to plot
        self.Xmin = 700.
        self.Xmax = 1950.
        self.Ymin = 0.
        self.Ymax = 1800.
        self.Zmin = 0.001
        self.Zmax = 2.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{g}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        
    def T5ttttDM175(self):
        # model name
        self.modelname = "T5ttttDM175"
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{g} #tilde{g},  #tilde{g} #rightarrow #tilde{t}_{1} t,  #tilde{t}_{1} #rightarrow #bar{t} "+lsp_s;
        self.label2= "m_{#tilde{t}_{1}} - m_{#tilde{#chi}^{0}_{1}} = 175 GeV";
        # scan range to plot
        self.Xmin = 600.
        self.Xmax = 1700.
        self.Ymin = 0.
        self.Ymax = 1800.
        self.Zmin = 0.001
        self.Zmax = 2.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{g}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
        
    def T1bbbb(self):
        # model name
        self.modelname = "T1bbbb"
        # decay chain
        lsp_s = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow b #bar{b} "+lsp_s;
        self.label2= "";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600.
        self.Xmax = 1950.
        self.Ymin = 0.
        self.Ymax = 1800.
        self.Zmin = 0.001
        self.Zmax = 2.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{g}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False

    def T1qqqq(self):
        # model name
        self.modelname = "T1qqqq"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow q #bar{q} #tilde{#chi}^{0}_{1}";
        self.label2= "";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600.
        self.Xmax = 1950.
        self.Ymin = 0.
        self.Ymax = 1600.
        self.Zmin = 0.001
        self.Zmax = 2.
        # produce sparticle
        self.sParticle = "m#kern[0.1]{_{#lower[-0.12]{#tilde{g}}}} [GeV]"
        # LSP
        self.LSP = "m#kern[0.1]{_{"+lsp_s+"}} [GeV]"
        # turn off diagonal lines
        self.diagOn = False
