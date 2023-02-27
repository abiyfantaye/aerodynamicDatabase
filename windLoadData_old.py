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
    def __init__(self, scale, exposure_type, data_type, air_density, units):
        
    # def __init__(self, height, width, depth, scale, 
    #              tap_locations, duration, sampling_frequency, 
    #              air_density, wind_speed, wind_direction,  
    #              exposure, data_type, units):
        self.scale = scale
        self.exposure_type = exposure_type
        self.data_type = data_type        
        self.air_density = air_density
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
    def tap_locations (self):
        return self._tap_locations
    
    @tap_locations .setter
    def tap_locations(self, value):
        self._tap_locations = value
        
    @property
    def tap_xyz (self):
        return self._tap_xyz
    
    @tap_xyz.setter
    def tap_xyz(self, value):
        self._tap_xyz = value
        
    @property
    def tap_normals (self):
        return self._tap_normals
    
    @tap_normals .setter
    def tap_normals(self, value):
        self._tap_normals = value
        
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
    def exposure_type(self):
        return self._exposure_type

    @exposure_type.setter
    def exposure_type(self, value):
        self._exposure_type = value
        
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
        
    # Functions 
    def dynamic_pressure(self):
        return 0.5*self.rho*self.wind_speed**2.0;

class HighRiseData(windLoadData):
    def __init__(self, scale, exposure_type, data_type, air_density, nstory, units):
        windLoadData.__init__(self, scale, exposure_type, data_type, air_density, units)
        
        self.nstory = nstory
    
    ### Functions 
    def write_to_json(self, fine_name):
        file = open(fine_name + '.json',"w")
        file.write("{\n")
        file.write("\"width\":%f," % self.width)
        file.write("\"depth\":%f," % self.depth)
        file.write("\"height\":%f," % self.height)        
        file.write("\"scale\":%f," % self.scale)       
        file.write("\"exposureType\":%s," % self.exposure_type)        
        file.write("\"dataType\":%s," % self.data_type)       
        file.write("\"windSpeed\":%f," % self.wind_speed)        
        file.write("\"duration\":%f," % self.duration)
        file.write("\"units\":{\"length\":\"m\",\"time\":\"sec\"},")
        file.write("\"samplingFrequency\":%f," % self.sampling_frequency)
        file.write("\"windDirection\":%f," % self.wind_direction)
        file.write("\"tapLocations\": [")
    
        for tapi in range(self.ntaps):
            if (tapi == self.ntaps-1):
                file.write("{\"id\":%d,\"x\":%f,\"y\":%f,\"z\":%f,\"face\":%d}]" % (self.tap_names[tapi], self.tap_xyz[tapi,0], self.tap_xyz[tapi,1], self.tap_xyz[tapi,2], self.tap_faces[tapi]))
            else:
                file.write("{\"id\":%d,\"x\":%f,\"y\":%f,\"z\":%f,\"face\":%d}," % (self.tap_names[tapi], self.tap_xyz[tapi,0], self.tap_xyz[tapi,1], self.tap_xyz[tapi,2], self.tap_faces[tapi]))
        
        file.write(",\"pressureCoefficients\": [")

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
    
    def read_matlab_file(self, file_name):

        mat_contents = sio.loadmat(file_name)
        
        self.height =  mat_contents['Building_height'][0][0]        
        self.width =  mat_contents['Building_breadth'][0][0]
        self.depth = mat_contents['Building_depth'][0][0]

        self.duration = mat_contents['Sample_period'][0][0]
        self.sampling_frequency = mat_contents['Sample_frequency'][0][0]
        # self.wind_direction = mat_contents['Wind_direction_angle'][0][0]
        self.wind_direction = 0
        self.wind_speed = float(mat_contents['Uh_AverageWindSpeed'][0])
    
        self.tap_locations = mat_contents['Location_of_measured_points']
        self.ntaps = self.tap_locations.shape[1]
        
        # cp = mat_contents['Wind_pressure_coefficients']
        self.pressure_coeffeints = mat_contents['Wind_pressure_coefficients']
        
        #Tap locations (x,y,z) in global coordinate system
        tap_xyz = np.zeros((self.ntaps, 3))
        tap_normals = np.zeros((self.ntaps, 3))
        
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
                tap_normals[tap,:] = np.array([1.0, 0.0, 0.0])
                
            if face == 2:
                tap_xyz[tap,0] = -self.depth/2.0 + (xLoc - self.width)
                tap_xyz[tap,1] = -self.width/2.0
                tap_normals[tap,:] = np.array([0.0, 1.0, 0.0])

            if face == 3:
                tap_xyz[tap,0] = self.depth/2.0
                tap_xyz[tap,1] = -self.width/2.0 + (xLoc - self.width - self.depth)
                tap_normals[tap,:] = np.array([-1.0, 0.0, 0.0])

            if face == 4:
                tap_xyz[tap,0] = self.depth/2.0 - (xLoc - 2*self.width - self.depth)
                tap_xyz[tap,1] = self.width/2.0
                tap_normals[tap,:] = np.array([0.0, -1.0, 0.0])

                
        self.tap_xyz = tap_xyz
        self.tap_normals = tap_normals


    def base_loads(self):
        NotImplemented
        
    def story_loads(self):
        NotImplemented

    def plot_Cp_contour (self, cp_type='mean'):
        NotImplemented

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