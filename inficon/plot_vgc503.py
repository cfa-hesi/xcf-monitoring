#!/usr/bin/env python

# -----------------------------------------------------------------------------
#  plot_vgc503.py
#
#  Plot pressure gauge data from the INFICON VGC503 gauge controller.
#
#   * Author: Everybody is an author!
#   * Creation date: 19 August 2023
# -----------------------------------------------------------------------------

import argparse
from collections import deque
import io
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import pandas as pd

#------------------------------------------------------------------------------
# functions
#------------------------------------------------------------------------------

def gauge_data(filename, n=86400):
    """
    gauge_data(filename, n)

    Reads in a CSV file with pressure gauge data.  the First column is 
    the datetime; the second, third, and fourth columns are channels 1,
    2, and 3 of the INFICON VGC503 gauge controller.

    Parameters
    ----------
    filename : str
        Path to file CSV file.
    n : int
        Number of rows to read starting from the end of the file.

    Returns
    -------
    df : pandas.DataFrame

    """
    names = ['datetime', 'ch1', 'ch2', 'ch3']
    df = None
    with open(filename, 'r') as f:
        q = deque(f, n)
        # i really don't want to use pandas, but here we are
        df = pd.read_csv(io.StringIO(''.join(q)), names=names,
                         parse_dates=['datetime'])
    return df

def plot(ax, df):
    """
    plot(ax, df)

    Plot pressure values in mbar as a function of datetime using data
    from the INFICON VGC503 gauge controller.

    Parameters
    ----------
    ax : matplotlib.axes
        matplotlib.axes object.
    df : pandas.DataFrame
        pandas DataFrame with pressure gauge data.

    Returns
    -------
    None

    """

    ax.cla()  # clear axes

    #////////////////////////////////////////////////////////
    # for testing timedelta
    #////////////////////////////////////////////////////////
    # t = np.array(df['datetime'], dtype=np.datetime64)
    # dt = t - np.datetime64(datetime.now())
    # dt = dt.astype('timedelta64[s]')
    # ax.plot(dt, df['ch1'], label='channel 1')
    # ax.plot(dt, df['ch2'], label='channel 2')
    # ax.axvline(x=then, color='k', linestyle=':')
    # ax.axvline(x=now, color='k', linestyle=':')
    #////////////////////////////////////////////////////////

    # plot pressure values
    ax.plot(df['datetime'], df['ch1'],
            label='channel 1: {:.2E} mbar'.format(df['ch1'].iloc[-1]))
    ax.plot(df['datetime'], df['ch2'],
            label='channel 2: {:.2E} mbar'.format(df['ch2'].iloc[-1]),
            linestyle='--')

    ax.set_ylabel('pressure [mbar]', horizontalalignment='right', y=1.0,
                  fontsize=14)

    ax.grid(True, which='both', axis='both', color='k', linestyle=':',    
            linewidth=1, alpha=0.2)                                   

    # semi-log
    ax.set_yscale('log')
    ax.xaxis.set_minor_locator(mticker.AutoMinorLocator())
    ax.yaxis.set_major_locator(mticker.LogLocator(numticks=999))
    ax.yaxis.set_minor_locator(mticker.LogLocator(numticks=999, subs='auto'))

    # fking legend
    ax.legend(loc='upper left', fontsize=12)

    # format and rotate datetime tick labels
    major_formatter = mdates.DateFormatter('%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(major_formatter)
    ax.xaxis.set_tick_params(rotation=80)

    # blood-sucking parasitic little tick
    ax.tick_params(axis='both', which='major', labelsize=12)

    # set view limits of axes
    ax.set_ylim(top=3000, bottom=2e-8)
    now = datetime.now()
    then = np.datetime64(now)-np.timedelta64(len(df.index), 's')
    ax.set_xlim(left=then, right=now)

#------------------------------------------------------------------------------
# initialize parameters
#------------------------------------------------------------------------------
rows = 86400  # number of rows to plot
update = 10   # update interval in seconds

#------------------------------------------------------------------------------
# parse arguments
#------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='path to CSV file')
parser.add_argument('--n', type=int, help='number of rows to read from EOF')
parser.add_argument('--update', type=int, help='update interval in seconds')
args = parser.parse_args()

input_file = args.file
if args.n:
    rows = args.n
if args.update:
    update = args.update

#------------------------------------------------------------------------------
# fetch pressure gauge data
#------------------------------------------------------------------------------
df = gauge_data(input_file, n=rows)

#------------------------------------------------------------------------------
# plot pressure gauge data
#------------------------------------------------------------------------------
# fig = plt.figure(figsize=(12, 9))
fig = plt.figure(figsize=(18, 5))
ax = fig.add_subplot()

plot(ax, df)

plt.tight_layout()
plt.ion()
plt.show()

#------------------------------------------------------------------------------
# update plot every `n` seconds
#------------------------------------------------------------------------------
while True:
    df = gauge_data(input_file, n=rows)
    plot(ax, df)
    plt.pause(update)
