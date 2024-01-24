from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import ColorProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle, BoxShadow
from kivy.clock import Clock

class RoundedShadowButtonWithImage(ButtonBehavior, RelativeLayout):
	id = ObjectProperty(None)
	selected_id = ObjectProperty(None)
	button_color = ColorProperty([88 / 255, 88 / 255, 88 / 255, 1])
	button_down_color = ColorProperty([50 / 255, 164 / 255, 206 / 255, 1])
	button_disabled_color = ColorProperty([186 / 255, 186 / 255, 186 / 255, 1])
	button_radius = NumericProperty(50)
	shadow = ObjectProperty(None)
	shape_color = ObjectProperty(None)
	shape = ObjectProperty(None)
	current_button_color = ColorProperty([88/255,88/255,88/255,1])
	text = StringProperty("")
	font_size = StringProperty('15sp')
	color = ColorProperty("black")
	btn = ObjectProperty(None)
	img_source = StringProperty("")
	img_width = NumericProperty(28)
	img_height = NumericProperty(28)
	img = ObjectProperty(None)
	lbl = ObjectProperty(None)
	buffer = NumericProperty(10)
	def __init__(self,**kwargs):
		super(RoundedShadowButtonWithImage, self).__init__(**kwargs)
		self.lbl = Label(color=self.color, text=self.text, font_size=self.font_size,size_hint=(None,None),bold=True)
		self.add_widget(self.lbl)
		self.img = Image(source=self.img_source,size_hint=(None,None),height=self.img_height,width=self.img_width)
		self.add_widget(self.img)
		self.current_button_color = self.button_color
		self.draw()
		Clock.schedule_once(self.update_shape,-1)
	def draw(self,*args):
		with self.canvas.before:
			self.shadow_color = Color(rgba=(0, 0, 0, 0.25))
			self.shadow = BoxShadow(pos=self.pos,size=self.size,offset=(10,-10),spread_radius=(-20,-20),blur_radius=50,border_radius=(self.button_radius, self.button_radius, self.button_radius, self.button_radius))
			self.shape_color = Color(self.current_button_color)
			self.shape_color.rgba = self.current_button_color
			self.shape = RoundedRectangle(pos=self.pos,size=self.size,radius=[self.button_radius])
		self.bind(pos=self.update_shape, size=self.update_shape)
	def update_shape(self,*args):
		self.shape.pos = (0,0)
		self.shape.size = self.size
		self.shadow.pos = (0,0)
		self.shadow.size = self.size
		self.lbl.size = self.lbl.texture_size
		img_pos_x=(self.width-(self.lbl.texture_size[0] + self.img.width + self.buffer))/2
		self.img.pos=(img_pos_x,self.height/2-self.img.height/2)
		lbl_pos_x = img_pos_x + self.img.width + self.buffer
		self.lbl.pos=(lbl_pos_x,self.height/2-self.lbl.height/2)

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
	def on_button_disabled_color(self,instance,value):
		self.button_disabled_color = value
		if self.btn != None:
			self.btn.button_disabled_color = value
	def on_text(self,instance,value):
		self.text = value
		if self.btn != None:
			self.btn.text = value
	def on_font_size(self,instance,value):
		self.font_size = value
		if self.btn != None:
			self.btn.font_size = value
	def on_color(self,instance,value):
		self.color = value
		if self.btn != None:
			self.btn.color = value
	def on_img_source(self,instance,value):
		self.img_source = value
		if self.img != None:
			self.img.source = value
	def on_img_height(self,instance,value):
		self.img_height = value
		if self.img != None:
			self.img.height = value
	def on_img_width(self,instance,value):
		self.img_width = value
		if self.img != None:
			self.img.width = value
