#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import h5py

filename2 = "nf12p5.h5" # replace with the name of the .h5 file created from the end of the field on simulation. Do this before running the simulation

with h5py.File(filename2, "r+") as file_handle:
    if "external_field" in file_handle:
        del file_handle["external_field"]
    else:
        print("There is no external field")
    nxyz = tuple(file_handle["parameter/nxyz"][:])
    ntypes = tuple(file_handle["parameter/n_types"][:])

    L = file_handle["parameter/lxyz"][0]
    g = ntypes + nxyz
    field = np.zeros(g) # turns the field to zero

    file_handle["external_field"] = field

