# Fractal Joshua Tree scene generator

| <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/title.png" height=400px> |
|---|

This repo contains code to produce (somewhat) realistic looking Joshua Trees in surreal landscapes, in Python & matplotlib. It uses a classic recursive fractal tree generation algorithm (with a few modifications: namely a depth-dependent reduction in split probabilities and random extreme angle anomalies) along with a pre-set suite of parameters & texture drawing routines, which together simulate the crazy Joshua Tree morphology.

In general, almost all of the functions (including landscape generation) are designed to give sensible, randomised defaults - meaning you only have to send the bare minimum amount of arguments. Random seeds are used throughout for reproducability.

## Repo layout

* [`tree.py`](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/tree.py) - main tree drawing functions
* [`landscape.py`](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/landscape.py) - sky, stars & terrain routines
* [`colours.py`](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/colours.py) - some default colours & colourmaps
* [`config.py`](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/config.py) - all the tree-specific parameters
* [`examples.py`](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples.py) - script to reproduce the output found in [`examples/`](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples)
* `ipynb/` - folder containing IPython Notebooks used in development of the code (COMING SOON!)
* `blog/` - series of articles describing the process of developing the code (COMING SOON!)

## Sample usage

The highest-level function will draw a fully randomised Joshua Tree (of course remove the `seed` argument, so that you generate a new one):

```python
import matplotlib.pyplot as plt
import tree

plt.figure()
tree.draw_random_joshua_tree(seed=27182)
plt.axis('equal')
plt.axis('off')
plt.show()
```

<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/example2.png" height=400px>

What this is really doing is calling a lower-level function which randomly samples Joshua Tree styles from six different configurations. Broadly speaking, there are two main styles of tress which are modelled: `Type I` (thicker, broader) and `Type II` (taller, skinnner, less branching):

```python
import config

tree.draw_joshua_tree(seed=1, **config.tree_type_i)
tree.draw_joshua_tree(seed=0, **config.tree_type_ii)
```

<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/example1.png" height=400px>

Each of these types is mutated twice to produce new varients: firstly by reducing the probability of a split branch the higher up the tree you go (designated `Type Ia`/`Type IIa` and characterised by longer single branches & assymetry); and secondly by randomly allowing extreme angle changes (designated `Type Ib`/`Type IIb` and characterised by weird, often downward facing limbs):

<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/example9.png" height=400px>

## Scenes

There are a number of simple functions to produce interesting looking scenes. A scene in this context it typically made up of at least a gradient sky background (`landscape.draw_sky`), and random terrain (`landscape.draw_terrain`) - though may optionally include some stars (`landscape.draw_stars`) and simulated Sun/Moon brightening (`landscape.draw_sun`). Most of these functions require arguments representing the width and height of the canvas (`w` and `h` respectively). For full details, see the examples ([script](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/example.py) and [gallery](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples)) and parameter documentation below.

<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/example5.png" height=400px>

We can even use a more simple variant - `tree.draw_dead_tree()` - to produce scenes with "dead tree" like qualities.

<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/example7.png" height=400px>

<details><summary>[CLICK TO EXPAND] Check out all the interesting backgrounds to choose from - have fun exploring!</summary>
<p>
<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/example8.png" height=600px>
</p>
</details>

## Parameters & detailed explanation

<details><summary>[EXPAND] Trees; Joshua Tree with random style</summary>
<p>

The function `tree.draw_random_joshua_tree()` is really designed to be used with as few parameters as possible. On it's own, you don't need to pass anything. In a scene, at a minimum you'll probably just need to call:

```python
tree.draw_random_joshua_tree(x, y, length)
```
and it will build a random tree of random type, where the six types are selected at fixed probabilities, found in [`config.py`](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/config.py). Other useful paramters would be `darken` (if you want to make them more silhouette-like) and `seed` (if you want it to be reproducible).

|Argument|Type|Default|Description|
|---|---|---|---|
|`x1`|float|`0`|x coordinate of the base of the tree|
|`y1`|float|`0`|y coordinate of the base of the tree|
|`length`|float|`10`|Length of the first tree segment|
|`col`|list of floats|`colours.cols['brown']`|RGB colour of tree (only used if `draw_rect` is `True`)|
|`draw_rect`|bool|`False`|Whether to draw the rectangular branch segments (behind the textures)|
|`draw_texture`|list of bools|`[True,True,True]`|Whether to draw the main tree spikes, green leaf spikes, and yellow dying spikes respectively|
|`darken`|float|`None`|Amount by which to darken each R,G,B element of the tree's colours. Defined as the fraction of the way between the current value, and `0.0`|
|`zorder`|int|`4`|Initial `zorder` of the first tree segment|
|`spike_forward_params`|dict|`config.spikes_green`|Configuration of forward-facing (green) leaf spikes|
|`spike_mid_params`|dict|`config.spikes_yellow`|Configuration of dying (yellow) leaf spikes|
|`spike_back_params`|dict|`config.spikes_brown`|Configuration of dead (brown) trunk spikes|
|`seed`|int|`None`|Initial seed which is passed to `np.random.seed`| for reproducability|

</p>
</details>

