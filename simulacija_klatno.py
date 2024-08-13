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

# Bez otpora
def model(x, t):
    return [x[1], -g/l * np.sin(x[0])]

# Sa otporom
#def model(x, t):
#    return [x[1], -B/m * x[1] - g/l * np.sin(x[0])]

init = [teta0, v0/l]

t = np.linspace(0, tend, 500)
x = odeint(model, init, t)

fig = plt.figure(figsize=(8, 10))

# Postavljanje rasporeda subplot-a pomoću gridspec
gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 1])

# Prvi subplot (grafik)
ax1 = fig.add_subplot(gs[0])
ax1.plot(t, x[:, 0])
ax1.plot(t, x[:, 1] * l)
ax1.set_xlabel('Vreme')
ax1.legend(['Ugao teta', 'Brzina'])

# Drugi subplot (animacija)
ax2 = fig.add_subplot(gs[1:])
ax2.axis('equal')  # odnos x i y ose (isto sto naredba: axis equal)
ax2.axis([-1.2 * l, 1.2 * l, -1.2 * l, 1.2 * l])  # granice za x i y osu u zavisnosti od l (20% vise)
ax2.set_aspect('equal', adjustable='box')  # očuvanje proporcija osa

O_circ = plt.Circle(O, 0.01, fill=False)  # postolje
ax2.add_patch(O_circ)

line, = ax2.plot([], [], lw=2)  # stap
ball = plt.Circle((0, 0), 0.05, fill=False)  # teg
ax2.add_patch(ball)

def update(frame):
    P = l * np.array([np.sin(x[frame, 0]), -np.cos(x[frame, 0])])  # polozaj tega
    line.set_data([O[0], P[0]], [O[1], P[1]])  # stap
    ball.set_center((P[0], P[1]))  # pozicija lopte
    return line, ball

ani = FuncAnimation(fig, update, frames=len(t), interval=50, blit=True)

# Drugi prozor za grafik zavisnosti perioda oscilovanja od pocetnog ugla
fig, ax3 = plt.subplots()
theta0_values = np.arange(0, np.pi/2 + 0.1, 0.1)
T1_values = []
T2_values = []

for theta in theta0_values:
    integrand = lambda x: 1/np.sqrt(np.abs(np.cos(x) - np.cos(theta)) + 1e-8)
    integral_value, _ = quad(integrand, 0, theta)
    T1_values.append(4 * np.sqrt(l/(2*g)) * integral_value)
    T2_values.append(2 * np.pi * np.sqrt(l/g))

ax3.plot(theta0_values, T1_values, label='Teta')
ax3.plot(theta0_values, T2_values, label='Mala theta<<1')
ax3.set_xlabel('Theta')
ax3.set_ylabel('Period T')
ax3.legend()



plt.show()

