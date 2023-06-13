# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import h5py

f = h5py.File("box_ana.h5", "r+") # use the file after the field on simulation is run
df = f["density_field"][:,0] # Dimensions are (time, particle type, x counts, y counts, z counts)

fe = h5py.File("nf_ana.h5", "r+") # use the file after the field off simulation is run
dfe = fe["density_field"][:,0] # Dimensions are (time, particle type, x counts, y counts, z counts)

amp = 2.5 # fill with the amplitude used in your simulations
s2 = np.shape(df) # time steps for field on
s2e = np.shape(dfe) # time steps for field off
tamp = np.linspace(0,2-2/s2[0],s2[0]) # two Rouse times used for field on
tamp2 = np.linspace(0,2-2/s2e[0],s2e[0]) # two Rouse times used for field off
x2 = np.linspace(-0.5,0.5,s2[1]) # x-coordinates for field on
x2e = np.linspace(-0.5,0.5,s2e[1])
def func(x,a):
    return 1 + a*np.cos(4*np.pi*x) # a is the amplitude of the density profile
ata = []
atae = []

# Find all amplitudes at given timesteps.
for i in range(s2[0]):
    plt.clf()
    rhox = []
    for j in range(s2[1]):
        rhox.append(np.sum(np.sum(df[i,j],axis=1))/(s2[2]*s2[3]))
        rho_tot = np.sum(np.sum(np.sum(df[i],axis=1)))/(s2[1]*s2[2]*s2[3])
    ata.append(curve_fit(func,x2,rhox/rho_tot)[0]) # adds the amplitude at each time
ata = np.squeeze(ata)
amin = min(ata)

for i in range(s2e[0]):
    plt.clf()
    rhox = []
    for j in range(s2e[1]):
        rhox.append(np.sum(np.sum(dfe[i,j],axis=1))/(s2e[2]*s2e[3]))
        rho_tot = np.sum(np.sum(np.sum(df[i],axis=1)))/(s2e[1]*s2e[2]*s2e[3])
    atae.append(curve_fit(func,x2e,rhox/rho_tot)[0]) # adds the amplitude at each time
atae = np.squeeze(atae)
amine = min(atae)

plt.figure(figsize = (10,8))
plt.scatter(tamp,-ata/max(-ata),label = "Data (field on)",color = "r") # starts at 0, ends at 1
plt.semilogy(tamp,-ata/max(-ata),color = "r")
plt.scatter(tamp2,1+atae/max(-atae),label = "Data (field off)",color = "g") # starts at 0, ends at 1
plt.plot(tamp2,1+atae/max(-atae),color = "g")
plt.xlabel(r"$t/ \tau_R$", size = 16)
plt.ylabel(r"Amplitude", rotation = 90, size = 16)
plt.xlim(0,1)
plt.title("Amplitude Plot over Time (Field Amplitude = " + str(amp) + ")", size = 22)
plt.legend(prop={'size': 15})
plt.grid()
plt.savefig("amp_all.png")
