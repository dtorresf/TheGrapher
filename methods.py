import csv
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import Config

def grouped(list, n):
	return zip(*[iter(list)]*n)

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

def graph(data,x,y,name):
	'''The function that does the magic, graphs x vs y'''
	graph_dir='/Users/daniela/DevOps/TheGrapher/graphs/' + name + '/'
	#cf = Config.Config()
	#graph_dir = cf.variables['graph_dir'] + '/' + name + '/'
	#print("Config", cf.variables)
	
	if not os.path.exists(graph_dir):
		os.mkdir(graph_dir) 
	graph_name=graph_dir + name + '_' + y + '.png'
	data_to_plot=data[[x,y]]
	ax=data_to_plot.plot(x=x, y=y)
	fig = ax.get_figure()
	fig.savefig(graph_name)
	plt.close(fig)
	