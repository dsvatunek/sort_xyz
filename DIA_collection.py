#!/usr/bin/env python 

import numpy as np
import copy
import os
import sys
import re

'''VARIABLES-VARIABLES-VARIABLES-VARIABLES-VARIABLES-VARIABLES-VARIABLES-VARIABLES-VARIABLES-VARIABLES-VARIABLES-VARIABLES
useful Variables
'''	

#Periodic table
periodic_table = ["","H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr",
    "Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl",
    "Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Uub","Uut","Uuq","Uup","Uuh","Uus","Uuo"]

'''USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL-USEFUL
Other useful functions
'''		
#checks if a string contains only an integer
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False	
	
'''PARSING-PARSING-PARSING-PARSING-PARSING-PARSING-PARSING-PARSING-PARSING-PARSING-PARSING-PARSING-PARSING-PARSING-PARSING
Functions for parsing comp chem input
'''	

#gets xyz structures from xyz file and provides a list of numpy arrays with xyz data of each structure, number of atoms and an atom list 
def xyz_from_xyz(file):
	n_atoms = 0
	atoms = []
	structures = []
	title = []
	file_object = open(file, 'r')
	input = (line for line in file_object) #make generator
	#search for number of atoms
	for line in input:
		if isInt(line.strip()):
			n_atoms=int(line)
			break	
	else: #exits if no line with number of atoms was found
		sys.exit('Error: No xyz coordinates found in file: ' + file)
			
	#skip one line
	title.append(next(input).strip())
	
	# now there should be n_atoms lines of coordinates WHAT IF NOT???
	for i in range(n_atoms):
		l=next(input).split()
		
		if l[0] in periodic_table:
			atoms.append(l[0]) #get atom symbol and append to atom list
		else:
			sys.exit('Error: something is wrong with the first structure in file: '+file)
		coords=[float(x) for x in l[1:]] #convert line to list of floats
		coords=np.array([coords]) #create array with coords
		try: #try append, doesn't work if XYZ doesn't exist yet
			XYZ=np.concatenate((XYZ,coords), axis=0)
		except NameError:
			XYZ=coords
				
	structures.append(XYZ) #append first structure to structures list
	del XYZ #get rid of that for the next structure
		
	#now search for more structures
	
	for line in input:
		#start extracting if atom number line is found
		try:
			if int(line.strip()) == n_atoms:
				#read one line to skip title
				title.append(next(input).strip())
				
				# now there should be n_atoms lines of coordinates WHAT IF NOT???
				for i in range(n_atoms):
					l=next(input).split()
					coords=[float(x) for x in l[1:]]
					coords=np.array([coords])
					try: #try append, doesn't work if XYZ doesn't exist yet
						XYZ=np.concatenate((XYZ,coords), axis=0)
					except NameError:
						XYZ=coords
				structures.append(XYZ)
				del XYZ
		except ValueError:
			pass
				
	return structures, n_atoms, atoms, title


'''OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT-OUTPUT
Functions for output
'''		
#appends xyz structure to file, takes numpy array for A, atoms list, opened file and title for structure
def print_xyz(A, atoms, file, title):
	
	file.write(str(len(atoms))+ "\n"+ title + "\n")
	for i in range(len(A)):
		file.write("{0:2s} {1:15.12f} {2:15.12f} {3:15.12f}\n".format(atoms[i], A[i, 0], A[i, 1], A[i, 2]))
	return