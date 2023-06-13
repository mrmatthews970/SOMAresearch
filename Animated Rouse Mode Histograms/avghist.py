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
    avgset = []
    for i in range(10): # number of averaged runs
        with open("f" + str(i+1) + "p" + str(p) + ".dat","rb") as fh: # replace with file name containing Rouse modes generated with rousemodes.py
            avgset.append(pickle.load(fh))
            
    avgoff = []
    for i in range(10): # number of averaged runs
        with open("nf" + str(i+1) + "p" + str(p) + ".dat","rb") as fh: # replace with file name containing Rouse modes generated with rouseoff.py
            avgoff.append(pickle.load(fh))
    
    w = 0.01
    brg = np.arange(-0.5,0.5,w) # bins for histogram function
    navg = np.shape(avgset)[0] # number of files uploaded
    nt = np.shape(avgset)[1] # number of time steps
    nmol = np.shape(avgset)[2]
    
    navgo = np.shape(avgoff)[0]
    nto = np.shape(avgoff)[1]
    nmolo = np.shape(avgoff)[2]
    
    mseton = np.zeros((navg,nt,100))
    for i1 in range(navg):
        for j in range(nt):
            on = np.histogram(avgset[i1][j][:,0],bins = brg)[0] # generates the distribution of Rouse modes in each bin in brg
            on = np.concatenate((on,[nmol - np.sum(on)]))
            mseton[i1,j] = on
            
    msetoff = np.zeros((navgo,nto,100))
    for i1 in range(navgo):
        for j in range(nto):
            off = np.histogram(avgoff[i1][j][:,0],bins = brg)[0]
            off = np.concatenate((off,[nmolo - np.sum(off)]))
            msetoff[i1,j] = off
           
    finavg = np.sum(mseton,axis=0)/navg # averages the counts of the Rouse modes
    finoff = np.sum(msetoff,axis=0)/navgo
    
    start1 = 0
    for i in range(nt):
        plt.figure(figsize = (10,8))
        plt.bar(brg,finavg[i],width = w)
        plt.xlabel("x-Coordinate Value",size=16)
        plt.ylabel("Average Counts",size=16)
        plt.title("Average Coordinate Counts, p = " + str(p) + ", Field On, t = " + str(start1),size=25)
        plt.ylim(0,0.1*nmol)
        plt.savefig("modeson" + str(start1) + "_p" + str(p) + ".png")
        
        start1 += 100
        plt.close()
    
    images = [Image.open(f"modeson{i*100}_p" + str(p) + ".png") for i in range(nt)]
    images[0].save('modeson_p' + str(p) + '.gif', save_all=True, append_images=images[1:], duration=500)
    
    start2 = 0
    for i in range(nt):
        plt.figure(figsize = (10,8))
        plt.bar(brg,finoff[i],width = w)
        plt.xlabel("x-Coordinate Value",size=16)
        plt.ylabel("Average Counts",size=16)
        plt.title("Average Coordinate Counts, p = " + str(p) + ", Field Off, t = " + str(start2),size=25)
        plt.ylim(0,0.1*nmolo)
        plt.savefig("modesoff" + str(start2) + "_p" + str(p) + ".png")
        
        start2 += 100
        plt.close()
    
    images = [Image.open(f"modesoff{i*100}_p" + str(p) + ".png") for i in range(nto)]
    images[0].save('modesoff_p' + str(p) + '.gif', save_all=True, append_images=images[1:], duration=500)

