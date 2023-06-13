#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import h5py

filename = "box5.h5" # replace with the name of the .h5 file generated from the start. Do this before running the simulations

period = 4
amp = 2.5

with h5py.File(filename, "r+") as file_handle:
    if "external_field" in file_handle:
        del file_handle["external_field"]
        # this will set a new external field.
    nxyz = tuple(file_handle["parameter/nxyz"][:])
    ntypes = tuple(file_handle["parameter/n_types"][:])

    L = file_handle["parameter/lxyz"][0]
    g = ntypes + nxyz
    field = np.ones(g)
    xc = np.linspace(-L/2,L/2,g[1])
    x = amp*np.cos(period*np.pi*xc/L) # a sinusiodal field is used
    for i in range(g[1]):
        field[:,i] = field[:,i]*x[i]
    # assign the value to the field as you like them

    file_handle["external_field"] = field

