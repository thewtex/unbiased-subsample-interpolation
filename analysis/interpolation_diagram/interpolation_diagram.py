#!/usr/bin/env python

import matplotlib
from matplotlib import pylab as plt
from scipy.special import j1
import numpy as np

matplotlib.rc('legend', fontsize='medium')

xx = np.arange(7.0, 11.2, 0.01)
yy = j1(xx)
figsize=(3,3)
fig = plt.figure(1, figsize=figsize)
figdpi=600
ax = plt.subplot(111)
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
samples_x = np.array([8.0, 9.5, 11.0])
samples_y = j1(samples_x)
ax.plot(samples_x, j1(samples_x), 'o')
ax.set_ylim([-0.3, 0.4])

def parabolic_interpolation(y0, y1, y2, T_s):
    numerator = y0 - y2
    denominator = 2.0*(y0 - 2*y1 + y2)
    return T_s * numerator / denominator

T_s = samples_x[1] - samples_x[0]
parabolic_peak = samples_x[1] + parabolic_interpolation(samples_y[0],
    samples_y[1], samples_y[2], T_s)

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

fig.savefig('../../doc/images/diagram_parabolic_interpolation.png', dpi=figdpi)
fig.savefig('../../doc/images/diagram_parabolic_interpolation.eps', dpi=figdpi)

fig = plt.figure(2, figsize=figsize)
ax = plt.subplot(111)
ax.plot(xx, yy, label='XCORR')
ax.plot([true_peak], [yy.max()], 'p')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel('Displacement')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.plot(samples_x, j1(samples_x), 'o')
ax.set_ylim([-0.3, 0.4])

def cosine_fit(y0, y1, y2):
    omega = np.arccos((y0+y2)/(2*y1))
    theta = np.arctan((y0-y2)/(2*y1*np.sin(omega)))
    delta = -theta/omega
    return delta, omega, theta

delta, omega, theta = cosine_fit(samples_y[0], samples_y[1], samples_y[2])
cosine_peak = samples_x[1] + T_s*delta
ax.plot(cosine_peak, j1(cosine_peak), '*')
ax.plot(xx, yy.max()*np.cos(((xx-samples_x[1])/T_s)*omega + theta), '--', label='cosine fit')
ax.legend(loc='lower left')

ax.vlines([cosine_peak, true_peak], bias_ylim[0], bias_ylim[1])

ax.annotate('bias', xy=(true_peak, 0.1), xytext=(true_peak+0.3, 0.0),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))

fig.savefig('../../doc/images/diagram_cosine_interpolation.png', dpi=figdpi)
fig.savefig('../../doc/images/diagram_cosine_interpolation.eps', dpi=figdpi)

fig = plt.figure(3, figsize=figsize)
ax = plt.subplot(111)
ax.plot(xx, yy, label='XCORR')
ax.plot([true_peak], [yy.max()], 'p')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel('Displacement')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.plot(samples_x, j1(samples_x), 'o')
ax.set_ylim([-0.3, 0.4])

first_point_x = samples_x[1] + 0.3 * T_s
first_point_y = j1(first_point_x)

second_point_x = samples_x[1] - 0.4 * T_s
second_point_y = j1(second_point_x)
FancyArrowPatch = matplotlib.patches.FancyArrowPatch
fa = FancyArrowPatch(posA=(first_point_x, first_point_y),
    posB=(second_point_x, second_point_y),
    arrowstyle='->,head_width=2.0,head_length=5.0',
    connectionstyle='arc3,rad=-0.19'
    )
ax.add_artist(fa)
ax.plot([first_point_x, second_point_x], [first_point_y, second_point_y], 'ko', markerfacecolor='none', markersize=3.0)
ax.annotate('start', xy=(first_point_x-0.05, first_point_y-0.01), xytext=(true_peak, samples_y[2]+0.1),
    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.1'))

first_point_x = second_point_x
first_point_y = second_point_y

second_point_x = samples_x[1] - 0.85 * T_s
second_point_y = j1(second_point_x)
FancyArrowPatch = matplotlib.patches.FancyArrowPatch
fa = FancyArrowPatch(posA=(first_point_x, first_point_y),
    posB=(second_point_x, second_point_y),
    arrowstyle='->,head_width=2.0,head_length=5.0',
    connectionstyle='arc3,rad=1.49'
    )
ax.add_artist(fa)
ax.plot([first_point_x, second_point_x], [first_point_y, second_point_y], 'ko', markerfacecolor='none', markersize=3.0)

first_point_x = second_point_x
first_point_y = second_point_y

second_point_x = samples_x[1] - 0.55 * T_s
second_point_y = j1(second_point_x)
FancyArrowPatch = matplotlib.patches.FancyArrowPatch
fa = FancyArrowPatch(posA=(first_point_x, first_point_y),
    posB=(second_point_x, second_point_y),
    arrowstyle='->,head_width=2.0,head_length=5.0',
    connectionstyle='arc3,rad=1.49'
    )
ax.add_artist(fa)
ax.plot([first_point_x, second_point_x], [first_point_y, second_point_y], 'ko', markerfacecolor='none', markersize=3.0)

first_point_x = second_point_x
first_point_y = second_point_y

second_point_x = samples_x[1] - 0.65 * T_s
second_point_y = j1(second_point_x)
FancyArrowPatch = matplotlib.patches.FancyArrowPatch
fa = FancyArrowPatch(posA=(first_point_x, first_point_y),
    posB=(second_point_x, second_point_y),
    arrowstyle='->,head_width=2.0,head_length=5.0',
    connectionstyle='arc3,rad=0.49'
    )
ax.add_artist(fa)
ax.plot([first_point_x, second_point_x], [first_point_y, second_point_y], 'ko', markerfacecolor='none', markersize=3.0)
ax.legend(loc='lower left')

fig.savefig('../../doc/images/diagram_sinc_interpolation.png', dpi=figdpi)
fig.savefig('../../doc/images/diagram_sinc_interpolation.eps', dpi=figdpi)

plt.show()