<details><summary>[EXPAND] Trees; Joshua Tree with arbitrary style</summary>
<p>
  
If you want to have a little bit more flexibility, use the fucnction `tree.draw_joshua_tree()`. Again, while no arguments are _required_ it is expectesd you'd pass `x`, `y` and `length`. Be default, all arguments are set to those which correspond to a `Type I` tree, but in this function every parameter can be set independently. If you want to draw a random tree of a fixed style, it is possible to pass the pre-defined configurations (e.g., pass `**config.tree_type_iia`), but it is important to know which more general parameters are _not_ included in those configurations, hence they are listed in the table below.

|Argument|Type|Default|Description|
|---|---|---|---|
|`x1`|float|`0`|x coordinate of the base of the tree|
|`y1`|float|`0`|y coordinate of the base of the tree|
|`length`|float|`10`|Length of the first tree segment|
|`length_change`|float|`0.8`|Average fraction by which to (typically) reduce the branch lengh each iteration|
|`length_vary_prop`|float|`0.2`|Proportion of `length_change` by which to randomise the length reduction|
|`length_width`|float|`0.2`|The initial width, expressed as a fraction of the initial length|
|`width`|float|`None`|The inital width (if `None` will resort to using `length_width` to calculate width)|
|`width_change`|float|`0.9`|Fraction by which to reduce the branch width each iteration|
|`angle`|float|`-90`|Initial angle of tree: `-90` is straight up, it can be interesting to randomise this to produce more slanted trees|
|`angle_change`|float|`30`|Average amount by which to change the angle at each split|
|`angle_vary_prop`|float|`0.4`|Proportion of `angle_change` by which to randomise the angle change|
|`large_angle_prob`|float|`0.0`|Probability of there being an extreme, AKA `large_angle` split|
|`large_angle`|float|`60`|What the large angle is|
|`split_prob`|float|`0.9`|Probability each iteration of having a split to one side|
|`split_prob_change`|float|`1.0`|Fraction by which `split_prob` changes each iteration - values less than one result in longer single branches, and often more lopsided trees|
|`depth`|int|`6`|How many times to iterate - this automatically reduces each recursive call|
|`max_depth`|int|`6`|How many times to iterate - this should be the same as `depth` initially and never changes - used to scale some things|
|`col`|list of floats|`colours.cols['brown']`|RGB colour of tree (only used if `draw_rect` is `True`)|
|`draw_rect`|bool|`False`|Whether to draw the rectangular branch segments (behind the textures)|
|`draw_texture`|list of bools|`[True,True,True]`|Whether to draw the main tree spikes, green leaf spikes, and yellow dying spikes respectively|
|`darken`|float|`None`|Amount by which to darken each R,G,B element of the tree's colours. Defined as the fraction of the way between the current value, and `0.0`|
|`zorder`|int|`4`|Initial `zorder` of the first tree segment|
|`spike_forward_params`|dict|`config.spikes_green`|Configuration of forward-facing (green) leaf spikes|
|`spike_mid_params`|dict|`config.spikes_yellow`|Configuration of dying (yellow) leaf spikes|
|`spike_back_params`|dict|`config.spikes_brown`|Configuration of dead (brown) trunk spikes|
|`seed`|int|`None`|Initial seed which is passed to `np.random.seed`| for reproducability|
                    
</p>
</details>

<details><summary>[EXPAND] Trees; dead tree</summary>
<p>
  
While quite boring on it's own (and _somewhat_ off-topic), I've kept one of the primitive tree generation functions, `tree.draw_dead_tree()` in here. They can look cool against the fiery twilight backdrops. Parameters are a subset of the Joshua Trees described above.

</p>
</details>

<details><summary>[EXPAND] Trees; spikes</summary>
<p>

This is getting into the weeds a bit, and while it is hoped that you won't need to modify or call the `tree.draw_spikes()` function (it is called automatically from within the Joshua Tree routines) here are the details in case you need to modify anything. The fastest way to modify the way the spikey leaves look would be to 1) modify `config.spikes_*` for the parameters; and 2) optionally modify the `draw_texture` parameter in the Joshua Tree functions (to toggle which of the three spike variants are drawn each time).

