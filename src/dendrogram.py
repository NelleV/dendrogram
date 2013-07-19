from matplotlib import collections
from matplotlib import pyplot as plt


def dendrogram(x, linkage=True, *args, **kwargs):
    """
    Plots a dendrogram
    """
    fig, axes = plt.subplots()

    # Now let's try to build the vertexes automatically, by going through the
    # tree
    markers = []
    verts = []

    depth = 0
    if linkage:
        x, _ = _prepare_linkage(x)
    else:
        x, _ = _prepare_list(x)
    height = 0
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

    line_coll = collections.LineCollection(verts, colors='#000000', linewidth=2)
    axes.add_collection(line_coll)
    axes.autoscale_view()
    return axes


class Leaf(object):
    def __init__(self, x, y=0, label=None):
        self.x = float(x)  # FIXME
        self.y = y
        self.label = label


def _prepare_linkage(children, i, n_leaves):
    x, y = children[i]
    if x > n_leaves:
        a, _ = _prepare_linkage(children, x - n_leaves, n_leaves)
    else:
        a = Leaf(x=x, label=str(x))
    if y > n_leaves:
        b, _ = _prepare_linkage(children, y - n_leaves, n_leaves)
    else:
        b = Leaf(y, label=str(y))

    return [a, b], None


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


if __name__ == "__main__":
    ## Examples
    # An idea of what we should have, with manual plotting.
    x = [[[[0, 1], [2, 3]], [[4, 5], [6, 7]]], [8, 9]]
    height = 4
    leaves = 4

    level_1 = [0, 1, 2, 3]
    level_2 = [0.5, 2.5]
    level_3 = [1.5]

    # FIXME should be computed when reading the binary tree
    min_x = -0.5
    max_x = leaves + 0.5
    min_y = -0
    max_y = height + 0.5
