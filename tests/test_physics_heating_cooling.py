"""

test_physics_rates.py

Author: Jordan Mirocha
Affiliation: University of Colorado at Boulder
Created on: Sun Apr 13 16:38:44 MDT 2014

Description: 

"""

import ares, sys
import numpy as np
import matplotlib.pyplot as pl

def test():
    species = 0
    dims = 32
    T = np.logspace(3.5, 6, 500)
    
    fig1, ax1 = pl.subplots(1, 1, num=1)
    fig2, ax2 = pl.subplots(1, 1, num=2)

    colors = list('kb')
    for i, src in enumerate(['fk94']):
    
        # Initialize grid object
        grid = ares.static.Grid(grid_cells=dims)
        
        # Set initial conditions
        grid.set_physics(isothermal=True)
        grid.set_chemistry()
        grid.set_density(1)
        grid.set_ionization(x=[1. - 1e-8, 1e-8])
        grid.set_temperature(T)
    
        coeff = coeffB = ares.physics.RateCoefficients(grid=grid, rate_src=src, T=T)
        coeffA = ares.physics.RateCoefficients(grid=grid, rate_src=src, T=T,
            recombination='A')
        
        # First: collisional ionization, recombination
        CI = [coeff.CollisionalIonizationRate(species, TT) for TT in T]
        RRB = [coeff.RadiativeRecombinationRate(species, TT) for TT in T]
        RRA = [coeffA.RadiativeRecombinationRate(species, TT) for TT in T]
        
        if i == 0:
            labels = [r'$\beta$', r'$\alpha_{\mathrm{B}}$', 
                r'$\alpha_{\mathrm{A}}$']
        else:
            labels = [None] * 2
        
        ax1.loglog(T, CI, color=colors[i], ls='-', label=labels[0])
        ax1.loglog(T, RRB, color=colors[i], ls='--', label=labels[1])
        ax1.loglog(T, RRA, color=colors[i], ls=':', label=labels[2])
        
        # Second: Cooling processes
        CIC = [coeff.CollisionalIonizationCoolingRate(species, TT) for TT in T]
        CEC = [coeff.CollisionalExcitationCoolingRate(species, TT) for TT in T]
        RRC = [coeff.RecombinationCoolingRate(species, TT) for TT in T]
    
        if i == 0:
            labels = [r'$\zeta$', r'$\psi$', r'$\eta$']
        else:
            labels = [None] * 3
    
        ax2.loglog(T, CIC, color=colors[i], ls='-', label=labels[0])
        ax2.loglog(T, CEC, color=colors[i], ls='--', label=labels[1])
        ax2.loglog(T, RRC, color=colors[i], ls=':', label=labels[2])

    ax1.set_ylim(1e-18, 1e-7)
    ax1.legend(loc='upper left')  
    ax2.legend(loc='lower right')  
    ax1.set_xlabel(r'Temperature $(\mathrm{K})$')
    ax1.set_ylabel(r'Rate $(\mathrm{cm}^{3} \ \mathrm{s}^{-1})$')
    ax2.set_xlabel(r'Temperature $(\mathrm{K})$')
    ax2.set_ylabel(r'Rate $(\mathrm{erg} \ \mathrm{cm}^{3} \ \mathrm{s}^{-1})$')
    pl.show()
    
    assert True
    
if __name__ == '__main__':
    test()
    
        
