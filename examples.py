"""
examples.py
Produce some example trees & scenes
"""

# Standard imports
import numpy as np
import matplotlib.pyplot as plt

# Self imports
import landscape
import tree
import colours
import config

# Scene size
w, h = 1600, 900

# Example 1 - draw a random tree of a given 'type'
def eg1():
    plt.figure(figsize=(16,9))
    
    plt.subplot(121)
    tree.draw_joshua_tree(seed=1, **config.tree_type_i)
    plt.axis('equal')
    plt.axis('off')
    plt.title("Type I (seed=1)")
    
    plt.subplot(122)
    tree.draw_joshua_tree(seed=0, **config.tree_type_ii)
    plt.axis('equal')
    plt.axis('off')
    plt.title('Type II (seed=0)')
    plt.tight_layout()
    
    plt.savefig('examples/example1.png')

# Example 2 - draw a random tree of a random 'type'
def eg2():
    plt.figure(figsize=(9,9))
    tree.draw_random_joshua_tree(seed=27182)
    plt.axis('equal')
    plt.axis('off')
    plt.title('seed=27182')
    plt.tight_layout()
    plt.savefig('examples/example2.png')

# Example 3 - draw 20 random trees (these won't exactly match the given example image)
def eg3():
    plt.figure(figsize=(16,9))
    
    for i in range(20):
        plt.subplot(4,5,i+1)
        s = int(np.random.random()*10000)
        tree.draw_random_joshua_tree(seed=s)
        plt.axis('equal')
        plt.axis('off')
        plt.title('seed={}'.format(s))
    
    plt.tight_layout()
    plt.savefig('examples/example3.png')

# Example 4 - draw some different variations for each type
def eg4():
    plt.figure(figsize=(24,18))

    for i in range(5):
        plt.subplot(5,6,(i*6)+1)
        tree.draw_joshua_tree(seed=i, **config.tree_type_i)
        plt.axis('equal')
        plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
        if i==0: plt.title("Type I")
        plt.ylabel("Seed {}".format(i))
        
        plt.subplot(5,6,(i*6)+2)
        tree.draw_joshua_tree(seed=i, **config.tree_type_ia)
        plt.axis('equal')
        plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
        if i==0: plt.title("Type Ia")
        
        plt.subplot(5,6,(i*6)+3)
        tree.draw_joshua_tree(seed=i, **config.tree_type_ib)
        plt.axis('equal')
        plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
        if i==0: plt.title("Type Ib")
        
        plt.subplot(5,6,(i*6)+4)
        tree.draw_joshua_tree(seed=i, **config.tree_type_ii)
        plt.axis('equal')
        plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
        if i==0: plt.title("Type II")
        
        plt.subplot(5,6,(i*6)+5)
        tree.draw_joshua_tree(seed=i, **config.tree_type_iia)
        plt.axis('equal')
        plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
        if i==0: plt.title("Type IIa")
        
        plt.subplot(5,6,(i*6)+6)
        tree.draw_joshua_tree(seed=i, **config.tree_type_iib)
        plt.axis('equal')
        plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
        if i==0: plt.title("Type IIb")
        
    plt.tight_layout()
    plt.savefig('examples/example4.png')

# Example 5 - draw a scene with two trees, one of each type
def eg5():
    plt.figure(figsize=(16,9))

    # Setup the scene
    np.random.seed(41)
    landscape.draw_sky(w, h, colours.cmaps['crimson_tide'])
    t = landscape.draw_terrain([0, 150], [w, 170], 1.1, 100, 8, col='0.1')
    landscape.draw_sun(w, h, size=800, terrain=t)

    # Tree1
    tree_x = w*0.4
    tree_y = t[np.argmin(np.abs(t[:,0]-tree_x)),1] - 50
    tree.draw_joshua_tree(tree_x, tree_y, length=200, darken=0.9, **config.tree_type_ia)

    # Tree2
    tree_x = w*0.8
    tree_y = t[np.argmin(np.abs(t[:,0]-tree_x)),1] - 100
    tree.draw_joshua_tree(tree_x, tree_y, length=350, width=30, darken=0.9, **config.tree_type_iib)

    # Finish the plot
    landscape.draw_stars(w, h, n=200)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('examples/example5.png')

