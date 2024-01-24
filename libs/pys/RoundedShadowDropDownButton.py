from libs.pys.RoundedShadowButton import RoundedShadowButton
from kivy.properties import ObjectProperty
class DropDownButton(RoundedShadowButton):
	selected_id = ObjectProperty(None)