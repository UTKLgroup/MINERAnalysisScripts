#! /usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
from ROOT import *
#from math import fabs,pi,sqrt
from math import *
from array import array
import profile
import time
import copy
#sys.setcheckinterval(1000)
import numpy as n
import subprocess


TH1.SetDefaultSumw2(kTRUE)
TH2.SetDefaultSumw2(kTRUE)
TH3.SetDefaultSumw2(kTRUE)


gROOT.LoadMacro("defs/HistManager.cc+")
gROOT.LoadMacro("defs/BaseHit.cc+")
gROOT.LoadMacro("defs/BaseTrack.cc+")
from ROOT import HistManager
from ROOT import BaseHit
from ROOT import BaseTrack

saveFile = TFile("Neutron_Testplots_480MGT4MeV.root","RECREATE")

theTree = TChain("theTree")
for fN in range(4800):
  theTree.Add("/work/03069/whf346/lonestar/MINERsim_Full_Neutron160401/Launcher/TestNeutronJobs480MGT4MeV/Job"+str(fN+1)+"/testNeutron.root")

#i=0
#f=open('1MGT4MeVnumbers.txt','r')
#for line in f:
#  i+=1
#  print line
#  if line > 0: theTree.Add("/work/03069/whf346/lonestar/MINERsim_Full_Neutron160401/Launcher/TestNeutronJobs1MGT4MeVv2/Job"+str(line.strip())+"/testNeutron.root")

#saveFile = TFile("test_plots.root","RECREATE")
#treeFile = TFile.Open("testN.root")
#theTree = treeFile.Get('theTree')

hists = HistManager(saveFile)
f1DH = hists.fill1DHist
f1DHU = hists.fill1DHistUnevenBins
f2DH = hists.fill2DHist
f2DHU = hists.fill2DHistUnevenBins
fProf = hists.fillProfile

def orderByTime(x1,x2):
    e1 = x1.time()
    e2 = x2.time()
    if e1 > e2: return 1
    if e1 == e2: return 0
    if e1 < e2: return -1

def orderByEnergy(x1,x2):
    e1 = x1.Ekin()
    e2 = x2.Ekin()
    if e1 > e2: return 1
    if e1 == e2: return 0
    if e1 < e2: return -1


saveFile.cd()

hits = TClonesArray("BaseHit",10)
theTree.SetBranchAddress("sHits",hits)

trks = TClonesArray("BaseTrack",10)
theTree.SetBranchAddress("sTracks",trks)

events = 0

EdepH = []
for i in range(11):
  EdepH.append(TH1F("EdepH_det"+str(i+1),";Energy [keV]; # events",4096,0, 5211.222845+0.5*1.272436))


for evt in theTree:

   events += 1
   if events%10000 == 0:
       print events
       sys.stdout.flush()

#   for trk in evt.sTracks:
#      posCheck.Fill(trk.pos().x(),trk.pos().y(),trk.pos().z())
   #if events == 30000: break

   eInc = evt.eInc
   f1DH(eInc,"Eincoming","",500,0,20,1.,"")

   #print ""
   sumE = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
   weight = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
   if evt.hitC > 0:

      hitDict = {}
      for hit in evt.sHits: 
         #print hit.preproc()
         try:
            hitDict[hit.preproc()].append(hit)
         except:
            hitDict[hit.preproc()] = []
            hitDict[hit.preproc()].append(hit)

      #print len(hitDict)
      for ID, hitlist in hitDict.iteritems():
         f1DH(len(hitlist),"nHits_per_event","",41,-0.5,40.5,1.,"")
         for hit in hitlist:
            if (hit.detID() > 12):
                f1DH(hit.Ekin(),"Det"+str(hit.detID())+"_Ekin_PID"+str(hit.pid()),"",500,0,10,hit.Weight(),"")
                f2DH(hit.pos().y(),hit.pos().z(),"Det"+str(hit.detID())+"_pos_PID"+str(hit.pid()),"",120,-600,600,120,-1900,-700,hit.Weight(),"")


            if (hit.detID() < 9 and hit.pid() == 22): f1DH(hit.Ekin()*1000,"Ekin_gamma","",100,0,2000,hit.Weight(),"")
            if (hit.detID() < 13):
              weight[hit.detID()-1] = hit.Weight()
  #            print hit.pid(), hit.Ekin(), hit.Edep(), hit.Weight()
              sumE[hit.detID()-1] += hit.Edep()*1000
              #f1DH(hit.Weight(),"Det"+str(hit.detID())+"_Weights_PID"+str(hit.pid()),"",500,0,.1,1.,"")
              #f1DH(hit.Ekin(),"Det"+str(hit.detID())+"_Ekin_PID"+str(hit.pid()),"",500,0,10,hit.Weight(),"")
              #f1DH(hit.Edep(),"Det"+str(hit.detID())+"_Edep_PID"+str(hit.pid()),"",100,0,10,hit.Weight(),"")
              #f1DH(eInc,"Det"+str(hit.detID())+"_Eincoming_given_outgoing_"+str(hit.pid()),"",100,0,20,hit.Weight(),"")

      for i in range(11):
         if sumE[i] > 0:
             EdepH[i].Fill(sumE[i],weight[i])
             if sumE[i] < 2. and i < 7: 
               for ID, hitlist in hitDict.iteritems():
                   for hit in hitlist: print i+1, hit.pid(), hit.Ekin(), hit.Edep(), hit.Weight()       

print "Done"
saveFile.Write()
saveFile.Close()
del hists
