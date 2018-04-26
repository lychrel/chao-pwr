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

print(df[df.time == 'waveform'])

df = df[300006:600000]
print(df[30000:300010])
print(df[600000:600015])

print(df[:-1])

#print(df)

df.drop(columns=['time'], inplace=True)


# threshold all the binary values
for col in list(df.columns.values)[1:]:
	df[col]=df[col].apply(lambda x: 1 if float(x)>1.0 else 0)
print(df)

# pickle it!
df.to_pickle('smalldata.pkl')
