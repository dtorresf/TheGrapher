import csv
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import glob
import methods
import Server
import os

def importdatatoserver(csvfile):
	'''The function that imports data from CSV file to a Server'''
	'''The head variable must be global and is on the config file'''
	head = "name,date,mem,cpu,established,timewait,closewait,finw1,finw2,nprocs,nopenf\n"
	methods.addheadformat(csvfile,head)
	data=pd.read_csv(csvfile,parse_dates=['date'],dayfirst=True)
	name_data = data[['name']]
	name_value = name_data.values
	name = str(name_value[0])
	s = Server.Server(name[2:-2],data[['date','mem']], data[['date','cpu']], data[['date','established']], data[['date','timewait']], data[['date','closewait']], data[['date','finw1']], data[['date','finw2']], data[['date','nprocs']], data[['date','nopenf']])
	return s

def importallservers():
	'''List files on the data directory and loads each file on a server. Returs a list with all servers'''
	data_dir = '/Users/daniela/DevOps/TheGrapher/data/computenodes/*'
	files = glob.glob(data_dir)
	servers = list()

	for f in files:
		s = importdatatoserver(f)
		servers.append(s)

	return servers

def graphdfs():
	'''Iterates over files and uses the impordata function for each one 
	and graphs each one'''
	servers = importallservers()
	for s in servers:
		s.graphserver()