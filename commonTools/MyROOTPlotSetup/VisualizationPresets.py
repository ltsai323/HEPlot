#!/usr/bin/env python3
from collections import namedtuple

style_marker = namedtuple('style_marker', ['linestyle', 'color', 'marker', 'barsabove', 'markersize'])
style_fill   = namedtuple('style_fill'  , ['histtype', 'edgecolor', 'linewidth', 'color', 'alpha'])
style_line   = namedtuple('style_line'  , ['histtype', 'edgecolor', 'linewidth', 'facecolor', 'alpha'])
style_bar    = namedtuple('style_bar'   , ['capsize', 'facecolor', 'ecolor', 'edgecolor'])

MYCOLORS = [ '#8C736F', '#D4B8B4', '#ADAAA5', '#B7B7BD', '#AAB8AB', '#A08887', '#53565C']
MORANDI_DARK = ['#2D241F', '#614E52', '#7A6747', '#A06A50', '#605D54', '#511F1E', '#7D6647', '#69647B']
MORANDI_LIGHT= ['#D0C1C6', '#D6D6D6', '#BCA9A2', '#92ACD1', '#9B908A']
MORANDI_SERIES = ['#D0C1C6', '#D6D6D6', '#BCA9A2', '#92ACD1', '#9B908A']
MY_MORANDI_LIGHT = ['black', '#D5A1A3',  '#DFD8AB', '#B4C6DC', '#1b1f21'] # 0 2
MY_MORANDI_LIGHT2 = ['#A7C6DB', '#C07A7A', '#A8B69C', '#D19A6A', '#A79BB7']

FILE_IDENTIFIER = 'VisualizationPresets.py'
DEBUG_MODE = True
def BUG(mesg):
    if DEBUG_MODE:
        print(f'b-{FILE_IDENTIFIER}@ {mesg}')


def light_colors(idx):
    return MY_MORANDI_LIGHT2[idx]