|Argument|Type|Default|Description|
|---|---|---|---|
|`x1`|float||Initial lower-mid `x`-coordinate of rectangle defining a branch segment|
|`y1`|float||Initial lower-mid `y`-coordinate of rectangle defining a branch segment|
|`width`|float||Width of the rectangle|
|`length`|float||Length of the rectangle|
|`spike_direction`|-1 or 1|`1`|Direction spikes should face: 1=forwards; -1=backwards|
|`spike_colour`|list|`colours.cols['green']`|Face colour of the spikes|
|`spike_edge_colour`||`k`|Edge colour of the spikes (any valid matplotlib colour)|
|`spike_edge_width`||`0.5`|Edge width of the spikes (any valid matplotlib colour)|
|`spike_colour_jitter`|float|`0.1`|How much to jitter the spike's colour|
|`spike_width`|float|`0.3`|Width of the spike (relative to the branch's width)|
|`spike_length`|float|`2`|Length of the spike (relative to the branch's width)|
|`spike_jitter`|float|`0.5`|How much to jitter the spike's positions|
|`spike_layout`|float|`'regular'`|Can be 'regular' or 'random'|
|`spike_density_x`|int|`3`|If the spike layout is `regular`, approx how many spikes should fit across the branch width|
|`spike_density_y`|int|`3`|If the spike layout is `regular`, approx how many spikes should fit across the branch height|
|`spike_density_rnd`|float|`10`|If the spike distribution is `random`, approx how many more spikes should be drawn than the area of the branch|
|`spike_max_angle`|float|`40`|Maximum angle at which the spikes will disperse radially (0 means they are all parallel with the branch direction; 90 means they are perpendicular to the branch|
|`spike_zorder`|float|`5`|Zorder of spikes|
|`darken`|float|`None`|Amount by which to darken each R,G,B element of the spike's colours. Defined as the fraction of the way between the current value, and `0.0`|
                
</p>
</details>

<details><summary>[EXPAND] Landscapes; sky</summary>
<p>

`landscape.draw_sky()` simply displays a matplotlib colormap on a figure. You can pass any of the standard matplotlib maps (e.g., `plt.cm.viridis`, etc) or you can use the presets in the `colours.cmaps` dictionary (see [this example](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/example8.png) for a visual representation of the colour gradients & keys for the dictionary).

|Argument|Type|Default|Description|
|---|---|---|---|
|`w`|float|`1600`|Width of canvas|
|`h`|float|`900`|Height of canvas|
|`cmap`|`matplotlib.colors.ListedColormap`|`None`|The colourmap to use (if `None` (default), one will be selected at random)|

</p>
</details>

<details><summary>[EXPAND] Landscapes; stars</summary>
<p>
  
`landscape.draw_stars()` draws some small dots at random positions throughout the canvas. Rather than selecting sizes (brightness) from a distribution, it calls a sub-function three times, to give three different size layers simulating actual distribution of star brightnesses.

|Argument|Type|Default|Description|
|---|---|---|---|
|`w`|float|`1600`|Width of canvas|
|`h`|float|`900`|Height of canvas|
|`n`|int|`750`|Number of stars|
|`max_size`|int|`5`|Size of the brightest star (pts)|
|`col`|-|`'w'`|Colour of the stars (any valid matplotlib colour)|
|`n_ratios`|list|`[0.005,0.15,0.85]`|Fraction of the `n` stars which will be large, medium and small|
|`s_ratios`|list|`[1.0, 0.2, 0.02]`|Fractio of `max_size` for the large, medium and small stars|

</p>
</details>

<details><summary>[EXPAND] Landscapes; sun</summary>
<p>
  
`landscape.draw_sun()` produces a simulated 'glow' from the Sun or Moon (both could be feasible, depending on which background is chosen) by generating a two-dimensional Gaussian blob, and (optionally) placing it at the height of the effective horizon as caused by some terrain, `t`.

|Argument|Type|Default|Description|
|---|---|---|---|
|`w`|float|`1600`|Width of canvas|
|`h`|float|`900`|Height of canvas|
|`center`|list|`None`|`[x,y]` coordinate of the Sun/Moon (if `None` (default), position will be chosen at random)|
|`size`|float|`None`|Size of the blob in canvas coordinates (if `None` (default), size will be chosen at random)|
|`terrain`|np.array|`None`|Array of shape `(N,2)`, typically returned by the function `landscape.draw_terrain()`. If supplied, a random `x` coordinate will be chosen but the `y` value will be matched to the effective horizon|
|`col`|list|`[1,1,1]`|RGB colour of the blob - note the blog is ultimatly overlaid on a gradient sky using transparency|

</p>
</details>

<details><summary>[EXPAND] Landscapes; terrain</summary>
<p>
  
`landscape.draw_terrain()` draws a simple 2D terrain profile. Typically this should span the entire `x` axis, so the x components of `start` and `end` should be `0` and `w` respectively. Unlike most other functions, this returns the profile, so that it can be fed into other routines (for example, it's useful to know where the terrain is for plotting the Sun or Moon glow; it is also useful to know if you are going to plot a tree - it should always be below the terrain's height!).

|Argument|Type|Default|Description|
|---|---|---|---|
|`start`|list|<required>|Initial `[x,y]` position of the terrain (typically `[0,y1]`)|
|`end`|list|<required>|Final `[x,y]` position of the terrain (typically `[w,y2])`|
|`roughness`|float|<required>|The roughness of the terrain: low values are rougher; higher values are smoother (typically betwen `0-2`)|
|`vertical_displacement`|float|`None`|Amount (in canvas coordinates) to displace each segment|
|`num_of_iterations`|int|`16`|Number of times to displace the terrain - effectively represents the 'granularity' of resultant profile|
|`col`||`'k'`|Colour to fill the terrain (any valid matplotlib colour)|

</p>
</details>

## Acknowledgements

* Most of the beautiful sky gradients are from [uiGradients](https://uigradients.com/)
* Terrain generation algorithm adapted from [Bites of code](https://bitesofcode.wordpress.com/2016/12/23/landscape-generation-using-midpoint-displacement/)
