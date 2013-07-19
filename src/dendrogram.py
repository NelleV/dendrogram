from matplotlib import collections as mcoll
from matplotlib import pyplot as plt

from matplotlib import cbook


def dendrogram(x, n_leaves=None, linkage=True, *args, **kwargs):
    """
    Plots a dendrogram
    """
    if linkage and n_leaves is None:
        raise ValueError("When providing a linkage matrix, you also need to "
                         "specify the number of leaves.")
    fig, axes = plt.subplots()

    # Now let's try to build the vertexes automatically, by going through the
    # tree
    markers = []
    verts = []

    if linkage:
        x = _prepare_linkage(x, n_leaves)

    x, _ = _prepare_list(x)
    order = _flatten_tree(x)

    height = 0
    depth = 0
    while cbook.iterable(x):
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

    markers = np.array(markers)
    lines_coll = mcoll.LineCollection(
        verts, colors='#000000', linewidth=2)
    axes.add_collection(lines_coll)
    axes.scatter(markers[:, 0],
                 markers[:, 1])
    axes.autoscale_view()
    return axes, order


def _flatten_tree(tree):
    """
    Get the order of the labels of the tree.

    Parameters
    ----------
    tree : tree-like structure
        iterable of iterable. Leaves should be of type Leaf

    Returns
    -------
    order : sequence of integers
        order of the leafs.
    """
    if not cbook.iterable(tree):
        return [tree.label]

    order = []
    for node in tree:
        if type(node) != Leaf:
            order += _flatten_tree(node)
        else:
            order += [node.label]
    return order


class Leaf(object):
    def __init__(self, x, y=0, label=None):
        self.x = float(x)  # FIXME
        self.y = y
        self.label = label


def _prepare_linkage(children, n_leaves, i=-1):
    x, y = children[i]
    if x > n_leaves:
        a = _prepare_linkage(children, n_leaves, x - n_leaves)
    else:
        a = x
    if y > n_leaves:
        b = _prepare_linkage(children, n_leaves, y - n_leaves)
    else:
        b = y

    return [a, b]


def _prepare_list(x, count=0):
    """
    Parcours x, remplace les feuilles par la syntaxe voulue.
    """
    for el, node in enumerate(x):
        if type(node) == list:
            x[el], count = _prepare_list(node, count)
        else:
            x[el] = Leaf(x=count, label=node)
            count += 1

    return x, count


# FIXME prototype is starting to get messy...
def compute_(x, depth, height, verts, markers):
    for el, level in enumerate(x):
        if cbook.iterable(level):
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

    return x


if __name__ == "__main__":
    import numpy as np
    from scipy.cluster import hierarchy

    n_leaves = 50
    X = np.random.randn(n_leaves, 3)

    children = hierarchy.linkage(X)[:, :2].astype(int)
    ax, order = dendrogram(children, n_leaves)
