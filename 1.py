import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, quad  
from matplotlib.animation import FuncAnimation

m = 0.001  # masa tega (kg)
r = 0.1    # precnik tega (m)
l = 0.7    # smanjena duzina kanapa (m)
g = 9.81   # gravitacija (m/s^2)
teta0 = np.pi/6   # smanjen ugao otklona (rad)
v0 = 0            # pocetna brzina
O = np.array([0, 0])  # koordinatni pocetak

tend = 50

#mi = 1.827e-5  # vazduh (kg/ms)
mi = 8.9e-4    # voda

B =  2 * np.pi * r * mi  

def odeint_custom(func, y0, t):
    """
    k1 = f(t_n, y_n)
    k2 = f(t_n + h/2, y_n + k1*h/2)
    k3 = f(t_n + h/2, y_n + k2*h/2)
    k4 = f(t_n + h, y_n + k3*h)
    k4 = f(t_n + h, y_n + k3*h)
    """
    


    """
    Numeričko rešavanje sistema običnih diferencijalnih jednačina (ODE) pomoću Runge-Kutta metode četvrtog reda.

    Parameters:
        - func: Funkcija koja opisuje sistem ODE.
        - y0: Početni uslovi.
        - t: Niz vremenskih tačaka na kojima se traže rešenja.

    Returns:
        - y: Matrica rešenja sistema ODE za svaku tačku u vremenu.
    """
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
#def model(x, t):
#    return [x[1], -g/l * np.sin(x[0])]

#############################################

# Sa otporom
def model(x, t):
    return [x[1], -B/m * x[1] - g/l * np.sin(x[0])]

init = [teta0, v0/l]

t = np.linspace(0, tend, 500)
x = odeint_custom(model, init, t)


fig, ax1 = plt.subplots(figsize=(8, 6))
ax1.plot(t, x[:, 0], label='Ugao teta')
ax1.plot(t, x[:, 1] * l, label='Brzina')
ax1.set_xlabel('Vreme')
ax1.legend()

# Simulacija klatna
fig, ax2 = plt.subplots()
ax2.axis('equal')
ax2.axis([-1.2 * l, 1.2 * l, -1.2 * l, 1.2 * l])
ax2.set_aspect('equal', adjustable='box')

O_circ = plt.Circle(O, 0.01, fill=False)
ax2.add_patch(O_circ)

line, = ax2.plot([], [], lw=2)
ball = plt.Circle((0, 0), 0.05, fill=False)
ax2.add_patch(ball)

def update(frame):
    P = l * np.array([np.sin(x[frame, 0]), -np.cos(x[frame, 0])])
    line.set_data([O[0], P[0]], [O[1], P[1]])
    ball.set_center((P[0], P[1]))
    return line, ball

ani = FuncAnimation(fig, update, frames=len(t), interval=50, blit=True)

plt.show()
