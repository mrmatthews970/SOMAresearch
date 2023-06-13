#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import h5py
import pickle
from numba import jit

ftime = []
for i in range(60): # number of dump files; dump files were created every 100 MCs and the simulation was run for 6000 MCs
    ft = h5py.File("nf12p5_t" + str((i+60)*100) + ".h5", "r+") # replace with name of dump files. The starting time of the files with the field off continues from the end time of the files with the field on
    ftime.append(ft)

for p in range(4): # p values used are 0,1,2,3
    modeset = []
    for file in ftime:
        bt = file["beads"][:] # positions of all the beads
        Nt = file["parameter/reference_Nbeads"][0] # number of beads in each molecule
        nmolt = file["parameter/n_polymers"][0] # number of molecules

        @jit(nopython = True)
        def rouseform_t():
            xnt = np.zeros((nmolt,3))
            for q in range(nmolt):
                rn = bt[q*Nt:(q+1)*Nt] # each molecule has Nt beads
                r2 = np.zeros(np.shape(rn))
                for i in range(Nt):
                    r2[i] = rn[i]*np.cos(p*np.pi*(i+0.5)/(Nt+1)) # Rouse mode equation
                xnt[q] = np.sum(r2,axis=0)/(Nt+1)
    
            for i1 in range(np.shape(xnt)[0]):
                for i2 in range(np.shape(xnt)[1]):
                    if xnt[i1,i2]>0.5 or xnt[i1,i2]<-0.5:
                        xnt[i1,i2] -= round(xnt[i1,i2],0) # puts the beads back into the domain if they escape
            return xnt
    
        xnt = rouseform_t()
        modeset.append(xnt)

    with open("nf12hp" + str(p) + ".dat","wb") as fh: # make sure to change the name if running multiple simulations
        pickle.dump(modeset,fh) # generates a .dat file with the Rouse modes for all the p values
