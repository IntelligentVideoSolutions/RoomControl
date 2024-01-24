from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, NumericProperty
from libs.modules.ivs import ivs
import threading
from libs.pys.RoundedButton import RoundedButton
from libs.pys.RoundedShadowButton import RoundedShadowButton
class Keypad(RelativeLayout):
	recordingname = StringProperty("Test Recording")
	pinlength = NumericProperty(6)
	def __init__(self, valt, room, **kwargs):
		super(Keypad, self).__init__(**kwargs)
		self.valt = valt
		self.room = room
		# self.build()
	def build(self):
		print(self.ids["display_label"].text)
	def PressButton(self,instance):
		self.ids["display_label"].text = self.ids["display_label"].text + instance.text
		if len(self.ids["display_label"].text) == self.pinlength:
			# self.event_Pin_Entered = Clock.schedule_once(self.PinEntered, .25)
			threading.Thread(target=self.PinEntered).start()
			# self.clear_display_label(0)
			Clock.schedule_once(self.disable_input,-1)
	@mainthread
	def update_display_label(self,text):
		self.ids["display_label"].text = text
	def PinEntered(self):
		# print("pin entered")
		enteredcode = self.ids["display_label"].text
		ivs.log("PIN entered: " + enteredcode)
		self.author = self.getuserid(enteredcode, self.valt.getusers())
		if self.author > 0:
			self.update_display_label("Good Pin")
			curroomstatus = self.valt.getroomstatus(self.room)
			if curroomstatus == 1 or curroomstatus == 5:
				# self.event_start_recording = Clock.schedule_once(self.start_recording, .5)
				threading.Thread(target=self.start_recording).start()
			elif curroomstatus == 2:
				# self.event_start_recording = Clock.schedule_once(self.stop_recording, .5)
				threading.Thread(target=self.stop_recording).start()
			else:
				self.update_display_label("Room is Busy")
				self.event_clear_display_label_status = Clock.schedule_once(self.clear_display_label, 2)
		else:
			self.update_display_label("Bad Pin")
			self.event_clear_display_label_status = Clock.schedule_once(self.clear_display_label, 2)
		# self.event_clear_display_label_status = Clock.schedule_once(self.clear_display_label, 2)
	def getuserid(self,cardnumber,users):
		retval = 0
		for user in users:
			if str(user['card_number']) == str(cardnumber):
				retval = user['id']
		return retval
	@mainthread
	def clear_display_label(self,dt):
		self.ids["display_label"].text = ""
		self.enable_input()
	def start_recording(self):
		self.valt.startrecording(self.room, self.recordingname, author=self.author)
		self.update_display_label("Recording Started")
		self.event_clear_display_label_status = Clock.schedule_once(self.clear_display_label, 2)
	def stop_recording(self):
		self.valt.stoprecording(self.room)
		self.update_display_label("Recording Stopped")
		self.event_clear_display_label_status = Clock.schedule_once(self.clear_display_label, 2)
	def enable_input(self):
		self.ids["1_button"].disabled = False
		self.ids["2_button"].disabled = False
		self.ids["3_button"].disabled = False
		self.ids["4_button"].disabled = False
		self.ids["5_button"].disabled = False
		self.ids["6_button"].disabled = False
		self.ids["7_button"].disabled = False
		self.ids["8_button"].disabled = False
		self.ids["9_button"].disabled = False
		self.ids["asterisk_button"].disabled = False
		self.ids["0_button"].disabled = False
		self.ids["pound_button"].disabled = False
	def disable_input(self,dt):
		self.ids["1_button"].disabled = True
		self.ids["2_button"].disabled = True
		self.ids["3_button"].disabled = True
		self.ids["4_button"].disabled = True
		self.ids["5_button"].disabled = True
		self.ids["6_button"].disabled = True
		self.ids["7_button"].disabled = True
		self.ids["8_button"].disabled = True
		self.ids["9_button"].disabled = True
		self.ids["asterisk_button"].disabled = True
		self.ids["0_button"].disabled = True
		self.ids["pound_button"].disabled = True
	def on_recordingname(self,instance,value):
		self.recordingname = value
	def on_pinlength(self,instance,value):
		self.pinlength = value
