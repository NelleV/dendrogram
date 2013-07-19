import numpy as np
from scipy.cluster import hierarchy

from matplotlib import pyplot as plt
from matplotlib import collections as mcolls

n_leaves = 50
X = np.random.randn(n_leaves, 3)

children = hierarchy.linkage(X)[:, :2].astype(int)

verts = []
nodes = {}
curs = 0
for i, (x, y) in enumerate(children):
    if x < n_leaves:
        nodes[x] = (curs, 0)
        curs += 1
    if y < n_leaves:
        nodes[y] = (curs, 0)
        curs += 1

    nodes[n_leaves + i] = (float(nodes[x][0] + nodes[y][0]) / 2,
                           max(nodes[x][1], nodes[y][1]) + 1)
    verts += [(nodes[x], (nodes[x][0], nodes[n_leaves + i][1])),
              (nodes[y], (nodes[y][0], nodes[n_leaves + i][1])),
              ((nodes[x][0], nodes[n_leaves + i][1]),
               (nodes[y][0], nodes[n_leaves + i][1]))
              ]

    
n_ = len(children)
def construct(children, i, n_leaves):
    x, y = children[i]
    if x > n_leaves:
        a = construct(children, x - n_leaves, n_leaves)
    else:
        a = x
    if y > n_leaves:
        b = construct(children, y - n_leaves, n_leaves)
    else:
        b = y

    return [a, b]

t = construct(children, -1, n_leaves)

fig, ax = plt.subplots()
line_coll = mcolls.LineCollection(verts, colors='#000000', linewidth=2)
ax.add_collection(line_coll)
ax.autoscale_view()
