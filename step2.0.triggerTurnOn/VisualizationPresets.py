#!/usr/bin/env python3

MYCOLORS = [ '#8C736F', '#D4B8B4', '#ADAAA5', '#B7B7BD', '#AAB8AB', '#A08887', '#53565C']
MORANDI_DARK = ['#2D241F', '#614E52', '#7A6747', '#A06A50', '#605D54', '#511F1E', '#7D6647', '#69647B']
MORANDI_LIGHT= ['#D0C1C6', '#D6D6D6', '#BCA9A2', '#92ACD1', '#9B908A']
#MORANDI_SERIES = ['#903B1C', '#955839', '#A68E76', '#5F524A', '#A0765D']
MORANDI_SERIES = ['#D0C1C6', '#D6D6D6', '#BCA9A2', '#92ACD1', '#9B908A']
MY_MORANDI_LIGHT = ['black', '#92ACD1', '#B17A7D', '#D0C1C6']
MY_MORANDI_LIGHT = ['black', '#D5A1A3',  '#DFD8AB', '#B4C6DC'] # 0 2
MY_MORANDI_LIGHT = ['black', '#D5A1A3',  '#B4C6DC'] # 0 2

def light_colors(idx):
    return MY_MORANDI_LIGHT[idx]

PLOTSTYLE_DATA   = { 'linestyle': 'None', 'color': 'black', 'marker': 'o', 'barsabove':True }
# 0 3 7 dark
PLOTSTYLE_STAR0 = { 'linestyle': 'None', 'color': 'black'        , 'marker': '*', 'barsabove':True, 'markersize':1}
PLOTSTYLE_STAR1 = { 'linestyle': 'None', 'color': light_colors(1), 'marker': '*', 'barsabove':True, 'markersize':4}
PLOTSTYLE_STAR2 = { 'linestyle': 'None', 'color': light_colors(2), 'marker': '*', 'barsabove':True, 'markersize':8}

PLOTSTYLE_CROSS0 = { 'linestyle': 'None', 'color': 'black'        , 'marker': 'x', 'barsabove':True, 'markersize':1 }
PLOTSTYLE_CROSS1 = { 'linestyle': 'None', 'color': light_colors(1), 'marker': 'x', 'barsabove':True, 'markersize':4 }
PLOTSTYLE_CROSS2 = { 'linestyle': 'None', 'color': light_colors(2), 'marker': 'x', 'barsabove':True, 'markersize':8 }

PLOTSTYLE_DIAMOND0 = { 'linestyle': 'None', 'color': 'black'        , 'marker': 'D', 'barsabove':True, 'markersize':1 }
PLOTSTYLE_DIAMOND1 = { 'linestyle': 'None', 'color': light_colors(1), 'marker': 'D', 'barsabove':True, 'markersize':4 }
PLOTSTYLE_DIAMOND2 = { 'linestyle': 'None', 'color': light_colors(2), 'marker': 'D', 'barsabove':True, 'markersize':8 }

PLOTSTYLE_SQUARE0 = { 'linestyle': 'None', 'color': 'black'        , 'marker': 's', 'barsabove':True, 'markersize':1 }
PLOTSTYLE_SQUARE1 = { 'linestyle': 'None', 'color': light_colors(1), 'marker': 's', 'barsabove':True, 'markersize':4 }
PLOTSTYLE_SQUARE2 = { 'linestyle': 'None', 'color': light_colors(2), 'marker': 's', 'barsabove':True, 'markersize':8 }
PLOTSTYLE_HIST = { 'histtype': 'fill', 'edgecolor': '1', 'linewidth': 0.5 } # need to set color afterhand

def PlotStyle(code:str, ) -> dict:
    if code == 'test':
        return PLOTSTYLE_DATA
    if code == 'data':
        return PLOTSTYLE_DATA

    if code == 'star0':
        return PLOTSTYLE_STAR0
    if code == 'star1':
        return PLOTSTYLE_STAR1
    if code == 'star2':
        return PLOTSTYLE_STAR2

    if code == 'cross0':
        return PLOTSTYLE_CROSS0
    if code == 'cross1':
        return PLOTSTYLE_CROSS1
    if code == 'cross2':
        return PLOTSTYLE_CROSS2


    if code == 'diamond0':
        return PLOTSTYLE_DIAMOND0
    if code == 'diamond1':
        return PLOTSTYLE_DIAMOND1
    if code == 'diamond2':
        return PLOTSTYLE_DIAMOND2

    if code == 'square0':
        return PLOTSTYLE_SQUARE0
    if code == 'square1':
        return PLOTSTYLE_SQUARE1
    if code == 'square2':
        return PLOTSTYLE_SQUARE2

    if code == 'hist':
        return PLOTSTYLE_HIST
    
