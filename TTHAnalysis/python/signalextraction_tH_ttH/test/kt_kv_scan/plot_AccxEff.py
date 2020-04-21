import sys
import os
import re
import multiprocessing
import numpy as np
import glob
import ROOT as rt
rt.gStyle.SetOptStat(0)
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.font_manager import FontProperties
from matplotlib import rc

year = '2018'
lumi = {'2016':35.9,'2017':41.4,'2018':59.7}

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

#dic with cards ordered by ratio
cards = {0.0: ['kt_0p0_kv_1p0'], 0.25: ['kt_0p25_kv_1p0'], 2.0: ['kt_2p0_kv_1p0'], 3.0: ['kt_3p0_kv_1p0'], 4.0: ['kt_2p0_kv_0p5'], 6.0: ['kt_3p0_kv_0p5'], 1.0: ['kt_1p0_kv_1p0'], -1.3333333333333333: ['kt_m2p0_kv_1p5'], -0.75: ['kt_m0p75_kv_1p0'], 0.16666666666666666: ['kt_0p25_kv_1p5'], -0.3333333333333333: ['kt_m0p5_kv_1p5'], -0.5: ['kt_m0p5_kv_1p0'], 0.5: ['kt_0p5_kv_1p0'], 0.8333333333333334: ['kt_1p25_kv_1p5'], -0.16666666666666666: ['kt_m0p25_kv_1p5'], -1.25: ['kt_m1p25_kv_1p0'], 1.25: ['kt_1p25_kv_1p0'], 1.5: ['kt_1p5_kv_1p0'], -1.5: ['kt_m1p5_kv_1p0'], 1.3333333333333333: ['kt_2p0_kv_1p5'], -0.8333333333333334: ['kt_m1p25_kv_1p5'], -2.5: ['kt_m1p25_kv_0p5'], 2.5: ['kt_1p25_kv_0p5'], -0.6666666666666666: ['kt_m1p0_kv_1p5'], 0.75: ['kt_0p75_kv_1p0'], -2.0: ['kt_m2p0_kv_1p0'], 0.6666666666666666: ['kt_1p0_kv_1p5'], -6.0: ['kt_m3p0_kv_0p5'], -0.25: ['kt_m0p25_kv_1p0'], -4.0: ['kt_m2p0_kv_0p5'], -3.0: ['kt_m3p0_kv_1p0'], -1.0: ['kt_m1p0_kv_1p0'], 0.3333333333333333: ['kt_0p5_kv_1p5']}


def print_header(axes, x_low, x_high, y_low, y_high, inside = False, logscale = False):
  y_val = y_high + 0.06 * (y_high - y_low)
  if inside:
    axes.text(x_low + abs(x_low) * 0.045, y_high - 0.46 * (y_high - y_low), 'CMS', style='normal', fontsize=15, fontweight='bold')
  else:
    axes.text(x_low, y_val, r'$\textbf{CMS}$', style='normal', fontsize=12, fontweight='bold') # 15 for a 6 X 6 figure
  #axes.text(x_low + (x_high - x_low) * 0.14, y_val, 'Preliminary', fontsize=15, style='italic') # for a 6 X 6 figure
  axes.text(x_low + (x_high - x_low) * 0.12, y_val, r'$\textit{Simulation Preliminary}$', fontsize=12, style='italic') # for a 5 X 5 figure
  if logscale:
    axes.text(x_low + (x_high - x_low) * 0.85, y_high + 0.05 * (y_high - y_low), '(13 TeV)', fontsize=10)
  else:
    axes.text(x_low + (x_high - x_low) * 0.85, y_high + 0.01 * (y_high - y_low), '(13 TeV)', fontsize=10)
 

def read_dcard(cardfile,channel,process):
       f = rt.TFile(cardfile)
       s = 0
       
       h1 = f.Get(channel+'/'+process+'_hww')
       h2 = f.Get(channel+'/'+process+'_htt')
       h3 = f.Get(channel+'/'+process+'_hzz')
       
       if h1:
          s = s+ h1.Integral()
       if h2:
          s = s+ h2.Integral()
       if h3:
          s = s+ h3.Integral()

       return s


def read_dcard_0taus(cardfile,channel,process):
       f = rt.TFile(cardfile)
       s = 0

       h1 = f.Get('x_'+process+'_hww')
       h2 = f.Get('x_'+process+'_htt')
       h3 = f.Get('x_'+process+'_hzz')
       
       if h1:
          s = s+ h1.Integral()
       if h2:
          s = s+ h2.Integral()
       if h3:
          s = s+ h3.Integral()
       
       return s
#
sigRates = [
    "ttH_2lss_0tau",
    "ttH_3l_0tau",
    "ttH_2lss_1tau"
]

