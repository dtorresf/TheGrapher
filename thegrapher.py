#!/usr/local/bin/python3.5

from Server import Server
import methodServer

s = methodServer.importdatatoserver('/Users/daniela/DevOps/TheGrapher/data/el01cn09_osmonitor.csv')
s.graphserver()