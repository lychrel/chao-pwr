# cpower
subjecting chaos-based logic gates to power-analysis side-channel attacks

### Outline

1. ``fianle_small.py`` saves recorded data as dataframe and pickles it
2. ``process.py`` splits data into distinct signatures and saves them 1D Numpy arrays
3. ``plot.py`` generates function table & average power signatures, plots signatures
4. ``fun.py`` performs analysis (signature correlation measurements, etc.)
