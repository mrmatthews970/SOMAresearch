#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import h5py
import pickle
from numba import jit

ftime = []
for i in range(60): # number of dump files; files were dumped every 100 MCs, and simulations were run for 6000 MCs
    ft = h5py.File("box3_t" + str(i*100) + ".h5", "r+") # replace with the names of the dump files created from the simulation
    ftime.append(ft)

for p in range(4): # the p-values used are 0,1,2,3
    modeset = []
    for file in ftime:
        bt = file["beads"][:] # gives the positions of all the beads
        Nt = file["parameter/reference_Nbeads"][0] # number of beads in each molecule
        nmolt = file["parameter/n_polymers"][0] # number of molecules

        @jit(nopython = True)
        def rouseform_t():
            xnt = np.zeros((nmolt,3))
            for q in range(nmolt):
                rn = bt[q*Nt:(q+1)*Nt] # molecules are Nt beads long
                r2 = np.zeros(np.shape(rn))
                for i in range(Nt):
                    r2[i] = rn[i]*np.cos(p*np.pi*(i+0.5)/(Nt+1)) # Rouse mode calculation
                xnt[q] = np.sum(r2,axis=0)/(Nt+1)
    
            for i1 in range(np.shape(xnt)[0]):
                for i2 in range(np.shape(xnt)[1]):
                    if xnt[i1,i2]>0.5 or xnt[i1,i2]<-0.5:
                        xnt[i1,i2] -= round(xnt[i1,i2],0) # brings the beads back into the domain if they leave; domain is a box centred around the origin with side length 1
            return xnt
    
        xnt = rouseform_t()
        modeset.append(xnt)

    with open("f1p" + str(p) + ".dat","wb") as fh: # make sure to change the name of the file if you are creating multiple .dat files
        pickle.dump(modeset,fh) # creates a .dat file with all the Rouse modes for all the given p-values
