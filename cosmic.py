import operator
from pprint import pprint
from pyne import nucname

from ROOT import gROOT
gROOT.LoadMacro("defs/HistManager.cc+")
gROOT.LoadMacro("defs/BaseHit.cc+")
gROOT.LoadMacro("defs/BaseTrack.cc+")
from ROOT import HistManager, TFile, TChain, TDatabasePDG


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
        self.pdg = TDatabasePDG()

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

    @staticmethod
    def get_event_count_elapsed_time():
        event_count = 0
        elapsed_time = 0.0
        with open(Cosmic.INPUT_FILENAME_LIST) as f_filename:
            for row in f_filename:
                tfile = TFile(row.strip())
                h_elapsed_time = tfile.Get('hElapsedTime')
                event_count += h_elapsed_time.GetEntries()
                elapsed_time += h_elapsed_time.GetBinContent(1)
                tfile.Close()
        return event_count, elapsed_time

    @staticmethod
    def get_l_z_a_i_from_pid(pid):
        pid_string = str(pid)
        l = pid_string[2:3]
        z = pid_string[3:6]
        a = pid_string[6:9]
        i = pid_string[9:10]
        return l, z, a, i

    @staticmethod
    def get_nucleus_name(pid):
        l, z, a, i = Cosmic.get_l_z_a_i_from_pid(pid)
        if l != '0':
            print 'warning n_lambda is not 0: {}'.format(l)
        return nucname.name('{}{}0000'.format(int(z), a))

    def get_particle_name(self, pid):
        try:
            return self.pdg.GetParticle(pid).GetName()
        except Exception:
            return Cosmic.get_nucleus_name(pid)

    def plot(self):
        pid_track_counts = {}
        pid_hit_counts = {}
        for event in Cosmic.get_event_tree():
            self.fill_1d_hist(event.trackC,
                              'h_event_track_count', '',
                              100, 0, 100, 1.0,
                              '')

            for track in event.sTracks:
                track_pid = track.pid()
                if track_pid not in pid_track_counts:
                    pid_track_counts[track_pid] = 0
                else:
                    pid_track_counts[track_pid] += 1

                self.fill_1d_hist((track.p4().Pz() / track.p()) ** 2,
                                  'h_primary_cos_theta_square_pid_{}'.format(track_pid), '',
                                  500, 0, 1, 1.0,
                                  '')
                self.fill_1d_hist(track.E(),
                                  'h_primary_energy_pid_{}'.format(track_pid), '',
                                  500, 0, 10000, 1.0,
                                  '')

            for hit in event.sHits:
                if hit.detID() > 8 or hit.detID() < 1:
                    continue

                hit_pid = hit.pid()
                if hit_pid not in pid_hit_counts:
                    pid_hit_counts[hit_pid] = 0
                else:
                    pid_hit_counts[hit_pid] += 1

                self.fill_2d_hist(hit.pos().x(), hit.pos().y(),
                                  'h_hit_pos_xy_pid_{}'.format(hit_pid), '',
                                  500, 2330, 2330,
                                  500, -50, 50,
                                  1.0,
                                  '')
                self.fill_2d_hist(hit.pos().x(), hit.pos().z(),
                                  'h_hit_pos_xz_pid_{}'.format(hit_pid), '',
                                  500, 2330, 2330,
                                  500, -1140, -1150,
                                  1.0,
                                  '')
                self.fill_1d_hist(hit.Edep(),
                                  'h_hit_edep_pid_{}'.format(hit_pid), '',
                                  500, 0, 10, 1.0,
                                  '')
                self.fill_1d_hist(hit.Ekin(),
                                  'h_hit_ekin_pid_{}'.format(hit_pid), '',
                                  500, 0, 10, 1.0,
                                  '')

        sorted_pid_track_counts = sorted(pid_track_counts.items(), key=operator.itemgetter(1), reverse=True)
        sorted_pid_hit_counts = sorted(pid_hit_counts.items(), key=operator.itemgetter(1), reverse=True)
        pprint(sorted_pid_hit_counts)
        pprint(sorted_pid_track_counts)

        with open('cosmic.tex', 'w') as f_pid_count:
            for sorted_pid_hit_count in sorted_pid_hit_counts:
                pid = sorted_pid_hit_count[0]
                hit_count = sorted_pid_hit_count[1]
                name = self.get_particle_name(pid)
                f_pid_count.write('{} & {} & {} \\\\ \n'.format(pid, name.replace('_', '\_'), hit_count))

            for sorted_pid_track_count in sorted_pid_track_counts:
                pid = sorted_pid_track_count[0]
                track_count = sorted_pid_track_count[1]
                name = self.get_particle_name(pid)
                f_pid_count.write('{} & {} & {} \\\\ \n'.format(pid, name.replace('_', '\_'), track_count))


with Cosmic() as cosmic:
    cosmic.plot()
    # print cosmic.get_event_count_elapsed_time()
    # print cosmic.get_l_z_a_i_from_pid(1000140280)
