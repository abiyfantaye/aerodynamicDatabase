# SimCenter Aerodynamic Database

Contains a python script for preparing, searching and post-processing aerodynamic database for buildings. The database holds pressure time-series measured at points(taps) distributed over the building surface. The aerodynamic data set can be: 

- **Experimetal** measurment
- **CFD** simulation (i.e., LES)
- Full-scale **feild** measurment  


## Data structure
The `aerodynamicDatabaseLib.py` is a python library to save and retrive any database entry. The core class of the library is the `WindLoadData` class which contains all the atributes of a database entry. The library also holds `HighRiseData` and `LowRiseData`that implement fuctions for manipulating wind load data for high-rise and low-rise buildings, respectively. 

The database is saved into JSON file format. Each database entry is stored using two associated files. The first file ends with *"_info.json"* and contains main atributes of the database entry, which include the building geometry, wind characterstics, data type, unit system, etc. The `HighRiseData` class has a function implemented to write this file for high rise building. Typical *"_info.json"* file for aerodynamic database looks like this:

```bash
{
windSpeed:		10.6924
width:			0.2
depth:			0.1
height:			0.3
heightToWidth:		1.5
widthToDepth:		2
duration:	        32
timeUnit:	        "sec"
lengthUnit:		"m"
samplingRate:		1000
windDirection:		0
exposureType:		"Open"
roughnessLength:	0.03
dataType:	        "CFD"
fileName:	        "HR_CFD_1.50_2.00_0.00_0.030"
}
```

The other file ends with just *".json"* and holds all the information *"_info.json"* file contains and additional data about measurment locations and the actual pressure time-series. This file is usually big and the *"_info.json"* is used instead for searching purpose. 

## Database entry naming
Each database entry is named based on the following convention. The name contains building type (high-rise or low-rise), data type (experiment, CFD or field), height to width ratio, width to depth ratio, wind direction, aerodynamic roughness length (z0). For example `HR_CFD_4_1.5_90_0.03` represents a high-rise building aerodynamic database extracted from CFD simulation with height/width and width/depth ratio of 4 and 1.5 for 90 degree wind direction in a terrain having 0.03 m aerodynamic roughness height. 

## Searching the database

For searching a particular entry in the database, generally the following information is required: 
- Building type (high-rise or low-rise) 
- Height to width ratio
- Width to depth ratio
- Wind direction 
- Exposure condition i.e. aerodynamic roughness length (z0)

## Future work needed
The current capability of the aerodynamic database is very limitted. Future work is needed to enhance its capability in the following key directions: 
 - Populate the database with more data (both experimetal and CFD). Performing CFD simulations variying different parameters listed above seem a feasible direction.  
 - Implement database interpolation technique for cases that can not be found in the database. This requires developing interpolation scheme based on  devreduced order modeling or machine learning techniques.     





