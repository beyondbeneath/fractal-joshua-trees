"""
tree.py
Contains the functions to draw:
    * simple line tree (the classic "dead tree" look)
    * joshua trees (tree generation, texture generation)

"""

# Standard imports
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

# Self imports
import colours
import config

def draw_random_joshua_tree(
                            x1=0,
                            y1=0,
                            length=10,
                            col=colours.cols['brown'],
                            draw_rect=False,
                            draw_texture=[True,True,True],
                            darken=None,
                            zorder=4,
                            spike_forward_params=config.spikes_green,
                            spike_mid_params=config.spikes_yellow,
                            spike_back_params=config.spikes_brown,
                            seed=None
                            ):
    if seed is not None:
        np.random.seed(seed)
    rnd_params = np.random.choice(config.forest_trees, p=config.forest_probabilities)
    draw_joshua_tree(
        x1=x1,
        y1=y1,
        length=length,
        col=col,
        draw_rect=draw_rect,
        draw_texture=draw_texture,
        darken=darken,
        zorder=zorder,
        spike_forward_params=spike_forward_params,
        spike_mid_params=spike_mid_params,
        spike_back_params=spike_back_params,
        **rnd_params
        )

def draw_joshua_tree(
                    x1=0,
                    y1=0,
                    length=10,
                    length_change=0.8,
                    length_vary_prop=0.2,
                    length_width=0.2,
                    width=None,
                    width_change=0.9,
                    angle=-90,
                    angle_change=30,
                    angle_vary_prop=0.4,
                    large_angle_prob=0.0,
                    large_angle=60, 
                    split_prob=0.9,
                    split_prob_change=1.0,
                    depth=6,
                    max_depth=6,
                    col=colours.cols['brown'],
                    draw_rect=False,
                    draw_texture=[True,True,True],
                    darken=None,
                    zorder=4,
                    spike_forward_params=config.spikes_green,
                    spike_mid_params=config.spikes_yellow,
                    spike_back_params=config.spikes_brown,
                    seed=None,
                    ):
    if seed is not None:
        np.random.seed(seed)
    if depth:
        zorder += 1
        # Calculatre end position of segment
        x2 = x1 + np.cos(np.radians(angle)) * length
        y2 = y1 - np.sin(np.radians(angle)) * length
        
        # Set the width
        if width is None:
            width = length * length_width

        # Draw baseline rectanglular segment
        if draw_rect:
            dcol = col
            if darken is not None:
                dcol = colours.darken(col, darken)
            rect = Rectangle((x1-(width/2), y1), width, length, color=dcol, zorder=zorder)
            t = mpl.transforms.Affine2D().rotate_deg_around(x1,y1,-angle-90) + plt.gca().transData
            rect.set_transform(t)
            plt.gca().add_patch(rect)
        
        #density = 2 + (2 * (1-(depth / max_depth)))
        #max_angle = 40 * (1-(depth / max_depth))
        #TODO: Add depth-varying density and angles
        if draw_texture[0]:
            spikes0 = draw_spikes(x1, y1+(length*0.25), width, length*0.75, spike_zorder=zorder, darken=darken, **spike_back_params)
            t0 = mpl.transforms.Affine2D().rotate_deg_around(x1,y1,-angle-90) + plt.gca().transData
            spikes0.set_transform(t0)
            plt.gca().add_collection(spikes0)
            
        # Randomise the angle & length changes
        rnd1 = np.random.random(4) - 0.5
        l1 = length_change + (rnd1[0] * length_change * length_vary_prop)
        l2 = length_change + (rnd1[1] * length_change * length_vary_prop)
        a1 = angle_change  + (rnd1[2] * angle_change  * angle_vary_prop)
        a2 = angle_change  + (rnd1[3] * angle_change  * angle_vary_prop)
        
        # Reduce split probability
        split_prob  = split_prob * split_prob_change
        
        # Add large angle split
        rnd2 = np.random.random(4)
        if rnd2[0] < large_angle_prob: a1 = large_angle * rnd2[1]/np.abs(rnd2[1]) 
        if rnd2[2] < large_angle_prob: a2 = large_angle * rnd2[3]/np.abs(rnd2[3])

        # Draw two more branches
        rnd3 = np.random.random(2)
        if rnd3[0] < split_prob: draw_joshua_tree(
            x1=x2,
            y1=y2,
            angle=angle-a1,
            length=length*l1,
            width=width*width_change,
            depth=depth-1,
            # Everything else as is
            length_change=length_change,
            length_vary_prop=length_vary_prop,
            length_width=length_width,
            width_change=width_change,
            angle_change=angle_change,
            angle_vary_prop=angle_vary_prop,
            large_angle_prob=large_angle_prob,
            large_angle=large_angle, 
            split_prob=split_prob,
            split_prob_change=split_prob_change,
            max_depth=max_depth,
            col=col,
            draw_rect=draw_rect,
            draw_texture=draw_texture,
            zorder=zorder,
            spike_forward_params=spike_forward_params,
            spike_mid_params=spike_mid_params,
            spike_back_params=spike_back_params,
            darken=darken,
            # Seed should not be used again
            seed=None
            )
        if rnd3[1] < split_prob: draw_joshua_tree(
            x1=x2,
            y1=y2,
            angle=angle+a2,
            length=length*l2,
            width=width*width_change,
            depth=depth-1,
            # Everything else as is
            length_change=length_change,
            length_vary_prop=length_vary_prop,
            length_width=length_width,
            width_change=width_change,
            angle_change=angle_change,
            angle_vary_prop=angle_vary_prop,
            large_angle_prob=large_angle_prob,
            large_angle=large_angle, 
            split_prob=split_prob,
            split_prob_change=split_prob_change,
            max_depth=max_depth,
            col=col,
            draw_rect=draw_rect,
            draw_texture=draw_texture,
            zorder=zorder,
            spike_forward_params=spike_forward_params,
            spike_mid_params=spike_mid_params,
            spike_back_params=spike_back_params,
            darken=darken,
            # Seed should not be used again
            seed=None
            )

        # Draw leaves at terminal branches
        if (rnd3[0] > split_prob and rnd3[1] > split_prob) or depth==1:
            # At a terminal branch, draw the leaves
            # This is set at the same angle as the preceding branch (to avoid spikes at weird angles)
            # Green
            # TODO: think about adding back in max(length,init_length/4) so the green spikes don't get tiny at higher depths
            if draw_texture[1]:
                spikes1 = draw_spikes(x2, y2, width, length, spike_zorder=zorder, darken=darken, **spike_forward_params)
                t1 = mpl.transforms.Affine2D().rotate_deg_around(x2,y2,-angle-90) + plt.gca().transData
                spikes1.set_transform(t1)
                plt.gca().add_collection(spikes1)
            
            if draw_texture[2]:
                spikes2 = draw_spikes(x2, y2-(length*0.25), width, length*0.25, spike_zorder=zorder, darken=darken, **spike_mid_params)
                t2 = mpl.transforms.Affine2D().rotate_deg_around(x2,y2,-angle-90) + plt.gca().transData
                spikes2.set_transform(t2)
                plt.gca().add_collection(spikes2) 

