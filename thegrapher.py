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
	cf.copydatafiles()
	#3) Graph all compute nodes
	methodServer.graphdfs(cf)
	#4) Graph EoIB swithces statistics
	methodSwitch.graphdfs(cf.variables['eoib_ports'],cf)
	#5) Generate PPT with graphs

<<<<<<< HEAD
=======
### Prueba de Calculo de promedios 
print("Promedio de CPU: ",s.meancpu())

s = methodServer.importdatatoserver('/Users/daniela/DevOps/TheGrapher/data/el01cn09_osmonitor.csv')
s.graphserver()

>>>>>>> master
