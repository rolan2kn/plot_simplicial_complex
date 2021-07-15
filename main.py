'''
@author: Rolando Kindelan Nuñez
@mail: rolan2kn@gmail.com
@institution: PhD Candidate in Computer Science at University of Chile

Intention:

This Unit allows to draw a gudhi simplicial complex in a SimplexTree
'''
import numpy as np
import gudhi

from draw_complex import DrawComplex


def randsphere(n, scale):
    np.random.seed(19680801)
    z = 2 * np.random.rand(n) - 1  # uniform on [vmin, vmax]

    theta = 2 * np.pi * np.random.rand(n) - np.pi  # uniform on [-pi, pi]
    x = np.sin(theta) * np.sqrt(1 - z ** 2)  # based on angle
    y = np.cos(theta) * np.sqrt(1 - z ** 2)

    X = []
    for i in range(n):
        X.extend([[(x[i]) * scale, (y[i]) * scale, (z[i]) * scale]])

    return X


def make_intersected(no_objects, sizes, scale):
    X = []

    for d in range(0, no_objects):
        X.extend(randsphere(sizes[d], scale[d]))

    return X


def data_generation():
    n_objs = 2
    size = [200, 100]
    scale = [1, 0.5]

    return make_intersected(n_objs, size, scale)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    point_clouds = data_generation()
    if len(point_clouds) == 0:
        raise Exception("Bad dataset")

    simplicial_complex_dimension = 4
    complex = gudhi.RipsComplex(points=point_clouds)
    max_dim = len(point_clouds[0])
    factor = max(simplicial_complex_dimension, max_dim)

    simplex_tree = complex.create_simplex_tree(max_dimension=1.0)
    simplex_tree.collapse_edges(np.ceil(factor))                # this reduces the simplicial complex size but maintaining the same homology groups
    simplex_tree.expansion(simplicial_complex_dimension)

    draw_sc = DrawComplex(simplicial_complex=simplex_tree, point_cloud=point_clouds, max_epsilon=0.5)
    draw_sc.execute()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
