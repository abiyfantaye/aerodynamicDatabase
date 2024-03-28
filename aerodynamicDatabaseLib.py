"""
A python code to store and process aerodynamic data (pressure time-series) on
buildings. The data is written to SimCenter's JSON format. Can be used with 
any type of data including experimental, CFD and field measurements.  

Also, in the future will implements functions for post-processing of mean and 
peak loads and responses of the building.
"""

import sys
import os
import subprocess
import json
import stat
import shutil
import numpy as np
import scipy.io as sio
from pprint import pprint


# A function to search a case from the aerodynamic database given the path of
# the directory containing the json files.  
def find_high_rise_data(json_path, data_type, height_to_width, width_to_depth, wind_direction, roughness_length):
    
    bldg_type = 'HR' # High rise building 
    
    #File naming convention
    case_name = '{}_{}_{:.2f}_{:.2f}_{:.2f}_{:.3f}'.format(bldg_type, data_type, height_to_width, width_to_depth, wind_direction, roughness_length)
   
    if os.path.isfile(json_path + '/' + case_name + '_info'):
        return json_path + '/' + case_name
    else:
        print("Case can not be found in the aerodynamic database")
        return None
    
class WindLoadData:
    def __init__(self, data_type='CFD'):
        self.data_type = data_type
        self.air_density = 1.225
        self.length_unit = "m"
        self.time_unit = "sec"
        self.wind_direction = 0.0

    #Properties - getters and setters 
    @property
    def building_type(self):
        return self._building_type

    @building_type.setter
    def building_type(self, value):
        self._building_type = value
        
    @property
    def roof_type(self):
        return self._roof_type

    @roof_type.setter
    def roof_type(self, value):
        self._roof_type = value

    @property
    def roof_slope(self):
        return self._roof_slope

    @roof_slope.setter
    def roof_slope(self, value):
        self._roof_slope = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    @property
    def height_to_width(self):
        return self._height_to_width

    @height_to_width.setter
    def height_to_width(self, value):
        self._height_to_width = value
        
    @property
    def width_to_depth(self):
        return self._width_to_depth

    @width_to_depth.setter
    def width_to_depth(self, value):
        self._width_to_depth = value

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        
    @property
    def tap_coordinates (self):
        return self._tap_coordinates
    
    @tap_coordinates .setter
    def tap_coordinates(self, value):
        self._tap_coordinates = value
        
    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def sampling_rate(self):
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, value):
        self._sampling_rate = value
        
    @property
    def air_density(self):
        return self.air_density

    @air_density.setter
    def air_density(self, value):
        self._air_density = value
        
    @property
    def wind_speed(self):
        return self._wind_speed

    @wind_speed.setter
    def wind_speed(self, value):
        self._wind_speed = value

    @property
    def wind_direction(self):
        return self._wind_direction

    @wind_direction.setter
    def wind_direction(self, value):
        self._wind_direction = value

    @property
    def exposure_type(self):
        return self._exposure_type

    @exposure_type.setter
    def exposure_type(self, value):
        self._exposure_type = value
        
    @property
    def roughness_length(self):
        return self._roughness_length

    @roughness_length.setter
    def roughness_length(self, value):
        self._roughness_length = value

    @property
    def power_law_alpha(self):
        return self._power_law_alpha

    @power_law_alpha.setter
    def power_law_alpha(self, value):
        self._power_law_alpha = value
        
    @property
    def length_unit(self):
        return self._length_unit

    @length_unit.setter
    def length_unit(self, value):
        self._length_unit = value

    @property
    def time_unit(self):
        return self._time_unit

    @time_unit.setter
    def time_unit(self, value):
        self._time_unit = value
        
    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        self._data_type = value
        
    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value
        
    @property
    def pressure_coefficients(self):
        return self._pressure_coefficients

    @pressure_coefficients.setter
    def pressure_coefficients(self, value):
        self._pressure_coefficients = value        
    
    ### Functions 
    def write_to_json_general_info(self, fine_name):
        file = open(fine_name + '_info.json' ,"w")
        file.write("{\n")
        file.write("\"buildingType\":\"%s\",\n" % self.building_type)      
        file.write("\"roofType\":\"%s\",\n" % self.roof_type)      
        file.write("\"roofSlope\":%f,\n" % self.roof_slope)      
        file.write("\"windSpeed\":%f,\n" % self.wind_speed)      
        file.write("\"width\":%f,\n" % self.width)
        file.write("\"depth\":%f,\n" % self.depth)
        file.write("\"height\":%f,\n" % self.height)
        file.write("\"heightToWidth\":%f,\n" % self.height_to_width)
        file.write("\"widthToDepth\":%f,\n" % self.width_to_depth)
        file.write("\"duration\":%f,\n" % self.duration)
        file.write("\"timeUnit\":\"%s\",\n" % self.time_unit)
        file.write("\"lengthUnit\":\"%s\",\n" % self.length_unit)
        file.write("\"samplingRate\":%f,\n" % self.sampling_rate)
        file.write("\"windDirection\":%f,\n" % self.wind_direction);    
        file.write("\"exposureType\":\"%s\",\n" % self.exposure_type) 
        file.write("\"roughnessLength\":%f,\n" % self.roughness_length)
        file.write("\"powerLawAlpha \":%f,\n" % self.power_law_alpha)
        file.write("\"dataType\":\"%s\",\n" % self.data_type)
        file.write("\"fileName\":\"%s\"\n" % self.file_name)
        file.write("}")
        file.close()
    
    ### Functions 
    def write_to_json_all(self, fine_name):
        file = open(fine_name + '.json',"w")
        file.write("{\n")
        file.write("\"buildingType\":\"%s\",\n" % self.building_type)      
        file.write("\"roofType\":\"%s\",\n" % self.roof_type)      
        file.write("\"roofSlope\":%f,\n" % self.roof_slope) 
        file.write("\"windSpeed\":%f,\n" % self.wind_speed)       
        file.write("\"width\":%f,\n" % self.width)
        file.write("\"depth\":%f,\n" % self.depth)
        file.write("\"height\":%f,\n" % self.height)
        file.write("\"heightToWidth\":%f,\n" % self.height_to_width)
        file.write("\"widthToDepth\":%f,\n" % self.width_to_depth)
        file.write("\"duration\":%f,\n" % self.duration)
        file.write("\"timeUnit\":\"%s\",\n" % self.time_unit)
        file.write("\"lengthUnit\":\"%s\",\n" % self.length_unit)
        file.write("\"samplingRate\":%f,\n" % self.sampling_rate)
        file.write("\"windDirection\":%f,\n" % self.wind_direction)
        file.write("\"exposureType\":\"%s\",\n" % self.exposure_type) 
        file.write("\"roughnessLength\":%f,\n" % self.roughness_length)
        file.write("\"dataType\":\"%s\",\n" % self.data_type)
        file.write("\"fileName\":\"%s\",\n" % self.file_name)
        file.write("\"tapCoordinates\": [")
    
        for tapi in range(self.ntaps):
            if (tapi == self.ntaps-1):
                file.write("{\"id\":%d,\"x\":%f,\"y\":%f,\"z\":%f,\"face\":%d}]" % (self.tap_names[tapi], self.tap_coordinates[tapi,0], self.tap_coordinates[tapi,1], self.tap_coordinates[tapi,2], self.tap_faces[tapi]))
            else:
                file.write("{\"id\":%d,\"x\":%f,\"y\":%f,\"z\":%f,\"face\":%d}," % (self.tap_names[tapi], self.tap_coordinates[tapi,0], self.tap_coordinates[tapi,1], self.tap_coordinates[tapi,2], self.tap_faces[tapi]))
        
        file.write(",\"pressureCoefficients\": [");

        ntime_steps = self.pressure_coefficients.shape[0]
    
        for tapi in range(self.ntaps):
            file.write("{\"id\": %d , \"data\":[" % (tapi + 1))
            for ti in range(ntime_steps-1):
                file.write("%f," % self.pressure_coefficients[ti, tapi])
            if (tapi != self.ntaps-1):
                file.write("%f]}," % self.pressure_coefficients[ntime_steps-1, tapi])
            else:
                file.write("%f]}]" % self.pressure_coefficients[ntime_steps-1, tapi])
    
        file.write("}")
        file.close()
        
    def read_json(self, path):
        raise NotImplementedError
    
    def read_matlab_file(self, file_name):

        mat_contents = sio.loadmat(file_name)
        
        self.height =  mat_contents['Building_height'][0][0]        
        self.width =  mat_contents['Building_breadth'][0][0]
        self.depth = mat_contents['Building_depth'][0][0]

        self.duration = mat_contents['Sample_period'][0][0]
        self.sampling_rate = mat_contents['Sample_frequency'][0][0]
        
        # self.wind_direction = mat_contents['Wind_direction_angle'][0][0]
        self.wind_speed = float(mat_contents['Uh_AverageWindSpeed'][0])
    
        self.tap_locations = mat_contents['Location_of_measured_points'];
        self.ntaps = self.tap_locations.shape[1];
        self.pressure_coefficients = mat_contents['Wind_pressure_coefficients'];
        
        #Tap locations (x,y,z) in global coordinate system
        tap_xyz = np.zeros((self.ntaps, 3))
        self.tap_names = []
        self.tap_faces = []
        
        for tap in range(self.ntaps):
            xLoc = self.tap_locations[0][tap]
            yLoc = self.tap_locations[1][tap]            
            tag = self.tap_locations[2][tap]
            face = self.tap_locations[3][tap]
            
            self.tap_names.append(tag)
            self.tap_faces.append(face)
            
            tap_xyz[tap,2] = yLoc
            
            if face == 1:
                tap_xyz[tap,0] = -self.depth/2.0
                tap_xyz[tap,1] = self.width/2.0 - xLoc
                
            if face == 2:
                tap_xyz[tap,0] = -self.depth/2.0 + (xLoc - self.width)
                tap_xyz[tap,1] = -self.width/2.0
                
            if face == 3:
                tap_xyz[tap,0] = self.depth/2.0
                tap_xyz[tap,1] = -self.width/2.0 + (xLoc - self.width - self.depth)
                
            if face == 4:
                tap_xyz[tap,0] = self.depth/2.0 - (xLoc - 2*self.width - self.depth)
                tap_xyz[tap,1] = self.width/2.0
                
        self.tap_coordinates = tap_xyz
        self.height_to_width = self.height/self.width
        self.width_to_depth = self.width/self.depth