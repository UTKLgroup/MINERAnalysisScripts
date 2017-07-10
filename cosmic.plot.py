from rootalias import *

f_output = TFile('cosmic.root')
figure_dir = '/Users/juntinghuang/google_drive/slides/beamer/20170706_miner_cosmic_hits/figures'


def get_elapsed_time():
    h_elapsed_time = f_output.Get('h_elapsed_time')
    return h_elapsed_time.GetBinContent(1)


def get_elapsed_time():
    h_event_count = f_output.Get('h_event_count')
    return h_event_count.GetBinContent(1)


def plot_track_count():
    gStyle.SetOptStat('mer')
    h1 = f_output.Get('h_event_track_count')
    c1 = TCanvas('c1', 'c1', 800, 600)
    set_margin()
    gPad.SetLogy()

    set_h1_style(h1)
    h1.GetXaxis().SetRangeUser(0, 20)
    h1.GetXaxis().SetTitle('Cosmic Ray Count')
    h1.GetYaxis().SetTitle('Cosmic Shower Count')
    h1.Draw('hist')

    c1.Update()
    p1 = h1.GetListOfFunctions().FindObject("stats")
    p1.SetTextColor(h1.GetLineColor())
    p1.SetLineColor(h1.GetLineColor())
    p1.SetX1NDC(0.7)
    p1.SetY1NDC(0.75)
    p1.SetX2NDC(0.95)
    p1.SetY2NDC(0.95)
    p1.Draw()

    c1.Update()
    c1.SaveAs('{}/plot_track_count.pdf'.format(figure_dir))
    raw_input('Press any key to continue.')


def plot_primary_energy(**kwargs):
    pid = kwargs.get('pid', 13)
    rebin = kwargs.get('rebin', 1)
    max_x = kwargs.get('max_x', 10000)
    particle_name_tex = kwargs.get('particle_name_tex')

    gStyle.SetOptStat('nemr')
    h_plus = f_output.Get('h_primary_energy_pid_-{}'.format(pid))
    h_minus = f_output.Get('h_primary_energy_pid_{}'.format(pid))
    h_plus.Rebin(rebin)
    h_minus.Rebin(rebin)
    set_h1_style(h_plus)
    set_h1_style(h_minus)

    c1 = TCanvas('c1', 'c1', 600, 600)
    set_margin()
    h_minus.SetName('{}^{{-}}'.format(particle_name_tex))
    h_minus.GetYaxis().SetRangeUser(0, get_max_y([h_minus, h_plus]) * 1.2)
    h_minus.GetXaxis().SetRangeUser(0, max_x)
    h_minus.GetXaxis().SetTitle('Energy (MeV)')
    h_minus.Draw('hist')

    h_plus.SetName('{}^{{+}}'.format(particle_name_tex))
    h_plus.SetLineColor(kRed)
    h_plus.Draw('sames, hist')
    
    c1.Update()
    p_minus = h_minus.GetListOfFunctions().FindObject("stats")
    p_minus.SetTextColor(h_minus.GetLineColor())
    p_minus.SetLineColor(h_minus.GetLineColor())
    p_minus.SetX1NDC(0.7)
    p_minus.SetY1NDC(0.75)
    p_minus.SetX2NDC(0.95)
    p_minus.SetY2NDC(0.95)
    p_minus.Draw()

    p_plus = h_plus.GetListOfFunctions().FindObject("stats")
    p_plus.SetTextColor(h_plus.GetLineColor())
    p_plus.SetLineColor(h_plus.GetLineColor())
    p_plus.SetX1NDC(0.7)
    p_plus.SetY1NDC(0.51)
    p_plus.SetX2NDC(0.95)
    p_plus.SetY2NDC(0.71)
    p_plus.Draw()

    c1.Update()
    c1.SaveAs('{}/plot_primary_energy.pid_{}.pdf'.format(figure_dir, pid))
    raw_input('Press any key to continue.')


def plot_primary_cos_theta_square(**kwargs):
    pid = kwargs.get('pid', 13)
    particle_name_tex = kwargs.get('particle_name_tex')

    gStyle.SetOptStat(0)
    h_plus = f_output.Get('h_primary_cos_theta_square_pid_-{}'.format(pid))
    h_minus = f_output.Get('h_primary_cos_theta_square_pid_{}'.format(pid))
    h_plus.Rebin(5)
    h_minus.Rebin(5)
    set_h1_style(h_plus)
    set_h1_style(h_minus)

    c1 = TCanvas('c1', 'c1', 600, 600)
    set_margin()
    h_minus.SetName('{}^{{-}}'.format(particle_name_tex))
    h_minus.GetYaxis().SetRangeUser(0, get_max_y([h_minus, h_plus]) * 1.2)
    h_minus.GetXaxis().SetTitle('cos^{2}#theta')
    h_minus.Draw('hist')

    h_plus.SetName('{}^{{+}}'.format(particle_name_tex))
    h_plus.SetLineColor(kRed)
    h_plus.Draw('sames, hist')
    
    lg1 = TLegend(0.2, 0.7, 0.58, 0.88)
    set_legend_style(lg1)
    lg1.AddEntry(h_minus, '{}^{{-}}'.format(particle_name_tex), 'l')
    lg1.AddEntry(h_plus, '{}^{{+}}'.format(particle_name_tex), 'l')
    lg1.Draw()

    c1.Update()
    c1.SaveAs('{}/plot_primary_cos_theta_square.pid_{}.pdf'.format(figure_dir, pid))
    raw_input('Press any key to continue.')

