import numpy as np
from scipy.cluster import hierarchy

from matplotlib import pyplot as plt
from matplotlib import collections as mcolls

n_leaves = 50
X = np.random.randn(n_leaves, 3)

children = hierarchy.linkage(X)[:, :2].astype(int)

n_ = len(children)
t = construct(children, -1, n_leaves)

fig, ax = plt.subplots()
line_coll = mcolls.LineCollection(verts, colors='#000000', linewidth=2)
ax.add_collection(line_coll)
ax.autoscale_view()
