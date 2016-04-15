#!/usr/local/bin/python3.5

from Server import Server
import methodServer

### Prueba de Calculo de promedios 
print("Promedio de CPU: ",s.meancpu())

s = methodServer.importdatatoserver('/Users/daniela/DevOps/TheGrapher/data/el01cn09_osmonitor.csv')
s.graphserver()

