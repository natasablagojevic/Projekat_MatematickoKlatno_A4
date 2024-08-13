import numpy as np 
from numpy import sin, cos
from scipy.integrate import odeint
from matplotlib import pyplot as plt 


# define the equations
def equations(y0, t):
	theta, x = y0
	f = [x, -(g/l) * sin(theta)]
	return f

def plot_results(time, theta1, theta2):
	plt.plot(time, theta1[:,0])
	plt.plot(time, theta2)

	s = '(Pocetni ugao = ' + str(initial_angle) + ' stepeni)'
	plt.title('Matematicko klatno: ' + s)
	plt.xlabel('vreme (s)')
	plt.ylabel('ugao (rad)')
	plt.grid(True)
	plt.legend(['bez aproksimacije', 'sa aproksimacijom'], loc='lower right')
	plt.show()

# parameters
g = 9.81
l = 1.0

time = np.arange(0, 10.0, 0.025)

# initial conditions
initial_angle = 45.0
theta0 = np.radians(initial_angle)
x0 = np.radians(0.0)

# find the solution to the nonlinear problem
theta1 = odeint(equations, [theta0, x0],  time)

# find the solution to the linear problem
w = np.sqrt(g/l)
theta2 = [theta0 * cos(w*t) for t in time]

# plot the results
plot_results(time, theta1, theta2)

