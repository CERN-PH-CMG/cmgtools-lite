import ROOT as r
from array import array
import sys, copy
import time
import os

#fileIn =Open("T2tt_results.root")
'''rootFilein=r.TFile.Open("T2tt_results.root")
graph=rootFilein.Get("ex_exp_smoothed_graph")
print graph
graph.Draw()
graph2=Transpose()
graph2.transposeGraph(graph)'''

#out=r.TFile("T2tt_results_tran.root","recreate")

#garph=r.f.Get("ex_exp_smoothed_graph")
class Transpose():
    def transposeHist(self,inHist):
        outName = inHist.GetName()
        binWidthX = 2*(inHist.GetXaxis().GetBinCenter(1)-inHist.GetXaxis().GetBinLowEdge(1))
        binWidthY = 2*(inHist.GetYaxis().GetBinCenter(1)-inHist.GetYaxis().GetBinLowEdge(1))
        xMass = [inHist.GetXaxis().GetBinCenter(x) for x in range(1,inHist.GetXaxis().GetNbins()+1)]
        yMass = [inHist.GetYaxis().GetBinCenter(y) for y in range(1,inHist.GetYaxis().GetNbins()+1)]
        xLow = [inHist.GetXaxis().GetBinLowEdge(x) for x in range(1,inHist.GetXaxis().GetNbins()+1)]
        yAxisTranspose = []
        for x in xMass:
            for y in yMass:
                if x-y >= binWidthY/2.:
                    yAxisTranspose.append(x-y-binWidthY/2.)
        minY = max(0,min(yAxisTranspose))
        maxY = max(yAxisTranspose)
        xAxis = array('d',xLow)
        yValue = minY
        yAxisTranspose = []
        while yValue <= maxY+binWidthY:
            yAxisTranspose.append(yValue)
            yValue += binWidthY
        yAxisTranspose = array('d',yAxisTranspose)
        outHist = r.TH2D(outName+"_transpose","",len(xAxis)-1,xAxis,len(yAxisTranspose)-1,yAxisTranspose)
        outHist.SetDirectory(0)
        for x in range(1,outHist.GetXaxis().GetNbins()+1):
            for y in range(1,outHist.GetYaxis().GetNbins()+1):
                value = inHist.GetBinContent(x,y)
                xValue,yValue = self.getBinCenter2D(x,y,inHist)
                newMass = xValue - yValue
                outHist.Fill(xValue,newMass,value)
        outHist.SetName(outName)
        return outHist

    def transposeGraph(self,graph):
        outputGraph = graph.Clone()
        outputSize = graph.GetN()
        outputX,outputY = array('d',[0.]*outputSize),array('d',[0.]*outputSize)
        tempX,tempY = r.Double(0.),r.Double(0.)
        for i in range(outputSize):
            graph.GetPoint(i,tempX,tempY)
            outputX[i],outputY[i] = tempX,tempX-tempY
        outputGraph = r.TGraph(outputSize,outputX,outputY)
        outputGraph.SetName(graph.GetName())
        return outputGraph

    def getBinCenter2D(self,x,y,hist):
        xValue = hist.GetXaxis().GetBinCenter(x)
        yValue = hist.GetYaxis().GetBinCenter(y)
        return xValue,yValue
    def save(self):
        print 'saving the UL histo and graphs in a file'
        f = r.TFile('tran.root','RECREATE')
        f.cd()
        self.transposeGraph(graph)        
        f.Write()
        
#rootFilein=r.TFile.Open("T2tt_results.root")

#out=r.TFile("T2tt_results_tran.root","recreate")
rootFilein=r.TFile.Open(" TChiNeuWZ_results.root")

out=r.TFile(" TChiNeuWZ_results_tran_m.root","recreate")
graph=rootFilein.Get("ex_exp_smoothed_graph")
graph_p1s=rootFilein.Get("ex_exp_p1s_smoothed_graph")
graph_m1s=rootFilein.Get("ex_exp_m1s_smoothed_graph")
graph_p2s=rootFilein.Get("ex_exp_p2s_smoothed_graph")
graph_m2s=rootFilein.Get("ex_exp_m2s_smoothed_graph")
graph_obs=rootFilein.Get("ex_obs_smoothed_graph")
graph_obs_p1s=rootFilein.Get("ex_obs_p1s_smoothed_graph")
graph_obs_m1s=rootFilein.Get("ex_obs_m1s_smoothed_graph")
#graph_obs_p2s=rootFilein.Get("ex_obs_p2s_smoothed_graph")
#graph_obs_m2s=rootFilein.Get("ex_obs_m2s_smoothed_graph")

print graph
graph.Draw()
graphtemp=Transpose()
graphtemp.transposeGraph(graph)
graphtemp_p1s=Transpose()
graphtemp_m1s=Transpose()
graphtemp_p2s=Transpose()
graphtemp_m2s=Transpose()
graphtemp_p1s.transposeGraph(graph_p1s)
graphtemp_m1s.transposeGraph(graph_m1s)
graphtemp_p2s.transposeGraph(graph_p2s)
graphtemp_m2s.transposeGraph(graph_m2s)
graphtemp_obs=Transpose()
graphtemp_obs_p1s=Transpose()
graphtemp_obs_m1s=Transpose()
#graphtemp_obs_p2s=Transpose()
#graphtemp_obs_m2s=Transpose()
graphtemp_obs.transposeGraph(graph_obs)
graphtemp_obs_p1s.transposeGraph(graph_obs_p1s)
graphtemp_obs_m1s.transposeGraph(graph_obs_m1s)
#graphtemp_obs_p2s.transposeGraph(graph_obs_p2s)
#graphtemp_obs_m2s.transposeGraph(graph_obs_m2s)
out.cd()
print os.system('pwd')

graph2=r.TGraph()
graph2=graphtemp.transposeGraph(graph)
graph_p1s2=r.TGraph()
graph_p1s2=graphtemp.transposeGraph(graph_p1s)
graph_m1s2=r.TGraph()
graph_m1s2=graphtemp.transposeGraph(graph_m1s)
graph_p2s2=r.TGraph()
graph_p2s2=graphtemp.transposeGraph(graph_p2s)
graph_m2s2=r.TGraph()
graph_m2s2=graphtemp.transposeGraph(graph_m2s)

graph_obs2=r.TGraph()
graph_obs2=graphtemp_obs.transposeGraph(graph_obs)
graph_obs_p1s2=r.TGraph()
graph_obs_p1s2=graphtemp.transposeGraph(graph_obs_p1s)
graph_obs_m1s2=r.TGraph()
graph_obs_m1s2=graphtemp.transposeGraph(graph_obs_m1s)
#graph_obs_p2s2=r.TGraph()
#graph_obs_p2s2=graphtemp.transposeGraph(graph_obs_p2s)
#graph_obs_m2s2=r.TGraph()
#graph_obs_m2s2=graphtemp.transposeGraph(graph_obs_m2s)

#ut=r.TFile("T2tt_results_tran.root","recreate")
c = r.TCanvas("cABS" ,"cABS" ,300,300)
graph2.Draw()
print os.system('pwd')
graph2.Write()
graph_p1s2.Write()
graph_m1s2.Write()
graph_p2s2.Write()
graph_m2s2.Write()
graph_obs2.Write()
graph_obs_p1s2.Write()
graph_obs_m1s2.Write()
#graph_obs_p2s2.Write()
#graph_obs_m2s2.Write()
graph2.SaveAs("trans_expected.pdf")
graph_obs2.SaveAs("test.root")
graphtemp.save()
#time.sleep(5.5) 
