import pandas as pd
import numpy as np
import math
from datetime import datetime
import time
import progressbar

OUTPUT_DIR = 'smalldata/'

df = pd.read_pickle('smalldata.pkl')
# our indices were messed up bc we removed ~25 rows
df = df.reset_index(drop=True)

#print(df)

# get sequence bounds from CLK3 crossings
sequence_starts = df.index[(df['CLK3'] == 0) & (df['CLK3'].shift(1) == 1)].values
sequence_ends = df.index[(df['CLK3'] == 1) & (df['CLK3'].shift(1) == 0)].values

# clean up sequence bounds
#sequence_ends = sequence_ends[1:]
sequence_starts = sequence_starts[:-1]
print(sequence_starts, len(sequence_starts))
print(sequence_ends, len(sequence_ends))

input_index = 0
Ci_written = [0] * (2**4)

bar = progressbar.ProgressBar(max_value=len(sequence_starts))
for s0,sf in zip(sequence_starts, sequence_ends):
    # fun fact: the first four elements in each Ci
    # are with inputs 00, 01, 10, 11
    #print("BOUNDS")
    #print(s0,sf)
    sequence = df.loc[s0:sf]
    #print("SEQ SHAPE")
    #print(sequence.shape[0])
    sequence = sequence.reset_index(drop=True)

    #print("\n\nsequence:\n{0}".format(sequence))

    if input_index % 4 == 0:
        inputs = '00'
    elif input_index % 4 == 1:
        inputs = '01'
    elif input_index % 4 == 2:
        inputs = '10'
    else:
        inputs = '11'

    #print("inputs:\n{0}".format(inputs))

    Ci = ''
    for c in ['C1', 'C2', 'C3', 'C4']:
        Ci += str(int(round(sequence[c].mean())))
    #print("\n\n Ci:")
    #print(Ci)

    out = str(int(round(sequence['out'].mean())))
    #print("out:\n{0}".format(out))

    Ci_index = int(Ci, 2)

    Ci_written[Ci_index] += 1

    label = Ci + '_' + inputs + '_' + str(Ci_written[Ci_index]) + '_' + out
    filename = label + '.txt'
    filepath = 'smalldata/' + filename
    #print(label)

    #ts = sequence['Current']
    ts = sequence.as_matrix(columns=['Current'])
    ts = ts.astype(np.float32)

    print(len(ts))

    np.savetxt(filepath, ts)

    input_index += 1

    bar.update(input_index)
