import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def Dvostruko_klatno_ODE(z, t):
    # Funkcija koja opisuje sistem običnih diferencijalnih jednačina za dvostruko klatno
    # z je vektor stanja koji sadrži uglove i brzine obrtaja za oba tega
    
    # Ova funkcija treba da vrati brzine promena za sve elemente vektora z
    # Implementacija funkcije bi trebala biti u skladu s postavljenim ODE
    phi1 = z[0]
    dtphi1 = z[1]
    phi2 = z[2]
    dtphi2 = z[3]
    g = z[4]
    m1 = z[5]
    m2 = z[6]
    l1 = z[7]
    l2 = z[8]

    zdot = np.zeros(9)

    # ODEs
    zdot[0] = dtphi1
    zdot[1] = -((g*(2*m1+m2)*np.sin(phi1) + m2*(g*np.sin(phi1-2*phi2) +
                2*(l2*dtphi2**2 + l1*dtphi1**2*np.cos(phi1-phi2))*np.sin(phi1-phi2))) /
                (2*l1*(m1+m2-m2*np.cos(phi1-phi2)**2)))

    zdot[2] = dtphi2
    zdot[3] = (((m1+m2)*(l1*dtphi1**2 + g*np.cos(phi1)) +
                l2*m2*dtphi2**2*np.cos(phi1-phi2))*np.sin(phi1-phi2)) / (l2*(m1+m2-m2*np.cos(phi1-phi2)**2))

    zdot[4] = 0  # g ostaje konstantno

    zdot[5] = 0  # m1 se ne menja tokom vremena
    zdot[6] = 0  # m2 se ne menja tokom vremena

    zdot[7] = 0  # l1 se ne menja tokom vremena
    zdot[8] = 0  # l2 se ne menja tokom vremena

    return zdot

def Dvostruko_klatno(ivp, vreme, fps, movie):
    # ivp - početni uslovi
    # vreme - ukupno vreme simulacije
    # fps - broj frejmova u sekundi za animaciju
    # movie - da li treba sačuvati animaciju u .mp4 formatu

    nframes = int(vreme * fps)

    # Resenje sistema ODE
    sol = odeint(Dvostruko_klatno_ODE, ivp, np.linspace(0, vreme, nframes))

    t = np.linspace(0, vreme, nframes)
    y = sol.T
    phi1 = y[0]  # Ugao prvog tega
    dtphi1 = y[1]  # Brzina obrtaja prvog tega
    phi2 = y[2]  # Ugao drugog tega
    dtphi2 = y[3]  # Brzina obrtaja drugog tega
    l1 = ivp[7]  # Dužina prvog niti
    l2 = ivp[8]  # Dužina drugog niti

    # Prikaz animacije
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title('Dvostruko klatno - Animacija')
    range_val = 1.1 * (l1 + l2)
    ax.set_xlim(-range_val, range_val)
    ax.set_ylim(-range_val, range_val)
    ax.set_aspect('equal')
    h, = ax.plot([], [], 'bo-', markersize=10, linewidth=2)

    def update(frame):
        # Ažuriranje pozicije tačaka za animaciju
        Xcoord = [0, l1 * np.sin(phi1[frame]), l1 * np.sin(phi1[frame]) + l2 * np.sin(phi2[frame])]
        Ycoord = [0, -l1 * np.cos(phi1[frame]), -l1 * np.cos(phi1[frame]) - l2 * np.cos(phi2[frame])]
        h.set_data(Xcoord, Ycoord)
        return h,

    anim = FuncAnimation(fig, update, frames=nframes, blit=True)

    # Grafici uglova u vremenu
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t, y[0], 'b-', label=r'$\theta_1(t)$', linewidth=2)
    ax.plot(t, y[2], 'r-', label=r'$\theta_2(t)$', linewidth=2)
    ax.set_xlabel('vreme (s)')
    ax.set_ylabel('ugao (\theta)')
    ax.set_title('Grafovi uglova u vremenu')
    ax.legend()
    ax.grid(True)


    if movie:
        anim.save('Dvostruko_klatno.mp4', writer='ffmpeg', fps=fps)
    else:
        plt.show()


# Dodatak za prikaz grafika uglova u vremenu
phi1 = np.pi / 4
dtphi1 = 0  # pocetna brzina prvog tega
phi2 = np.pi / 4
dtphi2 = 0  # pocetna brzina drugog tega
g = 9.81
m1 = 2
m2 = 1
l1 = 2
l2 = 1
vreme = 10
fps = 100
movie = False

ivp = [phi1, dtphi1, phi2, dtphi2, g, m1, m2, l1, l2]

# Resenje sistema ODE
sol = odeint(Dvostruko_klatno_ODE, ivp, np.linspace(0, 200, 1000))

t = np.linspace(0, vreme, fps * vreme)
u = sol.T

# Prikaz animacije i grafika uglova u vremenu
Dvostruko_klatno(ivp, vreme, fps, movie)
