#!/usr/local/bin/python3.5
'''
TheGrapher takes custom generated CSV files with Exalogic's compute nodes and 
IB Switches's information, loads them into python structures and graphs the variables
recolected.

Copyright (C) 2016  Daniela Torres Faria 
GitHub: dtorresf
Mail: daniela.torres.f@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later versi
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more detai
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

from Server import Server
from Switch import Switch
import methodServer
import methodSwitch
import methods
import Config

'''Defitinion of Main Method'''

if __name__ == "__main__":

	#1) Load config file 
	cf = Config.Config()
	cf.loadconfigfile("/Users/daniela/DevOps/TheGrapher/config/configfile.json")
	#2) Bring the data files to the corresponding directories (Validate Existence of directories)
	cf.copydatafiles()
	#3) Graph all compute nodes
	methodServer.graphdfs(cf)
	#4) Graph EoIB swithces statistics
	methodSwitch.graphdfs(cf.variables['eoib_ports'],cf)
	#5) Generate PPT with graphs
