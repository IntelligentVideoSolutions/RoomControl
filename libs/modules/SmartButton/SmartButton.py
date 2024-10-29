from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import mainthread
from kivy.properties import StringProperty, NumericProperty
from kivy.logger import Logger
from libs.modules.axis import axiscamera
from kivy.app import App
import threading
import time
from libs.pys.RoundedShadowButtonWithImage import RoundedShadowButtonWithImage

class SmartButton(RelativeLayout):
	recordingname = StringProperty("Test Recording")
	# button_font_size = "15sp"
	button_font_size = "45sp"
	buttons_list = {}
	def __init__(self, config,valt, room, **kwargs):
		super(SmartButton, self).__init__(**kwargs)
		self.config = config
		self.valt = valt
		self.valt.bind_to_selected_room_status(self.room_status_change)
		self.room = room
		self.start_cameras()
		self.define_buttons()
		self.enable_disable_buttons()


		# self.add_buttons()

	def define_buttons(self):
		#RECORDING BUTTON
		btn = RoundedShadowButtonWithImage(id='start_button', text="Start Recording", size_hint=(1, 1), color="black",
								   font_size=self.button_font_size, button_radius=10, button_color=(1, 1, 1, 1),
								   button_down_color=(220/255,220/255,220/255,1), img_source="images/record_icon.png",
								   always_release=True, on_release=lambda x: self.start_recording())
		self.buttons_list.update({'record_button': {'button': btn, 'enabled': False}})

		#COMMENT BUTTON
		btn = RoundedShadowButtonWithImage(id='comment_button', text="Add Comment", size_hint=(1, 1), color="black",
								   font_size=self.button_font_size, button_radius=10, button_color=(1, 1, 1, 1),
								   button_down_color=(220/255,220/255,220/255,1), img_source="images/comment_b.png",
								   always_release=True, on_release=lambda x: self.add_comment())
		self.buttons_list.update({'comment_button': {'button':btn,'enabled':False}})

		# PAUSE BUTTON
		btn = RoundedShadowButtonWithImage(id='pause_button', text="Pause Recording", size_hint=(1, 1), color="black",
										   font_size=self.button_font_size, button_radius=10, button_color=(1, 1, 1, 1),
										   button_down_color=(220/255,220/255,220/255,1), img_source="images/pause_icon.png",
										   always_release=True, on_release=lambda x: self.pause_recording())
		self.buttons_list.update({'pause_button': {'button': btn, 'enabled': False}})

		# RESUME BUTTON
		btn = RoundedShadowButtonWithImage(id='resume_button', text="Resume Recording", size_hint=(1, 1), color="black",
										   font_size=self.button_font_size, button_radius=10, button_color=(1, 1, 1, 1),
										   button_down_color=(220/255,220/255,220/255,1), img_source="images/resume_icon.png",
										   always_release=True, on_release=lambda x: self.resume_recording())
		self.buttons_list.update({'resume_button': {'button': btn, 'enabled': False}})

		# STOP BUTTON
		btn = RoundedShadowButtonWithImage(id='stop_button', text="Stop Recording", size_hint=(1, 1), color="black",
										   font_size=self.button_font_size, button_radius=10, button_color=(1, 1, 1, 1),
										   button_down_color=(220/255,220/255,220/255,1), img_source="images/stop_icon.png",
										   always_release=True, on_release=lambda x: self.stop_recording())
		self.buttons_list.update({'stop_button': {'button': btn, 'enabled': False}})

		#LOCK BUTTON
		btn = RoundedShadowButtonWithImage(id='lock_button', text="Room Unlocked", size_hint=(1, 1), color="black",
								   font_size=self.button_font_size, button_radius=10, button_color=(1, 1, 1, 1),
								   button_down_color=(220/255,220/255,220/255,1), img_source="images/unlocked_icon.png",
								   always_release=True, on_release=lambda x: self.lock_room())
		self.buttons_list.update({'lock_button': {'button':btn,'enabled':False}})

		#UNLOCK BUTTON
		btn = RoundedShadowButtonWithImage(id='unlock_button', text="Room Locked", size_hint=(1, 1), color="black",
								   font_size=self.button_font_size, button_radius=10, button_color=(1, 1, 1, 1),
								   button_down_color=(220/255,220/255,220/255,1), img_source="images/locked_icon.png",
								   always_release=True, on_release=lambda x: self.unlock_room())
		self.buttons_list.update({'unlock_button': {'button':btn,'enabled':False}})

		#PRIVACY BUTTON
		btn = RoundedShadowButtonWithImage(id='privacy_enable_button', text="Privacy Off", size_hint=(1, 1), color="black",
								   font_size=self.button_font_size, button_radius=10, button_color=(1, 1, 1, 1),
								   button_down_color=(220/255,220/255,220/255,1), img_source="images/priv_icon_4.png",
								   always_release=True, on_release=lambda x: self.toggle_privacy())
		self.buttons_list.update({'privacy_enable_button': {'button':btn,'enabled':False}})

		#PRIVACY BUTTON
		btn = RoundedShadowButtonWithImage(id='privacy_disable_button', text="Privacy On", size_hint=(1, 1), color="black",
								   font_size=self.button_font_size, button_radius=10, button_color=(1, 1, 1, 1),
								   button_down_color=(220/255,220/255,220/255,1), img_source="images/priv_icon_3.png",
								   always_release=True, on_release=lambda x: self.toggle_privacy())
		self.buttons_list.update({'privacy_disable_button': {'button':btn,'enabled':False}})


	def enable_disable_buttons(self):
		if int(self.config.get('smartbutton', 'record_button')):
			self.buttons_list['record_button']['enabled'] = True
		else:
			self.buttons_list['record_button']['enabled'] = False

		if int(self.config.get('smartbutton', 'privacy_button')):
			self.buttons_list['privacy_enable_button']['enabled'] = True
		else:
			self.buttons_list['privacy_enable_button']['enabled'] = False

		if int(self.config.get('smartbutton', 'comment_button')):
			self.buttons_list['comment_button']['enabled'] = True
		else:
			self.buttons_list['comment_button']['enabled'] = False
	def add_buttons(self):
		# if self.buttons_list:
		self.ids['main_window'].clear_widgets()
		for btn in self.buttons_list.values():
			if btn['enabled']:
				self.ids['main_window'].add_widget(btn['button'])
	def block_all_buttons(self):
		for btn in self.buttons_list.values():
			btn['enabled'] = False

	@mainthread
	def update_buttons(self,curroomstatus):
		Logger.debug("Updating Buttons")
		self.block_all_buttons()
		self.enable_buttons()
		if curroomstatus == 1 or curroomstatus == 5:
			if int(self.config.get('smartbutton', 'record_button')):
				self.buttons_list['record_button']['enabled'] = True
			if int(self.config.get('smartbutton', 'lock_button')):
				self.buttons_list['lock_button']['enabled'] = True
		elif curroomstatus == 2:
			if int(self.config.get('smartbutton', 'record_button')):
				self.buttons_list['stop_button']['enabled'] = True
				self.buttons_list['pause_button']['enabled'] = True
				self.buttons_list['comment_button']['enabled'] = True
		elif curroomstatus == 3:
			if int(self.config.get('smartbutton', 'record_button')):
				self.buttons_list['stop_button']['enabled'] = True
				self.buttons_list['resume_button']['enabled'] = True
				self.buttons_list['comment_button']['enabled'] = True
		elif curroomstatus == 4:
			if int(self.config.get('smartbutton', 'lock_button')):
				self.buttons_list['unlock_button']['enabled'] = True
		else:
			self.ids['main_window'].clear_widgets()
		if int(self.config.get('smartbutton', 'privacy_button')):
			if self.camera_control:
				if self.camera_control[0].privacy == 2:
					self.buttons_list['privacy_enable_button']['enabled'] = True
				elif self.camera_control[0].privacy == 1:
					self.buttons_list['privacy_disable_button']['enabled'] = True
		self.add_buttons()


	def do_nothing(self):
		pass
	def start_recording(self):
		# self.valt.startrecording(self.config.get("valt", "room"), self.config.get("valt", "recname"))
		self.disable_buttons()
		App.get_running_app().initiaterecording()
	def stop_recording(self):
		# self.valt.stoprecording(self.config.get("valt", "room"))
		self.disable_buttons()
		App.get_running_app().initiatestop()
	def enable_privacy(self):
		self.camera_control.toggle_privacy()
	def disable_privacy(self):
		self.camera_control.toggle_privacy()
	def add_comment(self):
		# self.valt.addcomment(self.config.get("valt", "room"),self.config.get("valt","markername"))
		App.get_running_app().initiatecomment()
	def pause_recording(self):
		# self.valt.pauserecording(self.config.get("valt", "room"))
		self.disable_buttons()
		App.get_running_app().initiatepause()
	def resume_recording(self):
		# self.valt.resumerecording(self.config.get("valt", "room"))
		self.disable_buttons()
		App.get_running_app().initiateresume()
	def lock_room(self):
		# self.valt.lockroom(self.config.get("valt", "room"))
		self.disable_buttons()
		App.get_running_app().initiatelock()
	def unlock_room(self):
		# self.valt.unlockroom(self.config.get("valt", "room"))
		self.disable_buttons()
		App.get_running_app().initiateunlock()
	def room_status_change(self,curroomstatus):
		self.update_buttons(curroomstatus)
	def get_cameras(self):
		self.cameralist = self.valt.getcameras(self.room)
		Logger.debug(self.cameralist)
	def connect_to_cameras(self):
		for camera in self.cameralist:
			self.camera_control.append(axiscamera.AxisCamera(camera["ip"], camera["username"], camera["password"]))
		for camera in self.camera_control:
			camera.bind_to_connected(self.camera_status_change)
			camera.bind_to_privacy(self.camera_privacy_change)
	def start_cameras(self):
		self.cameralist = None
		self.camera_control = []
		self.get_cameras()
		if self.cameralist != None:
			self.connect_to_cameras()
	def toggle_privacy(self):
		for camera in self.camera_control:
			camera.toggle_privacy()
		# self.update_buttons(self.valt.selected_room_status)

	@mainthread
	def camera_status_change(self,curcamstatus):
		Logger.debug("Camera Status Change")
		self.update_buttons(self.valt.selected_room_status)


	@mainthread
	def camera_privacy_change(self,curprivstatus):
		Logger.debug("Camera Privacy Change")
		self.update_buttons(self.valt.selected_room_status)
	def disconnect(self):
		self.ids['main_window'].clear_widgets()
		self.valt.unbind_to_selected_room_status(self.room_status_change)
		for camera in self.camera_control:
			camera.kill_threads = True
		self.camera_control = []
	@mainthread
	def disable_buttons(self):
		for btn in self.buttons_list.values():
			btn['button'].disabled = True
	@mainthread
	def enable_buttons(self):
		for btn in self.buttons_list.values():
			btn['button'].disabled = False