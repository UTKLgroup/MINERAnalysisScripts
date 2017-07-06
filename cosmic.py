from ROOT import gROOT
gROOT.LoadMacro("defs/HistManager.cc+")
gROOT.LoadMacro("defs/BaseHit.cc+")
gROOT.LoadMacro("defs/BaseTrack.cc+")
from ROOT import HistManager, TFile, TChain


class Cosmic:
    TREE_NAME = 'theTree'
    INPUT_FILENAME_LIST = 'cosmic.txt'
    OUTPUT_FILENAME = 'cosmic.root'

    def __init__(self):
        self.tfile = TFile(Cosmic.OUTPUT_FILENAME, 'RECREATE')
        hist_manager = HistManager(self.tfile)
        self.fill_1d_hist = hist_manager.fill1DHist
        self.tfile.cd()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tfile.Write()
        self.tfile.Close()

    @staticmethod
    def get_filenames():
        filenames = []
        with open(Cosmic.INPUT_FILENAME_LIST) as f_filename:
            for row in f_filename:
                filenames.append(row.strip())
        return filenames

    def make_hist(self):
        event_tree = TChain(Cosmic.TREE_NAME)
        for filename in Cosmic.get_filenames():
            event_tree.Add(filename)

        for event in event_tree:
            primary_energy = event.eInc
            self.fill_1d_hist(primary_energy, 'primary_energy', '', 500, 0, 20, 1.0, '')

            if event.hitC > 0:
                original_track_id_hits = {}
                for hit in event.sHits:
                    original_track_id = hit.preproc()
                    if original_track_id not in original_track_id_hits:
                        original_track_id_hits[hit.preproc()] = [hit]
                    else:
                        original_track_id_hits[hit.preproc()].append(hit)

                for original_track_id, hits in original_track_id_hits.iteritems():
                    self.fill_1d_hist(len(hits), 'h_event_hit_count', '', 41, -0.5, 40.5, 1.0, '')

with Cosmic() as cosmic:
    cosmic.make_hist()
