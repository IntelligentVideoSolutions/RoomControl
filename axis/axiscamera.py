#Axis API Python Module

import http.client
import urllib.error
import urllib.request
import urllib.parse
import threading
from ThreadWithReturnValue.ThreadWithReturnValue import ThreadWithReturnValue
import time


class AxisCamera:
	#username = ""
	#password = ""
	#authtype = 0
	#ptz = 0
	#privacy = 0
	def __init__(self, ip, un, pw):
		self.privacy_capable = False
		self.ptz_capable = False
		self.authtype = 0
		self.ptz = 0
		self.privacy = 0
		self.baseurl = 'http://' + ip + '/axis-cgi/'
		self.username = un
		self.password = pw
		self.digestthread = ThreadWithReturnValue(target=self.isdigest)
		self.digestthread.start()
		threading.Timer(1,self.check_camera_config).start()

	def isdigest(self):
		time.sleep(30)
		url = self.baseurl + 'param.cgi?action=list&group=root.Properties'
		passmgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
		passmgr.add_password(None, url, self.username, self.password)
		try:
			authhandler = urllib.request.HTTPDigestAuthHandler(passmgr)
			opener = urllib.request.build_opener(authhandler)
			urllib.request.install_opener(opener)
			response = opener.open(url)
		except urllib.error.HTTPError as e:
			if e.read().decode('utf-8').find("401") >= 0:
				try:
					authhandler = urllib.request.HTTPBasicAuthHandler(passmgr)
					opener = urllib.request.build_opener(authhandler)
					urllib.request.install_opener(opener)
					response = opener.open(url)
				except urllib.error.URLError as e:
					return 0
				except http.client.HTTPException as e:
					return 0
				except Exception:
					return 0
				else:
					return 2
			else:
				return 0
		except urllib.error.URLError as e:
			return 0
		except http.client.HTTPException as e:
			return 0
		except Exception:
			return 0
		else:
			return 1

	def check_camera_config(self):
		self.authtype = self.digestthread.join()
		#		print(self.authtype)
		#		print(time.asctime(time.gmtime()))
		ptzthread = ThreadWithReturnValue(target=self.isptz)
		ptzthread.start()
		#		print(time.asctime(time.gmtime()))
		privacythread = ThreadWithReturnValue(target=self.isprivacyenabled)
		privacythread.start()
		self.ptz = ptzthread.join()
		self.privacy = privacythread.join()
		# print("good")
		# print(self.ptz)
		# print(self.privacy)

	def isptz(self):
		if self.authtype != 0:
			url = self.baseurl + 'param.cgi?action=list&group=root.Properties'
			passmgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
			passmgr.add_password(None, url, self.username, self.password)
			if self.authtype == 1:
				authhandler = urllib.request.HTTPDigestAuthHandler(passmgr)
			elif self.authtype == 2:
				authhandler = urllib.request.HTTPBasicAuthHandler(passmgr)
			else:
				return 0
			try:
				opener = urllib.request.build_opener(authhandler)
				urllib.request.install_opener(opener)
				response = opener.open(url)
			except urllib.error.URLError as e:
				return 0
			except http.client.HTTPException as e:
				return 0
			except Exception:
				return 0
			else:
				data = response.read().decode('utf-8')
				if data.find('root.Properties.PTZ.PTZ=yes') >= 0:
					if data.find('root.Properties.PTZ.DigitalPTZ=no') >= 0:
						return 1
					else:
						return 2
				else:
					return 2
		else:
			return 0
	def is_privacy_capable(self):
		if self.authtype != 0:
			url = self.baseurl + 'param.cgi?action=list&group=root.Properties'
			passmgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
			passmgr.add_password(None, url, self.username, self.password)
			if self.authtype == 1:
				authhandler = urllib.request.HTTPDigestAuthHandler(passmgr)
			elif self.authtype == 2:
				authhandler = urllib.request.HTTPBasicAuthHandler(passmgr)
			else:
				return 0
			try:
				opener = urllib.request.build_opener(authhandler)
				urllib.request.install_opener(opener)
				response = opener.open(url)
			except urllib.error.URLError as e:
				return 0
			except http.client.HTTPException as e:
				return 0
			except Exception:
				return 0
			else:
				data = response.read().decode('utf-8')
				if data.find('root.Properties.PrivacyMask.PrivacyMask=yes') >= 0:
					return 1
				else:
					return 2
		else:
			return 0
	def query_camera_capibilites(self):
		if self.authtype != 0:
			url = self.baseurl + 'param.cgi?action=list&group=root.Properties'
			passmgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
			passmgr.add_password(None, url, self.username, self.password)
			if self.authtype == 1:
				authhandler = urllib.request.HTTPDigestAuthHandler(passmgr)
			elif self.authtype == 2:
				authhandler = urllib.request.HTTPBasicAuthHandler(passmgr)
			else:
				return 0
			try:
				opener = urllib.request.build_opener(authhandler)
				urllib.request.install_opener(opener)
				response = opener.open(url)
			except urllib.error.URLError as e:
				return 0
			except http.client.HTTPException as e:
				return 0
			except Exception:
				return 0
			else:
				data = response.read().decode('utf-8')
				if data.find('root.Properties.PrivacyMask.PrivacyMask=yes') >= 0:
					self.privacy_capable = True
				else:
					self.privacy_capable = False
				if data.find('root.Properties.PTZ.PTZ=yes') >= 0:
					if data.find('root.Properties.PTZ.DigitalPTZ=no') >= 0:
						self.ptz_capable = True
					else:
						self.ptz_capable = False
				else:
					self.ptz_capable = False
		else:
			return 0
	def isprivacyenabled(self):
		if self.authtype != 0:
			url = self.baseurl + 'privacymask.cgi?query=list'
			# print(url)
			passmgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
			passmgr.add_password(None, url, self.username, self.password)
			if self.authtype == 1:
				authhandler = urllib.request.HTTPDigestAuthHandler(passmgr)
			elif self.authtype == 2:
				authhandler = urllib.request.HTTPBasicAuthHandler(passmgr)
			else:
				return 0
			try:
				opener = urllib.request.build_opener(authhandler)
				urllib.request.install_opener(opener)
				response = opener.open(url)
			except urllib.error.URLError as e:
				return 0
			except http.client.HTTPException as e:
				return 0
			except Exception:
				return 0
			else:
				data = response.read().decode('utf-8')
				if data.find('ivsprivacy') >= 0:
					return 1
				else:
					return 2
		else:
			return 0
	def toggle_privacy(self):
		if self.privacy == 1:
			self.disableprivacy()
		elif self.privacy == 2:
			self.enableprivacy()
	def enableprivacy(self):
		if self.privacy == 2:
			if self.ptz == 1:
				url = self.baseurl + 'param.cgi?action=update&AudioSource.A0.InputGain=mute&PTZ.Various.V1.PanEnabled=false&PTZ.Various.V1.TiltEnabled=false&PTZ.Various.V1.ZoomEnabled=false'
			elif self.ptz == 2:
				url = self.baseurl + 'param.cgi?action=update&AudioSource.A0.InputGain=mute'
			else:
				return 0
			self.sendcmdtocamera(url)
			url = self.baseurl + 'privacymask.cgi?action=add&name=ivsprivacy&width=100&height=100'
			self.sendcmdtocamera(url)
			self.privacy = 1

	def disableprivacy(self):
		if self.privacy == 1:
			if self.ptz == 1:
				url = self.baseurl + 'param.cgi?action=update&AudioSource.A0.InputGain=0&PTZ.Various.V1.PanEnabled=true&PTZ.Various.V1.TiltEnabled=true&PTZ.Various.V1.ZoomEnabled=true'
			elif self.ptz == 2:
				url = self.baseurl + 'param.cgi?action=update&AudioSource.A0.InputGain=0'
			else:
				return 0
			self.sendcmdtocamera(url)
			url = self.baseurl + 'privacymask.cgi?action=remove&name=ivsprivacy'
			self.sendcmdtocamera(url)
			url = self.baseurl + 'com/ptz.cgi?action=update&autofocus=on'
			self.sendcmdtocamera(url)
			self.privacy = 2
		
	def gotopreset(self, preset):
		url = self.baseurl + 'com/ptz.cgi?action=update&gotoserverpresetname=' + preset 
		self.sendcmdtocamera(url)

	def sendcmdtocamera(self, url):
		#print(url)
		if self.authtype != 0:
			passmgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
			passmgr.add_password(None, url, self.username, self.password)
			if self.authtype == 1:
				authhandler = urllib.request.HTTPDigestAuthHandler(passmgr)
			elif self.authtype == 2:
				authhandler = urllib.request.HTTPBasicAuthHandler(passmgr)
			else:
				return 0
			try:
				opener = urllib.request.build_opener(authhandler)
				urllib.request.install_opener(opener)
				response = opener.open(url)
			except urllib.error.URLError as e:
				return 0
			except http.client.HTTPException as e:
				return 0
			except Exception:
				return 0
		else:
			pass

	def pan(self, step):
		if self.ptz == 1:
			url = self.baseurl + 'com/ptz.cgi?action=update&rpan=' + str(step) 
			self.sendcmdtocamera(url)

	def tilt(self, step):
		if self.ptz == 1:
			url = self.baseurl + 'com/ptz.cgi?action=update&rtilt=' + str(step) 
			self.sendcmdtocamera(url)

	def zoom(self, step):
		if self.ptz == 1:
			url = self.baseurl + 'com/ptz.cgi?action=update&rzoom=' + str(step) 
			self.sendcmdtocamera(url)

	def activateoutput(self, port):
		url = self.baseurl + 'io/port.cgi?action=' + str(port) + '%3A%2F'
		self.sendcmdtocamera(url)

	def deactivateoutput(self, port):
		url = self.baseurl + 'io/port.cgi?action=' + str(port) + '%3A%5C'
		self.sendcmdtocamera(url)

	def checkportdir(self, port):
		if self.authtype != 0:
			url = self.baseurl + 'io/port.cgi?checkdirection=' + str(port)
			passmgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
			passmgr.add_password(None, url, self.username, self.password)
			if self.authtype == 1:
				authhandler = urllib.request.HTTPDigestAuthHandler(passmgr)
			elif self.authtype == 2:
				authhandler = urllib.request.HTTPBasicAuthHandler(passmgr)
			else:
				return 0
			try:
				opener = urllib.request.build_opener(authhandler)
				urllib.request.install_opener(opener)
				response = opener.open(url)
			except urllib.error.URLError as e:
				return 0
			except http.client.HTTPException as e:
				return 0
			except Exception:
				return 0
			else:
				data = response.read().decode('utf-8')
				if data.find('input') >= 0:
					return 1
				else:
					return 2
		else:
			return 0

	def checkportstatus(self,port):
		if self.authtype != 0:
			url = self.baseurl + 'io/port.cgi?checkactive=' + str(port)
			passmgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
			passmgr.add_password(None, url, self.username, self.password)
			if self.authtype == 1:
				authhandler = urllib.request.HTTPDigestAuthHandler(passmgr)
			elif self.authtype == 2:
				authhandler = urllib.request.HTTPBasicAuthHandler(passmgr)
			else:
				return 0
			try:
				opener = urllib.request.build_opener(authhandler)
				urllib.request.install_opener(opener)
				response = opener.open(url)
			except urllib.error.URLError as e:
				return 0
			except http.client.HTTPException as e:
				return 0
			except Exception:
				return 0
			else:
				data = response.read().decode('utf-8')
				if data.find('inactive') >= 0:
					return 2
				else:
					return 1
		else:
			return 0