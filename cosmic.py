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

    @staticmethod
    def get_hit_edep_max(hit_pid):
        return {
            11: 0.1,
            -11: 1.0,
            22: 0.001,
            2212: 1.0,
            2112: 1.0,
            12: 0.001,
            -12: 0.001
        }.get(hit_pid, 10.0)

    @staticmethod
    def get_hit_ekin_max(hit_pid):
        return {
            11: 0.1,
            -11: 1.0,
            22: 0.001,
            2212: 1.0,
            2112: 1.0,
            12: 0.001,
            -12: 0.001
        }.get(hit_pid, 10.0)

    def plot(self):
        event_count, elapsed_time = self.get_event_count_elapsed_time()
        self.fill_1d_hist(0.5,
                          'h_event_count', '',
                          1, 0, 1, event_count,
                          '')
        self.fill_1d_hist(0.5,
                          'h_elapsed_time', '',
                          1, 0, 1, elapsed_time,
                          '')

        pid_track_counts = {}
        pid_hit_counts = {}
        pid_hit_edeps = {}
        for event in Cosmic.get_event_tree():
            self.fill_1d_hist(event.trackC,
                              'h_event_track_count', '',
                              100, 0, 100, 1.0,
                              '')

            for track in event.sTracks:
                track_pid = track.pid()
                if track_pid not in pid_track_counts:
                    pid_track_counts[track_pid] = 1
                else:
                    pid_track_counts[track_pid] += 1

                self.fill_1d_hist((track.p4().Pz() / track.p()) ** 2,
                                  'h_primary_cos_theta_square_pid_{}'.format(track_pid), '',
                                  500, 0, 1, 1.0,
                                  '')
                self.fill_1d_hist(track.E(),
                                  'h_primary_energy_pid_{}'.format(track_pid), '',
                                  10000, 0, 10000, 1.0,
                                  '')

            for hit in event.sHits:
                if hit.detID() > 8 or hit.detID() < 1:
                    continue

                hit_pid = hit.pid()
                hit_weight = hit.Weight()
                hit_edep = hit.Edep()
                hit_ekin = hit.Ekin()

                if hit_pid not in pid_hit_counts:
                    pid_hit_counts[hit_pid] = hit_weight
                else:
                    pid_hit_counts[hit_pid] += hit_weight

                if hit_pid not in pid_hit_edeps:
                    pid_hit_edeps[hit_pid] = hit_edep * hit_weight
                else:
                    pid_hit_edeps[hit_pid] += hit_edep * hit_weight

                self.fill_2d_hist(hit.pos().x(), hit.pos().y(),
                                  'h_hit_pos_xy_pid_{}'.format(hit_pid), '',
                                  120, 2280, 2400,
                                  120, -60, 60,
                                  hit_weight,
                                  '')
                self.fill_2d_hist(hit.pos().x(), hit.pos().z(),
                                  'h_hit_pos_xz_pid_{}'.format(hit_pid), '',
                                  120, 2280, 2400,
                                  450, -1500, -1050,
                                  hit_weight,
                                  '')
                self.fill_1d_hist(hit_edep,
                                  'h_hit_edep_pid_{}'.format(hit_pid), '',
                                  100000, 0, 100.0,
                                  hit_weight,
                                  '')
                self.fill_1d_hist(hit_ekin,
                                  'h_hit_ekin_pid_{}'.format(hit_pid), '',
                                  100000, 0, 100.0,
                                  hit_weight,
                                  '')

        sorted_pid_track_counts = sorted(pid_track_counts.items(), key=operator.itemgetter(1), reverse=True)
        sorted_pid_hit_counts = sorted(pid_hit_counts.items(), key=operator.itemgetter(1), reverse=True)
        sorted_pid_hit_edeps = sorted(pid_hit_edeps.items(), key=operator.itemgetter(1), reverse=True)

        with open('cosmic.tex', 'w') as f_tex:
            event_count, elapsed_time = cosmic.get_event_count_elapsed_time()
            f_tex.write('event_count = {}\n'.format(event_count))
            f_tex.write('elapsed_time = {}\n'.format(elapsed_time))

            f_tex.write('\nsorted_pid_hit_count\n')
            for sorted_pid_hit_count in sorted_pid_hit_counts:
                pid = sorted_pid_hit_count[0]
                hit_count = sorted_pid_hit_count[1]
                name = self.get_particle_name(pid)
                f_tex.write('{} & {} & {} \\\\ \n'.format(pid, name.replace('_', '\_'), hit_count))

            f_tex.write('\nsorted_pid_hit_edep\n')
            for sorted_pid_hit_edep in sorted_pid_hit_edeps:
                pid = sorted_pid_hit_edep[0]
                hit_edep = sorted_pid_hit_edep[1]
                name = self.get_particle_name(pid)
                f_tex.write('{} & {} & {} \\\\ \n'.format(pid, name.replace('_', '\_'), hit_edep))

            f_tex.write('\nsorted_pid_hit_avg_edep\n')
            for sorted_pid_hit_edep in sorted_pid_hit_edeps:
                pid = sorted_pid_hit_edep[0]
                hit_edep = sorted_pid_hit_edep[1]
                hit_count = pid_hit_counts[pid]
                hit_avg_edep = hit_edep / hit_count
                name = self.get_particle_name(pid)
                f_tex.write('{} & {} & {} \\\\ \n'.format(pid, name.replace('_', '\_'), hit_avg_edep))

            f_tex.write('\nsorted_pid_track_count\n')
            for sorted_pid_track_count in sorted_pid_track_counts:
                pid = sorted_pid_track_count[0]
                track_count = sorted_pid_track_count[1]
                name = self.get_particle_name(pid)
                f_tex.write('{} & {} & {} \\\\ \n'.format(pid, name.replace('_', '\_'), track_count))

            f_tex.write('\nfigures\n')
            for pid in [11, -11, 22, 2212, 2112, 12, -12]:
                particle_name = self.get_particle_name(pid).replace('_', '\_')
                f_tex.write('\n%.........................................................\n\n')
                f_tex.write('\\begin{frame}\n')
                f_tex.write('\\frametitle{{Hits Due to {}}}\n'.format(particle_name))
                f_tex.write('\\vspace{-0.6cm}\n')
                f_tex.write('\\begin{figure}\n')
                f_tex.write('\\includegraphics[scale = 0.55]{{figures/{{plot_hit.pid_{}}}.pdf}}\n'.format(pid))
                f_tex.write('\\caption{{Distributions of hit position, hit energy deposition and particle energy for {}.}}\n'.format(particle_name))
                f_tex.write('\\end{figure}\n')
                f_tex.write('\\end{frame}\n')

with Cosmic() as cosmic:
    cosmic.plot()
    # print cosmic.get_event_count_elapsed_time()
    # print cosmic.get_l_z_a_i_from_pid(1000140280)
