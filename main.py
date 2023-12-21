from Framework import ivs_accessory_framework
__version__ = ".2"

class RoomControlAccessory(ivs_accessory_framework.IVS_Accessory_Framework):
	pass

if __name__ == '__main__':
	RoomControlAcc = RoomControlAccessory()
	RoomControlAcc.run()
