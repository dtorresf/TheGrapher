import json
import paramiko
import subprocess

class Config():
	'''Class that represents the Configuration for the whole thing'''
	def __init__(self):
		self.variables = {} #Empty dictionary that will hold the values of the config file parameters

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
		local_data_cn= self.variables['data_dir_cn']

		remote_data_dir_gw = self.variables['remote_data_dir_gw']
		local_data_gw= self.variables['data_dir_gw']
		
		user = self.variables['ssh_user']
		password = self.variables['ssh_pass']

		#Compute nodes 
		scp_command = user + '@' + cn + ':' + remote_data_dir_cn + '/*.csv'
		proc = subprocess.Popen(['scp',scp_command,local_data_cn], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		#Switches 
		scp_command = user + '@' + cn + ':' + remote_data_dir_gw + '/*.csv'
		proc = subprocess.Popen(['scp',scp_command,local_data_gw], stdout=subprocess.PIPE,stderr=subprocess.PIPE)