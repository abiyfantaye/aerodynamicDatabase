# SimCenter Aerodynamic Database

Contains a python script for preparing, searching and post-processing aerodynamic database for buildings. The database holds pressure time-series measured at points(taps) distributed over the building surface. The aerodynamic data set can be: 

- **Experimetal** measurment
- **CFD** simulation (i.e., LES)
- Full-scale **feild** measurment  


## Data Structure
The database is saved into JSON file format. The `aerodynamicDatabaseLib.py` is a python library to save and retrive any database entry. The core class of the library is the `WindLoadData` class which contains all the atributes any database entry. The library also holds `HighRiseData` and `LowRiseData`that implement fuctions for manipulating wind load data for high-rise and low-rise buildings, respectively. 

Each database entry is stored using two associated files. The first file is `*_info.json` that contains main atributes of the database entry, which include the building geometry, wind characterstics, data type, unit system, etc. The `HighRiseData` class has a function implemented to write this file for high rise building. Typical `*_info.json` file for aerodynamic database looks like this:

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


- **OpenFOAM**, preferably v8  
- Intel's oneAPI MKL package or **LAPACK** library

    Download the installer here: https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit-download.html?operatingsystem=linux&distributions=webdownload&options=online
    
    Follow the Command Line Download and Installation instructions (`sudo` is not required, but we only selected the MKL package to install - 7.3 GB) \
    And make sure to follow these instructions: https://www.intel.com/content/www/us/en/develop/documentation/get-started-with-dpcpp-compiler/top.html \
    i.e. source the environment settings script (in our case that worked with `$ source $HOME/intel/oneapi/setvars.sh intel64` but might be dependent on where you installed it - also, you might want to add this line to the end of your `~/.bashrc` file, as it needs to be sourced every time you open a new terminal window)
