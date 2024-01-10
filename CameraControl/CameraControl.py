from kivy.uix.relativelayout import RelativeLayout

from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.video import Video
from axis import axiscamera

class StandardButton(Button):
	id = ObjectProperty(None)
class DropDownButton(StandardButton):
	selected_id = ObjectProperty(None)
class StandardDropDown(DropDown):
	id = ObjectProperty(None)

class CameraControl(RelativeLayout):
	def __init__(self, valt, room, vidtype="H264",fps="30",resolution="800x450",volume=0,**kwargs):
		super(CameraControl, self).__init__(**kwargs)
		self.valt = valt
		self.room = room
		self.vidtype = vidtype
		self.fps = fps
		self.resolution = resolution
		self.volume = volume
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
		self.build()
	def build(self):
		#Builder.load_file('CameraControl.kv')
		self.get_cameras()
	def get_cameras(self):
		self.cameralist = self.valt.getcameras(self.room)
		# print(type(self.cameralist))
		if type(self.cameralist).__name__ == 'list':
			dropdown = DropDown()
			for camera in self.cameralist:
				btn = StandardButton(id=camera["id"], text=camera["name"], size_hint_y=None, height=44)
				btn.bind(on_release=lambda btn: dropdown.select(btn.id))
				dropdown.add_widget(btn)
			dropdown.bind(on_select=lambda instance, x: self.selectcamera(x))
			self.selectcamera(self.cameralist[0]["id"])
			mainbutton = DropDownButton(text='Select Camera', size_hint=(1, 1), selected_id=self.camera_id)
			mainbutton.bind(on_release=dropdown.open)
			self.ids['camera_selector'] = mainbutton
			self.ids['select_layout'].add_widget(mainbutton)
	def selectcamera(self,cameraid):
		self.disable_camera_controls()
		self.disable_privacy_button()
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
		self.connect_to_camera(1)

	def enable_privacy_button(self):
		self.ids['privacy_button'].disabled = False

	def disable_privacy_button(self):
		self.ids['privacy_button'].disabled = True

	def enable_camera_controls(self):
		# self.ids['preset_button'].disabled = False

		self.ids['left_button'].disabled = False
		self.ids['right_button'].disabled = False
		self.ids['up_button'].disabled = False
		self.ids['down_button'].disabled = False
		self.ids['zoom_in_button'].disabled = False
		self.ids['zoom_out_button'].disabled = False
	def disable_camera_controls(self):
		self.ids['preset_button'].disabled = True
		self.ids['left_button'].disabled = True
		self.ids['right_button'].disabled = True
		self.ids['up_button'].disabled = True
		self.ids['down_button'].disabled = True
		self.ids['zoom_in_button'].disabled = True
		self.ids['zoom_out_button'].disabled = True
	def connect_to_camera(self,dt):
		try:
			self.event_check_camera_connection_status.cancel()
		except:
			pass
		self.camera_control = axiscamera.AxisCamera(self.camera_address, self.camera_username, self.camera_password)
		#self.my_camera = Video(source='http://' + self.camera_username + ':' + self.camera_password + '@' + self.camera_address + '/axis-cgi/mjpg/video.cgi?resolution=800x450&fps=23&0.mjpg',state='play', preview='splash.png')
		if self.vidtype == "MJPG":
			self.my_camera = Video(source='http://' + self.camera_username + ':' + self.camera_password + '@' + self.camera_address + '/axis-cgi/mjpg/video.cgi?resolution=' + self.resolution + '&fps=' + self.fps, state='play', preview='images/splash.png', volume=self.volume)
		elif self.vidtype == "H264":
			self.my_camera = Video(source='rtsp://' + self.camera_username + ':' + self.camera_password + '@' + self.camera_address + ':554/axis-media/media.amp?resolution=' + self.resolution + '&fps=' + self.fps, state='play', preview='images/splash.png', volume=self.volume)
		self.ids['cam_window'].clear_widgets()
		self.ids['cam_window'].add_widget(self.my_camera)
		# label = Label(text='Connecting to Camera. Please Wait...',color='black')
		# self.ids['cam_window'].add_widget(label)
		self.event_check_camera_connection_status = Clock.schedule_interval(self.check_camera_connection_status, 1)
		# self.enable_camera_controls()
	def check_camera_connection_status(self,dt):
		if self.camera_control.ptz == 1:
			self.enable_camera_controls()
		if self.camera_control.privacy == 2:
			self.ids['privacy_button'].text = 'Enable Privacy'
			self.enable_privacy_button()
		elif self.camera_control.privacy == 1:
			self.ids['privacy_button'].text = 'Disable Privacy'
			self.enable_privacy_button()
		if self.camera_control.ptz != 0 and self.camera_control.privacy !=0:
			self.event_check_camera_connection_status.cancel()
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
