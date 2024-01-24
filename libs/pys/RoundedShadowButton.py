from kivy.uix.label import Label
from kivy.properties import ColorProperty, NumericProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle, BoxShadow

class RoundedShadowButton(ButtonBehavior, Label):
	# background_color = ColorProperty([0,0,0,0])
	# background_normal = StringProperty('')
	id = ObjectProperty(None)
	selected_id = ObjectProperty(None)
	button_color = ColorProperty([88/255,88/255,88/255,1])
	button_down_color = ColorProperty([50/255,164/255,206/255,1])
	button_disabled_color = ColorProperty([186/255,186/255,186/255,1])
	button_radius = NumericProperty(50)
	# shadow_color = ColorProperty([0, 0, 0, 0.25])
	shadow = ObjectProperty(None)
	# shape_color = ColorProperty([88/255,88/255,88/255,1])
	shape_color = ObjectProperty(None)
	shape = ObjectProperty(None)
	current_button_color = ColorProperty([88/255,88/255,88/255,1])
	def __init__(self, **kwargs):
		super(RoundedShadowButton, self).__init__(**kwargs)
		self.current_button_color = self.button_color
		self.draw()
	def draw(self,*args):
		with self.canvas.before:
			self.shadow_color = Color(rgba=(0, 0, 0, 0.25))
			self.shadow = BoxShadow(pos=self.pos,size=self.size,offset=(10,-10),spread_radius=(-20,-20),blur_radius=50,border_radius=(self.button_radius, self.button_radius, self.button_radius, self.button_radius))
			self.shape_color = Color(self.current_button_color)
			self.shape_color.rgba = self.current_button_color
			self.shape = RoundedRectangle(pos=self.pos,size=self.size,radius=[self.button_radius])
		self.bind(pos=self.update_shape, size=self.update_shape)
	def update_shape(self, *args):
		self.shape.pos = self.pos
		self.shape.size = self.size
		self.shadow.pos = self.pos
		self.shadow.size = self.size
	def on_button_radius(self,instance,value):
		self.button_radius = value
		if self.shape != None:
			self.shape.radius = [self.button_radius]
	def on_button_color(self,instance,value):
		self.button_color = value
		if self.shape_color != None:
			self.shape_color.rgba = self.button_color
	def on_button_down_color(self,instance,value):
		self.button_down_color = value
	def on_press(self):
		self.shape_color.rgba = self.button_down_color
	def on_release(self):
		self.shape_color.rgba = self.button_color
	def on_disabled(self,instance,value):
		self.disabled = value
		if self.disabled:
			self.shape_color.rgba = self.button_disabled_color
		else:
			self.shape_color.rgba = self.button_color

