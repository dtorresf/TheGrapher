#!/usr/local/bin/python3.5
'''Parameters for Exalogic Size: Starting with half and Parameters por number of port switches EoIB used'''
from Server import Server
from Switch import Switch
import methodServer
import methodSwitch

#Graph compute nodes 

#methodServer.importallservers()
#methodServer.graphdfs()


#s = methodServer.importdatatoserver('/Users/daniela/DevOps/TheGrapher/data/el01cn09_osmonitor.csv')
#print("Promedio de CPU: ", str(s.meanmem()))


#Graph Switches 

# methodSwitch.importallswitches(2,2)
methodSwitch.graphdfs(2)

#s = methodSwitch.importdatatoswitch(2)
#s.graphports()
#s.graphserver()

#Graph Storage ZFS heads statistics 
