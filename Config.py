import json
import os
import socket
import sys
import SSHSession

class Config():
	'''Class that represents the Configuration for the whole thing'''
	def __init__(self):
		self.variables = {} #Empty dictionary that will hold the values of the config file parameters

	def validateconf(self):
		'''Validate correct format for configuration file
			Validate correct format for:
			exalogic_name
			exalogic_cn_prefix
			exalogic_sn_prefix
			exalogic_gw_prefix

			Validate existence for directories:
			data_files_dir
			graph_dir
			pptx_template
			pptx_report
			ssh_key
		'''
		if not os.path.exists(self.variables['data_files_dir']):
			raise Exception('ERROR: NoDataFilesDir - path does not exists, please provide a valid path')
			sys.exit(1)
		if not os.path.exists(self.variables['graph_dir']):
			raise Exception('ERROR: NoGraphDir - path does not exists, please provide a valid path')
			sys.exit(1)
		if not os.path.exists(self.variables['pptx_template']):
			raise Exception('ERROR: NoPptxTemplate - file does not exists, please provide a valid file')
			sys.exit(1)
		if not os.path.exists(self.variables['ssh_key']):
			raise Exception('ERROR: NoSshKey - ssh key file does not exists, please provide a valid file')
			sys.exit(1)
		if not os.path.exists(self.variables['pptx_report']):
			raise Exception('ERROR: NoReportDir - Directory for final report does not exists')
			sys.exit(1)

		cn = self.variables['exalogic_name'] + self.variables['exalogic_cn_prefix'] + '01'
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((cn,22))
		except socket.error:
			print("ERROR: CantConnect - Couldnt connect with the first node of especified exalogic node: " + cn + " .Please verify config file")
			sys.exit(1)

	def generateconfigfile():
		'''Generate config file from console input in case that no file is provided by command line'''


	def loadconfigfile(self, file):
		'''Method that loads the file to the structure, JSON file'''
		config = json.loads(open(file).read())

		if config['exalogic_rack_size'] == 'quarter':
			config['cn_number'] = 8
			config['gw_number'] = 2
		elif config['exalogic_rack_size'] == 'half': 
			config['cn_number'] = 16
			config['gw_number'] = 2
		else: 
			config['cn_number'] = 30
			config['gw_number'] = 4

		self.variables = config

	def copydatafiles(self):
		'''The function that scp the data files from first exalogic node'''
		cn = self.variables['exalogic_name'] + self.variables['exalogic_cn_prefix'] + '01'
		remote_data_dir_cn = self.variables['remote_data_dir_cn']
		local_data= self.variables['data_files_dir']
		remote_data_dir_gw = self.variables['remote_data_dir_gw']
		
		user = self.variables['ssh_user']
		key = self.variables['ssh_key']

		#Compute nodes 
		ssh=SSHSession.SSHSession(cn,user,key_file=open(key,'r'))
		ssh.get_all(remote_data_dir_cn,local_data)
		
		#Switches 
		ssh=SSHSession.SSHSession(cn,user,key_file=open(key,'r'))
		ssh.get_all(remote_data_dir_gw,local_data) 
