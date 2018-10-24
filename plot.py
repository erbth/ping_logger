# This file shall be dedicated to the Public Domain.

import pandas as pd
import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.dates import HourLocator, DateFormatter
from matplotlib.patches import Rectangle

input_filename='/home/therb/it/al_liss2000_ping_log.txt'
pdf_filename='/home/therb/it/al_liss2000_ping_log.pdf'
title='AL remote Server ping log'

headers = ['date', 'time', 'ip', 'status', 'response_time']
df = pd.read_csv(
        input_filename,
        parse_dates = {'datetime': [0,1]},
        names=headers,
        delimiter=' ')

asp = df.plot(
        x='datetime',
        y='response_time',
        style='x',
        markersize=3,
        title=title,
        figsize=(40 / 2.54, 22.5 / 2.54),
        legend=False);


asp.xaxis.set_major_locator(ticker.MultipleLocator(1))
asp.xaxis.set_minor_locator(HourLocator(byhour=[0,6,12,18]))

asp.xaxis.set_major_formatter(DateFormatter( '%d.%m.%Y' ))
asp.xaxis.set_minor_formatter(DateFormatter( '%H' ))

for tick in asp.xaxis.get_major_ticks():
    tick.set_pad( 3 * tick.get_pad())
    tick.label.set_fontsize(9)

for tick in asp.xaxis.get_minor_ticks():
    tick.label.set_fontsize(6)

# Add cursors
status = None
last_change = None
changes = []

for index, row in df.iterrows():
    if not last_change:
        last_change = row['datetime']

    if status and status != row['status']:
        color = 'green' if row['status'] == 'ok' else 'red'
        plt.axvline(
                x=row['datetime'],
                color=color,
                linewidth=1)

        changes.append((row['datetime'], row['status']))

        last_change = row['datetime']

    status = row['status']


for i in range(len(changes)):
    delta = pd.Timedelta(hours=3)

    if ((changes[i][1] == 'ok' and (i <= 0 or changes[i][0] - changes[i-1][0] > delta)) or
            (changes[i][1] != 'ok' and (i+1 >= len(changes) or changes[i+1][0] - changes[i][0] > delta))):

        label = ('OK %s' if changes[i][1] == 'ok' else 'Fehler %s') % changes[i][0].strftime('%d.%m.%Y %H:%M:%S')
        plt.text(changes[i][0] + pd.Timedelta(hours=1), 200, label, rotation=90, fontsize=6)



red = Rectangle((0,0), 1, 1, fc="r", fill=True)
green = Rectangle((0,0), 1, 1, fc='g', fill=True)
asp.legend([red, green], ['Verbindung verloren', 'Verbindung hergestellt'])

plt.ylabel('Antwortzeit / ms')
plt.xlabel('Datum & Uhrzeit')

plt.savefig(pdf_filename, dpi=600)
