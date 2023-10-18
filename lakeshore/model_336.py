#!/usr/bin/env python

# -----------------------------------------------------------------------------
#  model_336.py
#
#  Fetch temperature data from the LakeShore Model 336 temperature controller
#  and writes data to a CSV file.
#
#   * Author: Everybody is an author!
#   * Creation date: 21 August 2023
# -----------------------------------------------------------------------------

import time
import datetime
import csv
from lakeshore import Model336

#------------------------------------------------------------------------------
# functions
#------------------------------------------------------------------------------

def append(row):
    """
    append(row)

    Appends a line to CSV file.

    Parameters
    ----------
    row : list (mix of str, int, and float)
        List of data points to be appended to CSV file.

    Returns
    -------
    None

    """
    with open('lakeshore_model_336_data.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------

if __name__ == '__main__':

    # connect to LakeShore Model 336 temperature controller
    lake = Model336(com_port='COM4')

    while True:

        # i can see you laughing
        # through dreams of perfect sleep
        time.sleep(1)

        # old stuff, keep for now
        #
        # print(lake.get_all_kelvin_reading())
        #
        # channels_alpha = ['A', 'B', 'C', 'D']
        # channels = range(0+1, 4+1)
        #
        # temperatures = [ lake.get_celsius_reading(_) for _ in channels_alpha ]
        # setpoints = [ lake.get_control_setpoint(_) for _ in channels ]
        # heater_range = [ int(lake.get_heater_range(_)) for _ in channels ]
        # heater_output = [ float(lake.get_heater_output(_)) for _ in channels ]
        # heater_max_current = [ float(lake.get_heater_setup(_)['max_current']) for _ in channels ]
        # heater_p = [ lake.get_heater_pid(_)['gain'] for _ in channels ]
        # heater_i = [ lake.get_heater_pid(_)['integral'] for _ in channels ]
        # heater_d = [ lake.get_heater_pid(_)['ramp_rate'] for _ in channels ]

        # fetch data from LakeShore temperature controller unit
        channel = 1
        temperatures = [ lake.get_celsius_reading('A') ]
        setpoints = [ lake.get_control_setpoint(channel) ]
        heater_range = [ int(lake.get_heater_range(channel)) ]
        heater_output = [ float(lake.get_heater_output(channel)) ]
        heater_max_current = [ float(lake.get_heater_setup(channel)['max_current']) ]
        heater_p = [ lake.get_heater_pid(channel)['gain'] ]
        heater_i = [ lake.get_heater_pid(channel)['integral'] ]
        heater_d = [ lake.get_heater_pid(channel)['ramp_rate'] ]

        # line to be appended to CSV file
        row = [ str(datetime.datetime.now()) ] + temperatures + setpoints \
              + heater_range + heater_output + heater_max_current + heater_p \
              + heater_i + heater_d

        # print to stdout
        print(row)

        # append to CSV file
        append(row)

