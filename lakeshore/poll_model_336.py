#!/usr/bin/env python

# -----------------------------------------------------------------------------
#  poll_model_336.py
#
#  Poll data from the LakeShore Model 336 temperature controller.
#
#   * Author: Everybody is an author!
#   * Creation date: 21 August 2023
# -----------------------------------------------------------------------------

import os
import time
import datetime
import csv
from lakeshore import Model336

#------------------------------------------------------------------------------
# configurable parameters
#------------------------------------------------------------------------------
file_path = 'lakeshore_model_336_data.csv'

channel_a = True
channel_b = True
channel_c = True
channel_d = False

#------------------------------------------------------------------------------
# parameters
#------------------------------------------------------------------------------
channel_flags = [ channel_a, channel_b, channel_c, channel_d ]
channel_alpha_map = { 1 : 'A', 2 : 'B', 3 : 'C', 4 : 'D' }
channels = [ idx+1 for idx, _ in enumerate(channel_flags) if _ ]
channels_alpha = [ channel_alpha_map[channel] for channel in channels ]

temperature_labels = [ 'input_{}'.format(_.lower()) for _ in channels_alpha ]
setpoint_labels = [ 'setpoint_{}'.format(_) for _ in channels ]
heater_range_labels = [ 'heater_range_{}'.format(_) for _ in channels ]
heater_output_labels = [ 'heater_output_{}'.format(_) for _ in channels ]
heater_max_current_labels = [ 'heater_max_current_{}'.format(_) for _ in channels ]
heater_p_labels = [ 'heater_p_{}'.format(_) for _ in channels ]
heater_i_labels = [ 'heater_i_{}'.format(_) for _ in channels ]
heater_d_labels = [ 'heater_d_{}'.format(_) for _ in channels ]

header_row = [ 'datetime' ] + temperature_labels + setpoint_labels + \
             heater_range_labels + heater_output_labels + \
             heater_max_current_labels + \
             heater_p_labels + heater_i_labels + heater_d_labels

header_ok = False

#------------------------------------------------------------------------------
# functions
#------------------------------------------------------------------------------
def append(row, file_path):
    with open(file_path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

def check_header(header_row, file_path):
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        for row in csv.reader(f):
            print(row)
            if not header_row == row:
                msg = 'New header does not match header in CSV file.\n\n' \
                      'New header: {}\n\n' \
                      'Header in CSV file: {}\n'.format(header_row, row)
                raise ValueError(msg)
            break
    return True

#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
if __name__ == '__main__':

    # connect to LakeShore Model 336
    lake = Model336(com_port='COM4')

    while True:

        # sleep now in the fire
        time.sleep(1)

        #----------------------------------------------------------------------
        # for testing porpoises
        #----------------------------------------------------------------------
        # print(lake.get_all_kelvin_reading())
        # row = [ str(datetime.datetime.now()) ] + lake.get_all_kelvin_reading()
        #----------------------------------------------------------------------

        #----------------------------------------------------------------------
        # poll data from LakeShore Model 336
        #----------------------------------------------------------------------
        temperature = [ lake.get_celsius_reading(_) for _ in channels_alpha ]
        setpoint = [ lake.get_control_setpoint(_) for _ in channels ]
        heater_range = [ int(lake.get_heater_range(_)) for _ in channels ]
        heater_output = [ float(lake.get_heater_output(_)) for _ in channels ]
        heater_max_current = [ float(lake.get_heater_setup(_)['max_current']) for _ in channels ]
        heater_p = [ lake.get_heater_pid(_)['gain'] for _ in channels ]
        heater_i = [ lake.get_heater_pid(_)['integral'] for _ in channels ]
        heater_d = [ lake.get_heater_pid(_)['ramp_rate'] for _ in channels ]

        #----------------------------------------------------------------------
        # concatenate lists of data
        #----------------------------------------------------------------------
        row = [ str(datetime.datetime.now()) ] + temperature + setpoint + \
              heater_range + heater_output + heater_max_current + \
              heater_p + heater_i + heater_d

        #----------------------------------------------------------------------
        # append data to CSV file
        #----------------------------------------------------------------------
        # create file if it does not exist
        if not os.path.isfile(file_path):
            print('file does not exist')
            append(header_row, file_path)

        # check if headers match in CSV file before appending
        if not header_ok:
            header_ok = check_header(header_row, file_path)

        # append to file
        append(row, file_path)
        print(row)
