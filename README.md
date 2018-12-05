# Autoplot-for-kshell

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


v1.1 update:
-   A few bugs were removed.
-   Levels with exact same energy can now be automatically removed.
-   Plotting of levels for multiple nuclei. Add all values as usual, but as lists.
    e.g. number_of_states = [20, 14]
    this means 20 states from the first file, 14 for the last.
    For a single nuclei, all values can be added as numbers or True/False unless
    something else is stated.
    
Please send me suggestions for improvements or 
questions at mamoll@uio.no (or just ask me).

Enjoy! -Marianne

