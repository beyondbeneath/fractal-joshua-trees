"""
colours.py
Contains:
    * 28 non-standard colourmaps which look nice as scene backgrounds
    * Default Joshua Tree colours (trunk, spikes, leaves)
    * Some helper functions to produce colour variation & darken/lighten a given colour
"""

# Standard imports
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import numpy as np

# Custom colourmaps
# https://matplotlib.org/gallery/images_contours_and_fields/custom_cmap.html

# Similar to Alto's Odyssey
sky1 = [
    (0.0, [0.24, 0.25, 0.36]), # top of sky
    (0.5, [0.60, 0.42, 0.61]), # middle of sky
    (1.0, [0.94, 0.62, 0.68])  # bottom of sky (horizon)
]

# https://www.color-hex.com/color-palette/42455
sky2 = [
    (0.00, [0.27, 0.25, 0.43]),
    (0.70, [0.75, 0.30, 0.39]),
    (0.85, [0.88, 0.43, 0.34]),
    (0.95, [0.91, 0.67, 0.17]),
    (1.00, [0.94, 0.84, 0.41])
]

# Dark grey to blue (night time)
sky3 = [
    (0.00, [0.10, 0.10, 0.10]),
    (1.00, [0.20, 0.24, 0.38])
]

cmaps = {}
cmaps['alto'] = LinearSegmentedColormap.from_list('sky1', sky1)
cmaps['twilight_town'] = LinearSegmentedColormap.from_list('sky2', sky2)
cmaps['night'] = LinearSegmentedColormap.from_list('sky2', sky3)


# Add some interesting ones from UI gradients (https://uigradients.com)
ui_dict = {
    'blue_lagoon':['#191654','#43C6AC'],
    'what_lies_beyond':['#000C40', '#F0F2F0'],
    'dawn':['#3B4371','#F3904F'],
    'ibiza_sunset':['#ee0979','#ff6a00'],
    'cosmic_fusion':['#333399','#ff00cc'],
    'nepal':['#2657eb','#de6161'],
    'love_couple':['#3a6186','#89253e'],
    'dania':['#7BC6CC','#BE93C5'],
    'jupiter':['#19547b','#ffd89b'],
    'dusk':['#2C3E50','#FD746C'],
    'deep_sea_space':['#2C3E50','#4CA1AF'],
    'grapefruit_sunset':['#904e95','#e96443'],
    'sunset':['#0B486B','#F56217'],
    'sweet_morning':['#FF5F6D','#FFC371'],
    'transfile':['#CB3066','#16BFFD'],
    'alihossein':['#f7ff00','#db36a4'],
    'dark_skies':['#283E51','#4B79A1'],
    'shroom_haze':['#5C258D','#4389A2'],
    'electric_violet':['#4776E6','#8E54E9'],
    'kashmir':['#516395','#614385'],
    'crimson_tide':['#642B73','#C6426E'],
    'visions_of_grandeur':['#000046','#1CB5E0'],
    'blue_skies':['#2F80ED','#56CCF2'],
    'frost':['#000428','#004e92']
}

for k in ui_dict:
    cmaps[k] = LinearSegmentedColormap.from_list(k, [(0.0, ui_dict[k][0]), (1.0, ui_dict[k][1])])

cool_sky = [(0.0, '#2980B9'), (0.5, '#6DD5FA'), (1.0, '#FFFFFF')]
cmaps['cool_sky'] = LinearSegmentedColormap.from_list('cool_sky', cool_sky)

# Some pre-set colours for tree features
cols = {}
cols['green']        = [0.59, 0.78, 0.51]
cols['green_yellow'] = [0.74, 0.80, 0.60]
cols['yellow']       = [0.84, 0.80, 0.66]
cols['brown']        = [0.49, 0.45, 0.44]


def darken(col, amount):
    """Darken (amount > 0) or lighten (amount < 0) an [R,G,B] colour"""
    np_col = np.array(col)
    if amount < 0: adj_col = np_col - ((1 - np_col)*amount)
    else: adj_col = np_col - (np_col*amount)
    return list(adj_col)

def mod_col(col, amount, n):
    """Modify a given [R,G,B] colour by a fixed amount (randomly)
    TODO: Allow the RGB amounts to vary independently (so only one channels dithers for example)
    """
    assert amount >= 0 and amount <= 1, "Colour adjustment amount must be between 0 and 1"
    r = (np.random.random((n,3))-0.5)*amount
    new_cols = np.tile(col,(n,1)) + r
    new_cols[new_cols > 1] = 1
    new_cols[new_cols < 0] = 0
    return new_cols
