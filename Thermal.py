import numpy as np
from scipy.integrate import quad
from tabulate import tabulate
from glasstone.utilities import convert_units, ValueOutsideGraphError

def Thermal_Fluence(Y,r,h,f,yunits='kT', dunits='m',opunits='cal/cm^2'):
    rg=convert_units(r,dunits,'kilofeet')
    zb=convert_units(h,dunits,'kilofeet')
    t=.6           
    D = ((rg**2)+(zb**2))**.5
    return (85.6*f*Y*t)/(D**2);