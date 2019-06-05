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

There are a number of simple functions to produce interesting looking scenes. A scene in this context it typically made up of at least a gradient sky background (`landscape.draw_sky`), and random terrain (`landscape.draw_terrain`) - though may optionally include some stars (`landscape.draw_stars`) and simulated Sun/Moon brightening (`landscape.draw_sun`). Most of these functions require arguments representing the width and height of the canvas (`w` and `h` respectively). For full details, see the examples ([script](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/example.py) and [gallery](https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples)) and parameter documentation.

<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/example5.png" height=400px>
<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/example7.png" height=400px>

There are a range of interesting backgrounds to choose from, have fun exploring!

<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/examples/example8.png" height=600px>

## Acknowledgements

* Most of the beautiful sky gradients are from [uiGradients](https://uigradients.com/)
* Terrain generation algorithm adapted from [Bites of code](https://bitesofcode.wordpress.com/2016/12/23/landscape-generation-using-midpoint-displacement/)
