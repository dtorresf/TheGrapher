#!/usr/local/bin/python3.5
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
	#cf.copydatafiles()
	#3) Graph all compute nodes
	methodServer.graphdfs(cf)
	#4) Graph EoIB swithces statistics
	
	#5) Generate PPT with graphs

#Graph compute nodes 

# methodServer.importallservers()
#methodServer.graphdfs()


#s = methodServer.importdatatoserver('/Users/daniela/DevOps/TheGrapher/data/el01cn09_osmonitor.csv')
#print("Promedio de CPU: ", str(s.meanmem()))


#Graph Switches 

# methodSwitch.importallswitches(2,2)
# methodSwitch.graphdfs(2)

#s = methodSwitch.importdatatoswitch(2)
#s.graphports()
#s.graphserver()

#Graph Storage ZFS heads statistics 

#Import Configuration File 
# cf = Config.Config()
# cf.loadconfigfile("/Users/daniela/DevOps/TheGrapher/configfile.json")
# print("Variables from config file: ", cf.variables)