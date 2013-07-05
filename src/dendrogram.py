from matplotlib import pyplot as plt
from matplotlib import collections


def dendrogram(axes, x, *args, **kwargs):
    """
    Plots a dendrogram
    """


# An idea of what we should have, with manual plotting.
x = [[0, 1], [2, 3]]
height = 2
leaves = 4
fig, ax = plt.subplots()

level_1 = [0, 1, 2, 3]
level_2 = [0.5, 2.5]
level_3 = [1.5]

verts = [[(i, 0), (i, 1)] for i in level_1]
verts += [[[i, 1], [i, 2]] for i in level_2]
verts += [[[i, 2], [i, 3]] for i in level_3]
verts += [((0, 1), (1, 1)), ((2, 1), (3, 1))]
coll = collections.LineCollection(verts, colors='#000000', linewidth=2)
ax.add_collection(coll)
min_x = -0.5
max_x = leaves + 0.5
min_y = -0
max_y = height + 0.5
ax.update_datalim(((min_x, min_y), (max_x, max_y)))
ax.autoscale_view()
