import sys
import math
import json
import array as array
from optparse import OptionParser
import ROOT
from PhysicsTools.NanoAODTools.plotter import *



parser = OptionParser()

parser.add_option('--MC',dest="MC", default=False, action="store_true", help="Only plot the MC")

(options, args) = parser.parse_args()


if not options.MC :
    lumi = 5434.766# need to check CRAB report lumis but this should be close   #4008.37 

    dataFile = ROOT.TFile.Open("root://cmsxrootd.fnal.gov///store/user/asparker/NANOSkimsof80Xrecluster/ZplusJetSkim80XNANAODreclusterSingleMuon2016B-histos.root")

    dataFile.cd()

    #right now only muons present

    #get histos to plot
    dhists = {}

    dirList = ROOT.gDirectory.GetListOfKeys()
    print dirList
    for k1 in dirList: 
      d1 = k1.ReadObj()
      d1.cd()
      hList = ROOT.gDirectory.GetListOfKeys()
      for h in hList:
        print "hist name is "
        print h.ReadObj().GetName()
        if 'inning' in h.ReadObj().GetName() : continue
        if '_2d' in h.ReadObj().GetName() : continue
        if 'response' in h.ReadObj().GetName() : continue
        dhists[h.GetName()] = [h.ReadObj()]


mcFile = ROOT.TFile.Open("root://cmsxrootd.fnal.gov///store/user/asparker/NANOSkimsof80Xrecluster/ZandJetSkimof80XNANAODreclusterDY1JetsToLLM-50-histos-ext2.root")

#get histos to plot
mhists = {}
massnames = ['reco', 'fake', 'miss', 'gen']
znames = ['zpt', 'zeta', 'zphi', 'zmass']

titles = [
['h_reco' , 'Reconstructed AK8 SD Jet Mass (GeV)'],
['h_reco_2d' , 'Reconstructed AK8 SD Jet Mass (GeV)'],
['h_reco_u' , 'Reconstructed AK8 Ungroomed Jet Mass (GeV)'],
['h_gen' , 'Generated AK8 SD Jet Mass (GeV)'],
['h_gen_u' , 'Generated AK8 Ungroomed Jet Mass (GeV)'],
['h_fake' , 'Reconstructed  Fake AK8 SD Jet Mass (GeV)'],
['h_fake_u' , 'Reconstructed Fake AK8 Ungroomed Jet Mass (GeV)'],
['h_miss' , 'Missed Generated AK8 SD Jet Mass (GeV)'],
['h_miss_u' , 'Missed Generated AK8 Ungroomed Jet Mass (GeV)'],
['h_lep0pt' , 'Lepton 0 P_{T} (GeV)'],
['h_lep0eta' , 'Lepton 0 \eta'],
['h_lep0ephi' , 'Lepton 0 \phi'],
['h_lep1pt' , 'Lepton 1 P_{T} (GeV)'],
['h_lep1eta' , 'Lepton 1 \eta'],
['h_lep1phi' , 'Lepton 1 \phi'],


['zpt' , 'Leptonic Z candidate P_{T} (GeV)'],
['zmass' , 'Leptonic Z candidate Mass (GeV)'],
['zeta' , 'Leptonic Z candidate \eta '],
['zphi' , 'Leptonic Z candidate \phi '],

['h_genjetpt' , 'Generated AK8 SD Jet $P_{T}$ (GeV)'],
['h_genjetphi' , 'Generated AK8 SD Jet \phi (GeV)'],
['h_genjeteta' , 'Generated AK8 SD Jet \eta (GeV)'],
['h_genjetmass' , 'Generated AK8 SD Jet Mass (GeV)'],


['recojetpt' , 'Reconstructed AK8 SD Jet $P_{T}$ (GeV)'],
['h_recojetphi' , 'Reconstructed  AK8 SD Jet \phi (GeV)'],
['h_recojeteta' , 'Reconstructed  AK8 SD Jet \eta (GeV)'],
['h_recojetmass' , 'Reconstructed  AK8 SD Jet Mass (GeV)'],


['drGenReco' , ' \Delta R(genJet,recoJet) '],
['drGenGroomed' , ' \Delta R(genJet,recoSDJet) ']

]

Min = []
rangeMax = []

dirList = ROOT.gDirectory.GetListOfKeys()
print dirList
for k1 in dirList: 
  d1 = k1.ReadObj()
  d1.cd()
  hList = ROOT.gDirectory.GetListOfKeys()
  for h in hList:
    #print "hist name is "
    hname =  h.ReadObj().GetName()
    if 'response' in hname : continue
    if 'inning' in hname : continue  
    #if '_2d' in hname : continue
    #if 'jet' in hname : continue
    #if 'drGen' in hname : continue
    #if 'reco' in hname : continue
    #if 'gen' in hname : continue
    #if 'fake' in hname : continue
    print "hist name is "
    print hname
    if 'inning' in hname : continue
    if '_2d' in h.ReadObj().GetName() : continue
    if 'response' in h.ReadObj().GetName() : continue
    for t in titles :
        if t[0] in hname :
            title = t[1]
    mhists[h.GetName()] = [h.ReadObj() , title]


w = 1.
if not options.MC :
    xsec = 3. * 2008.4
    nevents = 11623646.   # ( 244876.)# ext2 DY Nevents processed    #(32553254. + 11623646.)
    w = xsec * lumi / nevents


y_max_scale = 1.55

rangexs = []

cans = []
if not options.MC :
    for name, hist in dhists.iteritems() :
        # get the hists
        data = hist[0] 
        mcl = mhists[name]
        mc = mcl[0]
        xtitle = mcl[1]
        #Apply scaling calculated above
        mc.Scale(w)
        mc.SetFillColor(ROOT.kGreen +1)
         
        # create the MC stack for the plot
        Stack = ROOT.THStack("mcStack"+ name, "mcStack"+ name )
        Stack.Add(mc)
        
        # rebin thse hists which need it
        rbnum = -1
        rangexs = None
        #if rbnum > 0. :
        #    print "rebinning!!! {}".format(int(rbnum))
        #    mc.Rebin(int(rbnum))
        #    data.Rebin(int(rbnum))
      
        #therange = rangexs[i] 
        #print "Now plotting histo {} name is {} rangex[i] is {}".format(i, name, therange)
        newcan = printPlot("80XNANOreclusterSkim_SingleMuondata", "zjetsDYext2", xtitle, name ,rangexs, y_max_scale, data , lumi, mc, Stack )
        cans.append(newcan)

if options.MC :
    for name, hist in mhists.iteritems() :
        data = None
       
        #print hist
        #Apply scaling calculated above
        #hist[0].Scale(w)
        ROOT.gStyle.SetOptStat(000000)

        # create the MC stack for the plot
        Stack = ROOT.THStack("mcStack"+ name, "mcStack"+ name )
        hist[0].SetFillColor(ROOT.kGreen+1)
        Stack.Add(hist[0])
        
        # rebin thse hists which need it
        rbnum = -1

        if rbnum > 0. :
            print "rebinning!!! {}".format(int(rbnum))
            hist[0].Rebin(int(rbnum))

        rangexs = None   
        xtitle =  hist[1]
        #if 'eta' in name :
        #    rangexs = [-3,3]
        #if 'phi' in name :
        #    rangexs = [-5,5]

        #print "Now plotting histogram {} with x range {}".format(name, rangexs)
        newcan = printPlot("94XNANOrecluster_ZplusJetSkim_allDY2017", "zjetsplots", xtitle, name ,rangexs, y_max_scale, data , hist[0], Stack ) 
        cans.append(newcan)

