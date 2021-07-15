'''
@author: Rolando Kindelan Nuñez
@mail: rolan2kn@gmail.com
@institution: PhD Candidate in Computer Science at University of Chile

Intention:

This class draws a simplicial complex from Gudhi.
We use matplotlib.
This code needs a lot of optimizations, but it works
'''

import itertools

import numpy as np
import matplotlib.pyplot as plt


class DrawComplex:
    '''
    Constructor: it receives a simplicial complex build in Gudhi. Since the simplicial complex is like an indexing
    data structure we actually need the original point set.
    The simplicial complex could be huge, for this reason is prudent to use a maximal epsilon value to draw.
    '''
    def __init__(self, simplicial_complex, point_cloud, max_epsilon=None, filename=None):
        self.simplicial_complex = simplicial_complex
        self.X = np.array(point_cloud)
        self.max_epsilon = max_epsilon
        self.filename = filename

    def execute(self):
        self.draw_simplices()

    def color_by_dimension(self, dim, max_dim):
        colors = ['r', 'c', 'r', 'y', 'g', 'b', 'm']
        c = colors[(dim) % 7]
        if dim > 7:
            c = plt.cm.hsv(np.float(dim) / (max_dim))

        return c

    def draw_point(self, point, max_dim):
        point = self.X[point[0]]

        self.ax.scatter(point[0], point[1], point[2], c=self.color_by_dimension(0, max_dim))

    def draw_line(self, line, max_dim):
        segment = self.X[line]

        self.ax.plot(segment[:, 0], segment[:, 1], segment[:, 2], c=self.color_by_dimension(1, max_dim), linewidth=0.21,
                linestyle='dashed')

    def draw_simplices(self):
        filtration = self.simplicial_complex.get_filtration()
        max_dim = self.simplicial_complex.dimension()

        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        for qsimplex, filt in filtration:
            if self.max_epsilon is not None and filt > self.max_epsilon:
                break

            d = len(qsimplex)-1
            if d == 0:
                self.draw_point(qsimplex, max_dim)
            elif d == 1:
                self.draw_line(qsimplex, max_dim)
            else:
                self.draw_qsimplex(qsimplex, d, max_dim)

        if self.filename is not None:
            plt.savefig(self.filename)
        else:
            plt.show()

    def draw_3d_triangles(self, triangle_points, face_color, alpha):
        self.ax.plot_trisurf(triangle_points[:, :, 0][0], triangle_points[:, :, 1][0], triangle_points[:, :, 2][0],
                        antialiased=True, color=face_color, alpha=alpha, edgecolor='k')

    def draw_qsimplex(self, qsimplex, dim, max_dim):
        face_lists = itertools.combinations(qsimplex, 3)
        face_color = self.color_by_dimension(dim, max_dim)

        triangle_points = []
        alpha = 1 - ((0.75 / max_dim) * dim)

        for qsimplex in face_lists:
            vrtx = self.X[list(qsimplex)]
            triangle_points.append(vrtx)
        self.draw_3d_triangles(np.array(triangle_points), face_color, alpha)

        del face_lists