# Example 6 - draw a scene with a bunch of 'Type II' trees on the ridge
def eg6():
    plt.figure(figsize=(16,9))

    # Setup the scene
    np.random.seed(10001)
    landscape.draw_sky(w, h, colours.cmaps['shroom_haze'])
    t = landscape.draw_terrain([0, 100], [w, 100], 1.1, 200, 8)
    landscape.draw_sun(w, h, size=800, terrain=t)

    # Draw the tree
    for tree_x in np.linspace(0,w,8)[1:-1]:
        tree_y = t[np.argmin(np.abs(t[:,0]-tree_x)),1]
        init_length = 150 + (np.random.random()*100)
        init_width = init_length / 10
        tree.draw_joshua_tree(tree_x,
                              tree_y-50,
                              length=init_length,
                              width=init_width,
                              darken=0.8,
                              **config.tree_type_iia)

    # Finish the plot
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('examples/example6.png')

# Example 7 - draw a dead tree (not a Joshua Tree!) scene
def eg7():
    plt.figure(figsize=(16,9))

    # Setup the scene
    np.random.seed(2)
    landscape.draw_sky(w, h, colours.cmaps['alto'])
    landscape.draw_stars(w, h, n=500)
    t = landscape.draw_terrain([0, 200], [w, 200], 1.2, 80, 8)
    landscape.draw_sun(w, h, size=600, terrain=t)

    # Calculate the trees (x,y) position
    tree_x = w/2
    tree_y = t[np.argmin(np.abs(t[:,0]-tree_x)),1]

    # Draw the tree
    tree.draw_dead_tree(tree_x, tree_y, seed=6)

    # Finish the plot
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('examples/example7.png')

# Example 8 - show all the available internal colourmaps, along with a random tree
def eg8():
    np.random.seed(314159)
    plt.figure(figsize=(30,30), facecolor='w')
    i = 1

    for k in colours.cmaps:
        plt.subplot(7,4,i)
        landscape.draw_sky(w, h, colours.cmaps[k])
        t = landscape.draw_terrain([0, 200], [w, 200], 1.2, 80, 8)
        tree_x = w*0.4
        tree_y = t[np.argmin(np.abs(t[:,0]-tree_x)),1] - 50
        tree.draw_joshua_tree(tree_x, tree_y, length=150, darken=0.9, **config.tree_type_ia)

        plt.title(k)
        plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
        i += 1
        
    plt.tight_layout()
    plt.savefig('examples/example8.png')

# Example 9 - show differences between Type I, Ia, Ib, II, IIa, IIb
def eg9():
    s1 = 333
    s2 = 5
    plt.figure(figsize=(18,9))

    plt.subplot(2,3,1)
    tree.draw_joshua_tree(seed=s1, **config.tree_type_i)
    plt.axis('equal')
    plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
    plt.ylabel('Type I (seed={})'.format(s1), fontsize=20)
    plt.title('')

    plt.subplot(2,3,2)
    tree.draw_joshua_tree(seed=s1, **config.tree_type_ia)
    plt.axis('equal')
    plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
    plt.title("Type a", fontsize=20)

    plt.subplot(2,3,3)
    tree.draw_joshua_tree(seed=s1, **config.tree_type_ib)
    plt.axis('equal')
    plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
    plt.title("Type b", fontsize=20)

    plt.subplot(2,3,4)
    tree.draw_joshua_tree(seed=s2, **config.tree_type_ii)
    plt.axis('equal')
    plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
    plt.ylabel('Type II (seed={})'.format(s2), fontsize=20)

    plt.subplot(2,3,5)
    tree.draw_joshua_tree(seed=s2, **config.tree_type_iia)
    plt.axis('equal')
    plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)

    plt.subplot(2,3,6)
    tree.draw_joshua_tree(seed=s2, **config.tree_type_iib)
    plt.axis('equal')
    plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
        
    plt.tight_layout()
    plt.savefig('examples/example9.png')

# Main
def main():
  eg1()
  eg2()
  eg3()
  eg4()
  eg5()
  eg6()
  eg7()
  eg8()
  eg9()
  
if __name__== "__main__":
  main()

