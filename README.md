TheGrapher Exalogic
===================

TheGrapher takes custom generated CSV files with Exalogic's compute nodes and EoIB Ports Switches's information, loads them into python structures and graphs the variables recolected.

The scripts that generates the CSV files can be found under the scripts folder. 

The variables recolected for the compute nodes are:

1. Compute Node's name
2. Date-Hour 
3. Memory
4. CPU
5. Number of Established connections
6. Number of Close Wait connections 
7. Number of Time Wait connections 
8. Number of Fin Wait 1 connections 
8. Number of Fin Wait 2 connections 
8. Number of processes runing 
8. Number of open files

The variables recolected for the switches are:

1. Switch Name
2. Port Name 
3. TX in bytes
4. RX in bytes 

Is it important to configure the first script in all the compute nodes's crontab and the second one on the first compute node. 

The idea is to generated automated reports for a month of data in pptx, pdf and html format for all components of an Exalogic machine. 

The Grapher uses a config JSON file to read all the paths, names an to make it more flexible and easy to use in different escenarios. 

## Usage


```
usage: thegrapher.py
```

The script (for now) doesn't have any arguments, it takes all the required parameters for the config file.

## Script Output

The Grapher's output should be a report with all the recolected data and graphs. Right now it only generates the graphs based on the CSV files.


### To do list
- [X] Code the generation of the automatic report on pptx format.
- [ ] Code the generation of the automatic report on pdf format.
- [ ] Code the generation of the automatic report on html format.
- [ ] Put a more explicit help function.
- [ ] Use try/catch for managing possible exceptions.
- [ ] Simplify code and imports.


=======

Copyright (C) 2016 Daniela Torres Faría

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
