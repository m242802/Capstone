import numpy as np
from glasstone.utilities import convert_units

def UOP(Y,r,h,D_w,yunits='kT', dunits='m'):
    r=convert_units(r,dunits,'kilofeet')
    r=r*1000
    h=convert_units(h,dunits,'kilofeet')
    h=h*1000
    D_w=convert_units(h,dunits,'kilofeet')
    D_w*1000
    R_s=(r**2+h**2)**.5 #Slant range to the surface
    R_b=(r**2+(2*D_w-h)**2)**.5
    return 4.380e6*(Y**(1/3)/R_s)**1.13+5.7e10*(Y**(1/3)/R_s)**3.7