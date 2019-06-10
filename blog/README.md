# Blog

This blog describes how to prcoedurally generate fractal-like Joshua Trees using `matplotlib` - something exceedingly unuseful. It is split into five broad sections:
1. Review of "classic" fractal trees
2. Parameter exploration & algorithm tweaks
3. Textures
4. Putting it all together
5. Forests & scenes

## Review of fracal tree generation

|Basic tree (A)|Length & angle randomness (B)|Split probabilities & increased depth (C)|Aesthetic branch thinning (D)|
|---|---|---|---|
| <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog1a.png"> | <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog1b.png"> | <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog1c.png"> | <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog1d.png"> |

There are plenty of blogs elsewhere on generic fractal tree generation, but we review the basics here for completeness (and so I could better understand the details). A few notable examples are:

1. [The "hello world" example from Rosetta Code](https://rosettacode.org/wiki/Fractal_tree#Python)
2. ["FractalTree2DJS" by hanskellner](https://github.com/hanskellner/FractalTree2DJS)
3. ["TreeGenerator" by someuser-321](https://someuser-321.github.io/TreeGenerator/)
4. [This example by filosophy.org](https://filosophy.org/projects/trees/)

Our most basic example is as follows, adapted from (1). We start with a vertical (represented by the initial angle of -90 degrees) line segment of length `INITIAL_LENGTH`. At the top of this line segment, we branch out two more line segments, with angles rotated by `ANGLE_CHANGE` degrees in either direction, and the length decreased by a factor of `LENGTH_CHANGE`. This process is repeated `DEPTH` times:

```python
def drawTree(x1, y1, angle, length, depth):
    if depth:
        # Calculate end position of segment
        x2 = x1 + (np.cos(np.radians(angle)) * length)
        y2 = y1 - (np.sin(np.radians(angle)) * length)
        # Plot
        plt.plot((x1, x2), (y1, y2), 'k-', lw='5')
        # Draw two more branches
        drawTree(x2, y2, angle-ANGLE_CHANGE, length*LENGTH_CHANGE, depth-1)
        drawTree(x2, y2, angle+ANGLE_CHANGE, length*LENGTH_CHANGE, depth-1)
```

What we get is a nice symmetric tree (A), with four (`DEPTH`) distinct branch segments. The simplest modification to this basic method is to introduce some randomness to both the angles and lengths (from here on in, we'll also seed each function with a number so the results are directly reproducible). To do this, we simply allow them to both to fluctuate by some proportion of themselves (`LENGTH_VARY_PROP` and `ANGLE_VARY_PROP`).

Immediately we can see this tree (B) is starting to look much more natural. The last major modification we will make is to set the probability of a split (`SPLIT_PROB`). This means we should get less symmetry in terms of the branches. At this stage, we'll also increase the number of iterations (`DEPTH`) since it will make more realistic looking trees.

Things are looking pretty good at this stage: tree (C) has random angle & length variation, as well as some branches "missing" giving a more natural variation. Before we wrap up this review section, it's worth touching briefly on the aesthetics. The trees so far have been drawn with constant width, and by simply reducing this width each iteration (D), it can make much nicer looking trees (for this we use the `linewidth` or `lw` argument in `plt.plot` - this isn't too versatile since it is specified in units of "points", but it will be changed anyway in Section 2).

<details><summary>[EXPAND] Code with added features</summary>
<p>
  
```python
def drawTree(x1, y1, angle, length, depth):
    if depth:
        # Calculatre end position of segment
        x2 = x1 + np.cos(np.radians(angle)) * length
        y2 = y1 - np.sin(np.radians(angle)) * length
        # Plot
        w = (depth**2)/8
        plt.plot((x1, x2), (y1, y2), 'k-', lw=w)
        # Randomise the angle & length changes
        rnd1 = np.random.random(4) - 0.5
        l1 = LENGTH_CHANGE + (rnd1[0] * LENGTH_CHANGE * LENGTH_VARY_PROP)
        l2 = LENGTH_CHANGE + (rnd1[1] * LENGTH_CHANGE * LENGTH_VARY_PROP)
        a1 = ANGLE_CHANGE  + (rnd1[2] * ANGLE_CHANGE  * ANGLE_VARY_PROP)
        a2 = ANGLE_CHANGE  + (rnd1[3] * ANGLE_CHANGE  * ANGLE_VARY_PROP)
        # Draw two more branches
        rnd2 = np.random.random(2)
        if rnd2[0] < SPLIT_PROB: drawTree(x2, y2, angle-a1, length*l1, depth-1)
        if rnd2[1] < SPLIT_PROB: drawTree(x2, y2, angle+a2, length*l2, depth-1)
# Seed
seed = 6
np.random.seed(seed)

# Constants
DEPTH = 8
ANGLE_CHANGE = 30
LENGTH_CHANGE = 0.6
INITIAL_LENGTH = 10
LENGTH_VARY_PROP = 1.0
ANGLE_VARY_PROP = 1.0
SPLIT_PROB = 0.9

# Draw a tree
plt.figure(figsize=(6,6))
drawTree(0, 0, -90, INITIAL_LENGTH, DEPTH)
plt.axis('equal')
plt.title('seed {}'.format(seed))
```

</p>
</details>

<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog1e.png">
