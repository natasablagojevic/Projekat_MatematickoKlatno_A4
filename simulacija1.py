import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def f(x, t):
    return [x[1], -k*x[1] - r*np.sin(x[0])]

m = 0.9  # masa tega
b = 0.2  # precnik tega
l = 0.5  # duzina kanapa
g = 9.81  # gravitacija
r = g / l
k = b / (m * l)

fig, ax = plt.subplots()
init = [np.pi/2, 0]  # pocetni polozaj (init = [theta_0 v_0])
t = np.linspace(0, 200, 1000)
sol = odeint(f, init, t)

O = np.array([0, 0])
ax.set_aspect('equal')
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.grid(True)

for i in range(len(t)):
    P = l * np.array([np.sin(sol[i, 0]), -np.cos(sol[i, 0])])
    O_circ = plt.Circle(O, 0.01, fill=False)
    pend = plt.Line2D([O[0], P[0]], [O[1], P[1]])
    ball = plt.Circle(P, 0.05, fill=True)

    ax.add_patch(O_circ)
    ax.add_line(pend)
    ax.add_patch(ball)

    plt.pause(0.001)

    if i < len(t) - 1:
        O_circ.remove()
        pend.remove()
        ball.remove()

plt.show()
