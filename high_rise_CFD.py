# -*- coding: utf-8 -*-
"""
Original code: fmk 
Modficiation for CFD data: Abiy

This is a temporary script file.
"""
# python code to open the TPU .mat file
# and put data into a SimCenter JSON file for
# wind tunnel data

import sys
import os
import subprocess
import json
import stat
import shutil
import numpy as np
import scipy.io as sio
from pprint import pprint
import windLoadData as wd

inputArgs = sys.argv

print ("Number of arguments: %d" % len(sys.argv))
print ("The arguments are: %s"  %str(sys.argv))

# set filenames
mat_file_name = sys.argv[1]
json_file_name = sys.argv[2]

dataDir = os.getcwd()
scriptDir = os.path.dirname(os.path.realpath(__file__))

scale = 1/400
air_density = 1.225
exposure = "Open"
data_type = "CFD"
units = {'Length':'m', 'Time':'s', 'Force':'N'}

data = wd.windLoadData(scale=scale, exposure=exposure, data_type=data_type,
                       air_density=air_density, units=units)


if __name__ == '__main__':
    data.read_matlab_file(mat_file_name)   
    data.write_to_json(json_file_name)

