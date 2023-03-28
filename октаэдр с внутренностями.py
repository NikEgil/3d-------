from matplotlib import pyplot as plt
import numpy as np
from math import *
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


fig = plt.figure()


x=np.zeros(1)
y=np.zeros(1)
r=1             #радиус гексагона
n=10           #количество точек на стороне
h=r*sqrt(3)/2   #высота гексогона
d=4             #длинна сетки
s=6            #расстояние по x



def hexagon(x,y):
    #создание верхней полосы
    for i in range(n):
        x=np.append(x, -r/2+r*i/n)
        y=np.append(y, h)
    #поворот полосы 
    for i in range(5*n):
        l=len(x)-n
        x=np.append(x, x[l]*cos(-pi/3)-y[l]*sin(-pi/3))
        y=np.append(y, x[l]*sin(-pi/3)+y[l]*cos(-pi/3))
    
    return x,y

def mesh(x,y,d):
    #создание высоких колонн
    for a in range(1,d,2):
        for b in range(-1,d+2,2):
            for op in range(n*6):
                x=np.append(x, a*1.5*r+x[n*6-op])
                y=np.append(y, b*h+y[n*6-op])
    #создание низких колонн
    for a in range(-1,d,2):
        for b in range(-1,d+2,2):
            for op in range(n*6):
                x=np.append(x, a*1.5*r+x[n*6-op]+1.5*r)
                y=np.append(y, b*h+y[n*6-op]+h)
    return x,y

def delpoint(x,y):
    x = np.delete(x, 0, axis=0)
    y = np.delete(y, 0, axis=0)
    x=np.round(x,3)
    y=np.round(y,3)
    print(len(x),len(y))
    i=0
    while(i<len(x)):
        k=1
        while(i+k<len(x)):
            if x[i]==x[i+k] and y[i]==y[i+k]:
                x = np.delete(x, i+k, axis=0)
                y = np.delete(y, i+k, axis=0)
                
            k+=1
        i+=1
    print(len(x),len(y))
    return x,y

x,y=hexagon(x,y)
x,y=mesh(x,y,d)
x,y=delpoint(x,y)

x1=np.arange(0,s+0.1,0.1)
y1=0*x1
x2=np.arange(0,s/2+0.1,0.1)
y2=sqrt(3)*x2
x3=np.arange(s/2,s+0.1,0.1)
y3=-sqrt(3)*x3+s*sqrt(3)


#расстояние по плоского графика
ax = fig.add_subplot()
ax.set_aspect(1)
ax.scatter(x,y)
ax.plot(x1,y1, color='red')
ax.plot(x2,y2, color='red')
ax.plot(x3,y3, color='red')


fig = plt.figure()



def mat_x(a):
    return [ 
        [1,0,0],
        [0,cos(a*pi/180),-sin(a*pi/180)],
        [0,sin(a*pi/180),cos(a*pi/180)]
        ]
def mat_y(a):
    return [ 
        [cos(a*pi/180),0,sin(a*pi/180)],
        [0,1,0],
        [-sin(a*pi/180),0,cos(a*pi/180)]
        ]
def mat_z(a):
    return [ 
        [cos(a*pi/180),-sin(a*pi/180),0],
        [sin(a*pi/180),cos(a*pi/180),0],
        [0,0,1]
        ]

def pov_x(rt,degrees):
    rn=np.zeros((len(rt),3))
    for i in range(len(rt)):
        rn[i]=np.dot(mat_x(degrees),rt[i])
    return rn

def pov_y(rt,degrees):
    rn=np.zeros((len(rt),3))
    for i in range(len(rt)):
        rn[i]=np.dot(mat_y(degrees),rt[i])
    return rn

def pov_z(rt,degrees):
    rn=np.zeros((len(rt),3))
    for i in range(len(rt)):
        rn[i]=np.dot(mat_z(degrees),rt[i])
    return rn

z=np.zeros((len(x)))

q0=np.column_stack([x,y,z])

q=np.zeros((0,3))

for i in range(len(x)):
    if q0[i][1]>=0 and q0[i][1]<=sqrt(3)*q0[i][0]+0.01 and q0[i][1]<=-sqrt(3)*q0[i][0]+s*sqrt(3)+0.01:
        q=np.append(q,[q0[i]], axis = 0)



mas=np.zeros((0,3))
mas1=np.zeros((0,3))
m=q
m=pov_z(m,60)
m=pov_x(m,55)

h=max(m[:,2])
u=h*sin(45*pi/180)

mas=np.append(mas,m, axis = 0)
mas=np.append(mas,pov_z(m,90), axis = 0)
mas=np.append(mas,pov_z(m,180), axis = 0)
mas=np.append(mas,pov_z(m,270), axis = 0)


m=q
m=pov_z(m,60)
m=pov_x(m,-55)

for i in range(len(m)):
    m[i,2]+=2*h
    

mas=np.append(mas,m, axis = 0)
mas=np.append(mas,pov_z(m,90), axis = 0)
mas=np.append(mas,pov_z(m,180), axis = 0)
mas=np.append(mas,pov_z(m,270), axis = 0)

print(len(mas))




v = np.array([  
            [-u,-u, h],
            [-u, u, h], 
            [u, u, h], 
            [u, -u, h],  
            [0, 0, 2*h],   
            [0, 0, 0]  
            ])
mas=np.append(mas,v, axis = 0)
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


ax = fig.add_subplot(projection='3d')
ax.add_collection3d(Poly3DCollection(verts, facecolors='grey',
 linewidths=0.5, edgecolors='black', alpha=1))


ax.scatter(mas[:,0],mas[:,1],mas[:,2],color='orange')
ax.axes.set_xlim(-h,h)
ax.axes.set_ylim(-h,h)

plt.show()