from matplotlib import pyplot as plt
from matplotlib import collections


def dendrogram(axes, x, *args, **kwargs):
    """
    Plots a dendrogram
    """

class Leaf(object):
    def __init__(self, x, y=0, label=None):
        self.x = float(x)  # FIXME
        self.y = y
        self.label = label


def prepare_(x, count=0):
    """
    Parcours x, remplace les feuilles par la syntaxe voulue.
    """
    for el, node in enumerate(x):
        if type(node) == list:
            x[el], count = prepare_(node, count)
        else:
            x[el] = Leaf(x=count, label=node)
            count += 1

    return x, count


# FIXME prototype is starting to get messy...
def compute_(x, depth, height, verts, markers):
    for el, level in enumerate(x):
        if type(level) == list:
            try:
                i, j = level
                if type(i) == Leaf and type(j) == Leaf:
                    verts += [((i.x, i.y), (i.x, max(i.y, j.y) + 1)),
                              ((j.x, j.y), (j.x, max(j.y, i.y) + 1)),
                              ((i.x, max(i.y, j.y) + 1),
                               (j.x, max(i.y, j.y) + 1))]
                    x[el] = Leaf(float(i.x + j.x) / 2., y=max(j.y, i.y) + 1)
                    markers += [(float(i.x + j.x) / 2., max(j.y, i.y) + 1)]
                    markers += [(i.x, i.y), (j.x, j.y)]
                else:
                    x[el] = compute_(level, depth + 1, height, verts, markers)

            except ValueError:
                print "Not a binary tree"
                raise ValueError
        else:
            markers += [(level.x, level.y)]
            markers += [(level, height - depth)]

    return x


# An idea of what we should have, with manual plotting.
x = [[[[0, 1], [2, 3]], [[4, 5], [6, 7]]], [8, 9]]
height = 2
leaves = 4

level_1 = [0, 1, 2, 3]
level_2 = [0.5, 2.5]
level_3 = [1.5]

verts = [[(i, 0), (i, 1)] for i in level_1]
verts += [[[i, 1], [i, 2]] for i in level_2]
verts += [[[i, 2], [i, 3]] for i in level_3]
verts += [((0, 1), (1, 1)), ((2, 1), (3, 1))]
min_x = -0.5
max_x = leaves + 0.5
min_y = -0
max_y = height + 0.5

fig, ax = plt.subplots()
coll = collections.LineCollection(verts, colors='#000000', linewidth=2)
ax.add_collection(coll)
ax.update_datalim(((min_x, min_y), (max_x, max_y)))
ax.autoscale_view()


# Now let's try to build the vertexes automatically, by going through the tree
markers = []
verts = []
depth = 0
labels = []




depth = 0
x, _ = prepare_(x)
while type(x) == list:
    compute_(x, depth + 1, height, verts, markers)
    try:
        i, j = x
        if type(i) == Leaf and type(j) == Leaf:
            verts += [((i.x, i.y), (i.x, max(i.y, j.y) + 1)),
                      ((j.x, j.y), (j.x, max(j.y, i.y) + 1)),
                      ((i.x, max(j.y, i.y) + 1),
                       (j.x, max(j.y, i.y) + 1))]
            x = float(i.x + j.x) / 2
    except ValueError:
        pass

# FIXME will not work with polar plots.
fig, ax = plt.subplots()
line_coll = collections.LineCollection(verts, colors='#000000', linewidth=2)
ax.add_collection(line_coll)
ax.update_datalim(((min_x, min_y), (max_x, max_y)))
ax.autoscale_view()
