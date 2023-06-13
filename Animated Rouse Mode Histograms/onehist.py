#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import h5py
import pickle
import matplotlib.pyplot as plt
from numba import jit
from PIL import Image

for p in range(4): # p values used are 0,1,2,3
    with open("f7hp" + str(p) + "_2.dat","rb") as fh: # replace with file name containing Rouse modes generated with rousemodes.py
        mode1 = pickle.load(fh)
            
    with open("nf7hp" + str(p) + "_2.dat","rb") as fh: # replace with file name containing Rouse modes generated with rouseoff.py
        mode2 = pickle.load(fh)
    
    w = 0.01
    brg = np.arange(-0.5,0.5,w) # bins for histogram function
    nt = np.shape(mode1)[0] # number of time steps
    nmol = np.shape(mode1)[1]
    
    nto = np.shape(mode2)[0]
    nmolo = np.shape(mode2)[1]
    
    mseton = np.zeros((nt,100))
    for j in range(nt):
        on = np.histogram(mode1[j][:,0],bins = brg)[0] # generates the distribution of Rouse modes in each bin in brg
        on = np.concatenate((on,[nmol - np.sum(on)]))
        mseton[j] = on
            
    msetoff = np.zeros((nto,100))
    for j in range(nto):
        off = np.histogram(mode2[j][:,0],bins = brg)[0]
        off = np.concatenate((off,[nmolo - np.sum(off)]))
        msetoff[j] = off
        
    start1 = 0
    for i in range(nt):
        plt.figure(figsize = (10,8))
        plt.bar(brg,mseton[i],width = w)
        plt.xlabel("x-Coordinate Value",size=16)
        plt.ylabel("Counts",size=16)
        plt.title("Coordinate Counts, p = " + str(p) + ", Field On, t = " + str(start1),size=25)
        plt.ylim(0,0.1*nmol)
        plt.savefig("modeson" + str(start1) + "_p" + str(p) + ".png")
        
        start1 += 100
        plt.close()
    
    images = [Image.open(f"modeson{i*100}_p" + str(p) + ".png") for i in range(nt)]
    images[0].save('modeson_p' + str(p) + '.gif', save_all=True, append_images=images[1:], duration=500)
    
    start2 = 0
    for i in range(nt):
        plt.figure(figsize = (10,8))
        plt.bar(brg,msetoff[i],width = w)
        plt.xlabel("x-Coordinate Value",size=16)
        plt.ylabel("Counts",size=16)
        plt.title("Coordinate Counts, p = " + str(p) + ", Field Off, t = " + str(start2),size=25)
        plt.ylim(0,0.1*nmolo)
        plt.savefig("modesoff" + str(start2) + "_p" + str(p) + ".png")
        
        start2 += 100
        plt.close()
    
    images = [Image.open(f"modesoff{i*100}_p" + str(p) + ".png") for i in range(nto)]
    images[0].save('modesoff_p' + str(p) + '.gif', save_all=True, append_images=images[1:], duration=500)

