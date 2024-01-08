#IVS Accessory Framework
#Version 1.3
#Last Updated: 12/27/2023
#Compatible with Valt Versions 5.x and 6.x
from kivy.config import Config
# Config.set('kivy', 'keyboard_mode', 'systemanddock')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior 
from kivy.uix.image import Image  
from kivy.uix.textinput import TextInput
from kivy.uix.settings import Settings, SettingsWithSpinner, SettingSpacer, SettingString, SettingOptions, SettingItem
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
import time,netifaces,os,json
from datetime import timedelta
from ivs import ivs
from kivy.lang import Builder
from CameraControl.CameraControl import CameraControl
from ScheduleDisplay.ScheduleDisplay import ScheduleDisplay
from Keypad.Keypad import Keypad
import threading
from functools import partial
# Builder.load_file('C:/Users/jbuttitta/PycharmProjects/CameraControl/CameraControl.kv')
# Builder.load_file('C:/Users/jbuttitta/PycharmProjects/ScheduleDisplay/ScheduleDisplay.kv')

# Window.clearcolor = (.8, .8, .8, 1)
Window.clearcolor = ("#E6E6E6")
Window.keyboard_anim_args = {"d":.2,"t":"linear"}

#Kivy Screen Declarations
class AboutScreen(Screen):
	pass

#Kivy Widget Declarations
class BackgroundLabel(Label):
	pass
class ActiveLabel(BackgroundLabel):
	pass
class LeftAlignLabel(Label):
	pass
class StandardTextLabel(LeftAlignLabel):
	pass
class NetworkTextLabel(StandardTextLabel):
	pass
class HeaderLabel(Label):
	pass
class ErrorLabel(Label):
	pass
class StandardTextInput(TextInput):
	id = ObjectProperty(None)
class StandardPassword(StandardTextInput):
	pass
class DisabledTextInput(StandardTextInput):
	pass
class StandardGridLayout(GridLayout):
	pass
class ImageButton(ButtonBehavior, Image): 
	downimage = ObjectProperty(None)
	upimage = ObjectProperty(None)
	id = ObjectProperty(None)
	def on_press(self):  
		self.source=self.downimage
	def on_release(self):
		self.source=self.upimage
class StandardButton(Button):
	id = ObjectProperty(None)
class LandscapeHome(Screen):
	pass
class PortraitHome(Screen):
	pass
class DropDownButton(StandardButton):
	selected_id = ObjectProperty(None)
class StandardDropDown(DropDown):
	id = ObjectProperty(None)
class PasswordLabel(Label):
	pass
class WrappedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

#Kivy Settings Declarations

class SettingScrollOptions(SettingOptions):

    def _create_popup(self, instance):
        # create the popup
        scroll = ScrollView(always_overscroll=False,size_hint=(1,1))
        content = BoxLayout(orientation='vertical', spacing='5dp', size_hint=(1,None))
        content.height=(len(self.options)+1) * dp(55)
        scroll.add_widget(content)
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(content=scroll, title=self.title, size_hint=(None, None),size=(popup_width, '400dp'))
        # popup.height = len(self.options) * dp(55) + dp(150)

        # add all the options
        content.add_widget(Widget(size_hint_y=None, height=1))
        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = ToggleButton(text=option, state=state, group=uid)
            btn.bind(on_release=self._set_option)
            content.add_widget(btn)

        # finally, add a cancel button to return on the previous panel
        content.add_widget(SettingSpacer())
        btn = Button(text='Cancel', size_hint_y=None, height=dp(50))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        # and open the popup !
        popup.open()

class SettingIP(SettingString):
	def _validate(self, instance):
		# we know the type just by checking if there is a '.' in the original
		# value
		# self._dismiss()
		# print(self.popup.ids.keys())
		try:
			if ivs.is_ipv4(self.textinput.text):
				self.value = self.textinput.text
				self._dismiss()
			else:
				self.popup.ids['feedback'].text = "Invalid IP Address"
				return
		except ValueError:
			return
	# def _create_popup(self, instance):
	# 	super(SettingIP, self)._create_popup(instance)
	# 	label = Label(size_hint_y=None, height='15',text="test")
	# 	self.content.add_widget(label)
	# 	self.popup.ids['feedback'] = label
	def _create_popup(self, instance):
		# create popup layout
		content = BoxLayout(orientation='vertical', spacing='5dp')
		popup_width = min(0.95 * Window.width, dp(500))
		self.popup = popup = Popup(
			title=self.title, content=content, size_hint=(None, None),
			size=(popup_width, '250dp'))

		# create the textinput used for numeric input
		self.textinput = textinput = TextInput(
			text=self.value, font_size='24sp', multiline=False,
			size_hint_y=None, height='42sp')
		textinput.bind(on_text_validate=self._validate)
		self.textinput = textinput

		# construct the content, widget are used as a spacer
		content.add_widget(Widget())
		content.add_widget(textinput)
		content.add_widget(Widget())
		# content.add_widget(SettingSpacer())
		label = Label(size_hint_y=None, height='15')
		content.add_widget(label)
		self.popup.ids['feedback'] = label

		# 2 buttons are created for accept or cancel the current value
		btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
		btn = Button(text='Ok')
		btn.bind(on_release=self._validate)
		btnlayout.add_widget(btn)
		btn = Button(text='Cancel')
		btn.bind(on_release=self._dismiss)
		btnlayout.add_widget(btn)
		content.add_widget(btnlayout)

		# all done, open the popup !
		popup.open()

class SettingPassword(SettingString):
	def _create_popup(self, instance):
		super(SettingPassword, self)._create_popup(instance)
		self.textinput.password = True

	def add_widget(self, widget, *largs):
		if self.content is None:
			super(SettingString, self).add_widget(widget, *largs)
		if isinstance(widget, PasswordLabel):
			return self.content.add_widget(widget, *largs)

class SettingStatus(SettingString):
	def on_touch_up(self, touch):
		pass
	def on_touch_down(self, touch):
		pass
class SettingButton(SettingItem):
	action = StringProperty()
# Main Application



