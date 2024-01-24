from libs.pys.StandardButton import StandardButton
from kivy.properties import ObjectProperty
class DropDownButton(StandardButton):
	selected_id = ObjectProperty(None)
