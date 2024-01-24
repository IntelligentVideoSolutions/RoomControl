def printchildren(object, layer):
	for child in object:
		print(str(layer) + " " + str(child))
		try:
			print(child.text)
		except:
			pass
		printchildren(child.children, layer + 1)
