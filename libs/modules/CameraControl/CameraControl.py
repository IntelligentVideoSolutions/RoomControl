from kivy.uix.relativelayout import RelativeLayout

from kivy.clock import Clock, mainthread
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.video import Video
import threading
from libs.modules.axis import axiscamera
from libs.pys.RoundedShadowButton import RoundedShadowButton
from libs.pys.RoundedButton import RoundedButton
from libs.modules.ivs import ivs
from kivy.properties import NumericProperty, StringProperty

class CameraControl(RelativeLayout):
	vidtype = StringProperty("H264")
	fps = NumericProperty(30)
	resolution = StringProperty("800x450")
	volume = NumericProperty(0)
	my_camera = None
	def on_vidtype(self,instance,value):
		self.vidtype = value
		if self.my_camera != None:
			self.connect_to_camera()
	def on_fps(self,instance,value):
		self.fps = value
		if self.my_camera != None:
			self.connect_to_camera()
	def on_resolution(self,instance,value):
		self.resolution = value
		if self.my_camera != None:
			self.connect_to_camera()
	def on_volume(self,instance,value):
		self.volume = value
		# print(self.volume)
		if self.my_camera != None:
			self.my_camera.volume = self.volume
	def __init__(self, valt, room, **kwargs):
		super(CameraControl, self).__init__(**kwargs)
		self.valt = valt
		self.room = room
		# self.vidtype = vidtype
		# self.fps = fps
		# self.resolution = resolution
		# self.volume = volume
		self.panstepsize = 5
		self.tiltstepsize = 5
		self.zoomstepsize = 100
		# self.camera_address = camera_address
		# self.camera_username = camera_username
		# self.camera_password = camera_password
		self.repeat_interval = .25
		self.tilt_up_count = 0
		self.tilt_down_count = 0
		self.pan_left_count = 0
		self.pan_right_count = 0
		self.zoom_in_count = 0
		self.zoom_out_count = 0
		self.my_camera = None
		self.last_camera_loaded = False
		self.build()
	def build(self):
		#Builder.load_file('CameraControl.kv')
		threading.Thread(target=self.get_cameras).start()
		label = Label(text='Connecting to Camera. Please Wait...',color='black')
		self.ids['cam_window'].add_widget(label)
	def get_cameras(self):
		self.cameralist = self.valt.getcameras(self.room)
		# print(type(self.cameralist))
		self.build_camera_list()
	@mainthread
	def build_camera_list(self):
		if type(self.cameralist).__name__ == 'list':
			self.camera_dropdown = DropDown()
			for camera in self.cameralist:
				# btn = StandardButton(id=camera["id"], text=camera["name"], size_hint_y=None, height=44, color="white",background_color=(247/255,142/255,48/255,1),background_normal='', font_size='30sp')
				# btn = RoundedShadowButton(id=camera["id"], text=camera["name"], size_hint_y=None, height=44, color="black",font_size='30sp',button_radius=10, button_color=(247/255,142/255,48/255,1))
				btn = RoundedButton(id=camera["id"], text=camera["name"], size_hint_y=None, height=44, color="white",font_size='20sp',button_radius=10, button_color=(247/255,142/255,48/255,1),button_down_color=(247/255,142/255,48/255,1),always_release=True)
				btn.bind(on_release=lambda btn: self.camera_dropdown.select(btn.id))
				self.camera_dropdown.add_widget(btn)
			self.camera_dropdown.bind(on_select=lambda instance, x: self.selectcamera(x))
			self.camera_dropdown.container.spacing = 10
			self.camera_dropdown.container.padding = 10
			self.selectcamera(self.cameralist[0]["id"])
			mainbutton = RoundedShadowButton(text='Select Camera', size_hint=(1, 1), selected_id=self.camera_id,font_size='20sp',button_radius=10, button_color=(1,1,1,1),color="black",button_down_color=(247/255,142/255,48/255,1),always_release=True)
			# mainbutton = DropDownButton(text='Select Camera', size_hint=(1, 1), selected_id=self.camera_id,font_size='30sp')
			mainbutton.bind(on_release=self.camera_dropdown.open)
			self.ids['camera_selector'] = mainbutton
			self.ids['select_layout'].add_widget(mainbutton)
	def selectcamera(self,cameraid):
		self.disable_camera_controls()
		self.disable_privacy_button()
		self.my_camera = None
		for camera in self.cameralist:
			if camera["id"] == cameraid:
				self.camera_id = camera["id"]
				self.camera_address = camera["ip"]
				self.camera_username = camera["username"]
				self.camera_password = camera["password"]
				# self.ids["camera_selector"].text = camera["name"]
		label = Label(text='Connecting to Camera. Please Wait...',color='black')
		self.ids['cam_window'].clear_widgets()
		self.ids['cam_window'].add_widget(label)
		# self.event_create_camera_control = Clock.schedule_once(self.connect_to_camera,5)
		self.connect_to_camera()

	def enable_privacy_button(self):
		if self.ids['privacy_button'].disabled:
			self.ids['privacy_button'].disabled = False

	def disable_privacy_button(self):
		if not self.ids['privacy_button'].disabled:
			self.ids['privacy_button'].disabled = True

	def enable_camera_controls(self):
		if self.ids['left_button'].disabled:
			# self.ids['preset_button'].disabled = False
			self.ids['left_button'].disabled = False
			self.ids['right_button'].disabled = False
			self.ids['up_button'].disabled = False
			self.ids['down_button'].disabled = False
			self.ids['zoom_in_button'].disabled = False
			self.ids['zoom_out_button'].disabled = False
	def disable_camera_controls(self):
		if not self.ids['left_button'].disabled:
			self.ids['preset_button'].disabled = True
			self.ids['left_button'].disabled = True
			self.ids['right_button'].disabled = True
			self.ids['up_button'].disabled = True
			self.ids['down_button'].disabled = True
			self.ids['zoom_in_button'].disabled = True
			self.ids['zoom_out_button'].disabled = True
	def connect_to_camera(self):
		try:
			self.event_check_camera_connection_status.cancel()
		except:
			pass
		self.camera_control = axiscamera.AxisCamera(self.camera_address, self.camera_username, self.camera_password)
		if self.vidtype == "MJPG":
			self.my_camera = Video(source='http://' + self.camera_username + ':' + self.camera_password + '@' + self.camera_address + '/axis-cgi/mjpg/video.cgi?resolution=' + self.resolution + '&fps=' + str(self.fps), state='play', preview='images/splash.png', volume=self.volume)
		elif self.vidtype == "H264":
			self.my_camera = Video(source='rtsp://' + self.camera_username + ':' + self.camera_password + '@' + self.camera_address + ':554/axis-media/media.amp?resolution=' + self.resolution + '&fps=' + str(self.fps), state='play', preview='images/splash.png', volume=self.volume)
			# self.my_camera.bind(on_preview=self.my_camera.texture_update())
		# self.ids['cam_window'].clear_widgets()
		# self.ids['cam_window'].add_widget(self.my_camera)
		# label = Label(text='Connecting to Camera. Please Wait...',color='black')
		# self.ids['cam_window'].add_widget(label)
		self.event_check_camera_connection_status = Clock.schedule_interval(self.check_camera_connection_status, 1)
		# self.enable_camera_controls()
	def check_camera_connection_status(self,dt):
		# ivs.log("Camera Connected: " + str(self.camera_control.connected))
		# ivs.log(self.my_camera)
		if self.my_camera != None:
			# ivs.log("Video Loaded: " + str(self.my_camera.loaded))
			if self.my_camera.loaded != self.last_camera_loaded:
				if self.my_camera.loaded:
					self.ids['cam_window'].clear_widgets()
					self.ids['cam_window'].add_widget(self.my_camera)
					ivs.log("reload")
				else:
					self.ids['cam_window'].clear_widgets()
					label = Label(text='Connecting to Camera. Please Wait...',color='black')
					self.ids['cam_window'].add_widget(label)
			self.last_camera_loaded = self.my_camera.loaded
		if self.camera_control.connected:
			if self.camera_control.ptz == 1:
				self.enable_camera_controls()
			if self.camera_control.privacy == 2:
				self.ids['privacy_button'].text = 'Enable Privacy'
				self.enable_privacy_button()
			elif self.camera_control.privacy == 1:
				self.ids['privacy_button'].text = 'Disable Privacy'
				self.enable_privacy_button()
			# if self.camera_control.ptz != 0 and self.camera_control.privacy !=0:
			# 	self.event_check_camera_connection_status.cancel()
			if self.my_camera == None:
				self.connect_to_camera()
		else:
			self.disable_camera_controls()
			self.disable_privacy_button()
			self.ids['cam_window'].clear_widgets()
			label = Label(text='Unable to Connect to Camera', color='black')
			self.ids['cam_window'].add_widget(label)
			self.my_camera = None
	def on_stop(self):
		#without this, app will not exit even if the window is closed
		self.capture.release()
	def pan_left_on(self):
		# print("Pan Left On")
		self.panleft(1)
		self.pan_left_event = Clock.schedule_interval(self.panleft, self.repeat_interval)
	def pan_left_off(self):
		# print("Pan Left Off")
		self.pan_left_event.cancel()
		self.pan_left_count = 0
	def panleft(self,x):
		self.pan_left_count = self.pan_left_count + 1
		movement = self.panstepsize * -1 * self.pan_left_count
		# print(movement)
		self.camera_control.pan(movement)
	def pan_right_on(self):
		# print("Pan Right On")
		self.panright(1)
		self.pan_right_event = Clock.schedule_interval(self.panright, self.repeat_interval)
	def pan_right_off(self):
		# print("Pan Right Off")
		self.pan_right_event.cancel()
		self.pan_right_count = 0
	def panright(self,x):
		self.pan_right_count = self.pan_right_count + 1
		movement = self.panstepsize * self.pan_right_count
		# print(movement)
		self.camera_control.pan(movement)
	def tilt_up_on(self):
		# print("Tilt Up On")
		self.tiltup(1)
		self.tilt_up_event = Clock.schedule_interval(self.tiltup, self.repeat_interval)
	def tilt_up_off(self):
		# print('Tilt Up Off')
		self.tilt_up_event.cancel()
		self.tilt_up_count = 0
	def tiltup(self,x):
		self.tilt_up_count = self.tilt_up_count + 1
		movement = self.tiltstepsize * self.tilt_up_count
		# print(movement)
		self.camera_control.tilt(movement)
	def tilt_down_on(self):
		# print("Tilt Down On")
		self.tiltdown(1)
		self.tilt_down_event = Clock.schedule_interval(self.tiltdown, self.repeat_interval)
	def tilt_down_off(self):
		# print("Tilt Down Off")
		self.tilt_down_event.cancel()
		self.tilt_down_count = 0
	def tiltdown(self,x):
		self.tilt_down_count = self.tilt_down_count + 1
		movement = self.tiltstepsize * self.tilt_down_count * -1
		# print(movement)
		self.camera_control.tilt(movement)
	def zoom_in_on(self):
		self.zoomin(1)
		self.zoom_in_event = Clock.schedule_interval(self.zoomin, self.repeat_interval)
	def zoom_in_off(self):
		self.zoom_in_event.cancel()
		self.zoom_in_count = 0
	def zoomin(self,x):
		self.zoom_in_count = self.zoom_in_count + 1
		movement = self.zoomstepsize * self.zoom_in_count
		# print(movement)
		self.camera_control.zoom(movement)
	def zoom_out_on(self):
		self.zoomout(1)
		self.zoom_out_event = Clock.schedule_interval(self.zoomout, self.repeat_interval)
	def zoom_out_off(self):
		self.zoom_out_event.cancel()
		self.zoom_out_count = 0
	def zoomout(self,x):
		self.zoom_out_count = self.zoom_out_count + 1
		movement = self.zoomstepsize * self.zoom_out_count * -1
		# print(movement)
		self.camera_control.zoom(movement)
	def toggle_privacy(self):
		if self.camera_control.privacy == 1:
			self.ids['privacy_button'].text = 'Enable Privacy'
		elif self.camera_control.privacy == 2:
			self.ids['privacy_button'].text = 'Disable Privacy'
		self.camera_control.toggle_privacy()
	def change_pantilt_step_size(self):
		# print(self.ids['pantiltslider'].value)
		self.panstepsize = self.ids['pantiltslider'].value
		self.tiltstepsize = self.ids['pantiltslider'].value
	def change_zoom_step_size(self):
		# print(self.ids['zoomslider'].value)
		self.zoomstepsize = self.ids['zoomslider'].value
	def change_step_size(self):
		self.panstepsize = self.ids['pantiltslider'].value
		self.tiltstepsize = self.ids['pantiltslider'].value
		self.zoomstepsize = self.ids['pantiltslider'].value * 20
	def change_volume(self):
		self.volume = self.ids['volume_slider'].value
		# print(self.ids['volume_slider'].value)
		# if self.my_camera != None:
		# 	self.my_camera.volume = self.ids['volume_slider'].value