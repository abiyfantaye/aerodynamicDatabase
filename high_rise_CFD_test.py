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

scale = 1/400
air_density = 1.225
exposure_type = "Open"
data_type = "CFD"
units = {'Length':'m', 'Time':'s', 'Force':'N'}
nstory = 10

data = wd.HighRiseData(scale=scale, exposure_type=exposure_type, data_type=data_type,
                       air_density=air_density, nstory=nstory, units=units)

data.read_matlab_file('../databaseRaw/fine_1049_nominal')   


# jsonstr1 = json.dumps(data.__dict__)
  
# # print created JSON objects
# print(jsonstr1)

data.write_to_json('data/output')

# if __name__ == '__main__':    
#     data.read_matlab_file('../databaseRaw/fine_1049_nominal')   
#     data.write_to_json('data/output')