def plot_hit(pid):
    h_xy = f_output.Get('h_hit_pos_xy_pid_{}'.format(pid))
    h_xz = f_output.Get('h_hit_pos_xz_pid_{}'.format(pid))
    h_edep = f_output.Get('h_hit_edep_pid_{}'.format(pid))
    h_ekin = f_output.Get('h_hit_ekin_pid_{}'.format(pid))

    canvas_y_ratio = 0.4
    gStyle.SetOptStat(0)
    c1 = TCanvas('c1', 'c1', 1200, 800)
    set_h2_color_style()

    pad1 = TPad("pad1", "pad1", 0, canvas_y_ratio, 0.5, 1)
    pad1.Draw()
    pad1.cd()
    pad1.SetBottomMargin(0.15)
    pad1.SetLeftMargin(0.25)
    pad1.SetRightMargin(0.2)
    set_h2_style(h_xy)
    h_xy.GetXaxis().SetTitle('X (mm)')
    h_xy.GetYaxis().SetTitle('Y (mm)')
    h_xy.GetZaxis().SetTitle('Energy Deposition (MeV)')
    h_xy.GetYaxis().SetTitleOffset(1.5)
    h_xy.GetXaxis().SetTitleOffset(2)
    h_xy.Draw("colz")

    c1.cd()
    pad2 = TPad("pad2", "pad2", 0.5, canvas_y_ratio, 1, 1)
    pad2.Draw()
    pad2.cd()
    pad2.SetBottomMargin(0.15)
    pad2.SetLeftMargin(0.25)
    pad2.SetRightMargin(0.2)
    set_h2_style(h_xz)
    h_xz.GetXaxis().SetTitle('X (mm)')
    h_xz.GetYaxis().SetTitle('Z (mm)')
    h_xz.GetZaxis().SetTitle('Energy Deposition (MeV)')
    h_xz.GetYaxis().SetTitleOffset(3)
    h_xz.GetXaxis().SetTitleOffset(2)
    h_xz.Draw("colz")

    c1.cd()
    pad3 = TPad('pad3', 'pad3', 0, 0, 0.5, canvas_y_ratio)
    pad3.SetRightMargin(0.15)
    pad3.SetLeftMargin(0.25)
    pad3.SetBottomMargin(0.25)
    pad3.Draw()
    pad3.cd()
    gPad.SetGrid()
    gPad.SetLogy()
    set_h1_style(h_edep)
    h_edep.GetXaxis().SetRangeUser(0, 1)
    h_edep.GetXaxis().SetTitle('Energy Deposition (MeV)')
    h_edep.GetYaxis().SetTitle('Hit Count')
    h_edep.GetXaxis().SetTitleOffset(2.5)
    h_edep.GetYaxis().SetTitleOffset(2)
    h_edep.Draw()

    c1.cd()
    pad4 = TPad('pad4', 'pad4', 0.5, 0, 1, canvas_y_ratio)
    pad4.SetRightMargin(0.15)
    pad4.SetLeftMargin(0.25)
    pad4.SetBottomMargin(0.25)
    pad4.Draw()
    pad4.cd()
    gPad.SetGrid()
    gPad.SetLogy()
    set_h1_style(h_ekin)
    h_ekin.GetXaxis().SetRangeUser(0, 1)
    h_ekin.GetXaxis().SetTitle('Track Energy (MeV)')
    h_ekin.GetYaxis().SetTitle('Hit Count')
    h_ekin.GetXaxis().SetTitleOffset(2.5)
    h_ekin.GetYaxis().SetTitleOffset(2)
    h_ekin.Draw()

    c1.Update()
    c1.SaveAs('{}/plot_hit.pid_{}.pdf'.format(figure_dir, pid))
    raw_input('Press any key to continue.')

# plot_primary_energy(pid=13,
#                     rebin=10,
#                     max_x=10000,
#                     particle_name_tex='#mu')
# plot_primary_energy(pid=11,
#                     rebin=1,
#                     max_x=500,
#                     particle_name_tex='e')

# plot_primary_cos_theta_square(pid=13,
                              # particle_name_tex='#mu')
# plot_primary_cos_theta_square(pid=11,
#                               particle_name_tex='e')

# plot_hit(11)
plot_hit(12)
# plot_hit(22)
# plot_hit(13)
# plot_track_count()
