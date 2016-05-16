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
matplotlib.style.use('ggplot')
import os
import Config
from pptx import Presentation
from datetime import datetime
import sys
import glob
import Server
import Switch

def grouped(list, n):
	return zip(*[iter(list)]*n)

def dividedfcolumn(df,column,scalar):
	df[column] = df[column].apply(lambda x: x/scalar)

def addheadformat(csvfile, head):
	'''Adds the head format to the CSV file. Validates existence of the head'''
	with open(csvfile, 'r') as file:
		first_line = file.readline()
		if 'name' not in first_line:
			f = open(csvfile)
			text = f.read()
			f.close()
			# open the file again for writing
			f = open(csvfile, 'w')
			f.write(head)
			# write the original contents
			f.write(text)
			f.close()

def graph(data,x,y,name,cf,ylabel,color):
	'''The function that does the magic, graphs x vs y'''
	param_graph_dir = cf.variables['graph_dir']
	graph_dir= param_graph_dir + '/' + name + '/'

	try:
		if not os.path.exists(graph_dir):
			os.mkdir(graph_dir) 
		graph_name=graph_dir + name + '_' + y + '.png'
		data_to_plot=data[[x,y]]
		s = pd.Series(data_to_plot[y]).ewm(span=60).mean()
		data_to_plot[y] = s
		if y == 'cpu' or y == 'mem' or y == 'Average percent':
			ax=data_to_plot.plot(x=x, y=y,legend=False,ylim=(0,100),color=color)
			plt.axhline(y=60, xmin=0, xmax=1, hold=None,color='gold')
			plt.axhline(y=80, xmin=0, xmax=1, hold=None,color='darkred')
		else:
			ax=data_to_plot.plot(x=x, y=y,legend=False,color=color)
		ax.set_xlabel("Fecha")
		ax.set_ylabel(ylabel)
		fig = ax.get_figure()
		fig.savefig(graph_name)
		plt.close(fig)
	except TypeError:
		print("ERROR: Bad data file format, please validate data for node: ",name)
		sys.exit(1)

def importallservers(cf):
	'''List files on the data directory and loads each file on a server. Returs a list with all servers'''
	data_dir = cf.variables['data_files_dir'] + '/OSMonitorData' +'/*'
	files = glob.glob(data_dir)

	servers = list()

	for f in files:
		s = Server.Server()
		s.importdatatoserver(f,cf)
		servers.append(s)

	return servers

def graphallservers(cf,servers):
	'''Iterates over files and uses the impordata function for each one 
	and graphs each one'''
	# servers = importallservers(cf)
	for s in servers:
		s.graphserver(cf)

def importallswitches(nports,cf):
	'''List files on the data directory and loads each file on a server. Returs a list with all servers'''
	data_dir = cf.variables['data_files_dir'] + '/IBMonitorData' +'/*.csv'
	files = glob.glob(data_dir)
	switches = list()
	
	zipped = grouped(files,nports)

	for f in zipped:
		 s = Switch.Switch()
		 s.importdatatoswitch(nports,f,cf)
		 switches.append(s)

	return switches

def graphallswitches(nports,cf,switches):
	'''Iterates over files and uses the impordata function for each one 
	and graphs each one'''
	# switches = importallswitches(nports,cf)
	for s in switches:
		# graphswitch(s.ports, s.nports,cf)
		s.graphswitch(cf)