nodes = ['ee_ttHnode', 'ee_tHQnode', 'ee_ttWnode','ee_Restnode','em_ttHnode', 'em_tHQnode', 'em_ttWnode','em_Restnode','mm_ttHnode', 'mm_tHQnode', 'mm_ttWnode','mm_Restnode']
reg3l = ['tH_bt', 'ttH_bt', 'rest_eee','tH_bl', 'ttH_bl', 'rest_eem_bl','rest_emm_bl','rest_mmm_bl','rest_eem_bt','rest_emm_bt','rest_mmm_bt']
taus = ['rest','tH','ttH']


def getXYtoplot(process,sigRates,nodes,reg3l):
   x_2lss_0tau=[]
   y_2lss_0tau = []
   y_3l_0tau = []
   x_3l_0tau = []
   y_2lss_1tau = []
   x_2lss_1tau = []
   if process == 'tHq': 
      xsec = 70.96 #fb
   elif process == 'tHW':
      xsec = 15.61 #fb
   for channel in sigRates:
      y=[]
      x=[]
      for q in cards:
    
        if channel == 'ttH_2lss_0tau':
           suma = 0
           
          
           for i in nodes:
               
               card = channel+'_'+i+'_'+year+'_'+cards[q][0]+'.root'
           
               s = read_dcard_0taus(card,channel,process)
               suma = suma +s

        elif channel == 'ttH_3l_0tau':
           suma = 0

           for i in reg3l:
               card = channel+'_'+i+'_'+year+'_'+cards[q][0]+'.root'
               s = read_dcard_0taus(card,channel,process)
               suma = suma +s
        elif channel == 'ttH_2lss_1tau':
           suma = 0

           for i in taus:
               card = channel+'_'+i+'_'+year+'_'+cards[q][0]+'.root'
               s = read_dcard(card,channel,process)
               suma = suma +s
        
        if channel == 'ttH_2lss_0tau': 
           y_2lss_0tau.append(suma/(xsec*lumi[year]))
           x_2lss_0tau.append(q)
        if channel == 'ttH_3l_0tau': 
           y_3l_0tau.append(suma/(xsec*lumi[year]))
           x_3l_0tau.append(q)
        if channel == 'ttH_2lss_1tau': 
           y_2lss_1tau.append(suma/(xsec*lumi[year]))
           x_2lss_1tau.append(q)
 
       
   x_2lss_0tau,y_2lss_0tau = zip(*sorted(zip(x_2lss_0tau, y_2lss_0tau)))
   x_3l_0tau,y_3l_0tau = zip(*sorted(zip(x_3l_0tau, y_3l_0tau)))
   x_2lss_1tau,y_2lss_1tau = zip(*sorted(zip(x_2lss_1tau, y_2lss_1tau)))
   return {'ttH_2l_0tau':{"latex" : r'$2\ell ss +0\tau_{h}$',"x": x_2lss_0tau,"y":y_2lss_0tau},'ttH_3l_0tau':{"latex" : r'$3\ell +0\tau_{h}$',"x":x_3l_0tau,"y":y_3l_0tau},'ttH_2l_1tau':{"latex" : r'$2\ell ss +1\tau_{h}$',"x":x_2lss_1tau,"y":y_2lss_1tau}}      


#plotting
x_low, x_high = -6.5, 6.5
y_low, y_high = 0.0001, 0.01

for process in ["tHq","tHW"] :
    fig, ax = plt.subplots(figsize=(5, 5))
    colors = [ "springgreen","fuchsia", "r"]
    dic = getXYtoplot(process,sigRates,nodes,reg3l)
    ii=0
    for key in dic.keys() :
        
        print key
        plt.plot(dic[key]["x"],dic[key]["y"], 'o-', markersize=3, color=colors[ii], linestyle='-', markeredgewidth=0, linewidth=1 ,label=dic[key]["latex"] )
        ii+=1   
    
    ax.set_ylabel("Acceptance X efficiency")
    plt.axis([x_low, x_high, y_low, y_high])
    print_header(ax, x_low, x_high, y_low, y_high,logscale = True)
   
    leg = ax.legend(loc='upper left', fancybox=False, shadow=False, frameon=1, ncol=2, fontsize=10,title= r'$\textbf{%s process}$'%(process)) 
    leg._legend_box.align = "left"
    
    leg.get_title().set_fontsize('12')
    leg.get_title().set_style('normal')
    frame = leg.get_frame()
    frame.set_color('white')
    frame.set_linewidth(0)
    ax.set_xlabel(r'$\kappa_{t} / \kappa_{\mathrm{V}}$')
    ax.set_yscale('log')
    ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=15))
    plt.axvline(x=1.0, color="k", linestyle=':', linewidth=1)
    namefig    = "AccTimeEff_" +year+'_'+ process +".pdf"
    fig.savefig(namefig)
    print ("saved",namefig)


