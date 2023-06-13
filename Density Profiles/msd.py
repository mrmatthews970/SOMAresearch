# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import h5py

file = h5py.File("box_ana.h5", "r+") # use the file after the simulation is run
df = file["density_field"][:,0] # Dimensions are (time, particle type, x counts, y counts, z counts)
msd = file["MSD"] # mean squared displacement

g1=msd[:,3]
g3=msd[:,7]
t = 500*np.arange(0,len(g1),1) # multiplier depends on the time between dump files

slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(t,g3) # the slope of the line is used for the Rouse time

fig_g3 = plt.figure()
plt.plot(t,g3,label="g_3(t) Values")
plt.scatter(t,g3)
plt.plot(t,slope1*t+intercept1*np.ones(len(g1)), label = "Best Fit Line")
plt.xlabel("t")
plt.ylabel(r"g_3(t)", rotation = 0, size = 16)
plt.title("Slope = " + str(slope1), size = 20)
plt.legend()
plt.grid()
plt.show()
fig_g3.savefig("g3.png", bbox_inches='tight')
