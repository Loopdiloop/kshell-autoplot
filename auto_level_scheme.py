import numpy as np 
import matplotlib.pyplot as plt 
import sys

""" 
Version 1.0
This is a program made to automatically plot the level scheme 
of a nuclei from a summary file from the kshell simulation.

For Linux:
To use it you make sure this file and the summary file 
is located in the same folder. You then change the parameters 
at the top, including the filename and number of levels.
Then, in the command line, go to your directory and type:
$ python auto_level_scheme.py

For now it can only handle level scheme, but not transitions.
This will probably be added later.

Please send me suggestions for improvements or 
questions at mamoll@uio.no (or just ask me).

Enjoy! -Marianne

"""


summary_filename = "summary_Cr54.txt"
nuclei_name = "$^{54}$Cr"
#How many excitation states are there?
number_of_states = 25

# Do you want the energies and spin/parity to be written in the diagram?
# True/False
write_energies = True

# Ignore some specific states?. 
#  N-values in a list or [0] = none
ignore_states = [0]

# Split into bands? True/False
split_bands = True
# If you chose to split the bands, how do you want to split them?
#  0 = N_Jp
#  list of bands for N-levels
#   eg. state 1 in band 1
#       state 2 in band 3
#       state 3 in band 5 
#       -> split_bands_method = [1, 3, 5]
#       (List needs to be the same length as the number of states!)
split_bands_method = 0

#Autoremove is same energy?
#Shuffle in the not-same energies? 
#I.e the 3rd two plus state should be in the second band.

class level_scheme(): 
    def __init__(self, filenames):
        """ Initializes the class and defines the filename. """
        self.filenames = filenames
        return None

    def load(self, number_of_states, ignore_states): 
        """ Loads the data from the file and ignores the states 
            you don't want, for example overlapping states."""
        datafile = open(self.filenames, 'r')
        N = [] ; J2 = []; prty = [] ; N_Jp =[] ; T = [] ; E = [] ; Ex = [] ; log_file = []
        for i in range(5):
            datafile.readline()
        for j in range(number_of_states):
            line = (datafile.readline().split())
            if j+1 not in ignore_states:
                N.append(float(line[0]))
                J2.append(int(line[1])) 
                prty.append(line[2]) 
                N_Jp.append(float(line[3]))  
                T.append(int(line[4]))
                E.append(float(line[5]))
                Ex.append(float(line[6]))
                log_file.append(line[7])
        self.N = N ; self.J2 = J2 ; self.prty = prty
        self.N_Jp = N_Jp ; self.T = T ; self.E = E 
        self.Ex = Ex ; self.log_file = log_file
        self.split_bands_parameters = list(np.ones(len(Ex)))
        return None

    def split_bands(self, split_bands_method):
        """ Here the bands are split according to preferences.
            You probably don't need tochange anything here. """
        if split_bands_method == 0:
            self.split_bands_parameters = self.N_Jp
        elif type(split_bands_method) == list:
            self.split_bands_parameters = split_bands_method
        else: 
            raise SyntaxWarning("Error! Split band parameters should be 0 or a list. Not a %s"%type(split_bands_method))
        return None
        
    def plot(self, nuclei_name):
        """ Initialize and make the plot. 
            Here you can change colors, thickness and length of the levels, 
            as well as the labels and axes."""
        print len(self.Ex)
        print self.Ex
        plt.plot(self.split_bands_parameters, self.Ex, '_', color = 'black', markersize=90, lw=80) #lw?
        plt.xlabel(nuclei_name, size='18')
        plt.ylabel('Excitation energy [MeV]', size='18')
        plt.xticks([])
        plt.xlim(0, max(self.split_bands_parameters)+1)
        plt.ylim(min(self.Ex)-0.1, max(self.Ex)+0.3)
        return None

    def write_energies(self):
        """ Adds energies, parities and spins to the level schemes. 
            If you want to edit the exact positions of the text, 
            this is the place to be. """
        for k in range(len(self.Ex)): #Adds the exitation energies as numbers
            if abs(float(self.J2[k])%2) < 0.1:
                spin_parity = str(int(self.J2[k]/2))+str(self.prty[k])
            else: #if 2J is odd, half spin
                spin_parity = str(self.J2[k])+"/2"+str(self.prty[k])
            #Here you can change the placements of the Ex text: (X,Y)
            plt.text(self.split_bands_parameters[k]+0.22, self.Ex[k]+0.03, str(self.Ex[k]), fontsize=13)
            #Here you can change the placements of the spin/parity: (X,Y)
            plt.text(self.split_bands_parameters[k]-0.4, self.Ex[k]+0.03, spin_parity , fontsize=13)
        return None
    
    def show(self):
        """ Shows plot. """
        plt.show()
        return None



# Make an instance with the correct filename
scheme = level_scheme(summary_filename)

# Load the data, ignore what you don't need.
scheme.load(number_of_states, ignore_states)

# Split the bands if you want to.s
if split_bands == True:
    scheme.split_bands(split_bands_method)

# Make the plot and add the nuclei name to the x-axis
scheme.plot(nuclei_name)

# Adds energies, spins and parities. 
if write_energies == True:
    scheme.write_energies()
    
# Show plot.
scheme.show()
