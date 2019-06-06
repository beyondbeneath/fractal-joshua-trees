# Fractal Joshua Tree scene generator

| <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/title.png" height=400px> |
|---|

This repo contains code to produce (somewhat) realistic looking Joshua Trees in surreal landscapes, in Python & matplotlib. It uses a classic recursive fractal tree generation algorithm (with a few modifications) along with a pre-set suite of parameters & texture drawing routines, which together simulate the crazy Joshua Tree morphology.

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

The highest-level function will draw a fully randomised Joshua Tree:

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

## Parameters

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
|`darken`|float|`None`|amount by which to darken each R,G,B element of the tree's colours. Defined as the fraction of the way between the current value, and `0.0`|
|`zorder`|int|`4`|Initial `zorder` of the first tree segment|
|`spike_forward_params`|dict|`config.spikes_green`|Configuration of forward-facing (green) leaf spikes|
|`spike_mid_params`|dict|`config.spikes_yellow`|Configuration of dying (yellow) leaf spikes|
|`spike_back_params`|dict|`config.spikes_brown`|Configuration of dead (brown) trunk spikes|
|`seed`|int|`None`|Initial seed which is passed to `np.random.seed`| for reproducability|

</p>
</details>

<details><summary>[EXPAND] Trees; Joshua Tree with arbitrary style</summary>
<p>
  
If you want to have a little bit more flexibility, use the fucnction `tree.draw_joshua_tree()`. Again while no arguments are _required_ it is expectesd you'd pass `x`, `y` and `length`. Be default, all arguments are set to those which correspond to a `Type I` tree, but in this function every parameter can be set independently. If you want to draw a random tree of a fixed style, it is possible to pass the pre-defined configurations (e.g., pass `**config.tree_type_iia`), but it is important to know which more general parameters are _not_ included in those configurations, hence they are listed in the table below.

TODO

</p>
</details>

<details><summary>[EXPAND] Trees; dead tree</summary>
<p>
  
While quite boring on it's own (and _somewhat_ off-topic), I've kept one of the primitive tree generation functions, `tree.draw_dead_tree()` in here. They can look cool against the fiery twilight backdrops.

TODO

</p>
</details>

<details><summary>[EXPAND] Landscapes; sky</summary>
<p>

`landscape.draw_sky()`

TODO

</p>
</details>

<details><summary>[EXPAND] Landscapes; stars</summary>
<p>
  
`landscape.draw_stars()`

TODO

</p>
</details>

<details><summary>[EXPAND] Landscapes; sun</summary>
<p>
  
`landscape.draw_sun()`

TODO

</p>
</details>

<details><summary>[EXPAND] Landscapes; terrain</summary>
<p>
  
`landscape.draw_terrain()`

TODO

</p>
</details>

## Acknowledgements

* Most of the beautiful sky gradients are from [uiGradients](https://uigradients.com/)
* Terrain generation algorithm adapted from [Bites of code](https://bitesofcode.wordpress.com/2016/12/23/landscape-generation-using-midpoint-displacement/)
