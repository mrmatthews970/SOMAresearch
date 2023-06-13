#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import h5py
import pickle
import matplotlib.pyplot as plt
from numba import jit

lineson = []
linesoff = []
for p in range(4): # p values used are 0,1,2,3
    with open("f7hp" + str(p) + "_2.dat","rb") as fh: # replace with file name containing Rouse modes generated with rousemodes.py
        mode1 = pickle.load(fh)
            
    with open("nf7hp" + str(p) + "_2.dat","rb") as fh: # replace with file name containing Rouse modes generated with rouseoff.py
        mode2 = pickle.load(fh)
            
    brg = np.arange(-0.5,0.5,0.01) # bins for histogram function
    nt = np.shape(mode1)[0] # number of time steps
    nto = np.shape(mode2)[0]
    
    mset1 = []
    for j in range(nt):
        on = np.histogram(mode1[j][:,0],bins = brg)[0] # generates the distribution of Rouse modes in each bin in brg
        mset1.append(max(on))
            
    mset2 = []
    for j in range(nto):
        off = np.histogram(mode2[j][:,0],bins = brg)[0]
        mset2.append(max(off))

    lineson.append(np.array(mset1))
    linesoff.append(np.array(mset2))

with open("indie_on.dat","wb") as fh:
    pickle.dump(lineson,fh) # produces the counts for each p value used

with open("indie_off.dat","wb") as fh:
    pickle.dump(linesoff,fh)