def draw_spikes(
                x1,
                y1,
                width,
                length,
                spike_direction=1, # 1=forwards; -1=backwards
                spike_colour=colours.cols['green'],
                spike_edge_colour='k',
                spike_edge_width=0.5,
                spike_colour_jitter=0.1,
                spike_width=0.3,
                spike_length=2,
                spike_jitter=0.5,
                spike_layout='regular',
                spike_density_x=3,
                spike_density_y=3,
                spike_density_rnd=10,
                spike_max_angle=40,
                spike_zorder=5,
                darken=None):
    """Draws some spikes (which can be the live green leaves pointing up, or dead brown leaves pointin down which cover the branches)"""
    # Rect mid positions
    rx, ry = x1-(width/2), y1
    
    # Determine the initial base mid-points of all the spikes
    # Random
    if spike_layout == 'random':
        n = int((width*length) / (0.5*spike_width*width*spike_length*width) * spike_density_rnd)
        pos = np.random.random((n,2)) * np.array([width, length]) + np.array([rx,ry])
    # Regular
    elif spike_layout == 'regular':
        nx = int(np.ceil((1 / spike_width) * spike_density_x))
        ny = int(np.ceil((1 / (spike_length*width/length)) * spike_density_y))
        n = nx*ny
        posx, posy = np.meshgrid(np.linspace(rx,rx+width,nx), np.linspace(ry,ry+length,ny))
        pos = np.vstack([posx.reshape(-1), posy.reshape(-1)]).T
        
    # Jitter them for some randomness
    jitter_x1 = 1+((np.random.random(n)-0.5)*spike_jitter)
    jitter_x2 = 1+((np.random.random(n)-0.5)*spike_jitter)

    # Calculate the verticies of the triangles
    v1 = pos - np.array([(jitter_x1*spike_width*width/2),np.zeros(n)]).T
    v2 = pos + np.array([(jitter_x2*spike_width*width/2),np.zeros(n)]).T
    v3 = pos
    
    # Tip of spikes
    edge_distance = (((v1[:,0]+v2[:,0])/2)-x1) / (width/2) # what proportion are they to the edge (with +/- sign)
    angles = spike_direction*spike_max_angle*edge_distance
    v3[:,0] += spike_direction * spike_length*width * np.cos(np.radians(90-angles))
    v3[:,1] += spike_direction * spike_length*width * np.sin(np.radians(90-angles))
    
    # Jitter the tip
    jitter_x3 = ((np.random.random(n)-0.5)*spike_jitter)*spike_width*width
    jitter_y3 = ((np.random.random(n)-0.5)*spike_jitter)*spike_width*width*2 #y should jitter a bit more than x!
    v3[:,0] += jitter_x3
    v3[:,1] += jitter_y3
    
    # Generate the colours and patches
    if darken is not None:
        spike_colour = colours.darken(spike_colour, darken)
    cols = colours.mod_col(spike_colour, spike_colour_jitter, n)
    spikes_list = []
    for i in range(n):
        spikes_list.append(plt.Polygon([v1[i,:],v2[i,:],v3[i,:]]))
    
    # Sort them so they draw in the correct order (from the base upwards)
    sort_idx = np.argsort(v1[:,1])[::-1*spike_direction]
    spikes_list = list(np.array(spikes_list)[sort_idx])
    spikes_collection = PatchCollection(spikes_list,
                                        zorder=spike_zorder,
                                        facecolors=cols,
                                        edgecolor=spike_edge_colour,
                                        lw=spike_edge_width)
    
    # Return
    return spikes_collection