MARKER_SIZE=8
HIST_LINE_WIDTH=0.8
PLOT_STYLES = {
        'test'  : style_marker(linestyle='None', color=light_colors(0),marker='o', barsabove=True, markersize=MARKER_SIZE),

        'data'  : style_marker(linestyle='None', color='black'        ,marker='o', barsabove=True, markersize=MARKER_SIZE),
        'data0' : style_marker(linestyle='None', color=light_colors(0),marker='o', barsabove=True, markersize=MARKER_SIZE),
        'data1' : style_marker(linestyle='None', color=light_colors(1),marker='o', barsabove=True, markersize=MARKER_SIZE),
        'data2' : style_marker(linestyle='None', color=light_colors(2),marker='o', barsabove=True, markersize=MARKER_SIZE),
        'data3' : style_marker(linestyle='None', color=light_colors(3),marker='o', barsabove=True, markersize=MARKER_SIZE),
        'data4' : style_marker(linestyle='None', color=light_colors(4),marker='o', barsabove=True, markersize=MARKER_SIZE),

        'star0' : style_marker(linestyle='None', color=light_colors(0), marker='*', barsabove=True, markersize=MARKER_SIZE),
        'star1' : style_marker(linestyle='None', color=light_colors(1), marker='*', barsabove=True, markersize=MARKER_SIZE),
        'star2' : style_marker(linestyle='None', color=light_colors(2), marker='*', barsabove=True, markersize=MARKER_SIZE),
        'star3' : style_marker(linestyle='None', color=light_colors(3), marker='*', barsabove=True, markersize=MARKER_SIZE),
        'star4' : style_marker(linestyle='None', color=light_colors(4), marker='*', barsabove=True, markersize=MARKER_SIZE),

        'cross0': style_marker(linestyle='None', color=light_colors(0), marker='x', barsabove=True, markersize=MARKER_SIZE),
        'cross1': style_marker(linestyle='None', color=light_colors(1), marker='x', barsabove=True, markersize=MARKER_SIZE),
        'cross2': style_marker(linestyle='None', color=light_colors(2), marker='x', barsabove=True, markersize=MARKER_SIZE),
        'cross3': style_marker(linestyle='None', color=light_colors(3), marker='x', barsabove=True, markersize=MARKER_SIZE),
        'cross4': style_marker(linestyle='None', color=light_colors(4), marker='x', barsabove=True, markersize=MARKER_SIZE),

        'diamond0': style_marker(linestyle='None', color=light_colors(0), marker='D', barsabove=True, markersize=MARKER_SIZE),
        'diamond1': style_marker(linestyle='None', color=light_colors(1), marker='D', barsabove=True, markersize=MARKER_SIZE),
        'diamond2': style_marker(linestyle='None', color=light_colors(2), marker='D', barsabove=True, markersize=MARKER_SIZE),
        'diamond3': style_marker(linestyle='None', color=light_colors(3), marker='D', barsabove=True, markersize=MARKER_SIZE),
        'diamond4': style_marker(linestyle='None', color=light_colors(4), marker='D', barsabove=True, markersize=MARKER_SIZE),

        'square0': style_marker(linestyle='None', color=light_colors(0), marker='s', barsabove=True, markersize=MARKER_SIZE),
        'square1': style_marker(linestyle='None', color=light_colors(1), marker='s', barsabove=True, markersize=MARKER_SIZE),
        'square2': style_marker(linestyle='None', color=light_colors(2), marker='s', barsabove=True, markersize=MARKER_SIZE),
        'square3': style_marker(linestyle='None', color=light_colors(3), marker='s', barsabove=True, markersize=MARKER_SIZE),
        'square4': style_marker(linestyle='None', color=light_colors(4), marker='s', barsabove=True, markersize=MARKER_SIZE),


        'hist' : style_fill(histtype='stepfilled', edgecolor='1', linewidth=HIST_LINE_WIDTH, color=light_colors(0), alpha=0.7),
        'hist0': style_fill(histtype='stepfilled', edgecolor='1', linewidth=HIST_LINE_WIDTH, color=light_colors(0), alpha=0.7),
        'hist1': style_fill(histtype='stepfilled', edgecolor='1', linewidth=HIST_LINE_WIDTH, color=light_colors(1), alpha=0.7),
        'hist2': style_fill(histtype='stepfilled', edgecolor='1', linewidth=HIST_LINE_WIDTH, color=light_colors(2), alpha=0.7),
        'hist3': style_fill(histtype='stepfilled', edgecolor='1', linewidth=HIST_LINE_WIDTH, color=light_colors(3), alpha=0.7),
        'hist4': style_fill(histtype='stepfilled', edgecolor='1', linewidth=HIST_LINE_WIDTH, color=light_colors(4), alpha=0.7),
        'histBKG': style_fill(histtype='stepfilled', edgecolor='1', linewidth=HIST_LINE_WIDTH, color='#777581', alpha=0.7),

        'line' : style_line(histtype='stepfilled', edgecolor=light_colors(0), linewidth=4, facecolor='none', alpha=0.7),
        'line0': style_line(histtype='stepfilled', edgecolor=light_colors(0), linewidth=4, facecolor='none', alpha=0.7),
        'line1': style_line(histtype='stepfilled', edgecolor=light_colors(1), linewidth=4, facecolor='none', alpha=0.7),
        'line2': style_line(histtype='stepfilled', edgecolor=light_colors(2), linewidth=4, facecolor='none', alpha=0.7),
        'line3': style_line(histtype='stepfilled', edgecolor=light_colors(3), linewidth=4, facecolor='none', alpha=0.7),
        'line4': style_line(histtype='stepfilled', edgecolor=light_colors(4), linewidth=4, facecolor='none', alpha=0.7),

        'nostackb'   : style_bar(edgecolor='1', facecolor='black'        , ecolor='black', capsize=5),
        'nostackb0'  : style_bar(edgecolor='1', facecolor=light_colors(0), ecolor='black', capsize=5),
        'nostackb1'  : style_bar(edgecolor='1', facecolor=light_colors(1), ecolor='black', capsize=5),
        'nostackb2'  : style_bar(edgecolor='1', facecolor=light_colors(2), ecolor='black', capsize=5),
        'nostackb3'  : style_bar(edgecolor='1', facecolor=light_colors(3), ecolor='black', capsize=5),
        'nostackb4'  : style_bar(edgecolor='1', facecolor=light_colors(4), ecolor='black', capsize=5),
        'nostackbBKG': style_bar(edgecolor='1', facecolor='#777581'      , ecolor='black', capsize=5),
        #'nostackb'  : style_marker(linestyle='None', color=light_colors(0), marker='o', barsabove=True, markersize=MARKER_SIZE+2),
        #'nostackb0' : style_marker(linestyle='None', color=light_colors(0), marker='o', barsabove=True, markersize=MARKER_SIZE+2),
        #'nostackb1' : style_marker(linestyle='None', color=light_colors(1), marker='*', barsabove=True, markersize=MARKER_SIZE+2),
        #'nostackb2' : style_marker(linestyle='None', color=light_colors(2), marker='s', barsabove=True, markersize=MARKER_SIZE+2),
        #'nostackb3' : style_marker(linestyle='None', color=light_colors(3), marker='D', barsabove=True, markersize=MARKER_SIZE+2),
        #'nostackb4' : style_marker(linestyle='None', color=light_colors(4), marker='^', barsabove=True, markersize=MARKER_SIZE+2),
        #'nostackbBKG': style_marker(linestyle='None', color='#777581'     , marker='x', barsabove=True, markersize=MARKER_SIZE+2),
        }
def PlotStyle(code:str, ) -> dict:
    if code in PLOT_STYLES:
        return PLOT_STYLES[code]._asdict()
    raise IOError(f'[InvalidStyle] Style "{code}" does not match any predefined style in VisualizationPresets.py')

if __name__ == '__main__':
    print(PlotStyle('hist1'))


    
