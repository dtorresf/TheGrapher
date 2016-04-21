import csv
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import glob
import methods
import Server

def importdatatoserver(csvfile,cf):
	'''The function that imports data from CSV file to a Server'''
	'''The head variable must be global and is on the config file'''
	head = cf.variables['computenode_head']
	methods.addheadformat(csvfile,head)
	data=pd.read_csv(csvfile,parse_dates=['date'],dayfirst=True)
	name_data = data[['name']]
	name_value = name_data.values
	name = str(name_value[0])
	s = Server.Server(name[2:-2],data[['date','mem']], data[['date','cpu']], data[['date','established']], data[['date','timewait']], data[['date','closewait']], data[['date','finw1']], data[['date','finw2']], data[['date','nprocs']], data[['date','nopenf']])
	return s

def importallservers(cf):
	'''List files on the data directory and loads each file on a server. Returs a list with all servers'''
	data_dir = cf.variables['data_dir_cn'] + '/*'
	files = glob.glob(data_dir)

	servers = list()

	for f in files:
		s = importdatatoserver(f,cf)
		servers.append(s)

	return servers

def graphdfs(cf):
	'''Iterates over files and uses the impordata function for each one 
	and graphs each one'''
	servers = importallservers(cf)
	for s in servers:
		s.graphserver(cf)