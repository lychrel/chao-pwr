import pandas as pd
import numpy as np
import math
from datetime import datetime
import time

"""
waveform	Current	CLK3	C1	C2	C3	C4	out
t0	4/22/2018  13:45:12.100572	4/22/2018  13:45:12.100573	4/22/2018  13:45:12.100573	4/22/2018  13:45:12.100574	4/22/2018  13:45:12.100574	4/22/2018  13:45:12.100575	4/22/2018  13:45:12.100575
delta t	3.330000E-6	3.330000E-6	3.330000E-6	3.330000E-6	3.330000E-6	3.330000E-6	3.330000E-6
"""

# delta t = 3.33 us

df = pd.read_csv('consumption.txt', sep='\t')

# I don't take input data bc I know the order: 00, 01, 10, 11
# technically I also know the Ci order: 0001, 0010, 0100, 1000

# simplify the 't' column: we can get rid of it!
# (just remember: each bin is )
# reclass everything as 0 or 1

# get last obnoxiuous row indexes
problem_rows = df.index[df['time'] = 'time'].values

# get sequence bounds from C crossings
for c in ['C1', 'C2', 'C3', 'C4']:
	c_changes = df.index[(df[c] == 0) & (df[c].shift(1) == 1) or (df[c] == 1) & (df[c].shift(1) == 0)].values

for row in problem_rows:
	# splice the dataframe: from problem_row to
	# (first c_change s.t. { problem_row - c_change < 0} )
	last_bad_row = next(change for change in c_changes if c_change>row)

	# cut out row -> last_bad_row
	df = df[:row].append(df[last_bad_row:])


"""
# now get everything to remove (everything after problem rows until Ci changes)
for problem_row in problem_rows:
	for c in ['C1', 'C2', 'C3', 'C4']:

		c_switch = df.loc[df[problem_row:][c] != df[problem_row:].change.shift(1)[c], 'capital'].item()

		# discard until that row + 1
		df = df.drop()

"""

# remove all the obnoxious rows
df = df[df.time != 'waveform']
df = df[df.time != 't0']
df = df[df.time != 'delta t']
df = df[df.time != '\n']
df = df[df.time != 'time']

print(df)

print(df.isnull().any())
print(df)

df.drop(columns=['time'], inplace=True)

print(df)

# threshold all the binary values
for col in list(df.columns.values)[1:]:
	df[col]=df[col].apply(lambda x: 1 if float(x)>1.0 else 0)
print(df)

# pickle it!
df.to_pickle('data.pkl')
