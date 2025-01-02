#!/usr/bin/env python3
from collections import namedtuple
style_marker = namedtuple('style_marker', ['linestyle', 'color', 'marker', 'barsabove', 'markersize'])
style_fill   = namedtuple('style_fill'  , ['histtype', 'edgecolor', 'linewidth', 'color', 'alpha'])
#style_line   = namedtuple('style_line'  , ['histtype', 'edgecolor', 'linewidth', 'color', 'alpha', 'lw'])
style_line   = namedtuple('style_line'  , ['histtype', 'edgecolor', 'linewidth', 'facecolor', 'alpha'])

MYCOLORS = [ '#8C736F', '#D4B8B4', '#ADAAA5', '#B7B7BD', '#AAB8AB', '#A08887', '#53565C']
MORANDI_DARK = ['#2D241F', '#614E52', '#7A6747', '#A06A50', '#605D54', '#511F1E', '#7D6647', '#69647B']
MORANDI_LIGHT= ['#D0C1C6', '#D6D6D6', '#BCA9A2', '#92ACD1', '#9B908A']
#MORANDI_SERIES = ['#903B1C', '#955839', '#A68E76', '#5F524A', '#A0765D']
MORANDI_SERIES = ['#D0C1C6', '#D6D6D6', '#BCA9A2', '#92ACD1', '#9B908A']
MY_MORANDI_LIGHT = ['black', '#92ACD1', '#B17A7D', '#D0C1C6']
MY_MORANDI_LIGHT = ['black', '#D5A1A3',  '#DFD8AB', '#B4C6DC', '#1b1f21'] # 0 2
#MY_MORANDI_LIGHT = ['black', '#D5A1A3',  '#B4C6DC'] # 0 2

def light_colors(idx):
    return MY_MORANDI_LIGHT[idx]

PLOT_STYLES = {
        'test'  : style_marker(linestyle='None', color=light_colors(0),marker='o', barsabove=True, markersize=4),

        'data'  : style_marker(linestyle='None', color=light_colors(0),marker='o', barsabove=True, markersize=4),
        'data0' : style_marker(linestyle='None', color=light_colors(0),marker='o', barsabove=True, markersize=4),
        'data1' : style_marker(linestyle='None', color=light_colors(1),marker='o', barsabove=True, markersize=4),
        'data2' : style_marker(linestyle='None', color=light_colors(2),marker='o', barsabove=True, markersize=4),
        'data3' : style_marker(linestyle='None', color=light_colors(3),marker='o', barsabove=True, markersize=4),

        'star0' : style_marker(linestyle='None', color=light_colors(0), marker='*', barsabove=True, markersize=1),
        'star1' : style_marker(linestyle='None', color=light_colors(1), marker='*', barsabove=True, markersize=4),
        'star2' : style_marker(linestyle='None', color=light_colors(2), marker='*', barsabove=True, markersize=8),
        'star3' : style_marker(linestyle='None', color=light_colors(3), marker='*', barsabove=True, markersize=8),

        'cross0': style_marker(linestyle='None', color=light_colors(0), marker='x', barsabove=True, markersize=1),
        'cross1': style_marker(linestyle='None', color=light_colors(1), marker='x', barsabove=True, markersize=4),
        'cross2': style_marker(linestyle='None', color=light_colors(2), marker='x', barsabove=True, markersize=8),
        'cross3': style_marker(linestyle='None', color=light_colors(3), marker='x', barsabove=True, markersize=8),

        'diamond0': style_marker(linestyle='None', color=light_colors(0), marker='D', barsabove=True, markersize=1),
        'diamond1': style_marker(linestyle='None', color=light_colors(1), marker='D', barsabove=True, markersize=4),
        'diamond2': style_marker(linestyle='None', color=light_colors(2), marker='D', barsabove=True, markersize=8),
        'diamond3': style_marker(linestyle='None', color=light_colors(3), marker='D', barsabove=True, markersize=8),

        'square0': style_marker(linestyle='None', color=light_colors(0), marker='s', barsabove=True, markersize=1),
        'square1': style_marker(linestyle='None', color=light_colors(1), marker='s', barsabove=True, markersize=4),
        'square2': style_marker(linestyle='None', color=light_colors(2), marker='s', barsabove=True, markersize=8),
        'square3': style_marker(linestyle='None', color=light_colors(3), marker='s', barsabove=True, markersize=8),


        'hist' : style_fill(histtype='stepfilled', edgecolor='1', linewidth=0.5, color=light_colors(0), alpha=1),
        'hist0': style_fill(histtype='stepfilled', edgecolor='1', linewidth=0.5, color=light_colors(0), alpha=1),
        'hist1': style_fill(histtype='stepfilled', edgecolor='1', linewidth=0.5, color=light_colors(1), alpha=1),
        'hist2': style_fill(histtype='stepfilled', edgecolor='1', linewidth=0.5, color=light_colors(2), alpha=1),
        'hist3': style_fill(histtype='stepfilled', edgecolor='1', linewidth=0.5, color=light_colors(3), alpha=1),

        'line' : style_line(histtype='stepfilled', edgecolor=light_colors(0), linewidth=4, facecolor='none', alpha=1),
        'line0': style_line(histtype='stepfilled', edgecolor=light_colors(0), linewidth=4, facecolor='none', alpha=1),
        'line1': style_line(histtype='stepfilled', edgecolor=light_colors(1), linewidth=4, facecolor='none', alpha=1),
        'line2': style_line(histtype='stepfilled', edgecolor=light_colors(2), linewidth=4, facecolor='none', alpha=1),
        'line3': style_line(histtype='stepfilled', edgecolor=light_colors(3), linewidth=4, facecolor='none', alpha=1),
        }
def PlotStyle(code:str, ) -> dict:
    if code in PLOT_STYLES:
        return PLOT_STYLES[code]._asdict()
    raise IOError(f'[InvalidStyle] Style "{code}" does not match any predefined style in VisualizationPresets.py')
    
if __name__ == '__main__':
    print(PlotStyle('hist1'))
