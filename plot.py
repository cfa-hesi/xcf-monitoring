#!/usr/bin/env python

# -----------------------------------------------------------------------------
#  plot.py
#
#  Plot pressure gauge data from the INFICON VGC503 gauge controller and
#  temperature data from the LakeShore Model 336 temperature controller.
#
#   * Author: Everybody is an author!
#   * Creation date: 1 April 2024
# -----------------------------------------------------------------------------

import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import inficon.plot_vgc503 as plot_vgc503
import lakeshore.plot_model_336 as plot_model_336

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
    parser.add_argument('--vgc503', type=str, required=True,
                        help='path to CSV file containing INFICON VGC503 gauge\
                              controller data')
    parser.add_argument('--model_336', type=str, required=True,
                        help='path to CSV file containing LakeShore Model 336 \
                              temperature controller data')
    parser.add_argument('--n', type=int,
                        help='number of rows to read from EOF')
    parser.add_argument('--update', type=int,
                        help='update interval in seconds')
    parser.add_argument('--truncate', action='store_true',
                        help='plot time axis up to most recent data point')
    args = parser.parse_args()

    vgc503_input_file = args.vgc503
    model_336_input_file = args.model_336
    if args.n:
        rows = args.n
    if args.update:
        update = args.update
    truncate = args.truncate

    #--------------------------------------------------------------------------
    # fetch pressure gauge data
    #--------------------------------------------------------------------------
    df_vgc503 = plot_vgc503.gauge_data(vgc503_input_file, n=rows)

    #--------------------------------------------------------------------------
    # fetch pressure gauge and temperature controller data
    #--------------------------------------------------------------------------
    df_model_336 = plot_model_336.temperature_data(model_336_input_file,
                                                   n=rows)

    #--------------------------------------------------------------------------
    # plot pressure gauge and temperature controller data
    #--------------------------------------------------------------------------
    fig = plt.figure(figsize=(18.3, 9.6))
    gs = gridspec.GridSpec(ncols=1, nrows=2, figure=fig)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax3 = ax2.twinx()
    ax1.tick_params(bottom=False, labelbottom=False)

    plot_vgc503.plot(ax1, df_vgc503, truncate)
    plot_model_336.plot(ax2, ax3, df_model_336, truncate)

    plt.tight_layout()
    plt.ion()
    plt.show()

    #--------------------------------------------------------------------------
    # update plot every `update` seconds
    #--------------------------------------------------------------------------
    while True:
        df_vgc503 = plot_vgc503.gauge_data(vgc503_input_file, n=rows)
        plot_vgc503.plot(ax1, df_vgc503, truncate)
        df_model_336 = plot_model_336.temperature_data(model_336_input_file,
                                                       n=rows)
        plot_model_336.plot(ax2, ax3, df_model_336, truncate)
        plt.pause(update)

