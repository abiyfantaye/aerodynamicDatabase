# SimCenter Aerodynamic Database

Contains a python script for preparing, searching and post-processing aerodynamic database for buildings. The database holds pressure time-series measured at points(taps) distributed over the building surface. The aerodynamic data set can be: 

- **Experimetal** measurment
- **CFD** simulation (i.e., LES)
- Full-scale **feild** measurment  


## Data Structure
The database is saved into JSON file format. The `aerodynamicDatabaseLib.py` is a python library to save and retrive any database entry. The core class of the library is the `WindLoadData` class which contains all the atributes any database entry. The library also holds `HighRiseData` and `LowRiseData`that implement fuctions for manipulating wind load data for high-rise and low-rise buildings, respectively. 

Each database entry is stored using two associated files. The first file ends with *"_info.json"* and contains main atributes of the database entry, which include the building geometry, wind characterstics, data type, unit system, etc. The `HighRiseData` class has a function implemented to write this file for high rise building. Typical *"_info.json"* file for aerodynamic database looks like this:

```bash
{
"windSpeed":10.692400,
"width":0.200000,
"depth":0.100000,
"height":0.300000,
"heightToWidth":1.500000,
"widthToDepth":2.000000,
"duration":32.000000,
"timeUnit":sec,
"lengthUnit":m,
"samplingRate":1000.000000,
"windDirection":0.000000,
"exposureType":Open,
"roughnessLength":0.030000,
"dataType":CFD
}
```

The other file ends with just *".json"* and holds all the information *"_info.json"* file contains and additional data about measurment locations and the actual pressure time-series. This file is usually big and the *"_info.json"* is used instead for searching purpose. 

## Database Entry Naming
Each database entry is named based on the following convention. The name contains building type (high-rise or low-rise), data type (experiment, CFD or field), height to width ratio, width to depth ratio, wind direction, aerodynamic roughness length. For example `HR_CFD_4_1.5_90_0.03` represents a high-rise building aerodynamic database extracted from CFD simulation with height/width and width/depth ratio of 4 and 1.5 for 90 degree wind direction in a terrain having 0.03 m aerodynamic roughness height.   
