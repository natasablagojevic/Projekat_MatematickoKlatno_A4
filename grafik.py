import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(0, np.pi, 100)  # Generiranje niza od 100 točaka od 0 do pi

# Crtanje grafa sin(theta) i theta
plt.plot(theta, np.sin(theta), label='sin(theta)')
plt.plot(theta, theta, label='theta')

# Dodavanje legende
plt.legend()

# Postavljanje oznaka na osima
plt.xlabel('theta')

# Prikaz grafa
plt.show()