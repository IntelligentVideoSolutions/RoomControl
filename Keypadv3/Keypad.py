from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.clock import Clock

class Keypad(FloatLayout):
	def __init__(self, valt, room, pinlength, **kwargs):
		super(Keypad, self).__init__(**kwargs)
		self.valt = valt
		self.room = room
		self.recordingname = "Test Recording"
		self.pinlength = pinlength
		# self.build()
	def build(self):
		print(self.ids["display_label"].text)
	def PressButton(self,instance):
		self.ids["display_label"].text = self.ids["display_label"].text + instance.text
		if len(self.ids["display_label"].text) == self.pinlength:
			self.event_Pin_Entered = Clock.schedule_once(self.PinEntered, .25)
	def PinEntered(self,dt):
		print("pin entered")
		enteredcode = self.ids["display_label"].text
		self.clear_display_label(0)
		self.disable_input()
		# ivs.log("PIN entered: " + enteredcode, logpath)
		self.author = self.getuserid(enteredcode, self.valt.getusers())
		if self.author > 0:
			curroomstatus = self.valt.getroomstatus(self.room)
			self.ids["display_label"].text = "Good Pin"
			if curroomstatus == 1 or curroomstatus == 5:
				self.event_start_recording = Clock.schedule_once(self.start_recording, .5)
			elif curroomstatus == 2:
				self.event_start_recording = Clock.schedule_once(self.stop_recording, .5)
			else:
				self.ids["display_label"].text = "Room is Busy"
		else:
			self.ids["display_label"].text = "Bad Pin"
		self.event_clear_display_label_status = Clock.schedule_once(self.clear_display_label, 5)
	def getuserid(self,cardnumber,users):
		retval = 0
		for user in users:
			if str(user['card_number']) == str(cardnumber):
				retval = user['id']
		return retval
	def clear_display_label(self,dt):
		self.ids["display_label"].text = ""
		self.enable_input()
	def start_recording(self,dt):
		self.valt.startrecording(self.room, self.recordingname, author=self.author)
		self.ids["display_label"].text = "Recording Started"
	def stop_recording(self, dt):
		self.valt.stoprecording(self.room)
		self.ids["display_label"].text = "Recording Stopped"
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
	def disable_input(self):
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