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

class BuildingLoad:
    def __init__(self, height, width, depth, scale, 
                 tap_locations, duration, sampling_frequency, 
                 air_density, wind_speed, wind_direction,  
                 exposure, pressure_coeffeints, data_type, units):
        
        self.height = height
        self.width = width
        self.depth = depth
        self.scale = scale
        self.tap_locations = tap_locations
        self.duration = duration
        self.sampling_frequency = sampling_frequency
        self.air_density = air_density
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.exposure = exposure
        self.pressure_coeffeints = pressure_coeffeints
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

class LowRiseLoad(BuildingLoad):
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
            
            
    
    