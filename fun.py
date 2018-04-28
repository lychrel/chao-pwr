import pandas as pd
import numpy as np
import math
from datetime import datetime
import time
import progressbar

from scipy import signal
import matplotlib.pyplot as plt

import itertools

import matplotlib.colors as mcolors

# gives crosscorr between 1 and 0
def jcross(sig1, sig2, delay=0):
    return np.dot(sig1, sig2) / math.sqrt(np.sum(sig1**2) * np.sum(sig2**2))

# gives crosscorr betweein 1 and -1
# http://paulbourke.net/miscellaneous/correlate/
def kcross(sig1, sig2, delay=0):
    m1 = np.mean(sig1)
    m2 = np.mean(sig2)

    sig1_norm = np.subtract(sig1, m1)
    sig2_norm = np.subtract(sig2, m2)

    top = np.dot(sig1_norm, sig2_norm)
    bottom = math.sqrt(np.sum(sig1_norm**2) * np.sum(sig2_norm**2))

    return top/bottom

# maps out cross correlations beteween 0 and 1 (doesn't know phase shifts)
def find_cross_correlations():

    # for each input,
    # histogram of similarity measurements:
    # coherence histogram, each axis 0000, 0001, 0010, 0100, 1000, etc.
    # 16 x 16 coherence plot
    clist = ["".join(seq) for seq in itertools.product("01", repeat=4)]

    for inpair in ['00', '01', '10', '11']:

        H = np.empty((2**4, 2**4))
        for ci_row in clist:

            for ci_col in clist:

                sig1 = np.loadtxt('smallavg/' + ci_row + '_' + inpair + '.txt')
                sig2 = np.loadtxt('smallavg/' + ci_col + '_' + inpair + '.txt')

                from sklearn.preprocessing import minmax_scale

                # scale signals between 0 and 1
                sig1 = minmax_scale(sig1)
                sig2 = minmax_scale(sig2)

                avg_crosscor = jcross(sig1, sig2)

                rindex = clist.index(ci_row)
                cindex = clist.index(ci_col)

                H[rindex][cindex] = avg_crosscor


        import matplotlib as mpl

        fig = plt.figure(figsize=(6, 3.2))

        ax = fig.add_subplot(111)

        print("YOU ALREADY KNOW WHAT TIME IT IS")
        print(np.mean(H))

        ax.set_title('Norm\'d Cross-Correlations for {0}'.format(inpair))
        plt.imshow(H)
        ax.set_aspect('equal')
        ax.invert_yaxis()

        cax = fig.add_axes([0.1, 0.12, 0.78, 0.8])
        cax.get_xaxis().set_visible(False)
        cax.get_yaxis().set_visible(False)
        cax.patch.set_alpha(0)
        cax.set_frame_on(False)
        plt.colorbar(orientation='vertical', cmap=mpl.cm.RdYlGn)
        plt.savefig('smallimg/corr/{0}.png'.format(inpair))

        plt.clf()

# maps out cross-correlations between 1 and -1 (phase-shift aware)
def find_cross_correlations_w_range():

    # for each input,
    # histogram of similarity measurements:
    # coherence histogram, each axis 0000, 0001, 0010, 0100, 1000, etc.
    # 16 x 16 coherence plot
    clist = ["".join(seq) for seq in itertools.product("01", repeat=4)]

    for inpair in ['00', '01', '10', '11']:

        H = np.empty((2**4, 2**4))
        for ci_row in clist:

            for ci_col in clist:

                sig1 = np.loadtxt('smallavg/' + ci_row + '_' + inpair + '.txt')
                sig2 = np.loadtxt('smallavg/' + ci_col + '_' + inpair + '.txt')

                from sklearn.preprocessing import minmax_scale

                # scale signals between 0 and 1
                sig1 = minmax_scale(sig1)
                sig2 = minmax_scale(sig2)

                avg_crosscor = kcross(sig1, sig2)

                rindex = clist.index(ci_row)
                cindex = clist.index(ci_col)

                H[rindex][cindex] = avg_crosscor


        import matplotlib as mpl

        fig = plt.figure(figsize=(6, 3.2))

        ax = fig.add_subplot(111)

        print("YOU ALREADY KNOW WHAT TIME IT IS")
        print(np.mean(H))

        ax.set_title('Norm\'d Cross-Correlations for {0}'.format(inpair))
        plt.imshow(H)
        ax.set_aspect('equal')
        ax.invert_yaxis()

        cax = fig.add_axes([0.1, 0.12, 0.78, 0.8])
        cax.get_xaxis().set_visible(False)
        cax.get_yaxis().set_visible(False)
        cax.patch.set_alpha(0)
        cax.set_frame_on(False)
        plt.colorbar(orientation='vertical', cmap=mpl.cm.RdYlGn)
        plt.savefig('smallimg/fullcorr/{0}.png'.format(inpair))

        plt.clf()

