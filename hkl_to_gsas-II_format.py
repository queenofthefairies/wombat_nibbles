""" This script takes a .hkl file output from Int3D and makes a new file that
is an acceptable format for GSAS-II 

the formatting is based on the class 
hb3a_INT_ReaderClass(G2obj.ImportStructFactor) in the GSAS-II developer
documentation """

import numpy as np

filename = 'y2sio5_int3d_strong.hkl'

new_file_lines = []
with open(filename,'r') as fp:
    for line,S in enumerate(fp):
        if S[0] == '#': continue       #ignore comments, if any
        data = S.split()
        h,k,l,Fo,sigFo = data[:5]                  
        h,k,l = [int(float(h)),int(float(k)),int(float(l))]
        if not any([h,k,l]):
            break
        Fo = float(Fo)
        sigFo = float(sigFo)
        new_file_line = [h,k,l,Fo,sigFo]
        new_file_lines.append(new_file_line)


# Define format: 10 characters for first col, 5 for second
fmt = '%3d %3d %3d %12d %12d' 
data = np.array(new_file_lines, dtype=object)

np.savetxt(filename[:-4]+'_gsas-II.hkl', data, 
           header = 'h    k   l   Fosq    sigFosq', fmt=fmt)