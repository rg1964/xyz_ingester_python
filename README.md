# XYZ Data Format Ingester for Citrination
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/rg1964/xyz_ingester_python">
    <img src="/misc/logo.png" alt="Logo" width="80" height="80">
  </a>
</p>


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Usage Flow](#usage-flow)
* [Support](#support)

<!-- ABOUT THE PROJECT -->
## About The Project
This is an implementation of an ingester to transform a Python pandas dataframe into the [PIF](http://citrineinformatics.github.io/pif-documentation/index.html) format.  
It includes a function [xyz_converter.py](https://github.com/rg1964/xyz_ingester_python/blob/master/2_xyz_converter.py) that takes in a Python pandas dataframe and outputs a PIF file.
The test uses data from [QM9](https://figshare.com/articles/Data_for_6095_constitutional_isomers_of_C7H10O2/1057646).
This is a relatively large data set, and one ca use only a representative subset of this data for illustrative purposes.
The main journal article that describes this data set (and the data file structure .XYZ) can be found [here](https://www.nature.com/articles/sdata201422). A summary document of the .XYZ format is provided as well: [XYZ file format for molecular structure and properties](https://github.com/rg1964/xyz_ingester_python/blob/master/XYZ%20file%20format%20for%20molecular%20structure%20and%20properties.pdf). A small sample of the PIF files generated through this conversion are placed in the [GDB-9-molecules-pif](https://github.com/rg1964/xyz_ingester_python/tree/master/GDB-9-molecules-pif) directory. Finally, I have included a [file](https://github.com/rg1964/xyz_ingester_python/blob/master/Post-mortem%20comments.pdf) which provides some details on some issues I have to deal with in the course of this project.

## Getting Started

This is an overview of the components of the project as well as details on how to make the best use of it.

### Prerequisites

This project has been developed with Python 3.7.3, and the following packages are used by the different components:

* os
* requests
* tarfile
* shutil
* random
* argparse
* pypif and pypif.obj
* citrination_client
* string

### Usage Flow

This repository contains 4 files, that should be used in a sequential manner:

1. Download the full QM9 dataset archive and extract it to predefined local directory 'GDB-9-molecules-all' by using [0_GDB-9_files_downloader.py](https://github.com/rg1964/xyz_ingester_python/blob/master/0_GDB-9_files_downloader.py):
```
python.exe 0_GDB-9_files_downloader.py
```
2. Select at random a user-defined number of files from the extracted archive and populate a pre-defined directory 'Randomized-xyz' with the selected files by using [1_random_files_selector.py](https://github.com/rg1964/xyz_ingester_python/blob/master/1_random_files_selector.py): 

```
usage: 1_random_files_selector.py [-h] [-n NRFILES]

select a number of random xyz files from "GDB-9-molecules-all" directory and
copy to "Randomized-xyz"

optional arguments:
  -h, --help            show this help message and exit
  -n NRFILES, --nrfiles NRFILES
                        number of files to select randomly
```
This is an optional step, mainly designed for visually testing the results of uploading the pif files on Citrination database and analytics platform. Skipping this step will result in processing the entire database of 134K files in one shot.

For example, to randomly select 200 .XYZ files from the archive and place them in the 'Randomized-xyz' directory, one needs to run the following command:

```
python.exe 1_random_files_selector.py -n 200
```
3. Convert the random selection of .xyz files into PIF format with the aid of [2_xyz_converter.py](https://github.com/rg1964/xyz_ingester_python/blob/master/2_xyz_converter.py):
```
python.exe 2_xyz_converter.py -a D:\Citrine\xyz_ingester_python\Randomized-xyz\
```
The general format for using [2_xyz_converter.py](https://github.com/rg1964/xyz_ingester_python/blob/master/2_xyz_converter.py) is this:
```
usage: 2_xyz_converter.py [-h] (-l LISTD LISTD | -a ALLD | -f FILES)

convert xyz file(s) to pif

optional arguments:
  -h, --help            show this help message and exit
  -l LISTD LISTD, --listd LISTD LISTD
                        2 arguments: the source directory full path and a
                        comma separated list of filenames to process in that
                        directory
  -a ALLD, --alld ALLD  1 argument: the source directory full path path where
                        all files of .xyz type reside
  -f FILES, --files FILES
                        1 argument: a comma separated list of filenames with
                        their full paths to process
```
4. Upload the generated PIF files on Citrination with the aid of [3_citrination_uploader.py](https://github.com/rg1964/xyz_ingester_python/blob/master/3_citrination_uploader.py):
```
python.exe 3_citrination_uploader.py
```
## Support
For any issues or questions, please send an email to [Roman Gafiteanu](mailto:Roman.Gafiteanu@gmail.com).
