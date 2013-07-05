from matplotlib import pyplot as plt
from matplotlib import collections


def dendrogram(axes, x, *args, **kwargs):
    """
    Plots a dendrogram
    """


# An idea of what we should have, with manual plotting.
x = [[[0, 1], [2, 3]], [[4, 5], [6, 7]]]
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


def compute_(x, depth, height, verts, markers):
    print "compute", x, height, depth, verts
    for el, level in enumerate(x):
        if type(level) == list:
            try:
                i, j = level
                if type(i) != list and type(j) != list:
                    markers += [(i, height - depth - 1),
                                (j, depth - height - 1)]
                    markers += [(i, height - depth),
                                (j, height - depth - 1)]
                    verts += [((i, height - depth), (i, height - depth - 1)),
                              ((j, height - depth), (j, height - depth - 1)),
                              ((i, height - depth),
                               (j, height - depth))]
                    x[el] = float(i + j) / 2
                else:
                    x[el] = compute_(level, depth + 1, height, verts, markers)

            except ValueError:
                print "Not a binary tree"
                raise ValueError
        else:
            markers += [(level, depth)]
            markers += [(level, height - depth)]

    return x


depth = 0
while type(x) == list:
    compute_(x, depth + 1, height, verts, markers)
    try:
        i, j = x
        if type(i) != list and type(j) != list:
            markers += [(i, height - 1),
                        (j, height - 1)]
            verts += [((i, height - 1), (i, height)),
                      ((j, height - 1), (j, height)),
                      ((i, height),
                       (j, height))]
            x = float(i + j) / 2
    except ValueError:
        pass


fig, ax = plt.subplots()
coll = collections.LineCollection(verts, colors='#000000', linewidth=2)
ax.add_collection(coll)
ax.update_datalim(((min_x, min_y), (max_x, max_y)))
ax.autoscale_view()
