#!/usr/bin/env python 

__version__= '1.0.0'

"""



"""

import numpy as np
import copy
import os
import sys
import re
import glob
import time

from DIA_collection import xyz_from_xyz, print_xyz, periodic_table

#Python2 compatibility
try:
	range = xrange
except NameError:
	pass

def main():
	
	XYZ = "*.xyz"
	filelist=sorted(glob.glob(XYZ))
	print(filelist)
	
	for item in filelist:
		input_structures,input_n_atoms,input_atoms,input_title=xyz_from_xyz(item)
	
		#now get the order according to x coordinate (x is column 0 in this numpy array). Using argsort for this
		# CHANGE THIS FOR SORTING ACCORDING TO y or Z axis! [0][:,1] for y and [0][:,2] for z
		new_order= np.argsort(input_structures[0][:,0])
	
		#now sort atoms and atom types
		output_atoms = np.array(input_atoms)[new_order[::-1]]
		output_structure = input_structures[0][new_order[::-1]]
	
		# now write to file
		output_file = open(item.split('.')[0]+"_sorted.xyz", 'w')
		print_xyz(output_structure, output_atoms, output_file, input_title[0])
		output_file.close()
		
	
if __name__ == "__main__":
	main()