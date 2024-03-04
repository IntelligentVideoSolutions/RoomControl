from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import time

from libs.pys.BackgroundScrollView import BackgroundScrollView
from libs.pys.HRLabel import HRLabel
from libs.pys.ActiveLabel import ActiveLabel
from libs.pys.ScheduleLabel import ScheduleLabel
class ScheduleDisplay(RelativeLayout):
	def __init__(self, valt, room, **kwargs):
		super(ScheduleDisplay, self).__init__(**kwargs)
		self.valt = valt
		self.room = room
		self.lasthr = int(time.strftime('%H'))
		self.build()
	def build(self):
		scrollbox = BackgroundScrollView()
		scrollbox.background_color = (.8, .8, .8, 1)
		# scrollbox.background_color = (.2, .2, .2, 1)
		maingrid = GridLayout(cols=2,size_hint_y=None)
		scrollbox.add_widget(maingrid)
		self.hrgrid = GridLayout(cols=1,size_hint_x=.25, size_hint_y=None,spacing=1,padding=1)
		self.schedgrid = GridLayout(cols=1, size_hint_x=1,size_hint_y = None,spacing=1,padding=1)
		maingrid.add_widget(self.hrgrid)
		maingrid.add_widget(self.schedgrid)
		self.add_widget(scrollbox)
		self.buildhours()
		self.buildschedule(1)
		self.event_buildschedule = Clock.schedule_interval(self.buildschedule, 30)
	def buildhours(self):
		self.hrgrid.clear_widgets()
		curhr = int(time.strftime('%H'))
		for i in range(curhr,24):
			if i == 0:
				lbl =  HRLabel(text="12:00 AM",size_hint=(1,None),height=59)
			elif i == 12:
				lbl =  HRLabel(text="12:00 PM",size_hint=(1,None),height=59)
			elif i < 13:
				lbl =  HRLabel(text=str(i)+":00 AM",size_hint=(1,None),height=59)
			else:
				lbl =  HRLabel(text=str(i-12)+":00 PM",size_hint=(1,None),height=59)
			self.hrgrid.add_widget(lbl)
	def buildschedule(self,dt):
		self.schedgrid.clear_widgets()
		curhr = int(time.strftime('%H'))
		if not curhr == self.lasthr:
			self.lasthr = curhr
			self.buildhours()
		curtime = time.time()
		schedrecs = self.valt.getschedule(self.room)
		if type(schedrecs).__name__ == 'list':
		#if schedrecs != 0:
			lastschedend = curtime - (curtime % 3600)
			curindex = 0
			eod = (24-curhr)*3600
			starthr = curtime - (curtime % 3600)
			#self.printlog(schedrecs)
			for schedule in schedrecs:
				if schedule[0] - starthr < eod:
					if schedule[0] <= lastschedend and schedule[1] >= lastschedend:
						lblheight= int((schedule[1] - lastschedend)/60)-1
						if curtime > lastschedend and curtime < schedule[1]:
							lbl = ActiveLabel(text=schedule[2][0:44], size_hint=(1,None),height=lblheight)
						else:
							lbl = ScheduleLabel(text=schedule[2][0:44], size_hint=(1,None),height=lblheight)
						#lbl = ScheduleLabel(text=str(lblheight), size_hint=(1,None),height=lblheight)
						self.schedgrid.add_widget(lbl)
						curindex = curindex + lblheight + 1
						lastschedend = schedule[1]
					elif schedule[0] > lastschedend:
						#lblheight= int((schedule[0] - lastschedend)/60)-1
						#lbl = HRLabel(size_hint=(1,None),height=lblheight)
						#lbl = HRLabel(text=str(lblheight),size_hint=(1,None),height=lblheight)
						#self.schedgrid.add_widget(lbl)
						totsize = int((schedule[0] - lastschedend)/60)
						#self.root.get_screen('Schedule_Display_Screen').ids.feedback.text = str(totsize)
						if totsize == 60:
							if (curindex % 60) > 0:
								lblheight = (curindex % 60)-1
								lbl = HRLabel(size_hint=(1,None),height=lblheight)
								#lbl = HRLabel(text=str(lblheight),size_hint=(1,None),height=lblheight)
								self.schedgrid.add_widget(lbl)
								lblheight = (60 - (curindex % 60))-1
								lbl = HRLabel(size_hint=(1,None),height=lblheight)
								#lbl = HRLabel(text=str(lblheight),size_hint=(1,None),height=lblheight)
								self.schedgrid.add_widget(lbl)
							else:
								lblheight = 59
								lbl = HRLabel(size_hint=(1,None),height=lblheight)
								#lbl = HRLabel(text=str(lblheight),size_hint=(1,None),height=lblheight)
								self.schedgrid.add_widget(lbl)
							curindex = curindex + 60
						if (curindex % 60) > 0 and totsize % 60 > 0:
							#self.root.get_screen('Schedule_Display_Screen').ids.feedback.text = str(int((curindex+totsize)/60))
							#if (totsize % 60) > (curindex % 60):
							if int((curindex+totsize)/60) > int(curindex/60) and (totsize % 60) > (curindex % 60):
								lblheight = (curindex % 60) -1
								lbl = HRLabel(size_hint=(1,None),height=lblheight)
								self.schedgrid.add_widget(lbl)
								lblheight = (totsize % 60) - (curindex % 60) -1
								#self.root.get_screen('Schedule_Display_Screen').ids.feedback.text = str(curindex % 60)
								#lbl = HRLabel(text=str(lblheight),size_hint=(1,None),height=lblheight)
								lbl = HRLabel(size_hint=(1,None),height=lblheight)
								self.schedgrid.add_widget(lbl)
							else:
								lblheight = (totsize % 60) -1
								#self.root.get_screen('Schedule_Display_Screen').ids.feedback.text = str(curindex % 60)
								#lbl = HRLabel(text=str(lblheight),size_hint=(1,None),height=lblheight)
								lbl = HRLabel(size_hint=(1,None),height=lblheight)
								self.schedgrid.add_widget(lbl)
						i = 0
						while i+60 <= totsize and totsize > 60:
							lblheight = 59
							lbl = HRLabel(size_hint=(1,None),height=lblheight)
							#lbl = HRLabel(text=str(i),size_hint=(1,None),height=lblheight,color=(1,1,1,1))
							self.schedgrid.add_widget(lbl)
							i = i+60
						if (curindex % 60) == 0 and totsize % 60 > 0:
							lblheight = (totsize % 60) -1
							#lbl = HRLabel(text=str(lblheight),size_hint=(1,None),height=lblheight)
							lbl = HRLabel(size_hint=(1,None),height=lblheight)
							self.schedgrid.add_widget(lbl)

						curindex = curindex+totsize
						lblheight= int((schedule[1] - schedule[0])/60)-1
						if curtime > schedule[0] and curtime < schedule[1]:
							lbl = ActiveLabel(text=schedule[2][0:44], size_hint=(1,None),height=lblheight)
						else:
							lbl = ScheduleLabel(text=schedule[2][0:44], size_hint=(1,None),height=lblheight)
						#lbl = ScheduleLabel(text=str(lblheight), size_hint=(1,None),height=lblheight)
						self.schedgrid.add_widget(lbl)
						curindex = curindex + lblheight + 1
						lastschedend = schedule[1]
					#else:
					#	lblheight= int((schedule[0] - (lastschedend))/60)-1
					#	lbl = ScheduleLabel(text=schedule[2], size_hint=(1,None),height=lblheight)
					#	self.schedgrid.add_widget(lbl)
					#	lastschedend = schedule[1]
			if lastschedend < starthr + eod:
				totsize = int((starthr+eod-lastschedend)/60)
				#self.root.get_screen('Schedule_Display_Screen').ids.feedback.text = str(totsize)
				if totsize % 60 > 0:
					lblheight = (totsize % 60) -1
					#lbl = HRLabel(text=str(lblheight),size_hint=(1,None),height=lblheight)
					lbl = HRLabel(size_hint=(1,None),height=lblheight)
					self.schedgrid.add_widget(lbl)
				i = 60
				while i <= totsize and totsize > 60:
					lblheight = 59
					lbl = HRLabel(size_hint=(1,None),height=lblheight)
					#lbl = HRLabel(text=str(i),size_hint=(1,None),height=lblheight)
					self.schedgrid.add_widget(lbl)
					i = i+60
		else:
			# self.root.get_screen('Schedule_Display_Screen').ids['feedback'].text = self.valt.errormsg
			pass
	def ClearSchedule(self,dt):
		self.schedgrid.clear_widgets()
	def disconnect(self):
		try:
			self.event_buildschedule.cancel()
		except:
			pass