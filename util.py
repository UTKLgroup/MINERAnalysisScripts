from ROOT import TDatabasePDG
from pyne import nucname


PDG = TDatabasePDG()

def get_l_z_a_i_from_pid(pid):
    pid_string = str(pid)
    l = pid_string[2:3]
    z = pid_string[3:6]
    a = pid_string[6:9]
    i = pid_string[9:10]
    return l, z, a, i


def get_nucleus_name(pid):
    l, z, a, i = get_l_z_a_i_from_pid(pid)
    if l != '0':
        print 'warning n_lambda is not 0: {}'.format(l)
    return nucname.name('{}{}0000'.format(int(z), a))


def get_particle_name(pid):
    try:
        return PDG.GetParticle(pid).GetName()
    except Exception:
        return get_nucleus_name(pid)


def order_by_time(x1, x2):
    e1 = x1.time()
    e2 = x2.time()
    if e1 > e2:
        return 1
    if e1 == e2:
        return 0
    if e1 < e2:
        return -1


def order_by_energy(x1, x2):
    e1 = x1.Ekin()
    e2 = x2.Ekin()
    if e1 > e2:
        return 1
    if e1 == e2:
        return 0
    if e1 < e2:
        return -1