class IVS_Accessory_Framework(App):

	use_kivy_settings = False
	# settings_cls = Settings
	recstarttime = 0  # Variable is used to keep track of the time a recording was initiated. Used in calculating display of recording time.
	configfilerechecktime = 5  # Interval in seconds to recheck config files for changes from the web interface.
	updatedconfig = False
	screenmgmt = ScreenManager(transition=SwapTransition())
	imagepath = 'images/'
	logpath = "logs/ivs.log"
	timezonefilepath = 'config/timezones.json'
	versionfilepath = 'config/version.json'
	configfilepath = 'config/accessory.ini'
	executedelay = .1 # Number of seconds to wait between a button press and execution of an API call. API calls "freeze" the application while waiting on a response, so this allows a screen update to be sent prior to the freeze.
	standardfontsize=15 # default size of font used in text labels and field.
	headerfontsize=15 # default size of font used in headers.
	roomchecktime = 5 # Number of seconds to wait between room status checks against the VALT server.
	lastroomstatus = 0 # Tracks previous room status so updates only occur on changes.
	# if os.name == "nt":
	# 	# kvpath = 'C:/Users/jbuttitta/PycharmProjects/'
	# 	# imagepath = 'images\\'
	# 	# logpath = "logs/ivs.log"
	# 	# timezonefilepath = 'config\\timezones.json'
	# 	# versionfilepath = 'config\\version.json'
	# 	# configfilepath = 'config\\accessory.ini'
	# 	pass
	# else:
	# 	# kvpath = '/usr/local/ivs/'
	# 	# imagepath = '/usr/local/ivs/images/'
	# 	logpath = "/usr/local/ivs/logs/ivs.log"
	# 	timezonefilepath = '/usr/local/ivs/config/timezones.json'
	# 	versionfilepath = '/usr/local/ivs/config/version.json'
	# 	configfilepath = '/usr/local/ivs/config/accessory.ini'
	def load_kv_files(self):
		Builder.load_file('Framework/ivs_accessory_framework.kv')
		Builder.load_file('CameraControl/CameraControl.kv')
		Builder.load_file('ScheduleDisplay/ScheduleDisplay.kv')
		Builder.load_file('Keypad/keypad.kv')
	def build(self):
		# self.icon=self.imagepath + 'valticon.png'
		self.icon = self.imagepath + 'ivsicon.png'
		return self.screenmgmt
		# pass
	def on_start(self):
		self.load_kv_files()

		screen = LandscapeHome(name='Landscape_Home_Screen')
		self.screenmgmt.add_widget(screen)
		screen = AboutScreen(name='About_Screen')
		self.screenmgmt.add_widget(screen)

		screen = PortraitHome(name='Portrait_Home_Screen')
		self.screenmgmt.add_widget(screen)

		self.homescreen = self.config.get("application", "orientation") + "_Home_Screen"
		self.screenmgmt.current = self.homescreen

		self.initialize(1)
		firmware = ivs.loadconfig(self.versionfilepath)
		self.screenmgmt.get_screen('About_Screen').ids['firmware'].text = firmware["version"]
		self.event_updatetime = Clock.schedule_interval(self.updatetime,1)
		# Uncomment to check config files periodically for external updates.
		# self.event_checkconfigfiles = Clock.schedule_interval(self.checkconfigfiles,self.configfilerechecktime)

	def build_config(self, config):
		# configfilepath = 'config/defaults.json'
		# configfile = open(configfilepath, 'r')
		# defaults = json.loads(configfile.read())

		# Change to use a sidebar instead of spinner
		# self.settings_cls = 'Settings'

		# Change to use spinner instead of sidebar. Was done to to make settings more compatible with portrait layout.
		self.settings_cls = 'SettingsWithSpinner'

		self.build_settings_defaults()
		defaults = self.defaultsjson
		self.config = Config
		self.config.read(self.configfilepath)

		for section in defaults:
			self.config.setdefaults(section, defaults[section])
		# self.create_settings()
	def build_settings(self, settings):
		# self.settings = Settings()
		self.settings = settings
		# self.settings = SettingsWithSpinner
		self.build_network_settings()
		self.build_time_settings()
		self.build_valt_settings()
		self.build_application_settings()
		self.build_system_settings()
		settings.register_type("ip", SettingIP)
		settings.register_type("scrolloptions", SettingScrollOptions)
		settings.register_type("password", SettingPassword)
		settings.register_type("status", SettingStatus)
		settings.register_type("button", SettingButton)
		settings.add_json_panel('Application', self.config, data=json.dumps(self.applicationjson))
		settings.add_json_panel('VALT', self.config, data=json.dumps(self.valtjson))

		# 1/8/2024: Disabled time panel in settings as there is no good way to set the time zone via python. As part of the migration to android, this feature has been deprecated.
		# settings.add_json_panel('Time', self.config, data=json.dumps(self.timejson))

		# 12/21/2023: Disabled network panel in settings as there is no good way to set the IP address from python. The way the address had been getting set was hacky using os commands. As part of the migration to android, this feature has been deprecated.
		# settings.add_json_panel('Network', self.config, data=json.dumps(self.networkjson))

		settings.add_json_panel('System', self.config, data=json.dumps(self.systemjson))
	def refresh_settings(self):
		panels = self.settings.interface.content.panels
		for panel in panels.values():
			children = panel.children
			for child in children:
				if isinstance(child, SettingItem):
					child.value = panel.get_value(child.section, child.key)

	def _on_keyboard_settings(self, window, *largs):
		pass
	def valt_config_change(self,key,value,b):
		self.valt.changeserver(self.config.get("valt", "server"), self.config.get("valt", "username"), self.config.get("valt", "password"))
		valtrooms = self.valt.getrooms()
		if key == "roomname":
			for room in valtrooms:
				if value == room["name"]:
					self.config.set('valt', 'room', room["id"])
					# print(self.config.get('valt','room'))
					self.write_config()
				pass
		elif key == 'recname':
			pass
		else:
			if type(valtrooms).__name__ == 'list':
				# print(valtrooms)
				roomlist = []
				for room in valtrooms:
					roomlist.append(room["name"])
				self.update_settings_options(self.settings.children, 'roomname', roomlist)
				if key == "server":
					print("test")
					self.config.set('valt', 'roomname', None)
					self.config.set('valt', 'room', None)
					self.write_config()
					try:
						self.refresh_settings()
					except:
						pass
			else:
				self.update_settings_options(self.settings.children, 'roomname', [])
				self.config.set('valt', 'roomname', None)
				self.config.set('valt', 'room', None)
				try:
					self.refresh_settings()
				except:
					pass
				self.write_config()
		if self.valt.accesstoken != 0:
			self.connsuccess()
		else:
			self.connfailure()
		self.notification.dismiss()
	def on_config_change(self, config, section, key, value):
			if section == "valt":
				self.notification = self.msgbox("Applying Changes. Please wait...", height='150dp',title="Notification")
				self.event_valt_config_change = Clock.schedule_once(partial(self.valt_config_change,key,value), self.executedelay)
			elif section == "time":
				if key == "region":
					self.update_settings_options(self.settings.children, 'timezone', self.timezones[value])
				if key == "timezone":
					# ivs.ChangeTimeZone(value)
					# quit()
					pass
			elif section == "application":
				if key == "recbutton" or key == "privbutton":
					#print(key)
					#print(value)
					self.addremovebuttons()
				if key == "webpassword":
					ivs.resetwebpassword(value)
				if key == "webinterface":
					if int(value):
						ivs.enablewebinterface()
					else:
						ivs.disablewebinterface()
				if key == "pinlength":
					self.reinitialize()
				if key == "mode":
					self.reinitialize()
				if key == "streamtype":
					self.reinitialize()
				if key == "fps":
					self.reinitialize()
				if key == "resolution":
					self.reinitialize()
				if key == "audio":
					self.reinitialize()
				if key == "orientation":
					self.homescreen = self.config.get("application", "orientation") + "_Home_Screen"
					self.screenmgmt.current = self.homescreen
					self.reinitialize()
			elif section == "network":
				if key.find("mode") > 0 and value == "DHCP":
					nic = key[0:key.find("mode")]
					self.config.set("network",nic+"ipaddress",None)
					self.config.set("network", nic + "gateway", None)
					self.config.set("network", nic + "dns1", None)
					self.config.set("network", nic + "dns2", None)
					self.config.set("network", nic + "subnet", None)
				# os.system("sudo /usr/bin/php /usr/local/ivs/network.php")

	def reinitialize(self):
		self.notification = self.msgbox("Applying Changes. Please wait...", height='150dp',title="Notification")
		self.event_initalize = Clock.schedule_once(self.initialize, self.executedelay)
	def initialize(self,b):
		ivs.log("Initializing Application", self.logpath)
		self.config.read(self.configfilepath)
		threading.Thread(target=self.connecttovalt).start()
	def connecttovalt(self):
		self.valt = ivs.valt(self.config.get("valt","server"),self.config.get("valt","username"),self.config.get("valt","password"),self.logpath)
		if self.valt.accesstoken != 0:
			self.connsuccess()
		else:
			self.connfailure()
	def checkconfigfiles(self,dt):
		# pass
		# ivs.log("Check Config Files for Changes",self.logpath)
		if self.updatedconfig:
			self.updatedconfig = False
		else:
			if os.path.exists(self.configfilepath):
				if (time.time() - os.path.getmtime(self.configfilepath)) <= self.configfilerechecktime:
					self.initialize(1)
					try:
						self.refresh_settings()
					except:
						pass
	@mainthread
	def connsuccess(self):
		#Add Widget to LeftWindow
		self.load_app_window()
		ivs.log("Connection Successful",self.logpath)
		self.config.set('valt','status','Connected')
		roomname = self.valt.getroomname(self.config.get("valt","room"))
		try:
			self.event_checkroomstatus.cancel()
		except:
			pass
		
		if roomname == 0:
			self.update_feedback(self.valt.errormsg,(1,0,0,1))
		else:
			self.screenmgmt.get_screen(self.homescreen).ids['display_room_name'].text = str(roomname)
			self.clear_feedback()
			self.checkroomstatusthread(1)
			self.addremovebuttons()
		try:
			self.event_recording.cancel()
		except:
			pass
		try:
			self.event_checkvalt.cancel()
		except:
			pass
		self.event_checkroomstatus = Clock.schedule_interval(self.checkroomstatusthread,self.roomchecktime)
		try:
			self.notification.dismiss()
		except:
			pass
	@mainthread
	def connfailure(self):
		self.config.set('valt', 'status', 'Not Connected')
		try:
			self.event_checkvalt.cancel()
		except:
			pass
		self.screenmgmt.get_screen(self.homescreen).ids['privacy_layout'].clear_widgets()
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].clear_widgets()
		self.screenmgmt.get_screen(self.homescreen).ids['display_room_name'].text = ""
		self.update_feedback("Unable to connect to VALT",(1,0,0,1))
		self.event_checkvalt = Clock.schedule_interval(self.checkvalt,1)
		try:
			self.event_checkroomstatus.cancel()
		except:
			pass
		#self.valt.auth()
		try:
			self.notification.dismiss()
		except:
			pass
	def checkvalt(self,dt):
		#ivs.log("Check Valt",self.logpath)
		if self.valt.accesstoken != 0:
			self.connsuccess()
	def initiaterecording(self):
		self.update_feedback("Initiating Recording",(0,0,0,1))
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].clear_widgets()
		self.screenmgmt.get_screen(self.homescreen).ids['privacy_layout'].clear_widgets()
		# self.event_startrecording = Clock.schedule_once(self.startrecording,self.executedelay)
		try:
			self.event_checkroomstatus.cancel()
		except:
			pass
		threading.Thread(target=self.startrecording).start()
	def initiatestop(self):
		self.update_feedback("Stopping Recording",(0,0,0,1))
		self.screenmgmt.get_screen(self.homescreen).ids['recording_time'].text = ""
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].clear_widgets()
		# self.event_stoprecording = Clock.schedule_once(self.stoprecording,self.executedelay)
		try:
			self.recevent.cancel()
		except:
			pass
		try:
			self.event_checkroomstatus.cancel()
		except:
			pass
		threading.Thread(target=self.stoprecording).start()
	def initiatepause(self):
		self.update_feedback("Pausing Recording",(0,0,0,1))
		self.screenmgmt.get_screen(self.homescreen).ids['recording_time'].text = ""
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].clear_widgets()
		# self.event_pauserecording = Clock.schedule_once(self.pauserecording,self.executedelay)
		try:
			self.recevent.cancel()
		except:
			pass
		try:
			self.event_checkroomstatus.cancel()
		except:
			pass
		threading.Thread(target=self.pauserecording).start()
	def initiateresume(self):
		self.update_feedback("Resuming Recording",(0,0,0,1))
		self.screenmgmt.get_screen(self.homescreen).ids['recording_time'].text = ""
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].clear_widgets()
		# self.event_resumerecording = Clock.schedule_once(self.resumerecording,self.executedelay)
		try:
			self.event_checkroomstatus.cancel()
		except:
			pass
		threading.Thread(target=self.resumerecording).start()
	def startrecording(self):
		if self.valt.startrecording(self.config.get("valt","room"),self.config.get("valt","recname")) != 0:
			self.updrecon()
		self.event_checkroomstatus = Clock.schedule_interval(self.checkroomstatusthread,self.roomchecktime)
	def stoprecording(self):
		if self.valt.stoprecording(self.config.get("valt","room")) != 0:
			self.updrecoff()
		self.event_checkroomstatus = Clock.schedule_interval(self.checkroomstatusthread,self.roomchecktime)
	def pauserecording(self):
		if self.valt.pauserecording(self.config.get("valt","room")) != 0:
			self.updpause()
			# self.clear_feedback()
		self.event_checkroomstatus = Clock.schedule_interval(self.checkroomstatusthread,self.roomchecktime)
	def resumerecording(self):
		if self.valt.resumerecording(self.config.get("valt","room")) != 0:
			self.updrecon()
			# self.clear_feedback()
		self.event_checkroomstatus = Clock.schedule_interval(self.checkroomstatusthread,self.roomchecktime)
	@mainthread
	def updrecon(self):
		self.clear_feedback()
		self.screenmgmt.get_screen(self.homescreen).ids.recording_time.color = (1,0,0,1)
		self.screenmgmt.get_screen(self.homescreen).ids['display_room_name'].color = (1, 0, 0, 1)
		if int(self.config.get('application','recbutton')):
			self.addpausestopbuttons()
		#lbl = Label(size_hint=(.6,1))
		#self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].add_widget(lbl)
		self.recevent = Clock.schedule_interval(self.updrectime,1)
		self.recstarttime = time.time() - self.valt.getrecordingtime(self.config.get("valt","room"))
		# self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].padding = 2
		# self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].spacing = 10
		self.screenmgmt.get_screen(self.homescreen).ids['privacy_layout'].clear_widgets()
	@mainthread
	def updrecoff(self):
		self.clear_feedback()
		if int(self.config.get('application', 'recbutton')):
			self.addrecordingbutton()
		if int(self.config.get('application','privbutton')):
			self.addlockbutton()
		try:
			self.recevent.cancel()
		except:
			pass
		self.recstarttime = 0
		self.screenmgmt.get_screen(self.homescreen).ids.recording_time.text = ""
		if self.config.get("application", "orientation") == "Landscape":
			self.screenmgmt.get_screen(self.homescreen).ids['display_room_name'].color = (.38,.38,.38,1)
		else:
			self.screenmgmt.get_screen(self.homescreen).ids['display_room_name'].color = (1, 1, 1, 1)

	@mainthread
	def updpause(self):
		self.clear_feedback()
		try:
			self.recevent.cancel()
		except:
			pass
		if int(self.config.get('application', 'recbutton')):
			self.addresumebutton()
		self.recstarttime = 0
		# self.screenmgmt.get_screen(self.homescreen).ids['recording_time'].text = "Recording Paused"
		# self.screenmgmt.get_screen(self.homescreen).ids['recording_time'].color = (1,.5,0,1)
		self.update_feedback("Recording Paused",(1,.5,0,1))

	@mainthread
	def updlock(self):
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].clear_widgets()
		self.update_feedback("Room is Locked",(0,0,0,1))
		self.addunlockbutton()
	@mainthread
	def updprepared(self):
		self.update_feedback("Room is Prepared",(0,0,0,1))
	@mainthread
	def updrectime(self,dt):
		if self.config.get("application", "orientation") == "Landscape":
			self.screenmgmt.get_screen(self.homescreen).ids.recording_time.text = "Recording: " + str(timedelta(seconds=int(time.time() - self.recstarttime)))
		else:
		 	self.screenmgmt.get_screen(self.homescreen).ids.recording_time.text = str(timedelta(seconds=int(time.time() - self.recstarttime)))

	@mainthread
	def updatetime(self, dt):
		#Clock only displays if in Landscape Mode
		self.screenmgmt.get_screen("Landscape_Home_Screen").ids.display_clock.text = time.strftime('%I:%M %p')
		self.screenmgmt.get_screen("Landscape_Home_Screen").ids.display_date.text = time.strftime('%A, %B %d')
	def open_auth(self):
		self.authpopup = self.msgbox('Enter the device password below to access the settings screen.',textinput=True,textaction=self.check_admin_auth,password=True,yesno=True,yestext='OK',yesaction=self.check_admin_auth,notext='Cancel',feedback="",title="Admin Authentication")
	def check_admin_auth(self,x):
		# print(x)
		if self.config.get('application', 'settingspassword') == self.authpopup.ids['password'].text:
			self.authpopup.dismiss()
			self.open_settings()
		else:
			self.authpopup.ids['feedback'].text = "Invalid Password"
	def gotosettings(self,x):
		if self.config.get('application','settingspassword') == self.screenmgmt.get_screen('Authentication_Screen').ids.auth_password.text:
			# self.screenmgmt.current = 'Settings_Screen'
			self.screenmgmt.get_screen('Authentication_Screen').ids.login_error.text = ""
			self.screenmgmt.get_screen('Authentication_Screen').ids.auth_password.text = ""
			# self.populatesettings()

			self.open_settings()
			self.screenmgmt.current = self.homescreen
		else:
			self.screenmgmt.get_screen('Authentication_Screen').ids.login_error.text = "Incorrect Password"
			self.screenmgmt.get_screen('Authentication_Screen').ids.auth_password.text = ""
	@mainthread
	def addrecordingbutton(self):
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].clear_widgets()
		# if self.config.get("application", "orientation") == "Landscape":
		btn = ImageButton(id='start_button', size_hint=(1, 1), source=self.imagepath + 'Start_Rec.png', upimage=self.imagepath + 'Start_Rec.png', downimage=self.imagepath + 'Start_Rec_down.png', always_release=True, on_release=lambda x: self.initiaterecording())
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].add_widget(btn)
		# else:
		# 	btn = ImageButton(id='start_button', size_hint=(1, 1), source=self.imagepath + 'record_icon.png', upimage=self.imagepath + 'record_icon.png', downimage=self.imagepath + 'record_icon.png', always_release=True, on_release=lambda x: self.initiaterecording())
		# 	self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].add_widget(btn)
		# 	label = Label(size_hint=(1,1))
		# 	self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].add_widget(label)
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].padding = 0
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].spacing = 10
	@mainthread
	def addunlockbutton(self):
		self.screenmgmt.get_screen(self.homescreen).ids['privacy_layout'].clear_widgets()
		if self.config.get("application", "orientation") == "Landscape":
			btn = ImageButton(id="privacy_button", size_hint=(1, 1), source=self.imagepath + 'Room_locked.png', upimage=self.imagepath + 'Room_locked.png', downimage=self.imagepath + 'Room_locked_down.png', always_release=True, on_release=lambda x: self.initiatedisableprivacy())
		else:
			btn = ImageButton(id="privacy_button", size_hint=(1, 1), source=self.imagepath + 'locked_icon.png', upimage=self.imagepath + 'locked_icon.png', downimage=self.imagepath + 'locked_icon.png', always_release=True, on_release=lambda x: self.initiatedisableprivacy())
		self.screenmgmt.get_screen(self.homescreen).ids['privacy_layout'].add_widget(btn)
	@mainthread
	def addlockbutton(self):
		self.screenmgmt.get_screen(self.homescreen).ids['privacy_layout'].clear_widgets()
		if self.config.get("application", "orientation") == "Landscape":
			btn = ImageButton(id="privacy_button", size_hint=(1, 1), source=self.imagepath + 'Room_unlocked.png', upimage=self.imagepath + 'Room_unlocked.png', downimage=self.imagepath + 'Room_unlocked_down.png', always_release=True, on_release=lambda x: self.initiateprivacy())
		else:
			btn = ImageButton(id="privacy_button", size_hint=(1, 1), source=self.imagepath + 'unlocked_icon.png', upimage=self.imagepath + 'unlocked_icon.png',	downimage=self.imagepath + 'unlocked_icon.png', always_release=True, on_release=lambda x: self.initiateprivacy())
		self.screenmgmt.get_screen(self.homescreen).ids['privacy_layout'].add_widget(btn)
	@mainthread
	def addpausestopbuttons(self):
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].clear_widgets()
		# if self.config.get("application", "orientation") == "Landscape":
		btn = ImageButton(id="pause_button", size_hint=(1, 1), source=self.imagepath + 'small_pause.png', upimage=self.imagepath + 'small_pause.png', downimage=self.imagepath + 'small_pause_down.png', always_release=True, on_release=lambda x: self.initiatepause())
		# else:
		# 	btn = ImageButton(id="pause_button", size_hint=(1, 1), source=self.imagepath + 'pause_icon.png', upimage=self.imagepath + 'pause_icon.png', downimage=self.imagepath + 'pause_icon.png', always_release=True, on_release=lambda x: self.initiatepause())
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].add_widget(btn)
		# if self.config.get("application", "orientation") == "Landscape":
		btn = ImageButton(id="stop_button", size_hint=(1, 1), source=self.imagepath + 'small_stop.png', upimage=self.imagepath + 'small_stop.png', downimage=self.imagepath + 'small_stop_down.png', always_release=True, on_release=lambda x: self.initiatestop())
		# else:
		# 	btn = ImageButton(id="stop_button", size_hint=(1, 1), source=self.imagepath + 'stop_icon.png', upimage=self.imagepath + 'stop_icon.png', downimage=self.imagepath + 'stop_icon.png', always_release=True, on_release=lambda x: self.initiatestop())
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].add_widget(btn)
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].padding = 2
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].spacing = 4
	@mainthread
	def addresumebutton(self):
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].clear_widgets()
		# if self.config.get("application", "orientation") == "Landscape":
		btn = ImageButton(size_hint=(1,1),source=self.imagepath + 'resume.png',upimage=self.imagepath + 'resume.png',downimage=self.imagepath + 'resume_down.png',always_release=True,on_release= lambda x: self.initiateresume())
		# else:
		# 	btn = ImageButton(size_hint=(1, 1), source=self.imagepath + 'resume_icon.png', upimage=self.imagepath + 'resume_icon.png', downimage=self.imagepath + 'resume_icon.png', always_release=True, on_release=lambda x: self.initiateresume())
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].add_widget(btn)
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].ids['resume_button'] = btn
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].padding = 0
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].spacing = 0
	@mainthread
	def addremovebuttons(self):
		self.screenmgmt.get_screen(self.homescreen).ids['privacy_layout'].clear_widgets()
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].clear_widgets()
		if int(self.config.get('application','recbutton')):
			if self.recstarttime == 0:
				self.addrecordingbutton()
			else:
				self.addpausestopbuttons()
		if int(self.config.get('application', 'privbutton')):
			if self.recstarttime == 0:
				if self.valt.getroomstatus(self.config.get("valt", "room")) == 4:
					self.addunlockbutton()
				else:
					self.addlockbutton()

	def getnetworkinfo(self):
		lblwidth = 100
		for nic in netifaces.interfaces():
			#print(nic)
			if nic != 'lo':
				lbl = HeaderLabel(text=nic,size_hint_y=None,height=30,font_size=self.standardfontsize)
				self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].add_widget(lbl)
				layout = StandardGridLayout(cols=2,row_default_height=30, size_hint_x=1,size_hint_y=None,spacing=10)
				self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].add_widget(layout)
				self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].ids[nic + '_layout'] = layout
				lbl = StandardTextLabel(text="MAC Address:", width=lblwidth, size_hint_x = None,size_hint_y=None,font_size=self.standardfontsize)
				textbox = DisabledTextInput(text=netifaces.ifaddresses(nic)[netifaces.AF_LINK][0]['addr'],size_hint_y=None,font_size=self.standardfontsize)
				self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].ids[nic + '_layout'].add_widget(lbl)
				self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].ids[nic + '_layout'].add_widget(textbox)
				for conf in netifaces.ifaddresses(nic):
					for x in netifaces.ifaddresses(nic)[conf]:
						#try:
						if ivs.is_ipv4(x['addr']):
							lbl = StandardTextLabel(text="IP:", width=lblwidth, size_hint_x = None,size_hint_y=None,font_size=self.standardfontsize)
							textbox = DisabledTextInput(text=x['addr'],size_hint_y=None,font_size=self.standardfontsize)
							self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].ids[nic + '_layout'].add_widget(lbl)
							self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].ids[nic + '_layout'].add_widget(textbox)
							if "netmask" in x:
								lbl = StandardTextLabel(text="Subnet Mask:", width=lblwidth, size_hint_x = None,size_hint_y=None,font_size=self.standardfontsize)
								textbox = DisabledTextInput(text=x['netmask'],size_hint_y=None,font_size=self.standardfontsize)
								self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].ids[nic + '_layout'].add_widget(lbl)
								self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].ids[nic + '_layout'].add_widget(textbox)
						#except:
						#		pass
				lbl = StandardTextLabel(size_hint_y=None,height=30)
				self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].add_widget(lbl)
		try:
			gateway=netifaces.gateways()['default'][netifaces.AF_INET][0]
		except:
			gateway="None"
		lbl = HeaderLabel(text="Default Gateway",size_hint_y=None,height=30,font_size=self.standardfontsize)
		self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].add_widget(lbl)
		lbl = StandardTextLabel(text=gateway,size_hint_y=None,height=30,halign='center',font_size=self.standardfontsize)
		self.screenmgmt.get_screen('About_Screen').ids['network_info_layout'].add_widget(lbl)
		self.screenmgmt.current = 'About_Screen'
	def checkroomstatusthread(self, dt):
		threading.Thread(target=self.checkroomstatus).start()
	def checkroomstatus(self):
		curroomstatus = self.valt.getroomstatus(self.config.get("valt", "room"))
		if curroomstatus != self.lastroomstatus:
			self.lastroomstatus = curroomstatus
			self.updroomstatus(curroomstatus)
	@mainthread
	def updroomstatus(self,curroomstatus):
		# ivs.log("Check Room",self.logpath)
		if self.valt.errormsg == None:
			self.clear_feedback()
			pass
		else:
			self.update_feedback(self.valt.errormsg,(1,0,0,1))
		if self.valt.accesstoken != 0:

			#ivs.log(curroomstatus,self.logpath)
			if curroomstatus == 2:
				if self.recstarttime == 0:
					self.updrecon()
					self.valt.errormsg = None
			elif curroomstatus == 1:
				if not self.screenmgmt.get_screen(self.homescreen).ids.recording_time.text == "":
					self.updrecoff()
					self.valt.errormsg = None
			elif curroomstatus == 0:
				self.update_feedback(self.valt.errormsg,(1,0,0,1))
				self.valt.errormsg = None
			elif curroomstatus == 3:
				self.updpause()
				self.valt.errormsg = None
			elif curroomstatus == 4:
				self.updlock()
				self.valt.errormsg = None
			elif curroomstatus == 5:
				self.updprepared()
				self.valt.errormsg = None
			else:
				pass
		else:
			self.connfailure()
	def startnetworksave(self):
		self.networkpopup = self.msgbox("Device is currently applying network settings.",height='150dp',title="Notification")
		self.event_accessorynetworksave = Clock.schedule_once(self.savenetworkconfig,1)
	def savenetworkconfig(self,dt):
		# os.system("sudo /usr/bin/php /usr/local/ivs/network.php")
		os.system("sudo netplan apply")
		# self.screenmgmt.current = "self.homescreen"
		self.networkpopup.dismiss()
		# self.open_settings()
	def startfactorydefault(self,x):
		self.factorydefaultpopup.dismiss()
		# self.screenmgmt.current="Factory_Default_In_Progress_Screen"
		self.close_settings()
		self.msgbox ("Device is currently resetting to factory defaults. Please wait...",height='150dp',title="Notification")
		self.event_accessoryfactorydefault = Clock.schedule_once(self.accessoryfactorydefault,1)
	def accessoryfactorydefault(self,dt):
		# print(self.config.filename)
		# ivs.factory_default(self.config.filename)
		os.remove("config/accessory.ini")
		quit()
	def initiateprivacy(self):
		self.update_feedback("Locking Room",(0,0,0,1))
		self.screenmgmt.get_screen(self.homescreen).ids['privacy_layout'].clear_widgets()
		self.screenmgmt.get_screen(self.homescreen).ids['recording_layout'].clear_widgets()
		try:
			self.event_checkroomstatus.cancel()
		except:
			pass
		threading.Thread(target=self.enableprivacy).start()
	def initiatedisableprivacy(self):
		self.update_feedback("Unlocking Room",(0,0,0,1))
		self.screenmgmt.get_screen(self.homescreen).ids['recording_time'].text = ""
		try:
			self.event_checkroomstatus.cancel()
		except:
			pass
		self.screenmgmt.get_screen(self.homescreen).ids['privacy_layout'].clear_widgets()
		threading.Thread(target=self.disableprivacy).start()
	def enableprivacy(self):
		# if self.valt.getroomstatus(self.config.get("valt","room")) == 1:
		self.valt.lockroom(self.config.get("valt","room"))
		self.updlock()
		self.event_checkroomstatus = Clock.schedule_interval(self.checkroomstatusthread, self.roomchecktime)
	def disableprivacy(self):
		self.valt.unlockroom(self.config.get("valt","room"))
		if int(self.config.get('application', 'recbutton')):
			self.addrecordingbutton()
		self.addlockbutton()
		self.clear_feedback()
		self.event_checkroomstatus = Clock.schedule_interval(self.checkroomstatusthread, self.roomchecktime)
	def restart(self):
		quit()
	def reboot(self):
		os.system("sudo reboot")
	def StartPopulateSSID(self,nic):
		self.ssidpopup = self.msgbox("Select a wireless network", scrollbox=True, okbutton=True, oktext='Cancel',height=400,title="Wireless Networks")
		self.event_PopulateSSID = Clock.schedule_once(self.PopulateSSID,1)
		lbl = StandardTextLabel(text="Scanning...")
		self.ssidpopup.ids['scrollbox'].add_widget(lbl)
		self.ssidnic = nic
	def PopulateSSID(self,dt):
		self.ssidlist = ivs.getSSIDs(self.ssidnic)
		# self.ssidlist = ['Wifi 1','Wifi 2','Wifi 3','Wifi 4','Wifi 5','Wifi 6']
		self.ssidpopup.ids['scrollbox'].clear_widgets()
		for ssid in self.ssidlist:
			btn = Button(text=ssid,on_release=lambda x: self.set_ssid(x.text))
			# btn = Button(text=ssid,on_release=lambda x: self.config.set("network",self.ssidnic + "ssid",x.text))
			# btn = Button(text=ssid,on_release=lambda x: print(x.text))
			self.ssidpopup.ids['scrollbox'].add_widget(btn)
		self.ssidpopup.ids['scrollbox'].height = len(self.ssidlist) * dp(55)
	def set_ssid(self,ssid):
		self.ssidpopup.dismiss()
		self.config.set("network", self.ssidnic + "ssid", ssid)
		self.write_config()
		try:
			self.refresh_settings()
		except:
			pass
		# print(self.ssidnic + "ssid")
		# print(ssid)
	def build_network_settings(self):
		self.networkjson = []
		self.build_settings_json(self.networkjson,settype="title",title="Network changes will be applied either on reboot or by using the Apply Network Settings button in the system menu.")
		for nic in netifaces.interfaces():
			#print(nic)
			i=0
			if nic != 'lo':
				self.build_settings_json(self.networkjson,settype="title",title=nic)
				self.build_settings_json(self.networkjson,settype="title",title="IPv4")
				self.build_settings_json(self.networkjson,settype="options",title="Mode",desc="Configuration Mode",section="network",key=str(nic) + "mode",options=['DHCP','STATIC'],default="DHCP")
				self.build_settings_json(self.networkjson,settype="ip",title="IP Address",desc="IPv4 Address",section="network",key=str(nic) + "ipaddress",default=None)
				self.build_settings_json(self.networkjson,settype="scrolloptions",title="Subnet Mask",desc="CIDR",section="network",key=str(nic) + "subnet",options=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32"],default="24")
				self.build_settings_json(self.networkjson,settype="ip",title="Gateway",desc="Default Gateway",section="network",key=str(nic) + "gateway",default=None)
				self.build_settings_json(self.networkjson,settype="ip",title="Primary DNS",desc="Primary Domain Name Server",section="network",key=str(nic) + "dns1",default=None)
				self.build_settings_json(self.networkjson,settype="ip",title="Secondary DNS",desc="Secondary Domain Name Server",section="network",key=str(nic) + "dns2",default=None)
				if nic[0] == "w" or nic[0] == "{":
					self.build_settings_json(self.networkjson,settype="title", title="Wireless")
					self.build_settings_json(self.networkjson,settype="string",title="SSID",desc="Wireless Network SSID",section="network",key=str(nic) + "ssid",default=None)
					self.build_settings_json(self.networkjson,settype="button",title="Scan for Wireless Networks",section="network",key=str(nic) + "scan",default=None)
					self.build_settings_json(self.networkjson,settype="bool",title="Hidden",desc="Hidden SSID",section="network",key=str(nic) + "hidden",default=None)
					self.build_settings_json(self.networkjson,settype="options", title="Type", desc="Authentication Type", section="network", key=str(nic) + "authtype", options=["WEP", "WPA", "WPA2"], default="WPA2")
					self.build_settings_json(self.networkjson,settype="options",title="Mode",desc="WPA Mode",section="network",key=str(nic) + "wpa2mode",options=["Personal","Enterprise"],default="Personal")
					self.build_settings_json(self.networkjson,settype="string",title="Username",desc="Username for WPA Authentication",section="network",key=str(nic) + "username",default=None)
					self.build_settings_json(self.networkjson,settype="password",title="Password",desc="Password for WPA Authentication",section="network",key=str(nic) + "password",default=None)
					self.build_settings_json(self.networkjson,settype="options",title="Key Management",desc="Key Management for WPA",section="network",key=str(nic) + "keymgmt",options=["none","psk","eap","802.1"],default="none")
					self.build_settings_json(self.networkjson,settype="options",title="Method",desc="WPA Method",section="network",key=str(nic) + "wpamethod",options=["peap","tls","ttls"],default="peap")
	def build_settings_json(self,settingsjson,**kwargs):
		settingsjson.append({})
		if 'settype' in kwargs:
			settingsjson[len(settingsjson)-1]["type"] = kwargs['settype']
		if 'title' in kwargs:
			# if kwargs['settype'] == 'title':
			# 	settingsjson[len(settingsjson) - 1]["title"] = nic + " " + kwargs['title']
			# else:
			# 	settingsjson[len(settingsjson)-1]["title"] = kwargs['title']
			settingsjson[len(settingsjson)-1]["title"] = kwargs['title']
		if 'desc' in kwargs:
			settingsjson[len(settingsjson) - 1]["desc"] = kwargs['desc']
		if 'section' in kwargs:
			settingsjson[len(settingsjson) - 1]["section"] = kwargs['section']
		if 'key' in kwargs:
			settingsjson[len(settingsjson) - 1]["key"] = kwargs['key']
		if 'options' in kwargs:
			settingsjson[len(settingsjson) - 1]["options"] = kwargs['options']
		if 'default' in kwargs:
			self.config.setdefault( kwargs['section'], kwargs['key'],  kwargs['default'])
	def build_time_settings(self):
		self.timezones = ivs.loadconfig(self.timezonefilepath)
		regionlist=[]
		timezonelist=[]
		self.timejson = []
		if type(self.timezones).__name__ == 'dict':
			for region in self.timezones.keys():
				regionlist.append(region)
		region = self.config.get('time','region')
		if region in self.timezones:
			if type(self.timezones[region]).__name__ == 'list':
				for timezone in self.timezones[region]:
					timezonelist.append(timezone)
		self.build_settings_json(self.timejson,settype="title",title = "Time Zone")
		self.build_settings_json(self.timejson,settype="scrolloptions",title="Region",desc="Time Zone Region",section="time",key="region",options=regionlist,default="America")
		self.build_settings_json(self.timejson,settype="scrolloptions",title="Time Zone",desc="Changing this setting will restart the application.",section="time",key="timezone",options=timezonelist,default="America/Chicago")
	def build_valt_settings(self):
		self.valtjson = []
		roomlist=[]
		valtrooms = self.valt.getrooms()
		if type(valtrooms).__name__ == 'list':
			for room in valtrooms:
				roomlist.append(room["name"])
		self.build_settings_json(self.valtjson,settype="title",title="Valt Server")
		self.build_settings_json(self.valtjson, settype="string", title="Server", desc="Valt Server Address (include https:// if using SSL/TLS)", section="valt", key="server")
		self.build_settings_json(self.valtjson, settype="string", title="Username", desc="Valt Username (Must Have Admin Access)", section="valt", key="username")
		self.build_settings_json(self.valtjson, settype="password", title="Password", desc="Valt Password", section="valt", key="password")
		self.build_settings_json(self.valtjson, settype="string", title="Recording Name", desc="Default name for all recordings initiated from this device.", section="valt", key="recname")
		self.build_settings_json(self.valtjson, settype="scrolloptions", title="Room", desc="VALT Room", section="valt", key="roomname",options=roomlist)
	def build_application_settings(self):
		self.applicationjson = []
		modelist=["Camera Control","Schedule","Keypad","None"]
		orientationlist= ["Landscape","Portrait"]
		streamtypelist = ["H264", "MJPG"]
		resolutionlist = ["640x480", "800x450", "1280x720","1920x1080"]
		fpslist = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
		self.build_settings_json(self.applicationjson, settype="title", title="Application Settings")
		self.build_settings_json(self.applicationjson, settype="password", title="Password", desc="Password to Access the Settings Menu", section="application", key="settingspassword")
		self.build_settings_json(self.applicationjson, settype="scrolloptions", title="Orientation", desc="Application to Display Orientation", section="application", key="orientation", options=orientationlist, default="Landscape")
		self.build_settings_json(self.applicationjson, settype="scrolloptions", title="Mode", desc="Appplication to Display in Primary Window", section="application", key="mode", options=modelist, default="Camera Control")
		self.build_settings_json(self.applicationjson, settype="title", title="Camera Control Settings")
		self.build_settings_json(self.applicationjson, settype="scrolloptions", title="Stream Type", desc="Stream Type to use in Camera Control Mode", section="application", key="streamtype", options=streamtypelist, default="H264")
		self.build_settings_json(self.applicationjson, settype="scrolloptions", title="Resolution", desc="Resolution to use in Camera Control Mode", section="application", key="resolution", options=resolutionlist, default="800x450")
		self.build_settings_json(self.applicationjson, settype="scrolloptions", title="FPS", desc="Frames Per Second to use in Camera Control Mode", section="application", key="fps", options=fpslist, default="30")
		self.build_settings_json(self.applicationjson, settype="bool", title="Audio",desc="Enable/Disable Audio", section="application", key="audio", default=0)
		self.build_settings_json(self.applicationjson, settype="title", title="Keypad Settings")
		self.build_settings_json(self.applicationjson, settype="numeric", title="Pin Length", desc="Length of Keypad Pin Code", section="application", key="pinlength", default=6)
		# self.build_settings_json(self.applicationjson, settype="title", title="Web Interface")
		# self.build_settings_json(self.applicationjson, settype="bool", title="Web Interface", desc="Enable/Disable the Web Interface", section="application", key="webinterface")
		# self.build_settings_json(self.applicationjson, settype="password", title="Web Password", desc="Password to Access the Web Interface", section="application", key="webpassword")
		self.build_settings_json(self.applicationjson, settype="title", title="Buttons")
		self.build_settings_json(self.applicationjson, settype="bool", title="Recording Button", desc="Enable/Disable the Recording Button", section="application", key="recbutton")
		self.build_settings_json(self.applicationjson, settype="bool", title="Lock Button", desc="Enable/Disable the Lock Button", section="application", key="privbutton")
	def build_settings_defaults(self):
		self.defaultsjson = {}
		self.defaultsjson['application'] = {"settingspassword":"admin51","mode":"None","webinterface": "1","webpassword": None,"recbutton":"1","privbutton":"1","orientation":"Landscape","streamtype":"H264"}
		self.defaultsjson['valt'] = {"server": None,"username": None,"password": None,"recname": "Accessory Recording","roomname": None,"room": None,"status": None}
		self.defaultsjson['time'] = {"region": "America","timezone": "America/Chicago","ntp": None}
		self.defaultsjson['network'] = {"mode": "DHCP","ipaddress": None,"subnet": "24","gateway": None,"dns1": None,"dns2": None,"ssid": None,"hidden": None,"authtype": "WPA2","wpamode": "Personal","username": None,"password": None,"wpakey": "none","wpamethod": "peap"}
		self.defaultsjson['system'] = {"reload":None,"reboot":None,"factory":None,"applynetwork":None}
	def build_system_settings(self):
		self.systemjson = []
		# self.build_settings_json(self.systemjson,settype="title",title="System")
		self.build_settings_json(self.systemjson,settype="button",title="Reload Application",section="system",key="reload",default=None)
		# self.build_settings_json(self.systemjson, settype="button", title="Reboot",section="system",key="reboot",default=None)
		self.build_settings_json(self.systemjson, settype="button", title="Factory Default",section="system",key="factory",default=None)
		# self.build_settings_json(self.systemjson, settype="button", title="Apply Network Configuration", section="system",key="applynetwork", default=None)
	def update_settings_options(self,object,searchterm,newvalues):
		for child in object:
			try:
				if child.key == searchterm:
					child.options = newvalues
			except:
				pass
			self.update_settings_options(child.children,searchterm,newvalues)
	def process_settings_button(self,key):
		if key == "reload":
			self.restart()
		elif key == "reboot":
			self.reboot()
		elif key == "factory":
			# self.screenmgmt.current = "Factory_Default_Screen"
			# self.close_settings()
			# self.open_factory_default()
			self.factorydefaultpopup = self.msgbox('Are you sure you want to reset the device to factory defaults?',yesno=True, yesaction=self.startfactorydefault,title="Confirmation")
		elif key == "applynetwork":
			# self.screenmgmt.current = "Network_Save_In_Progress_Screen"
			# self.close_settings()
			self.startnetworksave()
		elif key.find("scan") >= 0:
			# self.close_settings()
			self.StartPopulateSSID(key[0:key.find("scan")])

	def msgbox(self, message, **kwargs):
		content = BoxLayout(orientation='vertical', spacing='5dp')
		if 'width' in kwargs:
			popup_width = kwargs['width']
		else:
			popup_width = min(0.95 * Window.width, dp(500))
		if 'height' in kwargs:
			popup_height = kwargs['height']
		else:
			popup_height='250dp'
		if 'title' in kwargs:
			popup_title = kwargs['title']
		else:
			popup_title = ""
		popupbox = Popup(title=popup_title, content=content, size_hint=(None, None),size=(popup_width, popup_height), separator_color=(255 / 255, 122 / 255, 43 / 255, 1))
		# popupbox.title_size = popupbox.width/30
		# content.add_widget(Widget())
		# label = Label(size_hint_y=None, height='15', text=str(message))
		label = WrappedLabel(size_hint_y=None, text=str(message), halign='center', valign='center')
		content.add_widget(label)

		content.add_widget(Widget())
		if 'textinput' in kwargs:
			if kwargs['textinput']:
				textinput = TextInput(font_size='24sp', multiline=False,size_hint_y=None, height='42sp')
				if 'textaction' in kwargs:
					textinput.bind(on_text_validate=kwargs['textaction'])
				if 'password' in kwargs:
					if kwargs['password'] == True:
						textinput.password = True
				popupbox.ids['password'] = textinput
				content.add_widget(textinput)
		if 'scrollbox' in kwargs:
			if kwargs['scrollbox']:
				scroll_view= ScrollView(always_overscroll=False, size_hint=(1, None), height=dp(kwargs['height']-175))
				box_layout = BoxLayout(orientation='vertical', spacing='5dp', size_hint=(1, None))
				popupbox.ids['scrollbox'] = box_layout
				# for x in range(10):
				# 	box_layout.add_widget(Button(text=str(x)))
				# box_layout.height = 10 * dp(55)
				scroll_view.add_widget(box_layout)
				content.add_widget(scroll_view)
		if 'feedback' in kwargs:
			label = Label(text=kwargs['feedback'])
			content.add_widget(Widget())
			content.add_widget(label)
			content.add_widget(Widget())
			popupbox.ids['feedback'] = label
		if 'okbutton' in kwargs:
			if kwargs['okbutton']:
				if 'oktext' in kwargs:
					btntext = kwargs['oktext']
				else:
					btntext = "OK"
				btn = Button(text=btntext, size_hint_y=None, height=dp(50))
				btn.bind(on_release=popupbox.dismiss)
				content.add_widget(btn)
		if "yesno" in kwargs:
			if kwargs['yesno']:
				btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
				if 'yestext' in kwargs:
					btntext = kwargs['yestext']
				else:
					btntext = 'Yes'
				btn = Button(text=btntext)
				if 'yesaction' in kwargs:
					btn.bind(on_release=kwargs['yesaction'])
				else:
					btn.bind(on_release=popupbox.dismiss)
				btnlayout.add_widget(btn)
				if 'notext' in kwargs:
					btntext = kwargs['notext']
				else:
					btntext = 'no'
				btn = Button(text=btntext)
				if 'noaction' in kwargs:
					btn.bind(on_release=kwargs['noaction'])
				else:
					btn.bind(on_release=popupbox.dismiss)
				btnlayout.add_widget(btn)
				content.add_widget(btnlayout)
		popupbox.open()
		return popupbox
	def write_config(self):
		self.config.write()
		self.updatedconfig = True
	def load_app_window(self):
		if self.config.get("application","mode") == "Camera Control":
			lw=CameraControl(self.valt,self.config.get("valt","room"),self.config.get("application","streamtype"),self.config.get("application","fps"),self.config.get("application","resolution"),self.config.get("application","audio"))
		elif self.config.get("application","mode") == "Schedule":
			lw=ScheduleDisplay(self.valt,self.config.get("valt","room"))
		elif self.config.get("application","mode") == "Keypad":
			 lw=Keypad(self.valt,self.config.get("valt","room"),int(self.config.get("application","pinlength")))
			# lw = Keypad(self.valt, self.config.get("valt", "room"), 6)
		self.screenmgmt.get_screen(self.homescreen).ids['app_window'].clear_widgets()
		if self.config.get("application","mode") != "None":
			self.screenmgmt.get_screen(self.homescreen).ids['app_window'].add_widget(lw)
		# else:
		# 	lw=BackgroundLabel(text="test",size_hint=(1,1),color='black',font_size=15)
		# 	lw.background_color=(0,0,0,1)
		# 	self.screenmgmt.get_screen(self.homescreen).ids['app_window'].add_widget(lw)
	@mainthread
	def update_feedback(self,newfeedback,newcolor=(0,0,0,1)):
		if self.screenmgmt.get_screen(self.homescreen).ids['feedback'].text != newfeedback:
			self.screenmgmt.get_screen(self.homescreen).ids['feedback'].text = newfeedback
		if self.screenmgmt.get_screen(self.homescreen).ids['feedback'].color != newcolor:
			self.screenmgmt.get_screen(self.homescreen).ids['feedback'].color = newcolor
	@mainthread
	def clear_feedback(self):
		if self.screenmgmt.get_screen(self.homescreen).ids['feedback'].text != "":
			self.screenmgmt.get_screen(self.homescreen).ids['feedback'].text = ""
	def go_to_home_screen(self):
		self.screenmgmt.current = self.homescreen
def printchildren(object,layer):
	for child in object:
		print(str(layer) + " " + str(child))
		try:
			print(child.text)
		except:
			pass
		printchildren(child.children, layer+1)

# class ThreadedApp(App):
#
#     def on_stop(self):
#         # The Kivy event loop is about to stop, set a stop signal;
#         # otherwise the app window will close, but the Python process will
#         # keep running until all secondary threads exit.
#         self.root.stop.set()
#
#     def build(self):
#         return IVS_Accessory_Framework()

if __name__ == '__main__':
	IVS_Accessory_Framework().run()
