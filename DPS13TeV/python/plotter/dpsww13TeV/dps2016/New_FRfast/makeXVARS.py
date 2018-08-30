import os

#pts  = [25, 27, 30, 33, 37, 42, 45]
#etas = ['barrel', 'middle', 'endcap']
pts  = [25,30,35,40,45, 100]
etas = ['barrel', 'endcap']


g = open('plots.txt', 'r+a')
glines = g.readlines()
for i,pt in enumerate(pts):
    #if (i == len(pts)+1): continue
    if (i==len(pts)-1): break
    pt2 = pts[i+1]
    print glines
    for eta in etas:
        a= 'pt{pt1}to{pt2}_{eta} : LepGood1_pt  : [{pt1},{pt2}]  ; XTitle="Lep p_{{T}} {pt1}to{pt2} {eta}"'.format(pt1=pt, pt2=pt2, eta = eta)
        print a
        f = open('xvarpt{pt1}to{pt2}_{eta}.txt'.format(pt1=pt, pt2=pt2, eta=eta), 'w')
        f.write(a)
        f.close()

        for opt in ['', '_scaled', '_scaled_noMETnoMT']:
            nl1 = 'mu_pt{pt1}to{pt2}_{eta}_mtl1tk{opt} : mt_2(LepGood1_pt,LepGood1_phi,met_trkPt,met_trkPhi) : 60,0.,120; XTitle="m_{{T}} mu tkmet {pt1}to{pt2} {eta}"\n'.format(pt1=pt,pt2=pt2,eta=eta,opt=opt)
            nl2 =  'mu_pt{pt1}to{pt2}_{eta}_reliso03{opt} : LepGood1_relIso03 : 50,0.,1.; XTitle="relIso03 #mu {pt1}to{pt2} {eta}"\n'.format(pt1=pt,pt2=pt2,eta=eta,opt=opt)
            print nl1
            print nl2
            if not nl1 in glines:
                g.write(nl1)
            if not nl2 in glines:
                g.write(nl2)
g.close()
            
                
