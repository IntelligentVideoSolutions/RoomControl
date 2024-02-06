from libs.modules.Framework import ivs_accessory_framework
import os
from kivy.utils import platform
from jnius import autoclass
# from multiprocessing.dummy import Process
from kivy.clock import Clock

__version__ = "2.2.1"


if platform == "android":
     os.environ["SDL_AUDIODRIVER"] = "android"

class RoomControlAccessory(ivs_accessory_framework.IVS_Accessory_Framework):
	def on_start(self):
		# if platform == "android":
		# 	self.start_service()
		# 	print('service started')
		super().on_start()
	def start_service(self):
		service = autoclass("com.ipivs.valtrc.ServiceValtrc")
		mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
		service.start(mActivity,"")

if __name__ == '__main__':
	RoomControlAcc = RoomControlAccessory()
	RoomControlAcc.run()


# @staticmethod
