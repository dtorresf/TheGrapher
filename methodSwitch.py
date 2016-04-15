import csv
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import re
import Switch
import Port


#name,date,rxb,txb,rxm,txm

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
	addheadformat(csvfile)
	data=pd.read_csv(csvfile,parse_dates=['date'],dayfirst=True)
	port_data = data[['port']]
	port_value = port_data.values
	port = str(port_value[0])
	s = Switch.Switch(port[2:-2], data[['date','rx']], data[['date','tx']])
	return s
