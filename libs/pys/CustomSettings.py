from kivy.uix.settings import SettingSpacer, SettingString, SettingOptions, SettingItem
from kivy.properties import StringProperty
from libs.pys.PasswordLabel import PasswordLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import libs.modules.ivs.ivs as ivs

class SettingScrollOptions(SettingOptions):

	def _create_popup(self, instance):
		# create the popup
		scroll = ScrollView(always_overscroll=False, size_hint=(1, 1))
		content = BoxLayout(orientation='vertical', spacing='5dp', size_hint=(1, None))
		content.height = (len(self.options) + 1) * dp(55)
		scroll.add_widget(content)
		popup_width = min(0.95 * Window.width, dp(500))
		self.popup = popup = Popup(content=scroll, title=self.title, size_hint=(None, None),
								   size=(popup_width, '400dp'))
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
