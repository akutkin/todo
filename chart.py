#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 00:55:27 2018
@author: I
"""

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.patches import Rectangle
import matplotlib.cm as cm

from matplotlib.colors import Normalize

import datetime
import dateutil
import numpy as np
import os
import sys


# Global settings
ww = 14.0 # figure width
wh = ww / 1.414286 # to fit A4 paper size
h=0.8 # height of rectangles
cmap = cm.autumn # colormap
norm = Normalize(vmin=0.5, vmax=10.01) # Priority normalization [1-10]

now = datetime.datetime.now()

def to_datetime(datetxt):
    """Text to the date"""
    if isinstance(datetxt, datetime.datetime):
        return datetxt

    try:
        date = dateutil.parser.parse(datetxt)
        return date
    except:
        print("Error: can not get date from the string: {}".format(datetxt))
        return None


def chart(fname):
    """
        Create chart
    """
    names, dates, urgs = [], [], []
    with open(fname) as f:
        for l in f.readlines():
            if l.startswith('#') or not len(l.strip()): continue
            vals = [_.strip() for _ in l.split()]
            if len(vals) == 4:
                name, startdate, enddate, priority = vals
            elif len(vals) == 3 and len(vals[-1]) > 2:
                name, startdate, enddate = vals
                priority = 5
            elif len(vals) == 3 and len(vals[-1]) <= 2:
                name, enddate, priority = vals
                startdate = now
            elif len(vals) == 2:
                name, enddate = vals
                startdate = now
                priority = 5
            else:
                print('Wrong line format in file')
                return 1
            names.append(name.replace('\n',''))
            dates.append([to_datetime(startdate), to_datetime(enddate)])
            urgs.append(int(priority))

    dates = np.array(dates)

    xl1, xl2 = dates.min(axis=0)[0], dates.max(axis=0)[1]

    fig, ax = plt.subplots(1, figsize=(ww, wh))
    ax.set_yticklabels([])

    dt = (xl2 - xl1).total_seconds()

    if dt < 3600 * 24:
        fmt = '%H:%M'
    else:
        fmt = "%Y-%m-%d"

    formatter = DateFormatter(fmt)
    ax.xaxis.set_major_formatter(formatter)

    dt = datetime.timedelta(seconds=dt/75.0)

    ax.set_ylim([-len(names), 0])
    ax.set_xlim([xl1-dt, xl2+dt])


    for indy, name in enumerate(names):
        urg = urgs[indy]

        print name, dates[indy][1], dates[indy][0]
        w = dates[indy][1] - dates[indy][0]
        x1 = dates[indy][0]
        y1 = -indy - 1
        if len(name) > 25:
            sname = name.split()
            print sname, len(sname)/2+1
            sname[len(sname)/2] += '\n'
            name = ' '.join(sname)
        ax.text(xl1-2*dt, y1 + 0.5, name,
                backgroundcolor='None',
                horizontalalignment='right',
                verticalalignment='center')
        clr = cm.ScalarMappable(norm=norm, cmap=cmap).to_rgba(urg)
        ax.add_patch(Rectangle((x1, y1+(1-h)/2.0), w, h,
                               alpha=0.75,
                               facecolor=clr,
                               edgecolor='none'))

    ax.yaxis.set_tick_params(size=.1)
    ax.xaxis.set_tick_params(size=2)
    ax.grid(color = 'grey', ls = ':', lw=1, alpha=0.2)
    fig.autofmt_xdate()
    fig.tight_layout(rect=(0.1, 0.02, 0.99, 0.95))
    ax.set_title(u'{}'.format(os.path.basename(fname)).upper())

    plt.draw()

#    plt.savefig('gantt.pdf')
    plt.show()

if __name__ == '__main__':

    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        fname =  os.path.expanduser('~') + "/todo"
    a = chart(fname)
