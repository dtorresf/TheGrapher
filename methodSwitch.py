import csv
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import glob
import methods
import Switch
import Port

def addheadformat(csvfile):
	'''Adds the head format to the CSV file. Validates existence of the head'''
	with open(csvfile, 'r') as file:
		first_line = file.readline()
		if 'name' not in first_line:
			print("No header")
			f = open(csvfile)
			text = f.read()
			f.close()
			# open the file again for writing
			f = open(csvfile, 'w')
			f.write("name,port,date,rxb,txb,rxm,txm\n")
			# write the original contents
			f.write(text)
			f.close()

def importdatatoport(csvfile):
	'''The function that imports data from CSV file to a Port'''
	'''The head variable must be global and is on the config file'''
	head = "name,port,date,rxb,txb,rxm,txm\n"
	methods.addheadformat(csvfile,head)
	data=pd.read_csv(csvfile,parse_dates=['date'],dayfirst=True)
	port_data = data[['port']]
	name_data = data[['name']]
	port_value = port_data.values
	name_value = name_data.values
	port = str(port_value[0])
	name = str(name_value[0])
	p = Port.Port(port[2:-2],name[2:-2],data[['date','rxb']], data[['date','txb']])
	return p

def importdatatoswitch(nports,files):
	'''The function that imports data from CSV format to Switch'''
	'''I need a function that evaluates files on a directory and gets the info of the files for the ports'''
	
	ports = list()	

	for i in range(0,nports):
		'''Fill up an array with ports'''
		p = importdatatoport(files[i])
		ports.append(p)

	s = Switch.Switch(ports[0].switchname, nports, ports)
	return s

def importallswitches(nports):
	'''List files on the data directory and loads each file on a server. Returs a list with all servers'''
	data_dir = '/Users/daniela/DevOps/TheGrapher/data/switches/*'
	files = glob.glob(data_dir)
	switches = list()
	
	zipped = methods.grouped(files,nports)

	for f in zipped:
		 s = importdatatoswitch(nports,f)
		 switches.append(s)

	return switches

def graph(ports,nports):
	graph_dir='/Users/daniela/DevOps/TheGrapher/graphs/' + ports[0].switchname + '/'

	for i in range(0,nports):
		graph_name=graph_dir + ports[i].switchname + '_' + ports[i].name 
		data_to_plot1=ports[i].rx
		data_to_plot2=ports[i].tx
		ax= data_to_plot1.plot(x='date', y='rxb',style='-b', grid=True)
		ax2= data_to_plot2.plot(x='date', y='txb', style='-b', grid=True)
		fig = ax.get_figure()
		fig2 = ax2.get_figure()
		fig.savefig(graph_name + '_rx' + '.png')
		fig2.savefig(graph_name + '_tx' + '.png')
		plt.close(fig)
		plt.close(fig2)


def graphdfs(nports):
	'''Iterates over files and uses the impordata function for each one 
	and graphs each one'''
	switches = importallswitches(nports)
	for s in switches:
		s.graphports()