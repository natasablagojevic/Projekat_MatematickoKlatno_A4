import sys
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

# Pendulum rod lengths (m), bob masses (kg).
L1, L2 = 1, 1
m1, m2 = 1, 1
# The gravitational acceleration (m.s-2).
g = 9.81

def deriv(y, t, L1, L2, m1, m2):
    """Return the first derivatives of y = theta1, z1, theta2, z2."""
    theta1, z1, theta2, z2 = y

    c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)

    theta1dot = z1
    z1dot = (m2*g*np.sin(theta2)*c - m2*s*(L1*z1**2*c + L2*z2**2) -
             (m1+m2)*g*np.sin(theta1)) / L1 / (m1 + m2*s**2)
    theta2dot = z2
    z2dot = ((m1+m2)*(L1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) + 
             m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2)
    return theta1dot, z1dot, theta2dot, z2dot

def calc_E(y):
    """Return the total energy of the system."""
    th1, th1d, th2, th2d = y.T
    V = -(m1+m2)*L1*g*np.cos(th1) - m2*L2*g*np.cos(th2)
    T = 0.5*m1*(L1*th1d)**2 + 0.5*m2*((L1*th1d)**2 + (L2*th2d)**2 +
            2*L1*L2*th1d*th2d*np.cos(th1-th2))
    return T + V

# Maximum time, time point spacings and the time grid (all in s).
tmax, dt = 30, 0.01
t = np.arange(0, tmax+dt, dt)
# Initial conditions: theta1, dtheta1/dt, theta2, dtheta2/dt.
y0 = np.array([3*np.pi/7, 0, 3*np.pi/4, 0])

# Do the numerical integration of the equations of motion
y = odeint(deriv, y0, t, args=(L1, L2, m1, m2))

# Check that the calculation conserves total energy to within some tolerance.
EDRIFT = 0.05
# Total energy from the initial conditions
E = calc_E(y0)
if np.max(np.sum(np.abs(calc_E(y) - E))) > EDRIFT:
    sys.exit('Maximum energy drift of {} exceeded.'.format(EDRIFT))

# Unpack z and theta as a function of time
theta1, theta2 = y[:,0], y[:,2]

# Convert to Cartesian coordinates of the two bob positions.
x1 = L1 * np.sin(theta1)
y1 = -L1 * np.cos(theta1)
x2 = x1 + L2 * np.sin(theta2)
y2 = y1 - L2 * np.cos(theta2)

# Plotted bob circle radius
r = 0.05
# Plot a trail of the m2 bob's position for the last trail_secs seconds.
trail_secs = 1
# This corresponds to max_trail time points.
max_trail = int(trail_secs / dt)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8.3333, 6.25), dpi=72)
ax.set_xlim(-L1-L2-r, L1+L2+r)
ax.set_ylim(-L1-L2-r, L1+L2+r)
ax.set_aspect('equal', adjustable='box')
ax.axis('off')

# Plot the initial configuration
stapovi_klatna, = ax.plot([0, x1[0], x2[0]], [0, y1[0], y2[0]], lw=2, c='k')
zacelje, = ax.plot([0], [0], 'ko', markersize=5)
kugla1, = ax.plot([x1[0]], [y1[0]], 'bo', markersize=10)
kugla2, = ax.plot([x2[0]], [y2[0]], 'ro', markersize=10)
linija_traga, = ax.plot([], [], c='r', solid_capstyle='butt', lw=2)

# Function to initialize the plot
def init():
    stapovi_klatna.set_data([], [])
    zacelje.set_data([], [])
    kugla1.set_data([], [])
    kugla2.set_data([], [])
    linija_traga.set_data([], [])
    return stapovi_klatna, zacelje, kugla1, kugla2, linija_traga

# Function to update the plot for each frame
def update(i):
    stapovi_klatna.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
    zacelje.set_data([0], [0])
    kugla1.set_data([x1[i]], [y1[i]])
    kugla2.set_data([x2[i]], [y2[i]])

    # Trail
    ns = 20
    s = max_trail // ns
    imin = i - max_trail
    if imin < 0:
        imin = 0
    linija_traga.set_data(x2[imin:i+1:s], y2[imin:i+1:s])

    return stapovi_klatna, zacelje, kugla1, kugla2, linija_traga

# Frame rate, s-1
fps = 10
# Make an animation
animacija = FuncAnimation(fig, update, frames=np.arange(0, t.size), init_func=init, blit=True)

# Show the animation
plt.show()
