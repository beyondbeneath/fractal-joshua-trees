"""
landscape.py
Contains some simple functions, which when combined produce some twilight/night landscape scenes in numpy & matplotlib
    * gradient filled sky (zorder=0)
    * stars (zorder=1)
    * sun/moon brightness effect (zorder=2)
    * random terrain (zorder=3)
"""

# Standard imports
import matplotlib.pyplot as plt
import numpy as np
import bisect

# Self imports
import colours

def draw_sky(width=1600, height=900, cmap=None):
    """Draw a gradient filled sky on the current axis"""
    if cmap is None:
        rnd_key = np.random.choice(list(colours.cmaps.keys()))
        cmap = colours.cmaps[rnd_key]
    plt.xlim(0,width)
    plt.ylim(0,height)
    plt.imshow([[0, 0],[1, 1]], cmap=cmap, interpolation='bicubic', extent=plt.xlim()+plt.ylim(), zorder=0)
    return True

def midpoint_displacement(start, end, roughness, vertical_displacement=None, num_of_iterations=16):
    """
	Iterative midpoint vertical displacement (https://bitesofcode.wordpress.com/2016/12/23/landscape-generation-using-midpoint-displacement/)
	Given a straight line segment specified by a starting point and an endpoint
    in the form of [starting_point_x, starting_point_y] and [endpoint_x, endpoint_y],
    a roughness value > 0, an initial vertical displacement and a number of
    iterations > 0 applies the  midpoint algorithm to the specified segment and
    returns the obtained list of points in the form
    points = [[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
    """
    # Final number of points = (2^iterations)+1
    if vertical_displacement is None:
        # if no initial displacement is specified set displacement to:
        #  (y_start+y_end)/2
        vertical_displacement = (start[1]+end[1])/2
    # Data structure that stores the points is a list of lists where
    # each sublist represents a point and holds its x and y coordinates:
    # points=[[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
    #              |          |              |
    #           point 0    point 1        point n
    # The points list is always kept sorted from smallest to biggest x-value
    points = [start, end]
    iteration = 1
    while iteration <= num_of_iterations:
        # Since the list of points will be dynamically updated with the new computed
        # points after each midpoint displacement it is necessary to create a copy
        # of the state at the beginning of the iteration so we can iterate over
        # the original sequence.
        # Tuple type is used for security reasons since they are immutable in Python.
        points_tup = tuple(points)
        for i in range(len(points_tup)-1):
            # Calculate x and y midpoint coordinates:
            # [(x_i+x_(i+1))/2, (y_i+y_(i+1))/2]
            midpoint = list(map(lambda x: (points_tup[i][x]+points_tup[i+1][x])/2,
                                [0, 1]))
            # Displace midpoint y-coordinate
            midpoint[1] += np.random.choice([-vertical_displacement,vertical_displacement])
            # Insert the displaced midpoint in the current list of points         
            bisect.insort(points, midpoint)
            # bisect allows to insert an element in a list so that its order
            # is preserved.
            # By default the maintained order is from smallest to biggest list first
            # element which is what we want.
        # Reduce displacement range
        vertical_displacement *= 2 ** (-roughness)
        # update number of iterations
        iteration += 1
    return np.array(points)

def draw_uniform_stars(w, h, n=100, max_size=5, col='w'):
    """Draw n stars at random positions, with random sizes on the current axis"""
    stars = np.random.random((n,3)) * np.array([w, h, max_size])
    plt.scatter(stars[:,0], stars[:,1], s=stars[:,2], c=col, zorder=1)
    return stars


def draw_stars(w, h, n=750, max_size=5, col='w', n_ratios=[0.005,0.15,0.85], s_ratios=[1.0, 0.2, 0.02], **kwargs):
    """Draw n stars at random positions, but with size/number ratios to simulate a real star brightness distribution"""
    # Calculate the number of stars in each size group
    n_large = max(1,int(n*n_ratios[0]))
    n_med   = int(n*n_ratios[1])
    n_small = int(n*n_ratios[2])
    # Calculate the size of each star group
    s_large = s_ratios[0]*max_size
    s_med   = s_ratios[1]*max_size
    s_small = s_ratios[2]*max_size
    # Draw them
    draw_uniform_stars(w, h, n=n_large, col=col, max_size=s_large)
    draw_uniform_stars(w, h, n=n_med  , col=col, max_size=s_med)
    draw_uniform_stars(w, h, n=n_small, col=col, max_size=s_small)

def draw_terrain(start, end, roughness, vertical_displacement=None, num_of_iterations=16, col='k'):
    """Draw a randomly generated terrain on the current axis, in a given colour
    Returns a numpy array of the (x,y) points which define the terrain
    """
    layer = midpoint_displacement(start, end, roughness, vertical_displacement, num_of_iterations)
    plt.fill_between(layer[:,0], layer[:,1], y2=0, color=col, zorder=3)
    return layer

def makeGaussian(size, fwhm=3, center=None):
    """ Make a square gaussian kernel (https://stackoverflow.com/questions/7687679/how-to-generate-2d-gaussian-with-python)
    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    """
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)

def draw_sun(w, h, center=None, size=None, terrain=None, col=[1,1,1]):
    """Draw the sun/moon brightness effect on the current axis (essentially this is a white Gaussian blob)
    If terrain provided, position is random (x) and at the height of the terrain (y)
    if center not provided, position is random (x,y)
    If center provided, use it
    """
    # Find crop factor
    crop = int((max(w,h)-min(w,h))/2)
    # Set it at random (x) and near terrain (y)
    if terrain is not None:
        center_x = np.random.random() * w
        idx = np.argmin(np.abs(terrain[:,0]-center_x))
        center_y = terrain[idx,1]
        center = [center_x, center_y]
    # Else set it at random if not provided
    elif center is None:
        center = [np.random.random() * w, np.random.random() * h]
        print(center)
    # Adjust defined center position to allow cropping
    if w > h: center[1] += crop
    elif h > w: center[0] += crop
    # Set size
    if size is None: size = int(w / 5)
    # Make blob
    g = makeGaussian(max(w,h), fwhm=size, center=center)
    # Crop the larger axis
    if w > h: g = g[crop:-crop,:]
    elif h > w: g = g[:,crop:-crop]
    # Assign colour & transparency
    img = np.ones((h, w, 4))
    img[:,:,0:3] = img[:,:,0:3] * np.array(col) #set RGB colour
    img[:,:,3] = g #alpha channel
    # Draw
    plt.imshow(img, zorder=2)