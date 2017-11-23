# takes all 'datasetn.h5' and renames them 'datasetn+i.h5' where n is original
# number and i is how much you want to shift it up by

import numpy as np
import h5py
from os import walk
import os

directory = '/home/mpcr/Desktop/rodrigo/deepcontrol/'

directory = directory + raw_input("Input folder path (from /deepcontrol): ")

if not os.path.isdir(directory + '/renamed/'):
    os.makedirs(directory + '/renamed/')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

data_files = []

# Get all filenames of datasets into a list
for (dirpath, dirnames, filenames) in walk(directory):
    data_files.extend(filenames)
    break
# Extract the dataset numbers
for i in range(len(data_files)):
    if is_number(data_files[i][9]):
        data_files[i] = int(data_files[i][7] + data_files[i][8] + data_files[i][9])
    elif is_number(data_files[i][8]):
        data_files[i] = int(data_files[i][7] + data_files[i][8])
    else:
        data_files[i] = int(data_files[i][7])
data_files.sort()

print(data_files)

num_shift = int(raw_input("How much do you want to shift the file numbers by? "))
os.chdir(directory)
for set_num in range(len(data_files)):
    old_name = "dataset" + str(data_files[set_num]) + ".h5"
    new_name = "dataset" + str(data_files[set_num]+num_shift) + ".h5"
    print("Renaming " + old_name + " to " + new_name)
    os.rename(old_name, directory + "/renamed/" + new_name)
