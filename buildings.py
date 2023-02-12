"""
A python code to store and process aerodynamic wind load
data (both experimentand and CFD) on low-rise and high-
rise buildings.  

Finally, the data is written to JSON format for further
analysis. 

Also, implements functions for post-processing of mean and 
peak loads and responses on the building.

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
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        
    @property
    def tap_locations(self):
        return self._tap_locations

    @tap_locations.setter
    def tap_locations(self, value):
        self._tap_locations = value
        
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
    def exposure(self):
        return self._exposure

    @exposure.setter
    def exposure(self, value):
        self._exposure = value
        
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
    def data_type(self, value):
        self._pressure_coeffeints = value
        
    # Functions 
    def ref_pressure(self):
        return 0.5*self.rho*self.wind_speed**2.0;

class HighRiseData(windLoadData):
    def __init__(self, nstory):
        self.nstory = nstory
    
    ### Functions 
    def write_to_json(self, path):
        raise NotImplementedError
        
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

    
        # get xMax and yMax .. assuming first sensor is 1m from building edge
        # location on faces cannot be obtained from the inputs, at least not with 
        # current documentation, awaing email from TPU
    
        xMax = max(self.tap_locations[0]) + 1
        yMax = max(self.tap_locations[1]) + 1
        
        for tap in range(self.ntaps):
            tag = self.tap_locations[2][tap]
            xLoc = self.tap_locations[0][tap]
            yLoc = self.tap_locations[1][tap]
            face = self.tap_locations[3][tap]
    
            X = xLoc
            Y = yLoc
            if (face == 2):
                xLoc = X - breadth
            elif (face == 3):
                xLoc = X - breadth - depth
            elif (face == 4):
                xLoc = X - 2*breadth - depth
            
            if (loc == numLocations-1):
                file.write("{\"id\":%d,\"xLoc\":%f,\"yLoc\":%f,\"face\":%d}]" % (tag, xLoc, yLoc, face))
            else:
                file.write("{\"id\":%d,\"xLoc\":%f,\"yLoc\":%f,\"face\":%d}," % (tag, xLoc, yLoc, face))


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
            
            
    
    