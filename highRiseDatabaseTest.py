# -*- coding: utf-8 -*-
"""
Original code: fmk 
Modficiation for CFD data: Abiy

This is a temporary script file.
"""
# python code to read TPU .mat file and store 
# data into a SimCenter JSON file

import sys
import os
import subprocess
import json
import stat
import shutil
import numpy as np
import scipy.io as sio
from pprint import pprint
import aerodynamicDatabaseLib as db

scale = 1/400.0
air_density = 1.225
exposure_name = "Open"
z0 = 0.03
data_type = "CFD"
length_unit = 'm'
time_unit = 'sec'


data = db.HighRiseData(data_type=data_type)

data.scale = scale
data.exposure_name = exposure_name
data.air_density = air_density
data.roughness_length = z0
data.length_unit = length_unit
data.time_unit = time_unit


data.read_matlab_file('data/fine_1049_nominal')   


height_to_width = 1.5
width_to_depth = 2.0
wind_direction = 90.0
roughness_length = 0.03

# wind.find_high_rise_data(data_type, height_to_width, width_to_depth, wind_direction, roughness_length)


# jsonstr1 = json.dumps(data.__dict__)
  
# # print created JSON objects
# print(jsonstr1)

data.write_to_json_general_info('data/output')

# if __name__ == '__main__':    
#     data.read_matlab_file('../databaseRaw/fine_1049_nominal')   
#     data.write_to_json('data/output')


