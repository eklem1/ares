"""

generate_hmf_tables.py

Author: Jordan Mirocha
Affiliation: University of Colorado at Boulder
Created on: Wed May  8 11:33:48 2013

Description: Create lookup tables for collapsed fraction. Can be run in 
parallel, e.g.,

    mpirun -np 4 python generate_hmf_tables.py

"""

import os, ares

## INPUT
fit = 'ST'
format = 'pkl'
##


hmf_pars = \
{
 "fitting_function": fit,
 "hmf_dlogM": 0.01
}
##

hmf = ares.populations.HaloMassFunction.HaloDensity(hmf_analytic=False, 
    load_hmf=False, **hmf_pars)

hmf.save(format=format)

