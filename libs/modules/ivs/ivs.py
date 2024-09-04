# IVS Python Module
# Version 3.0
# Last Updated: 1/24/2024
# Contains functions used by ivs accessories.

import json
import os, time, subprocess, ipaddress
import logging
def log(message,logpath="ivs.log", **kwargs):
	# if os.name == "nt":
	# 	#logpath="V:\Accessories\pi\FrameWork\standard\ivs\logs\ivs.log"
	# 	logpath="ivs.log"
	# if 'severity' in kwargs:
	# 	severity = kwargs['severity']
	# else:
	# 	severity = "INFO"
	# logfile = open(logpath,"a+")
	# timetup = time.localtime()
	# print(time.strftime('%Y-%m-%d %H:%M:%S', timetup) + " " + severity + " " + str(message))
	# logfile.write(time.strftime('%Y-%m-%dT%H:%M:%S', timetup) + " " + severity + " " + str(message) + "\n")
	# logfile.close()
	logging.info(__name__ + ": " + str(message))

def factorydefault(factoryconfig,configfilepath,factorynetplan = "/usr/local/ivs/templates/ivs.yaml",netplanpath = "/etc/netplan/ivs.yaml", factorysystemconf="/usr/local/ivs/templates/system.cfg",systemconf = "/usr/local/ivs/config/system.cfg",factoryvaltconf="/usr/local/ivs/templates/valt.cfg",valtconf="/usr/local/ivs/config/valt.cfg"):
	factorynetconf = "/usr/local/ivs/templates/network.cfg"
	netconf = "/usr/local/ivs/config/network.cfg"
	factoryntp = "/usr/local/ivs/templates/ntpdefault.conf"
	ntp = "/etc/ntp.conf"
	os.system("sudo cp --no-preserve=all " + factoryntp + " " + ntp)
	os.system("sudo cp --no-preserve=all " + factoryconfig + " " + configfilepath)
	os.system("sudo cp --no-preserve=all " + factorynetplan + " " + netplanpath)
	os.system("sudo cp --no-preserve=all " + factorysystemconf + " " + systemconf)
	os.system("sudo cp --no-preserve=all " + factoryvaltconf + " " + valtconf)
	os.system("sudo cp --no-preserve=all " + factorynetconf + " " + netconf)
	resetwebpassword("admin51")
	enablewebinterface()
	ChangeTimeZone("America/Chicago")
	os.system("sudo reboot")

def factory_default(inifilepath):
	factorynetplan = "/usr/local/ivs/templates/ivs.yaml"
	netplanpath = "/etc/netplan/ivs.yaml"
	factoryntp = "/usr/local/ivs/templates/ntpdefault.conf"
	ntppath = "/etc/ntp.conf"
	log("Factory Default")
	os.system("sudo cp --no-preserve=all " + factoryntp + " " + ntppath)
	log("Reset NTP")
	os.system("sudo cp --no-preserve=all " + factorynetplan + " " + netplanpath)
	log("Reset Netplan")
	os.system("sudo rm " + inifilepath)
	log("Delete INI file")
	os.system("sudo touch " + inifilepath)
	log("Create INI file")
	os.system("sudo chmod 666 " + inifilepath)
	log("Change INI permissions")
	resetwebpassword("admin51")
	log("Reset Web Password")
	enablewebinterface()
	log("Enable Web Interface")
	ChangeTimeZone("America/Chicago")
	log("Change Time Zone")
	os.system("sudo reboot")
	log("Reboot")

def loadconfig(configfilepath):
	try:
		configfile = open(configfilepath,'r')
	except:
		return {}
	else:
		try:
			config = json.loads(configfile.read())
			configfile.close()
			
			return(config)
		except:
			return {}
		
def writeconfig(configarray, configfilepath):
	try:
		config = open(configfilepath,'w+')
	except:
		pass
	else:
		json.dump(configarray,config)
		config.close()
		
def enablewebinterface():
	try:
		log("Web Interface Enabled")
		#os.system("sudo systemctl enable apache2")
		#os.system("sudo service apache2 start")
		subprocess.Popen(["sudo","systemctl","enable","apache2"])
		subprocess.Popen(["sudo","service","apache2","start"])
	except:
		pass	
def disablewebinterface():
	try:
		log("Web Interface Disabled")
		#os.system("sudo systemctl disable apache2")
		#os.system("sudo service apache2 stop")
		subprocess.Popen(["sudo","systemctl","disable","apache2"])
		subprocess.Popen(["sudo","service","apache2","stop"])
	except:
		pass

def ChangeTimeZone(timezone):
	try:
		log("Timezone changed to " + timezone)
		#log("sudo timedatectl set-timezone " + timezone)
		#os.system("sudo timedatectl set-timezone " + timezone)
		subprocess.Popen(["sudo","timedatectl","set-timezone",timezone])
	except:
		pass

def resetwebpassword(password):
	try:
		log("Web Password Changed")
		#log("htpasswd -b -c /etc/apache2/.htpasswd ivs " + password)
		#os.system("htpasswd -b -c /etc/apache2/.htpasswd ivs " + password)
		subprocess.Popen(["sudo","htpasswd","-b","-c","/etc/apache2/.htpasswd","ivs",password])
	except:
		pass

def is_ipv4(string):
	try:
		ipaddress.IPv4Network(string)
		return True
	except ValueError:
		return False

def is_subnet(string):
	try:
		subnet=int(string)
		if subnet <= 32:
			return True
		else:
			return False
	except ValueError:
		return False

def getSSIDs(nic):
	try:
		result = os.popen("sudo iwlist " + nic + " scan | grep ESSID | cut -d \":\" -f2").read()
		result = result.replace('"', '')
		result = [*set(result.split("\n"))]
		result.remove("")
		result.sort()
		return result
	except:
		return []

def EnableNTP(server,ntptemplatepath="/usr/local/ivs/templates/ntp.conf",ntpconfigpath="/etc/ntp.conf"):
	try:
		#os.system("sudo cp --no-preserve=all " + ntptemplatepath + " " + ntpconfigpath)
		fin = open(ntptemplatepath, "rt")
		fout = open(ntpconfigpath, "wt")
		for line in fin:
			#read replace the string and write to output file
			fout.write(line.replace('replace.timeserver.com', server))
			#close input and output files
		fin.close()
		fout.close()
	except:
		pass