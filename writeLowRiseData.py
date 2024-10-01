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

geometric_scale = 1.0/100.0
air_density = 1.225
data_type = "CFD"
length_unit = "m"
time_unit = "sec"
roughness_length = 0.5
power_law_alpha = 0.2
exposure_type = "Suburban"
duration = 18.0
time_step = 0.002
sampling_rate = 1.0/time_step
wind_speed = 7.54
building_type = "lowRise"

bldg_width = np.array([16.0, 16.0, 16.0])
bldg_depth = np.array([24.0, 24.0, 24.0])
bldg_height = np.array([8.0, 12.0, 12.0])

roof_types = ["gable_roof", "flat_roof", "hip_roof"]
roof_type_names = ["G", "F", "H"]

roof_slopes = np.array([21.8, 0.0, 45.0])
roof_slope_names = ['22', '0', '45']

wind_directions = np.array([0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0])
# wind_direction_names = ['0', '15', '30', '45', '60', '75', '90']

n_wind_dxns = len(wind_directions)
n_bldg_type = len(roof_types)



for roofi in range(n_bldg_type):    
    for dxni in range(n_wind_dxns):
        
        data = adb.WindLoadData(data_type=data_type)
        
        data.building_type = building_type
        data.scale = geometric_scale
        data.air_density = air_density
        data.roughness_length = roughness_length    
        data.power_law_alpha = power_law_alpha
        data.exposure_type = exposure_type    
        data.wind_speed = wind_speed    
        data.duration = duration
        data.sampling_rate = sampling_rate
        
        data.length_unit = length_unit
        data.time_unit = time_unit
    
        data.width = bldg_width[roofi]
        data.depth = bldg_depth[roofi]
        data.height = bldg_height[roofi]
        data.roof_type = roof_types[roofi]
        data.roof_slope = roof_slopes[roofi]
    
        data.wind_direction = wind_directions[dxni]
        
        
        cp_file_name = "rawData\\LES_LowRiseCp\\lesCp{}{:d}.csv".format(roof_type_names[roofi], int(wind_directions[dxni]))
        tap_file_name = "rawData\\LES_LowRiseCp\\tapLoc{}{:d}.csv".format(roof_type_names[roofi], int(wind_directions[dxni]))
        
        data.read_csv_data(cp_file_name=cp_file_name, tap_file_name=tap_file_name)


        case_name = '{}_{}_HW{:.2f}_WD{:.2f}_A{:.0f}_R{:.2f}_{}_S{}'.format(data.building_type, 
                                                                     data.data_type, 
                                                                     data.height_to_width, 
                                                                     data.width_to_depth, 
                                                                     data.wind_direction, 
                                                                     data.roughness_length, 
                                                                     roof_type_names[roofi], 
                                                                     roof_slope_names[roofi])

        data.file_name = case_name
        
        #Write the general info file
        data.write_to_json_general_info('processedData/' + case_name)
        
        #Damp all the data
        data.write_to_json_all('processedData/' + case_name)
