# main.py
# David Li
# The main program used for any data reading.
# Uses the two classes (Data and Dataset) in data.py.

from data import *
import os

#path = raw_input('Please enter the folder/path where your data is stored: ').strip()
option = input('Please enter the option name: ').strip().upper()
#myData = Dataset('/Users/David/Desktop/Options', option) #IMPORTANT: Change the first argument to be whatever folder the data files are in
datafile = open('dataTable.txt', 'w')
datafile.write(myData.__str__())
datafile.close()
print(myData)
myData.plotData()