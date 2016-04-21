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
import os

def importdatatoport(csvfile,cf):
	'''The function that imports data from CSV file to a Port'''
	'''The head variable must be global and is on the config file'''
	# head = "name,port,date,rxb,txb,rxm,txm\n"
	head = cf.variables['switch_head']
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

def importdatatoswitch(nports,files,cf):
	'''The function that imports data from CSV format to Switch'''
	'''I need a function that evaluates files on a directory and gets the info of the files for the ports'''
	
	ports = list()	

	for i in range(0,nports):
		'''Fill up an array with ports'''
		p = importdatatoport(files[i],cf)
		ports.append(p)

	s = Switch.Switch(ports[0].switchname, nports, ports)
	return s

def importallswitches(nports,cf):
	'''List files on the data directory and loads each file on a server. Returs a list with all servers'''
	#data_dir = '/Users/daniela/DevOps/TheGrapher/data/switches/*'
	data_dir = cf.variables['data_dir_gw'] + '/*'
	files = glob.glob(data_dir)
	switches = list()
	
	zipped = methods.grouped(files,nports)

	for f in zipped:
		 s = importdatatoswitch(nports,f,cf)
		 switches.append(s)

	return switches

def graph(ports,nports,cf):
	param_graph_dir = cf.variables['graph_dir']
	graph_dir= param_graph_dir + '/' + ports[0].switchname + '/'

	if not os.path.exists(graph_dir):
		os.mkdir(graph_dir) 
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


def graphdfs(nports,cf):
	'''Iterates over files and uses the impordata function for each one 
	and graphs each one'''
	switches = importallswitches(nports,cf)
	for s in switches:
		s.graphports(cf)