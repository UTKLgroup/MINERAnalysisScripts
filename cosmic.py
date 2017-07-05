import ROOT
from ROOT import HistManager, TH1, TH2, TH3, gROOT, kTRUE, TFile, TChain, TClonesArray, TH1F

ROOT.PyConfig.IgnoreCommandLineOptions = True

TH1.SetDefaultSumw2(kTRUE)
TH2.SetDefaultSumw2(kTRUE)
TH3.SetDefaultSumw2(kTRUE)

gROOT.LoadMacro('defs/HistManager.cc+')
gROOT.LoadMacro('defs/BaseHit.cc+')
gROOT.LoadMacro('defs/BaseTrack.cc+')

tfile = TFile('cosmic.root', 'RECREATE')
event_tree = TChain('theTree')
event_tree.Add('/Users/juntinghuang/Desktop/miner/MINERsim/FullGeometry/GEANT4_MS/cmake-build-debug/neutron.root')

hists = HistManager(tfile)
fill_1d_hist = hists.fill1DHist
fill_1d_hist_uneven_bins = hists.fill1DHistUnevenBins
fill_2d_hist = hists.fill2DHist
fill_2d_hist_uneven_bins = hists.fill2DHistUnevenBins
fill_profile = hists.fillProfile


tfile.cd()

hits = TClonesArray('BaseHit', 10)
event_tree.SetBranchAddress('sHits', hits)

tracks = TClonesArray('BaseTrack', 10)
event_tree.SetBranchAddress('sTracks', tracks)

h_edeps = []
for i in range(11):
    h_edeps.append(TH1F('EdepH_det' + str(i + 1), ';Energy [keV]; # events', 4096, 0, 5211.222845 + 0.5 * 1.272436))

for event in event_tree:
    primary_energy = event.eInc
    fill_1d_hist(primary_energy, 'primary_energy', '', 500, 0, 20, 1., '')

    sumE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    weight = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    if event.hitC > 0:
        hitDict = {}
        for hit in event.sHits:
            try:
                hitDict[hit.preproc()].append(hit)
            except Exception:
                hitDict[hit.preproc()] = []
                hitDict[hit.preproc()].append(hit)

        for ID, hit_list in hitDict.iteritems():
            fill_1d_hist(len(hit_list), 'nHits_per_event', '', 41, -0.5, 40.5, 1., '')
            for hit in hit_list:
                if hit.detID() > 12:
                    fill_1d_hist(hit.Ekin(),
                                 'Det' + str(hit.detID()) + '_Ekin_PID' + str(hit.pid()),
                                 '', 500, 0, 10, hit.Weight(), '')
                    fill_2d_hist(hit.pos().y(),
                                 hit.pos().z(),
                                 'Det' + str(hit.detID()) + '_pos_PID' + str(hit.pid()),
                                 '', 120, -600, 600, 120, -1900, -700, hit.Weight(), '')

                if hit.detID() < 9 and hit.pid() == 22:
                    fill_1d_hist(hit.Ekin() * 1000, 'Ekin_gamma', '', 100, 0, 2000, hit.Weight(), '')

                if hit.detID() < 13:
                    weight[hit.detID()-1] = hit.Weight()
                    sumE[hit.detID()-1] += hit.Edep()*1000

        for i in range(11):
            if sumE[i] > 0:
                h_edeps[i].Fill(sumE[i], weight[i])

tfile.Write()
tfile.Close()
