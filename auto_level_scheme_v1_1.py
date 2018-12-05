import numpy as np 
import matplotlib.pyplot as plt 
import sys

""" 
Version 1.1
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

For a single nuclei, all values can be added as numbers or True/False unless
something else is stated. For more than one nuclei add the different 
values for the nuclei in a list. (See update for v1.1)

v1.1 update:
-   A few bugs were removed.
-   Levels with exact same energy can now be automatically removed.
-   Plotting of levels for multiple nuclei. Add all values as usual, but as lists.
    e.g. number_of_states = [20, 14]
    this means 20 states from the first file, 14 for the last.


Please send me suggestions for improvements or 
questions at mamoll@uio.no (or just ask me).

Enjoy! -Marianne


"""

#How many nuclei do you want to plot?
number_of_nuclei_to_plot = 2
# If more than one:
share_yaxis = True

summary_filename = ["summary_Cr54.txt", "summary_Ca43.txt"]
nuclei_name = ["$^{54}$Cr", "$^{43}$Ca"]
#How many excitation states do you want to plot?
number_of_states = [5, 5]

'''# Are there also transition probabilities given?
transition_probabilities = False #NOT A FEATURE YET'''

# Do you want the energies and spin/parity to be written in the diagram?
# True/False
write_energies = [True, True]

# Automatically ignore double states with same energy?
remove_double_states = [True, True]

# Ignore some specific states?. 
#  N-values in a list or [0] = none
ignore_states = [[0],[0]]

# Split into bands? True/False
split_bands = [True, True]
# If you chose to split the bands, how do you want to split them?
#  0 = N_Jp
#  list of bands for N-levels
#   eg. state 1 in band 1
#       state 2 in band 3
#       state 3 in band 5 
#       -> split_bands_method = [1, 3, 5]
#       (List needs to be the same length as the number of states!)
split_bands_method = [[2,4,4,5,3], [1,1,2,2,1]]





class level_scheme(): 
    def __init__(self, number_of_nuclei_to_plot, share_yaxis):
        """ Initializes the class and defines the filename. """
        self.number_of_nuclei_to_plot = number_of_nuclei_to_plot
        self.share_yaxis = share_yaxis
        self.plot_number = 0
        return None

    def load(self, filename, number_of_states, ignore_states): 
        """ Loads the data from the file and ignores the states 
            you don't want, for example overlapping states."""
        self.filename = filename
        datafile = open(self.filename, 'r')
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

        self.mask = np.zeros(len(self.Ex))

        return None
    
    def autoremove_double_states(self):
        Ex = np.array(self.Ex)
        for l in range(len(self.Ex)-1):
            if abs(Ex[l]-Ex[l+1]) < 0.00001:
                self.mask[l+1] = 1
        mask_arg = np.copy(np.nonzero(self.mask))
        for k in np.flip(mask_arg, 1)[0]:
            k = int(k)
            del self.N[k] ; del self.J2[k] ; del self.prty[k]
            del self.N_Jp[k] ; del self.T[k] ; del self.E[k] 
            del self.Ex[k] ; del self.log_file[k]
            del self.split_bands_parameters[k]
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
        self.plot_number += 1
        plt.subplot(1, self.number_of_nuclei_to_plot, self.plot_number)
        plt.plot(self.split_bands_parameters, self.Ex, '_', color = 'black', markersize=90)
        # Fixing axes: 
        plt.xlabel(nuclei_name, size='18')
        plt.xticks([])
        plt.xlim(0.2, max(self.split_bands_parameters)+1)
        if self.plot_number < 2:
            plt.ylabel('Excitation energy [MeV]', size='18')
            self.yaxes = [min(self.Ex)-0.1, max(self.Ex)+0.5]
            plt.subplots_adjust(wspace=0.0)
        else: 
            plt.yticks([])
        if self.share_yaxis != True:
            plt.ylim(min(self.Ex)-0.1, max(self.Ex)+0.5)
        if max(self.Ex)+0.3 > self.yaxes[1]:
            self.yaxes = [min(self.Ex)-0.1, max(self.Ex)+0.5]
        plt.ylim(self.yaxes)
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


""" This last part takes all of your input and runs the class.
    Usually does not need any changing. """


# Check that everything is in the right form.

if type(summary_filename) != list:
    summary_filename = [summary_filename]
if type(nuclei_name) != list:
    nuclei_name = [nuclei_name]
if type(number_of_states) != list:
    number_of_states = [number_of_states]
if type(write_energies) != list:
    write_energies = [write_energies]
if type(remove_double_states) != list:
    remove_double_states = [remove_double_states]
if type(ignore_states) != list:
    ignore_states = [ignore_states]
if type(split_bands) != list:
    split_bands = [split_bands]


# Make an instance with the correct filenames

scheme = level_scheme(number_of_nuclei_to_plot, share_yaxis)

for i in range(number_of_nuclei_to_plot):
    # Load the data, ignore what you don't need.
    scheme.load(summary_filename[i], number_of_states[i], ignore_states[i])
    # Split the bands if you want to.
    if split_bands[i] == True:
        scheme.split_bands(split_bands_method[i])
    #Autoremove doubles states?
    if remove_double_states[i] == True:
        scheme.autoremove_double_states()
    # Make the plot and add the nuclei name to the x-axis
    scheme.plot(nuclei_name[i])
    # Adds energies, spins and parities. 
    if write_energies[i] == True:
        scheme.write_energies()

# Show plot
scheme.show()

