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

    Reads in a CSV file with temperature data from the LakeShore Model 336
    temperature controller.

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

    # i really don't want to use pandas, but here we are
    df = pd.read_csv(filename, parse_dates=['datetime']).tail(n)
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
             color='C1', linestyle=':', linewidth=1)
    ax1.plot(df['datetime'], df['input_b'],
             label='input B: {} $\!^\circ\!$C'.format(df['input_b'].iloc[-1]),
             color='C2', linestyle='--')
    ax1.plot(df['datetime'], df['setpoint_2'],
             label='setpoint 2: {} $\!^\circ\!$C'
             .format(df['setpoint_2'].iloc[-1]),
             color='C3', linestyle=':', linewidth=1)

    # plot heater values
    ax2.plot(df['datetime'], df['heater_range_1']/20,
             label='heater range 1: {}'
             .format(heater_range_dict[df['heater_range_1'].iloc[-1]]),
             color='C4', linestyle=':', linewidth=1)
    ax2.plot(df['datetime'], df['heater_output_1']/100,
             label='heater output 1: {} %'
             .format(df['heater_output_1'].iloc[-1]),
             color='C5', linestyle=':', linewidth=1)
    ax2.plot(df['datetime'], df['heater_range_2']/20,
             label='heater range 2: {}'
             .format(heater_range_dict[df['heater_range_2'].iloc[-1]]),
             color='C4', linestyle=':', linewidth=1)
    ax2.plot(df['datetime'], df['heater_output_2']/100,
             label='heater output 2: {} %'
             .format(df['heater_output_2'].iloc[-1]),
             color='C5', linestyle=':', linewidth=1)

    ax1.set_ylabel('temperature [$\!^\circ\!$C]', horizontalalignment='right',
                   y=1.0, fontsize=14)

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
    textstr = 'heater 1\n' + '\n'.join((
        'P: {:>6.1f}'.format(df['heater_p_1'].iloc[-1], ),
        'I: {:>6.1f}'.format(df['heater_i_1'].iloc[-1], ),
        'D: {:>6.1f}'.format(df['heater_d_1'].iloc[-1], )))
    ax1.text(0.015, 0.575, textstr, transform=ax1.transAxes, fontsize=12,
             verticalalignment='top', bbox=props, fontname='monospace')
    textstr = 'heater 2\n' + '\n'.join((
        'P: {:>6.1f}'.format(df['heater_p_2'].iloc[-1], ),
        'I: {:>6.1f}'.format(df['heater_i_2'].iloc[-1], ),
        'D: {:>6.1f}'.format(df['heater_d_2'].iloc[-1], )))
    ax1.text(0.080, 0.575, textstr, transform=ax1.transAxes, fontsize=12,
             verticalalignment='top', bbox=props, fontname='monospace')

    # set view limits of axes
    ax2.set_ylim(bottom=0, top=1)
    ax1.set_ylim(bottom=-100, top=30)
    now = datetime.now()
    then = df['datetime'].iloc[0]
    ax1.set_xlim(left=then, right=now)

#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
if __name__ == '__main__':

    #--------------------------------------------------------------------------
    # initialize parameters
    #--------------------------------------------------------------------------
    rows = 86400  # number of rows to plot
    update = 10   # update interval in seconds

    #--------------------------------------------------------------------------
    # parse arguments
    #--------------------------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='path to CSV file')
    parser.add_argument('--n', type=int,
                        help='number of rows to read from EOF')
    parser.add_argument('--update', type=int,
                        help='update interval in seconds')
    args = parser.parse_args()

    input_file = args.file
    if args.n:
        rows = args.n
    if args.update:
        update = args.update

    #--------------------------------------------------------------------------
    # fetch temperature controller data
    #--------------------------------------------------------------------------
    df = temperature_data(input_file, n=rows)

    #--------------------------------------------------------------------------
    # plot temperature controller data
    #--------------------------------------------------------------------------
    # fig = plt.figure(figsize=(12, 9))
    fig = plt.figure(figsize=(18.3, 5))
    ax1 = fig.add_subplot()
    ax2 = ax1.twinx()

    plot(ax1, ax2, df)

    plt.tight_layout()
    plt.ion()
    plt.show()

    #--------------------------------------------------------------------------
    # update plot every `update` seconds
    #--------------------------------------------------------------------------
    while True:
        df = temperature_data(input_file, n=rows)
        plot(ax1, ax2, df)
        plt.pause(update)

