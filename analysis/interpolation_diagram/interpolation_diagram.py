#!/usr/bin/env python

import matplotlib
from matplotlib import pylab as plt
from scipy.special import j1
import numpy as np

matplotlib.rc('legend', fontsize='medium')

xx = np.arange(7.0, 11.2, 0.01)
yy = j1(xx)
fig = plt.figure(figsize=(6,6))
ax = plt.subplot(221)
ax.plot(xx, yy, label='XCORR')
max_idx = yy.argmax()
true_peak = xx[max_idx]
ax.plot([true_peak], [yy.max()], 'p')

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel('Displacement')
#ax.set_ylabel('XCORR')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
samples_x = np.array([7.9, 9.4, 10.9])
samples_y = j1(samples_x)
ax.plot(samples_x, j1(samples_x), 'o')
ax.set_ylim([-0.3, 0.4])

def parabolic_interpolation(y0, y1, y2, T_s):
    numerator = y0 - y2
    denominator = 2.0*(y0 - 2*y1 + y2)
    return T_s * numerator / denominator

parabolic_peak = samples_x[1] + parabolic_interpolation(samples_y[0],
    samples_y[1], samples_y[2], samples_x[1] - samples_x[0])

aa = np.array([samples_x**2, samples_x, np.ones((3,))])
aa = aa.transpose()
parabola_coef = np.linalg.solve(aa, samples_y)
def eval_parabola(parabola_coef, xx):
    return parabola_coef[0]*xx**2 + parabola_coef[1]*xx + parabola_coef[2]

ax.plot(xx, eval_parabola(parabola_coef, xx), 'r--', label='parabolic fit')
ax.plot(parabolic_peak, eval_parabola(parabola_coef, parabolic_peak), '*')
ax.legend(loc='lower left')

bias_ylim = np.array([-0.05, 0.35])
ax.vlines([parabolic_peak, true_peak], bias_ylim[0], bias_ylim[1])

ax.annotate('bias', xy=(true_peak, 0.1), xytext=(true_peak+0.3, 0.0),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))

plt.show()


