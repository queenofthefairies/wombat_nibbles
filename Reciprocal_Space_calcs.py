
import sys
import numpy as np

# Add DerApproximator to path for openopt compatibility
sys.path.append('J:/wombat_instrument_work/scattering_plane_software/OOSuite/DerApproximator')
# Add openopt to path for openopt compatibility
sys.path.append('J:/wombat_instrument_work/scattering_plane_software/OOSuite/OpenOpt/openopt')
sys.path.append('J:/wombat_instrument_work/scattering_plane_software/OOSuite/OpenOpt')

# Add UBmatrix to path
sys.path.append('J:/wombat_instrument_work/scattering_plane_software/ubmatrix')

# Add wombat_scattering_plane to path
sys.path.append('J:/wombat_instrument_work/scattering_plane_software/siobhan_scattering_plane')


#import oo as openopt
#from openopt import NLSP
from oo import NLSP
import ubmatrix

import wombat_scattering_plane 


# sample name
sample_name_prefix = 'in-kapellasite'

# Unit cell params for clinoatacamite
unit_cell_params = [11.324, 11.324, 6.035, 90.00, 90.00, 120.00]
wavelength = 2.41 # in Angstrom
# UB matrix found with Int3D
#UB_matrix = np.array([[-0.04263322800398, 0.13622714579105, 0.02506458014250],
#                      [0.15944631397724, 0.03636400774121, 0.02596857771277],
#                      [0.00023406882246, 0.04140481352806, -0.10527275502682]])

# calculate star (a.k.a. reciprocal lattice params)
star = ubmatrix.star(*unit_cell_params)
star = dict(zip(('astar','bstar','cstar','alphastar','betastar','gammastar'),
                star))
print('star')
print(star)

# calculate B matrix
#B_matrix = ubmatrix.calcB(star['astar'],star['astar'],star['astar'],
#                          star['alphastar'],star['betastar'],star['gammastar'],
#                          unit_cell_params[2], unit_cell_params[3])

# calculate 2theta of reflections 
hkl_list = [[0.125, 0.25, 0.25],
            [0.25, 0.5, 0.5],
            [1,0,0],
            [1,1,0],
            [1,1,1],
            [1.125, 1.25, 1.25]
            ]

for hkl in hkl_list:
    print('hkl: ({0}, {1}, {2})   2theta: {3:.2f} deg'.format(hkl[0],hkl[1],hkl[2],ubmatrix.calcTwoTheta(hkl, star, wavelength)))
#print(ubmatrix.calcTwoTheta(hkl, star, wavelength))