def draw_dead_tree(
                    x1=0,
                    y1=0,
                    depth=8,
                    max_depth=8,
                    length=200,
                    length_change=0.6,
                    length_vary_prop=1.0,
                    width=20,
                    width_change=0.8,
                    angle=-90,
                    angle_change=30,
                    angle_vary_prop=1.0,
                    split_prob=0.9,
                    col='k',
                    seed=None):
    """Draws a simple dead tree at using matplotlib Rectangles
    Default tree begins at (0,0) and has sensible defaults for a (1600 x 900) canvas
    Everything is fully customisable by setting the keyword arguments"""
    if seed is not None:
        np.random.seed(seed)
    if depth:
        # Calculatre end position of segment
        x2 = x1 + np.cos(np.radians(angle)) * length
        y2 = y1 - np.sin(np.radians(angle)) * length
        # Plot & rotate
        rect = Rectangle((x1-(width/2), y1), width, length, color=col, zorder=4) # Don't define rotation angle here, since it rotates by the corner which is not right
        t = mpl.transforms.Affine2D().rotate_deg_around(x1,y1,-angle-90) + plt.gca().transData # This uses the midpoint rather than corner
        rect.set_transform(t)
        plt.gca().add_patch(rect)
        # Randomise the angle & length changes
        rnd1 = np.random.random(4) - 0.5
        l1 = length_change + (rnd1[0] * length_change * length_vary_prop)
        l2 = length_change + (rnd1[1] * length_change * length_vary_prop)
        a1 = angle_change  + (rnd1[2] * angle_change  * angle_vary_prop)
        a2 = angle_change  + (rnd1[3] * angle_change  * angle_vary_prop)
        # Draw two more branches
        rnd2 = np.random.random(2)
        if rnd2[0] < split_prob: draw_dead_tree(
            x1=x2,
            y1=y2,
            depth=depth-1,
            max_depth=max_depth,
            angle=angle-a1,
            length=length*l1,
            width=width*width_change*(depth/max_depth),
            length_change=length_change,
            length_vary_prop=length_vary_prop,
            width_change=width_change,
            angle_change=angle_change,
            angle_vary_prop=angle_vary_prop,
            split_prob=split_prob,
            col=col,
            seed=None)
        if rnd2[1] < split_prob: draw_dead_tree(
            x1=x2,
            y1=y2,
            depth=depth-1,
            max_depth=max_depth,
            angle=angle+a2,
            length=length*l2,
            width=width*width_change*(depth/max_depth),
            length_change=length_change,
            length_vary_prop=length_vary_prop,
            width_change=width_change,
            angle_change=angle_change,
            angle_vary_prop=angle_vary_prop,
            split_prob=split_prob,
            col=col,
            seed=None)
