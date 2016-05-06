'''
TheGrapher takes custom generated CSV files with Exalogic's compute nodes and 
IB Switches's information, loads them into python structures and graphs the variables
recolected. 

Copyright (C) 2016  Daniela Torres Faria 
GitHub: dtorresf
Mail: daniela.torres.f@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later versi
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more detai
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''


import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
# matplotlib.use('TkAgg')
matplotlib.style.use('ggplot')
import Config
from datetime import datetime
import glob
import methods
import Switch
import Port
import os
import sys

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

	#Convert to KB from bytes 
	methods.dividedfcolumn(data,'rxb',1024)
	methods.dividedfcolumn(data,'txb',1024)

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
	data_dir = cf.variables['data_files_dir'] + '/IBMonitorData' +'/*.csv'
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

	try:
		if not os.path.exists(graph_dir):
			os.mkdir(graph_dir) 
		for i in range(0,nports):
			graph_name=graph_dir + ports[i].switchname + '_' + ports[i].name
			data_to_plot1=ports[i].rx
			data_to_plot2=ports[i].tx
			s1 = pd.Series(data_to_plot1['rxb']).ewm(span=60).mean()
			data_to_plot1['rxb'] = s1
			s2 = pd.Series(data_to_plot2['txb']).ewm(span=60).mean()
			data_to_plot2['txb'] = s2
			ax= data_to_plot1.plot(x='date', y='rxb',legend=False)
			ax2= data_to_plot2.plot(x='date', y='txb',legend=False)
			ax.set_xlabel("Fecha")
			ax.set_ylabel("RX(KB)")
			ax2.set_xlabel("Fecha")
			ax2.set_ylabel("TX(KB)")
			fig = ax.get_figure()
			fig2 = ax2.get_figure()
			fig.savefig(graph_name + '_rx' + '.png')
			fig2.savefig(graph_name + '_tx' + '.png')
			plt.close(fig)
			plt.close(fig2)
	except:
		print("ERROR: Bad data file format, please validate data for switche: ",ports[0].switchname)
		sys.exit(1)


def graphdfs(nports,cf,switches):
	'''Iterates over files and uses the impordata function for each one 
	and graphs each one'''
	# switches = importallswitches(nports,cf)
	for s in switches:
		s.graphports(cf)