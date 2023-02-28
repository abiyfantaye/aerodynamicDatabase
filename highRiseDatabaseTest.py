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
import aerodynamicDatabaseLib as adb

bldg_type = "HR"
scale = 1/400.0
air_density = 1.225
data_type = "CFD"
length_unit = "m"
time_unit = "sec"
roughness_length = 0.03


#Reading and writing data from Prof. Gorle
data = adb.HighRiseData(data_type=data_type)
data.scale = scale
data.air_density = air_density
data.roughness_length = roughness_length
data.length_unit = length_unit
data.time_unit = time_unit


#Read and write for Open exposure type
data.exposure_type = "Open"
data.read_matlab_file('../rawData/fine_1049_nominal')   
case_name = '{}_{}_{:.2f}_{:.2f}_{:.2f}_{:.3f}'.format(bldg_type, data_type, data.height_to_width, data.width_to_depth, data.wind_direction, data.roughness_length)

data.file_name = case_name
data.write_to_json_general_info('../processedData/' + case_name)


# #Read and write for Flat exposure type
# data.exposure_type = "Flat"
# data.read_matlab_file('../rawData/fine_0625_nominal')  
# case_name = '{}_{}_{:.2f}_{:.2f}_{:.2f}_{:.3f}'.format(bldg_type, data_type, data.height_to_width, data.width_to_depth, data.wind_direction, data.roughness_length)

# data.file_name = case_name
# data.write_to_json_general_info('../processedData/' + case_name)


# adb.find_high_rise_data(data_type, height_to_width, width_to_depth, wind_direction, roughness_length)

# if __name__ == '__main__':    
#     data.read_matlab_file('../databaseRaw/fine_1049_nominal')   
#     data.write_to_json('data/output')


