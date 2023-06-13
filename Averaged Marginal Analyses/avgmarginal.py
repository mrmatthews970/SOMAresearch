#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import h5py
import pickle
import matplotlib.pyplot as plt
from numba import jit

avglineson = []
avglinesoff = []
for p in range(4): # p values used are 0,1,2,3
    avgset = []
    for i in range(5): # number of averaged runs
        with open("f" + str(i+1) + "p" + str(p) + ".dat","rb") as fh: # replace with file name containing Rouse modes generated with rousemodes.py
            avgset.append(pickle.load(fh))
            
    avgoff = []
    for i in range(5): # number of averaged runs
        with open("nf" + str(i+1) + "p" + str(p) + ".dat","rb") as fh: # replace with file name containing Rouse modes generated with rouseoff.py
            avgoff.append(pickle.load(fh))
            
    brg = np.arange(-0.5,0.5,0.01) # bins for histogram function
    navg = np.shape(avgset)[0] # number of files uploaded
    nt = np.shape(avgset)[1] # number of time steps
    
    navgo = np.shape(avgoff)[0]
    nto = np.shape(avgoff)[1]
    
    mseton = np.zeros((navg,nt))
    for i1 in range(navg):
        for j in range(nt):
            on = np.histogram(avgset[i1][j][:,0],bins = brg)[0] # generates the distribution of Rouse modes in each bin in brg
            mseton[i1,j] = max(on)
            
    msetoff = np.zeros((navgo,nto))
    for i1 in range(navgo):
        for j in range(nto):
            off = np.histogram(avgoff[i1][j][:,0],bins = brg)[0]
            msetoff[i1,j] = max(off)
           
    finavg = np.sum(mseton,axis=0)/navg # averages the counts of the Rouse modes
    finoff = np.sum(msetoff,axis=0)/navgo
    avglineson.append(finavg)
    avglinesoff.append(finoff)

with open("avgon.dat","wb") as fh:
    pickle.dump(avglineson,fh) # produces the average counts for each p value used

with open("avgoff.dat","wb") as fh:
    pickle.dump(avglinesoff,fh)
