from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
from math import *
import matplotlib as mpl
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# вершины
v = np.array([  
            [0, 0, 0],
            [0, 1, 0], 
            [1, 1, 0], 
            [1, 0, 0],  
            [0.5, 0.5, sqrt(2)/2],   
            [0.5, 0.5, -sqrt(2)/2]  
            ])

ax.scatter3D(v[:, 0], v[:, 1], v[:, 2],visible=False)

# создание треугольников между вершинами
verts = [ 
        [v[0],v[1],v[4]], 
        [v[0],v[3],v[4]],
        [v[2],v[1],v[4]], 
        [v[2],v[3],v[4]], 
        [v[0],v[1],v[5]], 
        [v[0],v[3],v[5]],
        [v[2],v[1],v[5]], 
        [v[2],v[3],v[5]], 
        ]



# plot sides
ax.add_collection3d(Poly3DCollection(verts, facecolors='blue',
 linewidths=1, edgecolors='black', alpha=1))
ax.axes.set_xlim(-0.5,1.5)
ax.axes.set_ylim(-0.5,1.5)
plt.show()