# maps out cross-correlations between 1 and -1, then equates -1 to 1 (doesn't care abt phase shifts)
def find_cross_correlations_w_range_ignored():

    # for each input,
    # histogram of similarity measurements:
    # coherence histogram, each axis 0000, 0001, 0010, 0100, 1000, etc.
    # 16 x 16 coherence plot
    clist = ["".join(seq) for seq in itertools.product("01", repeat=4)]

    for inpair in ['00', '01', '10', '11']:

        H = np.empty((2**4, 2**4))
        for ci_row in clist:

            for ci_col in clist:

                sig1 = np.loadtxt('smallavg/' + ci_row + '_' + inpair + '.txt')
                sig2 = np.loadtxt('smallavg/' + ci_col + '_' + inpair + '.txt')

                from sklearn.preprocessing import minmax_scale

                # scale signals between 0 and 1
                sig1 = minmax_scale(sig1)
                sig2 = minmax_scale(sig2)

                avg_crosscor = kcross(sig1, sig2)

                rindex = clist.index(ci_row)
                cindex = clist.index(ci_col)

                H[rindex][cindex] = abs(avg_crosscor)


        import matplotlib as mpl

        fig = plt.figure(figsize=(6, 3.2))

        ax = fig.add_subplot(111)

        print("YOU ALREADY KNOW WHAT TIME IT IS")
        print(np.mean(H))

        ax.set_title('Norm\'d Cross-Correlations for {0}'.format(inpair))
        plt.imshow(H)
        ax.set_aspect('equal')
        ax.invert_yaxis()

        cax = fig.add_axes([0.1, 0.12, 0.78, 0.8])
        cax.get_xaxis().set_visible(False)
        cax.get_yaxis().set_visible(False)
        cax.patch.set_alpha(0)
        cax.set_frame_on(False)
        plt.colorbar(orientation='vertical', cmap=mpl.cm.RdYlGn)
        plt.savefig('smallimg/abscorr/{0}.png'.format(inpair))

        plt.clf()

def find_correlations_for_config():

    # for each input,
    # histogram of similarity measurements:
    # coherence histogram, each axis 0000, 0001, 0010, 0100, 1000, etc.
    # 16 x 16 coherence plot
    clist = ["".join(seq) for seq in itertools.product("01", repeat=4)]

    for ci in clist:

        H = np.empty((4, 4))

        for inpair1 in ['00', '01', '10', '11']:

            for inpair2 in ['00', '01', '10', '11']:

                sig1 = np.loadtxt('smallavg/' + ci + '_' + inpair1 + '.txt')
                sig2 = np.loadtxt('smallavg/' + ci + '_' + inpair2 + '.txt')

                from sklearn.preprocessing import minmax_scale

                sig1 = minmax_scale(sig1)
                sig2 = minmax_scale(sig2)

                avg_crosscor = jcross(sig1, sig2)

                rindex = ['00', '01', '10', '11'].index(inpair1)
                cindex = ['00', '01', '10', '11'].index(inpair2)

                H[rindex][cindex] = avg_crosscor


        import matplotlib as mpl

        fig = plt.figure(figsize=(6, 3.2))

        ax = fig.add_subplot(111)


        ax.set_title('Norm\'d Cross-Correlations for {0}'.format(ci))
        plt.imshow(H)
        ax.set_aspect('equal')
        ax.invert_yaxis()

        cax = fig.add_axes([0.1, 0.12, 0.78, 0.8])
        cax.get_xaxis().set_visible(False)
        cax.get_yaxis().set_visible(False)
        cax.patch.set_alpha(0)
        cax.set_frame_on(False)
        plt.colorbar(orientation='vertical', cmap=mpl.cm.RdYlGn)
        plt.savefig('smallimg/corr/ci/{0}.png'.format(ci))

        plt.clf()

"""
from sklearn.preprocessing import minmax_scale

sig1 = np.loadtxt('smallavg/0100_10.txt')
sig2 = np.loadtxt('smallavg/0000_10.txt')

n1 = minmax_scale(sig1)
n2 = minmax_scale(sig2)

# normalized CC
cross_corr = jcross(sig1, sig2)
print(cross_corr)
ncross_corr = jcross(n1, n2)
print(ncross_corr)

x = np.arange(0, 320, 96)
plt.gcf().subplots_adjust(left=0.2)#, right=0.73)
plt.gcf().subplots_adjust(bottom=0.2)
plt.ylabel('Current (A)')
plt.xlabel('\nTime (320 us)')
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off

plt.plot(sig1, label='0101(10)')
plt.plot(sig2, label='0011(10)')
#plt.plot(n1, label='n0101(01)')
#plt.plot(n2, label='n0011(01)')

# Place a legend to the right of this smaller subplot.
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.title("Power Signatures of Similar Signals")
plt.savefig('smallimg/corr/cc_test.png')


find_cross_correlations()
find_correlations_for_config()
"""

find_cross_correlations_w_range_ignored()
