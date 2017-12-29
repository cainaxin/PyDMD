import matplotlib
matplotlib.use('Qt4Agg')
import pylab

import crash_on_ipy
import matplotlib.pyplot as plt
from pydmd import MrDMD
from pydmd import DMD
import numpy as np
from past.utils import old_div

def create_sample_data():
    x = np.linspace(-10, 10, 80)
    t = np.linspace(0, 20, 1600)
    Xm, Tm = np.meshgrid(x, t)
    D = np.exp(-np.power(Xm/2, 2)) * np.exp(0.8j * Tm)
    D += np.sin(0.9 * Xm) * np.exp(1j * Tm)
    D += np.cos(1.1 * Xm) * np.exp(2j * Tm)
    D += 0.6 * np.sin(1.2 * Xm) * np.exp(3j * Tm)
    D += 0.6 * np.cos(1.3 * Xm) * np.exp(4j * Tm)
    D += 0.2 * np.sin(2.0 * Xm) * np.exp(6j * Tm)
    D += 0.2 * np.cos(2.1 * Xm) * np.exp(8j * Tm)
    D += 0.1 * np.sin(5.7 * Xm) * np.exp(10j * Tm)
    D += 0.1 * np.cos(5.9 * Xm) * np.exp(12j * Tm)
    D += 0.1 * np.random.randn(*Xm.shape)
    D += 0.03 * np.random.randn(*Xm.shape)
    D += 5 * np.exp(-np.power((Xm+5)/5, 2)) * np.exp(-np.power((Tm-5)/5, 2))
    D[:800, 40:] += 2
    D[200:600, 50:70] -= 3
    D[800:, :40] -= 2
    D[1000:1400, 10:30] += 3
    D[1000:1080, 50:70] += 2
    D[1160:1240, 50:70] += 2
    D[1320:1400, 50:70] += 2
    return D.T


def make_plot(X, x=None, y=None, title=''):
    """
    Plot of the data X
    """
    plt.title(title)
    X = np.real(X)
    CS = plt.pcolor(x, y, X)
    cbar = plt.colorbar(CS)
    plt.xlabel('Space')
    plt.ylabel('Time')

sample_data = create_sample_data()
x = np.linspace(-10, 10, 80)
t = np.linspace(0, 20, 1600)
plt.figure(1)
make_plot(sample_data.T, x=x, y=t)

first_dmd = DMD(svd_rank=-1)
first_dmd.fit(X=sample_data) # 80*1600
plt.figure(2)
modes = first_dmd.modes
eig = first_dmd.eigs
# make_plot(first_dmd.recon_fn_data(modes, eig).T, x=x, y=t)
index = np.argsort(np.abs(old_div(np.log(eig), (2. * np.pi))))
slow_models = index <= 0
s_modes = modes[:, index]
print(np.shape(s_modes))
for i in range(0, 80):
    plt.clf()
    make_plot(first_dmd.recon_fn_data(np.resize(modes[i], [80, 1]), eig[i]).T, x=x, y=t)
    print(np.abs(old_div(np.log(eig[i]), (2. * np.pi))))

dmd = MrDMD(svd_rank=-1, max_level=7, max_cycles=1)
dmd.fit(X=sample_data)
plt.figure(3)
plt.title('MrDMD')
make_plot(dmd.reconstructed_data.T, x=x, y=t)
#
plt.show()
# print 'The number of eigenvalues is ' + str(dmd.eigs.shape[0])
# dmd.plot_eigs(show_axes=True, show_unit_circle=True, figsize=(8, 8))
#
# dmd.plot_eigs(show_axes=True, show_unit_circle=True, figsize=(8, 8), level=3, node=0)
#
# pmodes = dmd.partial_modes(level=0)
# fig = plt.plot(x, pmodes.real)
#
# pdyna = dmd.partial_dynamics(level=0)
# fig = plt.plot(t, pdyna.real.T)
#
# pdyna = dmd.partial_dynamics(level=1)
# print 'The number of modes in the level number 1 is ' + str(pdyna.shape[0])
# fig = plt.plot(t, pdyna.real.T)
#
# pdata = dmd.partial_reconstructed_data(level=0)
# make_plot(pdata.T, x=x, y=t, title='level 0', figsize=(7.5, 5))
#
# for i in range(1, 7):
#     pdata += dmd.partial_reconstructed_data(level=i)
#     make_plot(pdata.T, x=x, y=t, title='levels 0-' + str(i), figsize=(7.5, 5))


