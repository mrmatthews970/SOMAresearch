# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import h5py
from PIL import Image

f = h5py.File("box_ana.h5", "r+") # use the file after the field on simulation is run
df = f["density_field"][:,0] # Dimensions are (time, particle type, x counts, y counts, z counts)

s = np.shape(df)
x = np.linspace(-0.5,0.5,s[1])
for i in range(s[0]):
    plt.clf()
    rhox = []
    for j in range(s[1]):
        rhox.append(np.sum(np.sum(df[i,j],axis=1))/(s[2]*s[3]))
        rho_tot = np.sum(np.sum(np.sum(df[i],axis=1)))/(s[1]*s[2]*s[3])
        rhofrac = rhox/rho_tot
    plt.scatter(x,rhofrac)
    plt.plot(x,rhofrac)
    plt.xlabel("$x$")
    plt.ylabel(r"$\frac{\rho (x)}{\rho_{tot}}$", rotation = 0,size=16)
    plt.title("Timestep = " + str(10*i))
    plt.ylim(0,2)
    plt.savefig(f"{i}.png")
    plt.close()
    
images = [Image.open(f"{i}.png") for i in range(s[0])]

images[0].save('densityprof.gif', save_all=True, append_images=images[1:], duration=10)
