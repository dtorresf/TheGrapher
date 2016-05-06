import json
import os
import socket
import sys
import SSHSession

class Config():
	'''Class that represents the Configuration for the whole thing'''
	def __init__(self):
		self.variables = {} #Empty dictionary that will hold the values of the config file parameters
		self.file = ''

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

	def generateconfigfile(self):
		'''Generate config file from console input in case that no file is provided by command line'''

		exalogic_name = input("* Exalogic name (default: el01) :~$ ")
		if exalogic_name:
			self.variables['exalogic_name']=exalogic_name
		else:
			self.variables['exalogic_name']="el01"

		exalogic_cn_prefix = input("* Exalogic CN prefix (default: cn) :~$ ")
		if exalogic_cn_prefix:
			self.variables['exalogic_cn_prefix']=exalogic_cn_prefix
		else:
			self.variables['exalogic_cn_prefix']="cn"

		exalogic_gw_prefix = input("* Exalogic GW prefix (default: gw) :~$ ")
		if exalogic_gw_prefix:
			self.variables['exalogic_gw_prefix']=exalogic_cn_prefix
		else:
			self.variables['exalogic_gw_prefix']="gw"

		self.variables['exalogic_sn_prefix'] = "sn"	

		exalogic_rack_size = input("* Exalogic Rack Size [quarter,half,full] (default: half) :~$ ")
		if exalogic_rack_size:
			self.variables['exalogic_rack_size']=exalogic_rack_size
		else:
			self.variables['exalogic_rack_size']="half"


		remote_data_dir_cn = ''
		while not remote_data_dir_cn:
			remote_data_dir_cn = input("* Remote path where data files are (Compute Nodes) :~$ ")
			if remote_data_dir_cn:
				self.variables['remote_data_dir_cn']=remote_data_dir_cn
				break
			else:
				print("* Not empty values allowed ... Please input")


		remote_data_dir_gw = ''
		while not remote_data_dir_gw:
			remote_data_dir_gw = input("* Remote path where data files are (Switches) :~$ ")
			if remote_data_dir_gw:
				self.variables['remote_data_dir_gw']=remote_data_dir_gw
				break
			else:
				print("* Not empty values allowed ... Please input")


		data_files_dir = ''
		while not data_files_dir:
			data_files_dir = input("* Path where data files must be transfered :~$ ")
			if data_files_dir:
				if not os.path.exists(data_files_dir):
					print("ERROR: NoDataFilesDir - path does not exists, please provide a valid path")
					data_files_dir = ''
				else:
					self.variables['data_files_dir']=data_files_dir
					break
			else:
				print("* Not empty values allowed ... Please input")


		graph_dir = ''
		while not graph_dir:
			graph_dir = input("* Path where to leave genarated graphs :~$ ")
			if graph_dir:
				if not os.path.exists(graph_dir):
					print("ERROR: NoDataFilesDir - path does not exists, please provide a valid path")
					graph_dir = ''
				else:
					self.variables['graph_dir']=graph_dir
					break
			else:
				print("* Not empty values allowed ... Please input")


		ssh_user = input("* SSH user (default: root) :~$ ")
		if ssh_user:
			self.variables['ssh_user']=ssh_user
		else:
			self.variables['ssh_user']="root"

		ssh_key = ''
		while not ssh_key:
			ssh_key = input("* Path to ssh key for user :~$ ")
			if ssh_key:
				self.variables['ssh_key']=ssh_key
				break
			else:
				print("* Not empty values allowed ... Please input")


		eoib_ports = input("* Number of EoIB active ports (default 2) :~$ ")
		#Validate that you introduce a valid number between 2 and 4
		if eoib_ports:
			self.variables['eoib_ports']=int(eoib_ports)
		else:
			self.variables['eoib_ports']=int(2)


		self.variables['computenode_head'] = "name,date,mem,cpu,established,timewait,closewait,finw1,finw2,nprocs,nopenf\n"	
		self.variables['switch_head'] = "name,port,date,rxb,txb,rxm,txm\n"
		self.variables['pptx_template']	= data_files_dir + "/Oracle_Template.pptx"
		self.variables['pptx_report'] = data_files_dir


	def copydatafiles(self):
		'''The function that scp the data files from first exalogic node'''
		cn = self.variables['exalogic_name'] + self.variables['exalogic_cn_prefix'] + '01'
		remote_data_dir_cn = self.variables['remote_data_dir'] + '/OSMonitorData'
		local_data= self.variables['data_files_dir']
		remote_data_dir_gw = self.variables['remote_data_dir'] + '/IBMonitorData'
		remote_data_dir_zfs = self.variables['remote_data_dir'] + '/ZFSstatsData'
		
		user = self.variables['ssh_user']
		key = self.variables['ssh_key']

		#Compute nodes 
		ssh=SSHSession.SSHSession(cn,user,key_file=open(key,'r'))
		ssh.get_all(remote_data_dir_cn,local_data)
		
		#Switches 
		ssh=SSHSession.SSHSession(cn,user,key_file=open(key,'r'))
		ssh.get_all(remote_data_dir_gw,local_data) 

		#ZFS 
		ssh=SSHSession.SSHSession(cn,user,key_file=open(key,'r'))
		ssh.get_all(remote_data_dir_zfs,local_data) 
