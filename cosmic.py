from ROOT import gROOT
gROOT.LoadMacro("defs/HistManager.cc+")
gROOT.LoadMacro("defs/BaseHit.cc+")
gROOT.LoadMacro("defs/BaseTrack.cc+")
from ROOT import HistManager, BaseHit, BaseTrack, TFile, TChain, TH1D, TCanvas


class Cosmic:
    TREE_NAME = 'theTree'
    INPUT_FILENAME_LIST = 'cosmic.txt'
    OUTPUT_FILENAME = 'cosmic.root'

    def __init__(self):
        self.tfile = TFile(Cosmic.OUTPUT_FILENAME, 'RECREATE')
        hist_manager = HistManager(self.tfile)
        self.fill_1d_hist = hist_manager.fill1DHist
        self.fill_2d_hist = hist_manager.fill2DHist
        self.tfile.cd()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tfile.Write()
        self.tfile.Close()

    @staticmethod
    def get_event_tree():
        event_tree = TChain(Cosmic.TREE_NAME)
        with open(Cosmic.INPUT_FILENAME_LIST) as f_filename:
            for row in f_filename:
                event_tree.Add(row.strip())
        return event_tree

    def plot_primary_energy(self):
        for event in Cosmic.get_event_tree():
            for track in event.sTracks:
                cos_theta_square = (track.p4().Pz() / track.p())**2
                self.fill_1d_hist(cos_theta_square,
                                  'h_primary_cos_theta_square_pid_{}'.format(track.pid()), '',
                                  500, 0, 1, 1.0,
                                  '')
                self.fill_1d_hist(track.E(),
                                  'h_primary_energy_pid_{}'.format(track.pid()), '',
                                  500, 0, 10000, 1.0,
                                  '')

            for hit in event.sHits:
                if hit.detID() > 8 or hit.detID() < 1:
                    continue

                self.fill_2d_hist(hit.pos().x(), hit.pos().y(),
                                  'h_hit_pos_xy_pid_{}'.format(hit.pid()), '',
                                  500, 2330, 2330,
                                  500, -50, 50,
                                  1.0,
                                  '')

                self.fill_2d_hist(hit.pos().x(), hit.pos().z(),
                                  'h_hit_pos_xz_pid_{}'.format(hit.pid()), '',
                                  500, 2330, 2330,
                                  500, -1140, -1150,
                                  1.0,
                                  '')

                self.fill_1d_hist(hit.Edep(),
                                  'h_hit_edep_pid_{}'.format(hit.pid()), '',
                                  500, 0, 10, 1.0,
                                  '')

                self.fill_1d_hist(hit.Ekin(),
                                  'h_hit_ekin_pid_{}'.format(hit.pid()), '',
                                  500, 0, 10, 1.0,
                                  '')

with Cosmic() as cosmic:
    cosmic.plot_primary_energy()
