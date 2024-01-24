from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty
from kivy.uix.image import Image

class ImageButton(ButtonBehavior, Image):
	downimage = ObjectProperty(None)
	upimage = ObjectProperty(None)
	id = ObjectProperty(None)

	def on_press(self):
		self.source = self.downimage

	def on_release(self):
		self.source = self.upimage
