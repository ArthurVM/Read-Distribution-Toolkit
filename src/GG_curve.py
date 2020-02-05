#!/usr/bin/env python3

"""Generate the Gini Granularity curve and calculates the area under the curve
Takes a .tsv format file generated by GG_out_merge.py, structured as:

W    D1   D2   D3  ...
1     G    G    G  ...
2     G    G    G  ...
3     G    G    G  ...
...

Where Dn refers to a dataset, W refers to window size, and G is the Gini.

Dependancies:
Python3.6<=
argparse
numpy
matplotlib
"""

import argparse
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calc_GG_area(args):

    ## Calculates the area under the GG curves and outputs a plot from the GG-merge file

    gg_df=pd.read_csv(args.GG_mfile, sep="\t", header=0, index_col=0)

    window_array = gg_df.index.values
    w = window_array[1]-window_array[0]

    plt.style.use('ggplot')
    GG_f, GG_p = plt.subplots(2, figsize=(15, 10))

    for (colname, coldata) in gg_df.iteritems():
        norm_array = [x+1-np.max(coldata.values) for x in coldata.values]
        m_area = np.trapz(np.array(coldata.values), dx=w)/np.max(window_array)
        m_areaN = np.trapz(norm_array, dx=w)/np.max(window_array)
        print(f"{colname}\tGG-a={np.round(m_area, 3)}\tnGG-a={np.round(m_areaN, 3)}")

        GG_p[0].plot(window_array, coldata, linestyle="-", linewidth=0.75, label=f"{colname}    {np.round(m_area, 3)}")
        GG_p[1].plot(window_array, norm_array, linestyle="-", linewidth=0.75, label=f"{colname}    {np.round(m_areaN, 3)}")

    if args.s is False:

        GG_p[0].set_xlim([0, np.max(window_array)+1])
        GG_p[1].set_xlim([0, np.max(window_array)+1])
        GG_p[1].set_ylim([None, 1])

        GG_p.flat[0].set(ylabel="$G$", xlabel="$W$")
        GG_p.flat[1].set(ylabel="Normalised $G$", xlabel="$W$")

        GG_p[0].legend(ncol=3)
        GG_p[1].legend(ncol=3)
        plt.tight_layout()
        plt.show()

def parse_args(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument('script_path', action='store', help=argparse.SUPPRESS)

    parser.add_argument('GG_mfile', action='store', help='GG merge file generated by GG-merge.py.')
    parser.add_argument('-s', action='store_true', default=False, help='Suppress GG plot. Default = False.')

    args = parser.parse_args(argv)

    return args

def main(argv):

    args = parse_args(argv)

    calc_GG_area(args)

if __name__ == "__main__":
    if len(sys.argv) < 2 or "-h" in sys.argv:
        print(__doc__)
        main([sys.argv[0], "-h"])
        sys.exit(1)
    main(sys.argv)
