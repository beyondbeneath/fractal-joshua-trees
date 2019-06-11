# Blog

This blog describes how to prcoedurally generate fractal-like Joshua Trees using `matplotlib` - something exceedingly unuseful. It is split into five broad sections:

1. Review of fracal tree generation
2. Parameter exploration & algorithm tweaks
3. Textures
4. Putting it all together
5. Forests & scenes
6. Interactive Javascript version?

## 1. Review of fracal tree generation

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

What we get is a nice symmetric tree [(A)](blog1a.png), with four (`DEPTH`) distinct branch segments. The simplest modification to this basic method is to introduce some randomness to both the angles and lengths (from here on in, we'll also seed each function with a number so the results are directly reproducible). To do this, we simply allow them to both to fluctuate by some proportion of themselves (`LENGTH_VARY_PROP` and `ANGLE_VARY_PROP`).

Immediately we can see this tree [(B)](blog1b.png) is starting to look much more natural. The last major modification we will make is to set the probability of a split (`SPLIT_PROB`). This means we should get less symmetry in terms of the branches. At this stage, we'll also increase the number of iterations (`DEPTH`) since it will make more realistic looking trees.

Things are looking pretty good at this stage: tree [(C)](blog1c.png) has random angle & length variation, as well as some branches "missing" giving a more natural variation. Before we wrap up this review section, it's worth touching briefly on the aesthetics. The trees so far have been drawn with constant width, and by simply reducing this width each iteration [(D)](blog1d.png), it can make much nicer looking trees (for this we use the `linewidth` or `lw` argument in `plt.plot` - this isn't too versatile since it is specified in units of "points", but it will be changed anyway in Section 2).

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

## 2. Parameter exploration & algorithm tweaks

Before playing with any more code, we really need to inspect some real Joshua Trees and try and describe how they behave, in terms of the parameters of the model we have built up so far. Likely we will end up with a number of different sets of parameters, that best describe different styles of trees.  The general approach will be, for a number of classic Joshua Tree photographs:

