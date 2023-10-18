#!/usr/bin/env python

# -----------------------------------------------------------------------------
#  plot_model_336.py
#
#  Plot temperature data from the LakeShore Model 336 temperature controller.
#
#   * Author: Everybody is an author!
#   * Creation date: 21 August 2023
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

def temperature_data(filename, n=86400):
    """
    temperature_data(filename, n)

    Reads in a CSV file with temperature data.  the First column is 
    the datetime; the second, third, fourth, and fifth columns are
    inputs A, B, C, and D of the LakeShore Model 336 temperature
    controller; the sixth, seventh, eighth, and ninth columns are
    the control setpoints; the ninth, tenth, eleventh, and twelfth
    columns are the heater ranges; the thirteenth, fourteenth,
    fifteenth, and sixteenth columns are the heater outputs, and the
    seventeenth, eighteenth, nineteenth, and twentieth columns are
    the maximum currents.

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

    # names = [
    #     'datetime',
    #     'input_a', 'input_b', 'input_c', 'input_d',
    #     'setpoint_1', 'setpoint_2', 'setpoint_3', 'setpoint_4',
    #     'heater_range_1', 'heater_range_2', 'heater_range_3', 'heater_range_4',
    #     'heater_output_1', 'heater_output_2', 'heater_output_3', 'heater_output_4',
    #     'max_current_1', 'max_current_2', 'max_current_3', 'max_current_4',
    #     ]

    names = [
        'datetime',
        'input_a',
        'setpoint_1',
        'heater_range_1',
        'heater_output_1',
        'max_current_1',
        'heater_p_1',
        'heater_i_1',
        'heater_d_1',
        ]

    df = None
    with open(filename, 'r') as f:
        q = deque(f, n)
        # i really don't want to use pandas, but here we are
        df = pd.read_csv(io.StringIO(''.join(q)), names=names,
                         parse_dates=['datetime'])
    return df

def plot(ax1, ax2, df):
    """
    plot(ax1, ax2, df)

    Plot temperature values in Celsius as a function of datetime using
    data from the LakeShore Model 336 controller.

    Parameters
    ----------
    ax1 : matplotlib.axes
        matplotlib.axes object.
    ax2 : matplotlib.axes
        matplotlib.axes object.
    df : pandas.DataFrame
        pandas DataFrame with temperature data.

    Returns
    -------
    None

    """

    # labels for heater range values
    heater_range_dict = { 0 : 'off', 1 : 'low', 2 : 'med', 3 : 'high' }

    # clear axes
    ax1.cla()
    ax2.cla()

    # plot temperature and setpoint values
    ax1.plot(df['datetime'], df['input_a'],
             label='input A: {} $\!^\circ\!$C'.format(df['input_a'].iloc[-1]),
             color='C0')
    ax1.plot(df['datetime'], df['setpoint_1'],
             label='setpoint 1: {} $\!^\circ\!$C'
             .format(df['setpoint_1'].iloc[-1]),
             color='C1', linestyle='--', linewidth=1)

    # plot temperature and setpoint values
    ax2.plot(df['datetime'], df['heater_range_1']/20,
             label='heater range 1: {}'
             .format(heater_range_dict[df['heater_range_1'].iloc[-1]]),
             color='C2', linestyle=':', linewidth=1)
    ax2.plot(df['datetime'], df['heater_output_1']/100,
             label='heater output 1: {} %'
             .format(df['heater_output_1'].iloc[-1]),
             color='C3', linestyle=':', linewidth=1)

    ax1.set_ylabel('temperature [$\!^\circ\!$C]', horizontalalignment='right', y=1.0,
                   fontsize=14)

    ax1.grid(True, which='both', axis='both', color='k', linestyle=':',    
            linewidth=1, alpha=0.2)                                   

    ax1.xaxis.set_minor_locator(mticker.AutoMinorLocator())
    ax1.yaxis.set_minor_locator(mticker.AutoMinorLocator())

    # fking legend
    ax1.legend(loc='upper left', fontsize=12)
    ax2.legend(loc='lower left', fontsize=12)

    # format and rotate datetime tick labels
    major_formatter = mdates.DateFormatter('%m-%d %H:%M:%S')
    ax1.xaxis.set_major_formatter(major_formatter)
    ax1.xaxis.set_tick_params(rotation=80)

    # blood-sucking parasitic little tick
    ax1.tick_params(axis='both', which='major', labelsize=12)

    # text box
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    textstr = '\n'.join((
        'P: {:>6.1f}'.format(df['heater_p_1'].iloc[-1], ),
        'I: {:>6.1f}'.format(df['heater_i_1'].iloc[-1], ),
        'D: {:>6.1f}'.format(df['heater_d_1'].iloc[-1], )))
    ax1.text(0.014, 0.75, textstr, transform=ax1.transAxes, fontsize=14,
             verticalalignment='top', bbox=props, fontname='monospace')

    # set view limits of axes
    ax1.set_ylim(bottom=-60, top=40)
    # ax1.set_ylim(bottom=15, top=30)
    # ax1.set_ylim(bottom=15.0, top=30.0)
    # ax1.set_ylim(bottom=-35.0, top=-25.0)
    # ax1.set_ylim(bottom=-100.0, top=0.0)
    ax1.set_ylim(bottom=-100, top=40)
    ax2.set_ylim(bottom=0, top=1)
    now = datetime.now()
    then = np.datetime64(now)-np.timedelta64(len(df.index), 's')
    ax1.set_xlim(left=then, right=now)

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
df = temperature_data(input_file, n=rows)

#------------------------------------------------------------------------------
# plot pressure gauge data
#------------------------------------------------------------------------------
# fig = plt.figure(figsize=(12, 9))
fig = plt.figure(figsize=(18.3, 5))
ax1 = fig.add_subplot()
ax2 = ax1.twinx()

plot(ax1, ax2, df)

plt.tight_layout()
plt.ion()
plt.show()

#------------------------------------------------------------------------------
# update plot every `n` seconds
#------------------------------------------------------------------------------
while True:
    df = temperature_data(input_file, n=rows)
    plot(ax1, ax2, df)
    plt.pause(update)
