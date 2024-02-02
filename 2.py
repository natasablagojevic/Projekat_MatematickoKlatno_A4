import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation

m = 0.001  # masa tega (kg)
r = 0.1    # precnik tega (m)
l = 0.7    # smanjena duzina kanapa (m)
g = 9.81   # gravitacija (m/s^2)
teta0 = np.pi/4   # smanjen ugao otklona (rad)
v0 = 0            # pocetna brzina
O = np.array([0, 0])  # koordinatni pocetak

tend = 50

# mi = 1.827e-5  # vazduh (kg/ms)
mi = 8.9e-4    # voda

B =  2 * np.pi * r * mi  

def odeint_custom(func, y0, t):
    y = np.zeros((len(t), len(y0)))
    y[0, :] = y0

    for i in range(1, len(t)):
        dt = t[i] - t[i-1]
        k1 = np.array(func(y[i-1, :], t[i-1]))
        k2 = np.array(func(y[i-1, :] + 0.5 * dt * k1, t[i-1] + 0.5 * dt))
        k3 = np.array(func(y[i-1, :] + 0.5 * dt * k2, t[i-1] + 0.5 * dt))
        k4 = np.array(func(y[i-1, :] + dt * k3, t[i]))

        y[i, :] = y[i-1, :] + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    return y

# Bez otpora
def model(x, t):
    return [x[1], -g/l * np.sin(x[0])]

def model2(x, t):
    return [x[1], -g/l * x[0]]

init = [teta0, v0/l]

t = np.linspace(0, tend, 500)
x = odeint_custom(model, init, t)

x2 = odeint_custom(model2, init, t)

fig, (ax2) = plt.subplots(1, 1, figsize=(8, 10))



# Drugi graf za simulaciju klatna
ax2.axis('equal')
ax2.axis([-1.2 * l, 1.2 * l, -1.2 * l, 1.2 * l])
ax2.set_aspect('equal', adjustable='box')

O_circ = plt.Circle(O, 0.01, fill=False)
ax2.add_patch(O_circ)

line, = ax2.plot([], [], lw=2, label='Klatno bez aproksimacije')
ball = plt.Circle((0, 0), 0.05, fill=False)
ax2.add_patch(ball)

line2, = ax2.plot([], [], lw=2, label='Klatno sa aproksimacijom')
ball2 = plt.Circle((0, 0), 0.05, fill=False)
ax2.add_patch(ball2)
ax2.legend()

def update(frame):
    # Prvo klatno
    P = l * np.array([np.sin(x[frame, 0]), -np.cos(x[frame, 0])])
    line.set_data([O[0], P[0]], [O[1], P[1]])
    ball.set_center((P[0], P[1]))

    # Drugo klatno - koristi x2
    P2 = l * np.array([np.sin(x2[frame, 0]), -np.cos(x2[frame, 0])])
    line2.set_data([O[0], P2[0]], [O[1], P2[1]])
    ball2.set_center((P2[0], P2[1]))

    return line, ball, line2, ball2

# Pokrenite animaciju
ani = FuncAnimation(fig, update, frames=len(t), interval=50, blit=True)

plt.show()
