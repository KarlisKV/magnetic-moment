#imports libraries
import pickle
import matplotlib.pyplot as plt
import numpy as np
import math
from math import pi
import scipy.optimize
from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D

#for the graph
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# h = height of all measured points, mm d = diameter of dipole, mm
h = 8
d = 10
H =h/1000
D = d/1000
#Plots a sphere at point (0,0,0)
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
xx = D * np.outer(np.cos(u), np.sin(v))
yy = D * np.outer(np.sin(u), np.sin(v))
zz = D * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(xx, yy, zz, color='#1f77b4',
                alpha=0.8,linewidth=1.0)

#imports measured magnetic field values           
objects = []
with (open("19mm_3.pkl", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break
xyz = []        
coords1 = [item for t in objects for item in t] 
coords2 = coords1[0] 
x = []
y = []
z = []
bx = []
by = []
bz = []
for i in range(49):
    coords3 = coords2[i] 
    x.append(0.001*coords3[0])
    y.append(0.001*coords3[1])
    z.append(H+0.001*coords3[2])
    bx.append(0.001*coords3[4])    
    by.append(0.001*coords3[6])
    bz.append(0.001*coords3[8])
    
#calculates the distance from the measured point to the dipole and the corresponding unit vectors
r =  []
y_hat = []
x_hat = []
z_hat = []
for i in range(49):
    r.append(math.sqrt(x[i]**2+y[i]**2+z[i]**2))
    y_hat.append(y[i]/r[i]) 
    x_hat.append(x[i]/r[i]) 
    z_hat.append(z[i]/r[i]) 
    
#initial guess value for the optimization function
magnetic_moment = 2
#optimization function to get magnetic moment values
def magnetic_field(magnetic_moment):
    mu_zero = 4*pi*1*10**-7
    bex = []
    bey = []
    bez = []
    for i in range(49):
        bey.append(((mu_zero)/(4*pi*r[i]**3))*(3*y_hat[i]*(magnetic_moment*y_hat[i])))
        bex.append(((mu_zero)/(4*pi*r[i]**3))*(3*x_hat[i]*(magnetic_moment*y_hat[i])))
        bez.append(((mu_zero)/(4*pi*r[i]**3))*(3*z_hat[i]*(magnetic_moment*y_hat[i])-magnetic_moment))  
    pot_field = 0
    for i in range(49):
        b_field= ((bx[i]-bex[i])**2 + (by[i]-bey[i])**2 + (bz[i]-bez[i])**2)
        pot_field = pot_field + b_field 
    return pot_field
params_guess = [magnetic_moment]
res = minimize(magnetic_field, params_guess, method='nelder-mead',
               options={'xatol': 1e-8, 'disp': True})                             
print(res)
print("Magnetic moment value is:" + str(res.x))

# for the graph
plt.xlim([-0.05,0.05])
plt.ylim([-0.05,0.05])
ax.set_zlim(-0.01,0.05)
ax.scatter(x, y, z, c='red')
ax.quiver(x, y, z, bz, by, bz, length=0.1, arrow_length_ratio=0.3, pivot='tail', normalize=False)
ax.view_init(elev=15, azim=10)
ax.set_xlabel('x coordinate, m',fontsize=10)
ax.set_ylabel('y coordinate, m',fontsize=10)
ax.set_zlabel('z coordinate, m',fontsize=10)
plt.show()