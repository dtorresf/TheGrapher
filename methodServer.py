import csv
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import re
import Server

#(self,name,cpu,mem,established,timewait,closewait,finw1,finw2,nprocs,nopenf)

def addheadformat(csvfile):
	'''Adds the head format to the CSV file. Validates existence of the head'''
	with open(csvfile, 'r') as file:
		#has_header = csv.Sniffer().has_header(file.read(2048))
		first_line = file.readline()
		if 'cpu' not in first_line:
			print("No header")
			f = open(csvfile)
			text = f.read()
			f.close()
			# open the file again for writing
			f = open(csvfile, 'w')
			f.write("name,date,mem,cpu,established,timewait,closewait,finw1,finw2,nprocs,nopenf\n")
			# write the original contents
			f.write(text)
			f.close()

def importdatatoserver(csvfile):
	'''The function that imports data from CSV file to a Server'''
	addheadformat(csvfile)
	data=pd.read_csv(csvfile,parse_dates=['date'],dayfirst=True)
	name_data = data[['name']]
	name_value = name_data.values
	name = str(name_value[0])
	s = Server.Server(name[2:-2],data[['date','mem']], data[['date','cpu']], data[['date','established']], data[['date','timewait']], data[['date','closewait']], data[['date','finw1']], data[['date','finw2']], data[['date','nprocs']], data[['date','nopenf']])
	return s

def graph(data,y,name):
	'''The function that does the magic'''
	#Validar si existe 
	graph_dir='/Users/daniela/DevOps/TheGrapher/graphs/' + name + '/'
	graph_name=graph_dir + name + '_' + y + '.png'
	data_to_plot=data[['date',y]]
	ax=data_to_plot.plot(x='date', y=y)
	fig = ax.get_figure()
	fig.savefig(graph_name)

def getdatafiles():
	'''Obtains the data from the servers with ssh'''

def graphdfs():
	'''Iterates over files and uses the impordata function for each one 
	and graphs each one'''