from matplotlib import pyplot as plt
import numpy as np
from math import *
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


fig = plt.figure()


x=np.zeros(1)
y=np.zeros(1)
r=1             #радиус гексагона
n=5           #количество точек на стороне
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
        [0,cos(a),-sin(a)],
        [0,sin(a),cos(a)]
        ]
def mat_y(a):
    return [ 
        [cos(a),0,sin(a)],
        [0,1,0],
        [-sin(a),0,cos(a)]
        ]
def mat_z(a):
    return [ 
        [cos(a),-sin(a),0],
        [sin(a),cos(a),0],
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
m=pov_z(m,pi/3)
m=pov_x(m,pi/4.8)


u=h*sin(45*pi/180)



ang=pi/2.5

mas=np.append(mas,m, axis = 0)
mas=np.append(mas,pov_z(m,ang), axis = 0)
mas=np.append(mas,pov_z(m,ang*2), axis = 0)
mas=np.append(mas,pov_z(m,ang*3), axis = 0)
mas=np.append(mas,pov_z(m,ang*4), axis = 0)

ym=max(mas[:,1])
z0=min(mas[:,2])
z1=max(mas[:,2])



m=q
m=pov_z(m,pi/3)

m=pov_x(m,5*pi/9)
m=pov_y(m,pi)


for i in range(len(m)):
    m[i,2]+=z1+(s)*sqrt(3)/2
    m[i,1]+=ym+(s-h)*sin(pi/18)

mas=np.append(mas,m, axis = 0)
mas=np.append(mas,pov_z(m,ang), axis = 0)
mas=np.append(mas,pov_z(m,ang*2), axis = 0)
mas=np.append(mas,pov_z(m,ang*3), axis = 0)
mas=np.append(mas,pov_z(m,ang*4), axis = 0)


z2=max(mas[:,2])

m=pov_x(mas,pi)
for i in range(len(m)):
    m[i,2]+=z2+z1+h*cos(pi/18)

ax = fig.add_subplot(projection='3d')


ax.scatter(mas[:,0],mas[:,1],mas[:,2],color='orange')
ax.scatter(m[:,0],m[:,1],m[:,2],color='blue')
ax.axes.set_xlim(-ym,ym)
ax.axes.set_ylim(-ym,ym)

plt.show()