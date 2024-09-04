from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.video import Video

class TouchVideo(Video):
	def on_release(self):
		print("released")