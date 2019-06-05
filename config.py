"""
config.py
Contains some default parameters used to generate certain styles of trees & spikes
"""

# Standard imports
import copy

# Self imports
import colours




# The tree parameters are often the same, so we copy & inherit them to make it less verbose
# See repo docs for description of which trees are which
tree_basic = {
    'angle':-90,
    'width_change':0.9,
    'split_prob_change':1.0,
    'large_angle_prob': 0.0,
    'large_angle': 60,    
}

tree_type_i = copy.deepcopy(tree_basic)
tree_type_i.update({
    'length_change':0.8,
    'length_vary_prop':0.2,
    'length_width':0.2,
    'angle_change':30,
    'angle_vary_prop':0.4,
    'split_prob':0.9,
    'depth':6,
    'max_depth':6
})

tree_type_ii = copy.deepcopy(tree_basic)
tree_type_ii.update({
    'length_change':0.5,
    'length_vary_prop':0.1,
    'length_width':0.1,
    'angle_change':20,
    'angle_vary_prop':1.0,
    'split_prob':0.95,
    'depth':4,
    'max_depth':4
})

tree_type_ia = copy.deepcopy(tree_type_i)
tree_type_ia.update({'split_prob_change': 0.9})

tree_type_iia = copy.deepcopy(tree_type_ii)
tree_type_iia.update({'split_prob_change': 0.9})

tree_type_ib = copy.deepcopy(tree_type_ia)
tree_type_ib.update({'large_angle_prob': 0.2})

tree_type_iib = copy.deepcopy(tree_type_iia)
tree_type_iib.update({'large_angle_prob': 0.2})

forest_trees = [tree_type_i, tree_type_ia, tree_type_ib, tree_type_ii, tree_type_iia, tree_type_iib]
forest_probabilities = [0.1, 0.2, 0.2, 0.1, 0.2, 0.2]


# Forward-facing green spike leaves
spikes_green = {
                "spike_direction":1,
                "spike_colour":colours.cols['green'],
                "spike_edge_colour":'k',
                "spike_edge_width":0.5,
                "spike_colour_jitter":0.1,
                "spike_width":0.3,
                "spike_length":2,
                "spike_jitter":0.5,
                "spike_layout":'regular',
                "spike_density_x":3,
                "spike_density_y":3,
                "spike_density_rnd":10,
                "spike_max_angle":40
}

# Mid-facing green/yellow dying spike leaves
spikes_yellow = {
                "spike_direction":-1,
                "spike_colour":colours.cols['green_yellow'],
                "spike_edge_colour":'k',
                "spike_edge_width":0.5,
                "spike_colour_jitter":0.1,
                "spike_width":0.3,
                "spike_length":2,
                "spike_jitter":0.5,
                "spike_layout":'regular',
                "spike_density_x":3,
                "spike_density_y":6,
                "spike_density_rnd":10,
                "spike_max_angle":70
}

# Backward-facing brown dead spikes
spikes_brown = {
                "spike_direction":-1,
                "spike_colour":colours.cols['brown'],
                "spike_edge_colour":'k',
                "spike_edge_width":0.5,
                "spike_colour_jitter":0.1,
                "spike_width":0.3,
                "spike_length":2,
                "spike_jitter":0.5,
                "spike_layout":'regular',
                "spike_density_x":3,
                "spike_density_y":6,
                "spike_density_rnd":10,
                "spike_max_angle":15
}