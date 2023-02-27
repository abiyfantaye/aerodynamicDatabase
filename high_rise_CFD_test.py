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

scale = 1/400.0
air_density = 1.225
exposure_name = "Open"
z0 = 0.03
data_type = "CFD"
length_unit = 'm'
time_unit = 'sec'


data = wd.HighRiseData(data_type=data_type)

data.scale = scale
data.exposure_name = exposure_name
data.air_density = air_density
data.roughness_length = z0
data.length_unit = length_unit
data.time_unit = time_unit


data.read_matlab_file('../databaseRaw/fine_1049_nominal')   


# jsonstr1 = json.dumps(data.__dict__)
  
# # print created JSON objects
# print(jsonstr1)

data.write_to_json('data/output')

# if __name__ == '__main__':    
#     data.read_matlab_file('../databaseRaw/fine_1049_nominal')   
#     data.write_to_json('data/output')


