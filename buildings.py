"""
A python code to store and process aerodynamic data (pressure time-series) on
buildings. Can be used with experimental or CFD data.  

Finally, the data is written to JSON format for further analysis. 

Also, implements functions for post-processing of mean and peak loads and 
responses on the building.
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

class windLoadData:
    def __init__(self, scale, exposure, data_type, air_density, units):
        
    # def __init__(self, height, width, depth, scale, 
    #              tap_locations, duration, sampling_frequency, 
    #              air_density, wind_speed, wind_direction,  
    #              exposure, data_type, units):
        self.scale = scale
        self.air_density = air_density
        self.exposure = exposure
        self.data_type = data_type
        self.units = units

    #Properties - getters and setters 
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
    def sampling_frequency(self):
        return self._sampling_frequency

    @sampling_frequency.setter
    def sampling_frequency(self, value):
        self._sampling_frequency = value
        
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
    def exposure_name(self):
        return self._exposure_name

    @exposure_name.setter
    def exposure_name(self, value):
        self._exposure_name = value
        
    @property
    def roughness_length(self):
        return self._roughness_length

    @roughness_length.setter
    def roughness_length(self, value):
        self._roughness_length = value
        
    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units = value
        
    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        self._data_type = value
        
    @property
    def pressure_coeffeints(self):
        return self._pressure_coeffeints

    @pressure_coeffeints.setter
    def pressure_coeffeints(self, value):
        self._pressure_coeffeints = value
        

class HighRiseData(windLoadData):
    def __init__(self, nstory):
        self.nstory = nstory
    
    ### Functions 
    def write_to_json_general_info(self, fine_name):
        file = open(fine_name,"w")
        file.write("{\n")
        file.write("\"windSpeed\":%f," % self.wind_speed)      
        file.write("\"width\":%f," % self.width)
        file.write("\"depth\":%f," % self.depth)
        file.write("\"height\":%f," % self.height)
        file.write("\"heightToWidth\":%f," % self.height_to_width)
        file.write("\"widthToDepth\":%f," % self.width_to_depth)
        file.write("\"duration\":%f," % self.duration)
        file.write("\"units\":{\"length\":\"m\",\"time\":\"sec\"},")
        file.write("\"samplingFrequency\":%f," % self.sampling_frequency)
        file.write("\"windDirection\":%f," % self.wind_direction);    
        file.write("\"exposureName\":%f," % self.exposure_name) 
        file.write("\"roughnessLength\":%f," % self.roughness_length)
        file.write("}")
        file.close()
    
    ### Functions 
    def write_to_json_all(self, fine_name):
        file = open(fine_name,"w")
        file.write("{\n")
    
        file.write("\"windSpeed\":%f," % self.wind_speed)       
        file.write("\"width\":%f," % self.width)
        file.write("\"depth\":%f," % self.depth)
        file.write("\"height\":%f," % self.height)
        file.write("\"heightToWidth\":%f," % self.height_to_width)
        file.write("\"widthToDepth\":%f," % self.width_to_depth)
        file.write("\"duration\":%f," % self.duration)
        file.write("\"units\":{\"length\":\"m\",\"time\":\"sec\"},")
        file.write("\"samplingFrequency\":%f," % self.sampling_frequency)
        file.write("\"windDirection\":%f," % self.wind_direction)
        file.write("\"exposureName\":%f," % self.exposure_name) 
        file.write("\"roughnessLength\":%f," % self.roughness_length)
        file.write("\"tapCoordinates\": [")
    
        for tapi in range(self.ntaps):
            if (tapi == self.ntaps-1):
                file.write("{\"id\":%d,\"x\":%f,\"y\":%f,\"z\":%f,\"face\":%d}]" % (self.tap_names[tapi], self.tap_coordinates[tapi,0], self.tap_coordinates[tapi,1], self.tap_coordinates[tapi,2], self.tap_faces[tapi]))
            else:
                file.write("{\"id\":%d,\"x\":%f,\"y\":%f,\"z\":%f,\"face\":%d}," % (self.tap_names[tapi], self.tap_coordinates[tapi,0], self.tap_coordinates[tapi,1], self.tap_coordinates[tapi,2], self.tap_faces[tapi]))
        
        file.write(",\"pressureCoefficients\": [");

        ntime_steps = self.pressure_coeffeints.shape[0]
    
        for tapi in range(self.ntaps):
            file.write("{\"id\": %d , \"data\":[" % (tapi + 1))
            for ti in range(ntime_steps-1):
                file.write("%f," % self.pressure_coeffeints[ti, tapi])
            if (tapi != self.ntaps-1):
                file.write("%f]}," % self.pressure_coeffeints[ntime_steps-1, tapi])
            else:
                file.write("%f]}]" % self.pressure_coeffeints[ntime_steps-1, tapi])
    
        file.write("}")
        file.close()
        
    def read_json(self, path):
        raise NotImplementedError
    
    def parse_matlab_file(self, file_name):

        mat_contents = sio.loadmat(file_name)
        
        self.height =  mat_contents['Building_height'][0][0]        
        self.width =  mat_contents['Building_breadth'][0][0]
        self.depth = mat_contents['Building_depth'][0][0]

        self.duration = mat_contents['Sample_period'][0][0]
        self.sampling_frequency = mat_contents['Sample_frequency'][0][0]
        self.wind_direction = mat_contents['Wind_direction_angle'][0][0]
        self.wind_speed = float(mat_contents['Uh_AverageWindSpeed'][0])
    
        self.tap_locations = mat_contents['Location_of_measured_points'];
        self.ntaps = self.tap_locations.shape[1];
        self.pressure_coeffeints = mat_contents['Wind_pressure_coefficients'];
        
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
                
        self.tap_xyz = tap_xyz
        


class LowRiseData(windLoadData):
    def __init__(self, roof_type, pitch_angle):
        self.roof_type = roof_type
        self.pitch_angle = pitch_angle
        
        if self.roof_type == "flat":
            self.pitch_angle = 0
    
    #Functions 
    def write_to_json(self, path):
        NotImplemented
        
    #Functions 
    def read_json(self, path):
        NotImplemented
    
    def parse_matlab_file(self, path):
        NotImplemented