1. Describe it qualitatively in terms of our model parameters
2. Take a guess at which constants might work
3. Generate a lot of examples to see how it works
4. Rinse and repeat (this step, essentially trial & error, won't be shown)

Here are a bunch of different trees:

<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog2a.png" width=75% height=75%>

<details><summary>[EXPAND] Sources of photographs</summary>
<p>

1. https://www.axios.com/government-shutdown-national-parks-joshua-trees-98350e1b-496b-4508-a0d5-45bd4074e42b.html
2. https://www.smithsonianmag.com/smart-news/californias-joshua-trees-are-under-threat-180959991/
3. https://gearpatrol.com/2015/06/30/joshua-tree-travel-guide/
4. https://gearpatrol.com/2015/06/30/joshua-tree-travel-guide/
5. https://www.washingtonpost.com/nation/2019/01/11/travesty-this-nation-people-are-destroying-joshua-trees-joshua-tree-national-park
6. https://backroadplanet.com/best-hikes-joshua-tree-day-trip/
7. https://www.palmspringslife.com/rock-around-the-clock/
8. http://www.ghumr.com/joshua-tree-national-park-flintstone-land/
9. http://www.ghumr.com/joshua-tree-national-park-flintstone-land/
10. https://www.nationalgeographic.com/travel/national-parks/joshua-tree-national-park/
11. https://en.wikipedia.org/wiki/Yucca_brevifolia#/media/File:JoshuaTreesMexico.jpg
12. https://www.tripsavvy.com/joshua-tree-national-park-4116596
13. https://www.tripsavvy.com/joshua-tree-national-park-4116596
14. http://cannundrum.blogspot.com/2010/07/joshua-tree.html
  
</p>
</details>

Observations:
* In general, the trunk size remains relativelty constant from the base all the way to the terminal branches (high `WIDTH_CHANGE`)
* Larger trees (#1,#2) can be fairly symmetrical (high `LENGTH_CHANGE`)
* Some trees can be slanted (#5,#7,#10)
* All but the largest trees have tall initial segments
* Tall, "simple" trees (#3,#6,#8) have low depth (~3?), long base trunks (large `INITIAL_LENGTH`), and rapidly shrink (large `LENGTH_CHANGE`)
* It's not uncommon to have huge angle variations on some branches (sometimes 90 degrees)
* There are often long single, yet curvy, branches (this indicates that `SPLIT_PROB` should decrease with depth, not currently implemented)

From [this description](http://www.flowersociety.org/JT_Botanical.htm):

> Unlike a typical tree branch, this new stem grows rigidly in a totally different direction, at an angle, horizontally, or even down towards the ground. Each branching stem also abruptly ends its growth after blossoming, and further branches veer off in new directions. As well as ending in blossoming, branching may occur where a stem has been damaged by insects.
> 
> After many years, some Joshua trees develop a complex system of twisted branches growing in many directions. Others develop a more harmonious tree shape, while still others remain mostly vertical. The amazing variety of shapes and growth patterns imparts an unusual individuality to each tree.

These images show some trials to mimic the two broad styles of trees: firstly the larger broader trees (e.g., #1, #2); and secondly the taller trees (e.g., #3, #6, #8) with less angle variation:

|Example `Type I`|Example `Type II`|
|---|---|
| <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog2b.png"> | <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog2c.png"> |

These two simple parameter combinations (designated now as `Type I` and `Type II` trees respectively) allow a decent first pass at generating two drastically different stlyed trees. Amazingly, even just be keeping the trunks the same width it makes a huge different in terms of their similarity to actual trees. This is a list of the parameters used demonstrating the key differences which produce the features:

|Parameter|`Type I`|`Type II`|
|---|---|---|
|`LENGTH_CHANGE`|0.8|0.5|
|`ANGLE_CHANGE`|30|20|
|`ANGLE_VARY_PROP`|0.4|1.0|
|`LENGHT_WIDTH_RATIO`|0.2|0.1|
|`SPLIT_PROB`|0.90|0.95|
|`DEPTH`|6|4|

Now we can think about adding some more functionality to the system. First, let's allow the split probability (`SPLIT_PROB`) to decrease by a factor of `SPLIT_PROB_CHANGE` with each iteration, which should have the effect of producing long, curvy branches, which can be demonstrated by looking at the `Type I` examples shown earlier with the added functionality - the same seeds are used to show how the trees evolve differently:

|`Type I` with fixed split probability|`Type I` with decreasing split probability|
|---|---|
| <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog2b.png"> | <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog2d.png"> |

These variants (with decreasing split probabilities, `SPLIT_PROB_CHANGE`) will be designated `Type Ia` and `Type IIa`. Note we can have the previous `Type I` trees (at a value of `1.0`) or increasingly weirder versions of these trees (at lower values of `0.9`). For these trees anything lower than `0.9` and the split probality decreases too rapidly resulting in the trees being too bare. It is also noted `Type II` trees need to be compensated with larger `DEPTH` in order to allow curvature to form & add a nice amount of weirdness.

The next thing to add is the extreme angle changes. A simple way of doing this is just to enforce a large angle change (`LARGE_ANGLE`) at some set probability (`LARGE_ANGLE_PROB`):

|`Type Ia`| `Type Ia` with probabilistic large angles|
|---|---|
| <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog2e.png"> | <img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog2f.png"> |

These variants (with decreasing split probabilities AND random large angles) will be designated `Type Ib` and `Type IIb`.

While not perfect, this probably gives us enough to work with for now - later tweaks can be made if necessary. The next steps are to add the textures & colours.

## 3. Textures

## 3 - Textures

Our simple black silhouette-like branch segments are not yet resembling Joshua Trees because they are lacking two distinct characteristics: the leaves and the shaggy bark which covers parts of the trunk. Actually, upon reading it appears the spiky bark are actually older leaves which change from upright green spikes, to downward facing brown-grey spikes which protect the trunk:

> The younger ones remain green, but as they age the leaves fade to gray and become a fibrous residue which droops and finally covers the branch or trunk in a protective coating.

So to make them look better, we will simulate these two effects.

### Trunk spikes

The trunk spikes can be simulated by a host of downard-facing near-isoscelese triangles. By observing the samples above, we can see a few important parameters we might wish to include: firstly, the density of the spikes decreases as you move up toward the tree (and often, they only begin appearing after the first split); 2) as you get closer and closer to the green leaves, they start to point radially out (rather than directly 'down' along the axis of the trunk). So both the density and radial pointing are proportional to how close to the terminal branch they are.

Considering a simple experiment, we can (1) produce a branch segment; (2) randomly choose positions from which a spike will originate; (3) draw a downward-facing triangle; (4) radially point them out, proportional to their distance from the center; (5) order the spikes so produce a more physically realistic pattern; (6) assign a base colour and small per-spike colour variation to them all. This simple workflow produces pretty reasonably looking tree branch segments:

<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog3a.png">

Unfortunately this didn't look right for the green leafy spikes - it just looked too disorganised, this is the third image (3) below. So a few more iterations were made: (4) create a regular grid of spikes - this is starting to look better; (5) naively displace the pointy ends down a bit (to retain their "length" as they point outward); (6) use trig to create a more realistic pointing function:

<img src="https://github.com/beyondbeneath/fractal-joshua-trees/blob/master/blog/blog3b.png">

The final result is pretty close to reality, and it makes sense. If you consider the 3D structure of what is happening, the spikes are roughly the same size and all point outward at a fixed angle. The reason we observe an increase in radial pointing as you move away from the branch center is just a 2D projection effect: the spikes in the middle are still facing out; they are just directly in our line of sight so we can't see it.

Having a decent physicaly model and colour routine means we can combine branch segments (brown), leaf segments (green), and the dying leaves (yellow) all together with a parameterised function.

And drawing this on top of our trees from earlier gives remarkably good results. One key consideration made was that the green spikes cannot simply be draw on the last segment, since that creates weird angle changes which aren't physically realistic. In practice what happens is the green spikes point out at the same angle as the previous branch, so this was accommodated for.
