import matplotlib.pyplot as plt
import numpy as np

import itertools
from glob import glob

import progressbar

AVG_DIR = 'smallavg/'

def function_table():
    # function numbers
    # AND   00 01 10 11 -> 0001 = 1
    AND = 1
    # OR    00 01 10 11 -> 0111 = 7
    OR = 1 + 2 + 4
    # NAND  00 01 10 11 -> 1110 = 14
    NAND = 8 + 4 + 2
    # NOR   00 01 10 11 -> 1001 = 9
    NOR = 8 + 1
    # XOR   00 01 10 11 -> 0110 = 6
    XOR = 4 + 2

    # compile function table

    # for each Ci
    # make a binary output string 'XXXX'
    # corresponding to inputs 00 01 10 11
    # if the integer version of that binary number is a func,
    # add it to the function dict
    Ci_possibilities = ["".join(seq)
                        for seq in itertools.product("01", repeat=4)]
    function_table = {}
    for ci in Ci_possibilities:
        outstring = ''
        for inpair in ['00', '01', '10', '11']:

            outputs_for_input = list(map(float, [fname[-5:-4]
                                     for fname in glob('smalldata/' + ci + '_' + inpair + '*')]))

            avg_output_for_input = int(round(sum(outputs_for_input)/len(outputs_for_input)))

            outstring += str(avg_output_for_input)

        #print("output string for {0}: {1}".format(ci, outstring))

        outval = int(outstring, 2)

        #print("output string int: {0}".format(outval))

        if outval == AND:
            function_table[ci] = 'AND'
        elif outval == OR:
            function_table[ci] = 'OR'
        elif outval == NAND:
            function_table[ci] = 'NAND'
        elif outval == NOR:
            function_table[ci] = 'NOR'
        elif outval == XOR:
            function_table[ci] = 'XOR'
        else:
            function_table[ci] = 'none'

    return function_table

def generate_average_signals():
    Ci_possibilities = ["".join(seq)
                        for seq in itertools.product("01", repeat=4)]
    for ci in Ci_possibilities:

        for inpair in ['00', '01', '10', '11']:

            signals = glob('smalldata/' + ci + '_' + inpair + '*')
            reduced_signals = signals

            for signal in signals:
                siggy = np.loadtxt(signal)
                if len(siggy) < 96:
                    reduced_signals.remove(siggy)
                if len(siggy) > 100:
                    print("removing overlong signal: {0}".format(len(siggy)))
                    reduced_signals.remove(siggy)
            signals = reduced_signals

            # begin np array of signals (assume len 98)
            avg_signal = np.empty((96, len(signals)))

            # construct np array of ci,inp files (one ts per column)
            bar = progressbar.ProgressBar(max_value=len(signals))
            for index, signal in enumerate(signals):
                siggy = np.loadtxt(signal)
                if len(siggy) > 96:
                    print("signal too long: length {0}".format(len(siggy)))
                    while len(siggy) > 96:
                        siggy = siggy[:-1]
                        # remove last entry
                # add signal to array
                avg_signal[:,index] = siggy.T

                bar.update(index)

            avg_signal = avg_signal.mean(axis=1)

            fpath = 'smallavg/' + ci + '_' + inpair + '.txt'

            np.savetxt(fpath, avg_signal)

    print("finished generating avg signals")

def plot_all():

    for ci in ["".join(seq)
                for seq in itertools.product("01", repeat=4)]:

        for inpair in ['00', '01', '10', '11']:

            x = np.linspace(0, 96*3.3, 97*3.3)
            plt.gcf().subplots_adjust(left=0.2)#, right=0.73)
            #plt.gcf().subplots_adjust(bottom=0.3)
            plt.ylabel('Current (A)')
            plt.xlabel('\nTime (320 us)')
            plt.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                labelbottom='off') # labels along the bottom edge are off

            for avg_signal in glob('smalldata/' + ci + '_' + inpair + '*'):
                ts = np.loadtxt(avg_signal)

                plt.plot(ts, label = avg_signal[:-4].strip('smalldata/'))

            # Place a legend to the right of this smaller subplot.
            #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., ncol=2)
            plt.title("Power Signature of {0}({1})".format(ci, inpair))
            plt.savefig('smallimg/' + ci + '_' + inpair + '.png')

            plt.clf()

    #plt.show()

def plot_averages():

    for ci in ["".join(seq)
                for seq in itertools.product("01", repeat=4)]:

        for inpair in ['00', '01', '10', '11']:

            x = np.linspace(0, 96, 97)
            #plt.gcf().subplots_adjust(left=0.2)#, right=0.73)
            #plt.gcf().subplots_adjust(bottom=0.2)
            plt.ylabel('Current (A)')
            plt.xlabel('\nTime (320 us)')
            plt.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                labelbottom='off') # labels along the bottom edge are off

            fname = 'smallavg/' + ci + '_' + inpair + '.txt'

            ts = np.loadtxt(fname)

            plt.plot(ts, label = fname[:-4].strip('smallavg/'))

            # Place a legend to the right of this smaller subplot.
            #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., ncol=2)
            #plt.title("Average Power Signature of {0}({1})".format(ci, inpair))
            plt.axis('off')
            plt.savefig('smallimgavg/noplots/' + ci + '_' + inpair + '.png')

            plt.clf()

    #plt.show()

def plot_all_by_input():

        for inpair in ['00', '01', '10', '11']:

            for ci in ["".join(seq)
                        for seq in itertools.product("01", repeat=4)]:

                x = np.linspace(0, 96, 97)
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

                for fname in glob('smalldata/' + ci + '_' + inpair + '*'):

                    ts = np.loadtxt(fname)

                    plt.plot(ts, label = fname[:-4].strip('smallavg/')[:-3])

            # Place a legend to the right of this smaller subplot.
            #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)#, ncol=2)
            plt.title("Average Power Signature of {0}".format(inpair))
            plt.savefig('smallimg/input/' + inpair + '.png')

            plt.clf()

def plot_all_averages_by_input():

        for inpair in ['00', '01', '10', '11']:

            for ci in ["".join(seq)
                        for seq in itertools.product("01", repeat=4)]:

                x = np.linspace(0, 96, 97)
                plt.gcf().subplots_adjust(left=0.2, right=0.73)
                plt.gcf().subplots_adjust(bottom=0.2)
                plt.ylabel('Current (A)')
                plt.xlabel('\nTime (320 us)')
                plt.tick_params(
                    axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom='off',      # ticks along the bottom edge are off
                    top='off',         # ticks along the top edge are off
                    labelbottom='off') # labels along the bottom edge are off

                fname = 'smallavg/' + ci + '_' + inpair + '.txt'

                ts = np.loadtxt(fname)

                plt.plot(ts, label = fname[:-4].strip('smallavg/')[:-3])

            # Place a legend to the right of this smaller subplot.
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)#, ncol=2)
            #plt.title("Average Power Signature of {0}".format(inpair))
            plt.savefig('smallimgavg/input/' + inpair + '.png')

            plt.clf()

#plot_all()
#plot_averages()
#plot_all_by_input()
#plot_all_averages_by_input()
