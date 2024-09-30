# -*- coding: utf-8 -*-
"""
Original code: fmk 
Modification for CFD data: Abiy

This is a temporary script file for writing the data
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

bldg_type = "highRise"
roof_type = "flat"
roof_slope = 0.0
scale = 1.0/400.0
air_density = 1.225
data_type = "EXP"
length_unit = "m"
time_unit = "sec"
roughness_length = 0.03
power_law_alpha = 1.0/6.0


#Reading and writing data from TPU database
data = adb.WindLoadData(data_type=data_type)
data.building_type = bldg_type
data.scale = scale
data.air_density = air_density
data.roughness_length = roughness_length
data.length_unit = length_unit
data.time_unit = time_unit
data.power_law_alpha = power_law_alpha
data.exposure_type = "Open"
data.roof_type = roof_type
data.roof_slope = roof_slope


#Read and write for Open exposure type
data.read_matlab_file('rawData/T114_6_000_1.mat')   
case_name = '{}_{}_{:.2f}_{:.2f}_{:.2f}_{:.3f}'.format(bldg_type, data_type, data.height_to_width, data.width_to_depth, data.wind_direction, data.roughness_length)

data.file_name = case_name

#Write the general info file
data.write_to_json_general_info('processedData/' + case_name)

#Damp all the data
data.write_to_json_all('processedData/' + case_name)
