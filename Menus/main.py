#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '414')
Config.set('graphics', 'height', '736')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
import os
from time import strftime
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.factory import Factory
from kivy.lang import Builder

from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import gc
from kivy.animation import Animation
from kivy.clock import Clock

year = int(strftime("%Y"))
if year % 4 == 0:
 	extra = 1
else:
 	extra = 0

allmonth = {"01": 0, "02": 31, "03": 59+extra, 
"04": 90+extra, "05": 120+extra, "06": 151+extra, 
"07": 181+extra, "08": 212+extra, "09": 243+extra,
"10": 273+extra, "11": 304+extra, "12": 334+extra, "13": 365+extra}

class SuppaLabel(Label):

	container1 = ObjectProperty(10)
	container2 = ObjectProperty(10)


class Core(BoxLayout):
	col = ObjectProperty((.1, .1, .1, .0))
	sp_text = ObjectProperty("")
	worktext = StringProperty("Введите артикул")
	press = NumericProperty(0)
	cuart = ""
	cudate = ""
	standartdate = ""
	standartname = ""

	now = datetime.now()
	yez = str(now.year)

	step = 0

	g_input = ObjectProperty({"center_x":.5,"center_y":.68})
	ex_input1 = ObjectProperty({"center_x":-5,"center_y":.68})
	ex_input2 = ObjectProperty({"center_x":-5,"center_y":.68})
	ex_input3 = ObjectProperty({"center_x":-5,"center_y":.68})

	before_after = ObjectProperty('before')

	pos_before_after1 = ObjectProperty({"center_x": -5,"center_y":.8}) #{"center_x": .35,"center_y":.8}
	pos_before_after2 = ObjectProperty({"center_x": -5,"center_y":.8}) #{"center_x": .65,"center_y":.8}

	pos_day_month_year1 = ObjectProperty({"center_x": -5,"center_y":.8}) #{"center_x": .2,"center_y":.8}
	pos_day_month_year2 = ObjectProperty({"center_x": -5,"center_y":.8}) #{"center_x": .5,"center_y":.8}
	pos_day_month_year3 = ObjectProperty({"center_x": -5,"center_y":.8}) #{"center_x": .8,"center_y":.8}

	pos_el1 = ObjectProperty({"center_x":-5,"center_y":.795})
	pos_el2 = ObjectProperty({"center_x":-5,"center_y":.795})
	pos_el3 = ObjectProperty({"center_x":-5,"center_y":.795})
	pos_el4 = ObjectProperty({"center_x":-5,"center_y":.795})
	pos_el5 = ObjectProperty({'center_x':.5, 'center_y': .1})

	container1 = ObjectProperty(10)
	container2 = ObjectProperty(10)

	day_or_what = ObjectProperty('day')

	ranger1 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger2 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger3 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger4 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger5 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger6 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger7 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger8 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger9 = ObjectProperty({"center_x":-5,"center_y":.795})

	prosrochka_button = ObjectProperty({"center_x": -5,"center_y":.9625})

	current_year = str(datetime.now().year)

	def show_prosrok(self, data):
		if data:
			self.prosrochka_button = {"center_x": .5,"center_y":.9625}
		else:
			self.prosrochka_button = {"center_x": -5,"center_y":.9625}

	def old_trash_out(self):

		master = []

		for each in self.arch:
			hm = each.split('.')
			resulter = hm[2]+hm[0]
			master.append(resulter)

		if len(self.arch) == 0:
			return
		else:

			f = open("saver.txt", "r+")
			dawread = f.read()
			f.close()
			dawread = dawread.split("$")
			del dawread[-1]

			special = []

			enough = False
			temp = []

			for each in dawread:
				if enough == False:
					temp.append(each)
					enough = not enough
				else:
					temp.append(each)
					special.append(temp)
					temp = []
					enough = not enough

			superb = []

			for each in special:
				resulter = each[0]+each[1]
				superb.append(resulter)


			for each in master:
				if each in superb:
					superb.remove(each)

			soviet = []

			for each in superb:
				first = each[:8]
				second = each[8:]

				soviet.append(first)
				soviet.append(second)

			with open("saver.txt", "w") as f:
				for each in soviet:
					f.write(str(each + "$"))

			sync()

			self.ids.griddy_trash.clear_widgets()

			self.arch = []
			self.memory = []

			self.ids.fi.state = 'down'
			self.ids.mana.current = 'work'

			popup("Внимание", "Данные были удалены")

			self.show_prosrok(False)

			self.alarm()

			



	def put_trash(self):

		list_temp = []
		temp = []

		ddate = True
		for each in entries:
			if ddate:
				temp.append(each)
				ddate = not ddate
			else:
				temp.append(each)
				list_temp.append((temp[0], temp[1]))
				temp = []
				ddate = not ddate

		another_list = []

		for each in list_temp:
			day = each[0][:2]
			month = each[0][2:4]
			year = each[0][4:]

			c = date(int(year), int(month), int(day))

			temp = (c, each[1])

			another_list.append(temp)

		just_list = []

		curent = datetime.now()

		for each in another_list:
			if each[0] < curent.date():
				just_list.append(each)

		new_kind = sorted(just_list, key=lambda x: x[0])

########################-------------------------We have all what we want sorted now###############

		self.grid = self.ids.griddy_trash
		self.grid.bind(minimum_height=self.grid.setter("height"))
		self.grid.clear_widgets()

		last_year = ''

		counter = 0
		for each in new_kind:
			counter += 1

			day = str(each[0].day)
			month = str(each[0].month)
			year = str(each[0].year)

			if len(day) == 1:
				day = '0'+day
			if len(month) == 1:
				month = '0'+month

			sentence = '{}{}{}'.format(day, month, year)
			self.memory.append(sentence)

			m_label = SuppaLabel()


			if last_year != each[0].year:
				dayr = str(each[0].day)
				monthr = str(each[0].month)

				if len(dayr) < 2:
					dayr = '0'+dayr
				if len(monthr) < 2:
					monthr = '0'+monthr

				m_label.text = 'Просрок до {}.{}.{}'.format(dayr, monthr, each[0].year)
				m_label.container1 = 0.06*self.height
				m_label.container2 = 0.035*self.height
				self.grid.add_widget(m_label)
			else:
				pass

			self.texter = str(counter)+'. ' + each[1] + ' ' + art_names[each[1]]
			self.btn = ToggleButton(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size=0.035*self.height)
			self.grid.add_widget(self.btn)
			self.btn.bind(on_press=self.check_status2)




	def check_status2(self, button):

		if button.state == 'down':
			flat = button.text.split(' ')
			number = flat[0]
			article = flat[1]
			name = flat[2]

			number = number.replace(' ', '')
			article = article.replace(' ', '')
			name = name.replace(' ', '')

			number = number.replace('.', '')

			mem_date = self.memory[int(number)-1]

			self.arch.append('{}.{}.{}'.format(article, name, mem_date))
		else:
			flat = button.text.split(' ')
			number = flat[0]
			article = flat[1]
			name = flat[2]

			number = number.replace(' ', '')
			article = article.replace(' ', '')
			name = name.replace(' ', '')

			number = number.replace('.', '')

			mem_date = self.memory[int(number)-1]

			searching_for = '{}.{}.{}'.format(article, name, mem_date)
			self.arch.remove(searching_for)


	memory = []
	arch = []

	def alarm_out(self, *args):
		self.animation = Animation(pos_hint=({"center_x": .4,"center_y": 2}), duration=0.25)
		self.animation.start(self.ids.warner)

		self.a = Animation(pos_hint=({"center_x": .9,"center_y": 2}), duration=0.25)
		self.a.start(self.ids.warner2)

	def alarm(self, *args):

		counter = True
		for each in entries:
			try:
				if counter == True:
					counter = not counter
					day = int(each[:2])
					month = int(each[2:4])
					year = int(each[4:])

					c = date(year, month, day)
					curent = datetime.now()

					if c <= curent.date():
						self.animation = Animation(pos_hint=({"center_x": .4,"center_y":.5}), duration=1)
						self.animation.start(self.ids.warner)

						self.a = Animation(pos_hint=({"center_x": .9,"center_y":.5}), duration=1)
						self.a.start(self.ids.warner2)
						self.show_prosrok(True)
						break
					else:
						self.alarm_out()

				else:
					counter = not counter
					continue
			except:
				self.alarm_out()

	def ranger_main(self):

		try:
			self.grid.clear_widgets()
		except:
			None
			
		try:
			start_date = date(int(self.ids.to_range3.text), int(self.ids.to_range2.text), int(self.ids.to_range1.text))
			end_date = date(int(self.ids.to_range6.text), int(self.ids.to_range5.text), int(self.ids.to_range4.text))
		except:
			popup('Внимание', 'Дата введена не корректно!')
			return

		between = (end_date-start_date).days
		between += 1

		start_date -= timedelta(1)
		
		for x in range(between):
			start_date += timedelta(1)

			day = str(start_date.day)
			month = str(start_date.month)
			year = str(start_date.year)

			if len(day) == 1:
				day = '0'+day

			if len(month) == 1:
				month = '0'+month

			tommorow = '{}{}{}'.format(day, month, year)


			hound = [i for i,x in enumerate(entries) if x==tommorow]

			if len(hound) == 0:
				continue
			else:
				self.col = (.1, .1, .1, .0)
				self.sp_text =''
				storage = []

				for each in hound:
					storage.append(entries[each+1])


				self.grid = self.ids.griddy4
				self.grid.bind(minimum_height=self.grid.setter("height"))

				m_label = SuppaLabel()

				m_label.text = 'Списать до {}.{}.{}'.format(day, month, year)
				m_label.container1 = 0.06*self.height
				m_label.container2 = 0.035*self.height


				self.grid.add_widget(m_label)


				for each in storage:
					self.texter = each + ' ' + art_names[each]
					self.btn = Button(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size=0.035*self.height)
					self.grid.add_widget(self.btn)
		

	def show_rangers(self, data):
		if data == True:
			self.ranger1 = ({"center_x":.22,"center_y":.83})
			self.ranger2 = ({"center_x":.335,"center_y":.83})
			self.ranger3 = ({"center_x":.497,"center_y":.83})
			self.ranger4 = ({"center_x":.22,"center_y":.77})
			self.ranger5 = ({"center_x":.335,"center_y":.77})
			self.ranger6 = ({"center_x":.497,"center_y":.77})
			self.ranger7 = ({"center_x":.78,"center_y":.8})
			self.ranger8 = ({"center_x":.1,"center_y":.83})
			self.ranger9 = ({"center_x":.1,"center_y":.77})

			self.pos_el5 = ({"center_x":-5,"center_y":.77})

		else:
			self.ranger1 = ({"center_x":-5,"center_y":.83})
			self.ranger2 = ({"center_x":-5,"center_y":.83})
			self.ranger3 = ({"center_x":-5,"center_y":.83})
			self.ranger4 = ({"center_x":-5,"center_y":.77})
			self.ranger5 = ({"center_x":-5,"center_y":.77})
			self.ranger6 = ({"center_x":-5,"center_y":.77})
			self.ranger7 = ({"center_x":-5,"center_y":.8})
			self.ranger8 = ({"center_x":-5,"center_y":.83})
			self.ranger9 = ({"center_x":-5,"center_y":.77})

	def extra_checker2(self, data):
		if data[0] == '1':
			if data == '1dd':
				if len(self.ids.to_range1.text) == 2:
					if self.ids.to_range2.text != '':
						self.ids.to_range1.focus = False
					else:
						self.ids.to_range2.focus = True
				if len(self.ids.to_range1.text) > 2:
					self.ids.to_range1.text = ''
			elif data == '1mm':
				if len(self.ids.to_range2.text) == 2:
					if self.ids.to_range3.text != '':
						self.ids.to_range2.focus = False
					else:
						self.ids.to_range3.focus = True
				if len(self.ids.to_range2.text) > 2:
					self.ids.to_range2.text = ''
			elif data == '1yy':
				if len(self.ids.to_range3.text) == 4:
					self.ids.to_range3.focus = False
				if len(self.ids.to_range3.text) > 4:
					self.ids.to_range3.text = ''
		else:
			if data == '2dd':
				if len(self.ids.to_range4.text) == 2:
					if self.ids.to_range5.text != '':
						self.ids.to_range4.focus = False
					else:
						self.ids.to_range5.focus = True
				if len(self.ids.to_range4.text) > 2:
					self.ids.to_range4.text = ''
			elif data == '2mm':
				if len(self.ids.to_range5.text) == 2:
					if self.ids.to_range6.text != '':
						self.ids.to_range5.focus = False
					else:
						self.ids.to_range6.focus = True
				if len(self.ids.to_range5.text) > 2:
					self.ids.to_range5.text = ''
			elif data == '2yy':
				if len(self.ids.to_range6.text) == 4:
					self.ids.to_range6.focus = False
				if len(self.ids.to_range6.text) > 4:
					self.ids.to_range6.text = ''




	def extra_checker(self, data):
		if data == 'dd':
			if len(self.ids.to_d1.text) == 2:
				if self.ids.to_d2.text != '':
					self.ids.to_d1.focus = False
				else:
					self.ids.to_d2.focus = True
			if len(self.ids.to_d1.text) > 2:
				self.ids.to_d1.text = ''
		elif data == 'mm':
			if len(self.ids.to_d2.text) == 2:
				if self.ids.to_d3.text != '':
					self.ids.to_d2.focus = False
				else:
					self.ids.to_d3.focus = True
			if len(self.ids.to_d2.text) > 2:
				self.ids.to_d2.text = ''
		elif data == 'yy':
			if len(self.ids.to_d3.text) == 4:
				self.ids.to_d3.focus = False
			if len(self.ids.to_d3.text) > 4:
				self.ids.to_d3.text = ''

	def show_el(self, data):
		if data == True:
			self.pos_el1 = ({"center_x":.185,"center_y":.795})
			self.pos_el2 = ({"center_x":.3,"center_y":.795})
			self.pos_el3 = ({"center_x":.46,"center_y":.795})
			self.pos_el4 = ({"center_x": .73,"center_y":.795})

			self.pos_el5 = ({'center_x': -5, 'center_y': .1})
		else:
			self.pos_el1 = ({"center_x":-5,"center_y":.795})
			self.pos_el2 = ({"center_x":-5,"center_y":.795})
			self.pos_el3 = ({"center_x":-5,"center_y":.795})
			self.pos_el4 = ({"center_x":-5,"center_y":.795})

			self.pos_el5 = ({'center_x': .5, 'center_y': .1})

	def day_or_what_changer(self, data):
		if data != self.day_or_what:
			self.day_or_what = data

	def pos_day_month_visible(self, data):
		if data == True:
			self.pos_day_month_year1 = ({"center_x": .2,"center_y":.8})
			self.pos_day_month_year2 = ({"center_x": .5,"center_y":.8})
			self.pos_day_month_year3 = ({"center_x": .8,"center_y":.8})
		else:
			self.pos_day_month_year1 = ({"center_x": -5,"center_y":.8})
			self.pos_day_month_year2 = ({"center_x": -5,"center_y":.8})
			self.pos_day_month_year3 = ({"center_x": -5,"center_y":.8})

	def switch_before_after(self, data):
		if self.before_after != data:
			self.before_after = data

	def dater_visible(self):
		self.g_input = {"center_x": -5,"center_y":.68}
		self.ex_input1 = {"center_x":.18,"center_y":.68}
		self.ex_input2 = {"center_x":.407,"center_y":.68}
		self.ex_input3 = {"center_x":.73,"center_y":.68}

	def dater_invisible(self):
		self.g_input = {"center_x": .5,"center_y":.68}
		self.ex_input1 = {"center_x":-5,"center_y":.68}
		self.ex_input2 = {"center_x":-5,"center_y":.68}
		self.ex_input3 = {"center_x":-5,"center_y":.68}

	def type(self, data):
		if self.step == 0:
			if data == 'CLS':
				self.ids.inputer.text = ''
			elif data == '<<':
				self.ids.inputer.text = self.ids.inputer.text[:len(self.ids.inputer.text)-1]
			else:
				self.ids.inputer.text = self.ids.inputer.text+data

		if self.step == 1:
			current_lenght = len(self.ids.ex_inputer.text) + len(self.ids.ex_inputer2.text) + len(self.ids.ex_inputer3.text)
			
			if current_lenght == 0:
				if data == 'CLS':
					pass
				elif data == '<<':
					pass
				else:
					self.ids.ex_inputer.text = self.ids.ex_inputer.text+data

			elif current_lenght == 1:
				if data == 'CLS':
					self.ids.ex_inputer.text = ''
				elif data == '<<':
					self.ids.ex_inputer.text = self.ids.ex_inputer.text[:len(self.ids.ex_inputer.text)-1]
				else:
					self.ids.ex_inputer.text = self.ids.ex_inputer.text+data

			elif current_lenght == 2:
				if data == 'CLS':
					self.ids.ex_inputer.text = ''
				elif data == '<<':
					self.ids.ex_inputer.text = self.ids.ex_inputer.text[:len(self.ids.ex_inputer.text)-1]
				else:
					self.ids.ex_inputer2.text = self.ids.ex_inputer2.text+data

			elif current_lenght == 3:
				if data == 'CLS':
					self.ids.ex_inputer2.text = ''
				elif data == '<<':
					self.ids.ex_inputer2.text = self.ids.ex_inputer2.text[:len(self.ids.ex_inputer2.text)-1]
				else:
					self.ids.ex_inputer2.text = self.ids.ex_inputer2.text+data

			elif current_lenght >= 4 and current_lenght < 8:
				if data == 'CLS' and len(self.ids.ex_inputer3.text) == 0:
					self.ids.ex_inputer2.text = ''
				elif data == 'CLS':
					self.ids.ex_inputer3.text = ''
				elif data == '<<' and len(self.ids.ex_inputer3.text) == 0:
					self.ids.ex_inputer2.text = self.ids.ex_inputer2.text[:len(self.ids.ex_inputer2.text)-1]
				elif data == '<<':
					self.ids.ex_inputer3.text = self.ids.ex_inputer3.text[:len(self.ids.ex_inputer3.text)-1]
				else:
					self.ids.ex_inputer3.text = self.ids.ex_inputer3.text+data

			elif current_lenght == 8:
				if data == 'CLS':
					self.ids.ex_inputer3.text = ''
				elif data == '<<':
					self.ids.ex_inputer3.text = self.ids.ex_inputer3.text[:len(self.ids.ex_inputer3.text)-1]


	def change_pos(self):
		self.test = {"center_x":.18,"center_y":.58}

	def trash_out(self):
		global found_arts

		if len(self.found_arts) == 0:
			return
		else:
			tommorow = date.today() + timedelta(days=1)

			day = str(tommorow.day)
			month = str(tommorow.month)
			year = str(tommorow.year)

			tommorow = '{}{}{}'.format(day, month, year)

			f = open("saver.txt", "r+")
			dawread = f.read()
			f.close()
			dawread = dawread.split("$")
			del dawread[-1]
			hound = []
			for each in self.found_arts:
				temp = [i for i,x in enumerate(dawread) if x==each]
				for each in temp:
					if dawread[each-1] == tommorow:
						hound.append(each)
						hound.append(each-1)
			hound.sort()
			hound = hound[::-1]

			for each in hound:
				del dawread[each]

			with open("saver.txt", "w") as f:
				for each in dawread:
					f.write(str(each + "$"))

			sync()

			self.ids.griddy4.clear_widgets()

			self.define_today_art()

			self.found_arts = []

			popup("Внимание", "Данные были удалены")

	def define_another_art(self):

			day = self.ids.to_d1.text
			month = self.ids.to_d2.text
			year = self.ids.to_d3.text

			absolute = date.today()
			if year == '':
				year = absolute.year

			check = self.check2('{}{}'.format(day, month))

			if check:
				tommorow = '{}{}{}'.format(day, month, year)

				hound = [i for i,x in enumerate(entries) if x==tommorow]

				if len(hound) == 0:
					self.ids.mana.current = "today"
					self.ids.griddy4.clear_widgets()
					self.col = (.1, .1, .1, .3)
					self.sp_text ='Нет артикулов'
				else:
					self.col = (.1, .1, .1, .0)
					self.sp_text =''
					storage = []

					for each in hound:
						storage.append(entries[each+1])


					self.grid = self.ids.griddy4
					self.grid.bind(minimum_height=self.grid.setter("height"))
					self.grid.clear_widgets()

					m_label = SuppaLabel()

					m_label.text = 'Списать до {}.{}.{}'.format(day, month, year)
					m_label.container1 = 0.06*self.height
					m_label.container2 = 0.035*self.height


					self.grid.add_widget(m_label)


					for each in storage:
						self.texter = each + ' ' + art_names[each]
						self.btn = Button(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size=0.035*self.height)
						self.grid.add_widget(self.btn)

					self.ids.mana.current = "today"
					self.ids.to_d1.text = ''
					self.ids.to_d2.text = ''
					self.ids.to_d3.text = ''
			else:
				popup("Внимание", "Вы ввели неверную дату")
				self.ids.to_d1.text = ''
				self.ids.to_d2.text = ''
				self.ids.to_d3.text = ''

	def define_today_art(self, data):
		self.ids.griddy4.clear_widgets()
		if data == 'today':
			tommorow = date.today() + timedelta(days=1)

			day = str(tommorow.day)
			month = str(tommorow.month)
			year = str(tommorow.year)

			if len(day) < 2:
				day = '0'+day
			if len(month) < 2:
				month = '0'+month

			tommorow = '{}{}{}'.format(day, month, year)

			hound = [i for i,x in enumerate(entries) if x==tommorow]

			if len(hound) == 0:
				self.ids.mana.current = "today"
				self.ids.griddy4.clear_widgets()
				self.col = (.1, .1, .1, .3)
				self.sp_text ='Нет артикулов'
			else:
				self.col = (.1, .1, .1, .0)
				self.sp_text =''
				storage = []

				for each in hound:
					storage.append(entries[each+1])


				self.grid = self.ids.griddy4
				self.grid.bind(minimum_height=self.grid.setter("height"))
				self.grid.clear_widgets()

				m_label = SuppaLabel()

				m_label.text = 'Списать сегодня'
				m_label.container1 = 0.06*self.height
				m_label.container2 = 0.035*self.height


				self.grid.add_widget(m_label)


				for each in storage:
					self.texter = each + ' ' + art_names[each]
					self.btn = ToggleButton(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size=0.035*self.height)
					self.grid.add_widget(self.btn)
					self.btn.bind(on_press=self.check_status)

				self.ids.mana.current = "today"

		elif data == 'another':
			self.ids.griddy4.clear_widgets()

	found_arts = []

	def check_status(self, button):
		global found_arts
		temp = []
		for each in button.text:
			if each != " ":
				temp.append(each)
			else:
				break
		art = ''.join(temp)

		if art in self.found_arts:
			self.found_arts.remove(art)
		else:
			self.found_arts.append(art)

	def previous(self):
		self.press = 0
		self.ids.inputer.text = ''
		self.worktext = 'Введите артикул'

		self.pos_day_month_visible(False)

		self.catch_art()

	def repeat(self):

		if last_art == None:
			popup("Внимание", "Нет прошлого артикула")
		else:
			self.ids.inputer.text = last_art

	def show_buttons_before_after(self, argument):
		if argument == 'show':
			self.pos_before_after1 = ({"center_x": .35,"center_y":.8})
			self.pos_before_after2 = ({"center_x": .65,"center_y":.8})
		else:
			self.pos_before_after1 = ({"center_x": -5,"center_y":.8})
			self.pos_before_after2 = ({"center_x": -5,"center_y":.8})

	def catch_art(self):
		global standartdate
		global standartname

		if self.press == 1:
			self.work()
		elif self.press == 2:
			self.work2()
		elif self.press == 3:
			pass
		elif self.press == 100:
			self.standartdate = self.ids.inputer.text
			self.define_date()
		elif self.press == 200:
			self.standartname = self.ids.inputer.text
			self.define_name()
		elif self.press == 500:
			self.standartdate = self.ids.inputer.text
			self.define_date_sp()

	def define_date_sp(self):

		if len(self.standartdate) == 0:
			self.ids.inputer.text = ""
			self.pos_day_month_visible(True)
			self.worktext = "Введите срок годности" 
			self.press = 99
			popup("Внимание!", "Срок годности должен быть числом")
			return

		for each in self.standartdate:
			if each.isdigit() == False and (each.upper() != "M"):
				self.ids.inputer.text = ""
				self.pos_day_month_visible(True)
				self.worktext = "Введите срок годности в днях или месяцах \n"+"Или укажите 0 для указания даты ДО"
				self.press = 499
				popup("Внимание!", "Срок годности должен быть числом дней или месяцев с буквой 'M' в конце")
				return

		if self.day_or_what == 'month':
			self.standartdate = self.standartdate + 'm'
		elif self.day_or_what == 'year':
			self.standartdate = self.standartdate + 'y'

		self.pos_day_month_visible(False)

		f = open("daysoflife.txt", "a")
		f.write(str((self.cuart + "$" + self.standartdate + "$")))
		f.close()

		sync()

		self.go()

	def work(self):
		global cuart
		global last_art

		article = self.ids.inputer.text
		if not article.isdigit():
			self.ids.inputer.text = ""
			popup("Ошибка", "Введите числовой артикул")
			self.press -= 1
			return
		else:
			self.step = 1
			self.dater_visible()
			self.show_buttons_before_after('show')

			global last_art
			last_art = self.ids.inputer.text
			self.cuart = article
			self.ids.inputer.text = ""
			self.worktext = "Введите дату производства\n или окончания срока ДДММ"

	def work2(self):
		global cudate
		global standartdate

		sitrep = self.before_after

		article = self.cuart

		day = self.ids.ex_inputer.text
		mon = self.ids.ex_inputer2.text
		yer = self.ids.ex_inputer3.text

		if len(yer) == 0:
			yer = str(self.yez)

		if len(day) < 2:
			day = '0'+day

		if len(mon) < 2:
			mon = '0'+mon

		ask = '{}{}'.format(day, mon)

		if ask.isalnum(): 
			if len(ask) == 4:
				if ask[0].isalpha() == False and ask[1].isalpha() == False and ask[2].isalpha() == False and ask[3].isalpha() == False:
					if int(ask[2:]) <= 12 and int(ask[2:]) >= 1 and int(ask[:2]) <= 31 and int(ask[:2]) >= 1:
						if self.check2(ask):
							self.cudate = (ask, yer)

							worker = True

							if self.cuart in art_names:
								if sitrep == 'after':
									self.standartdate = "0"
									worker = False
								else:
									self.standartdate = days_of_life[self.cuart]

								if self.standartdate == "0" and worker == True:
									self.pos_day_month_visible(True)
									self.worktext = 'Введите срок годности'
									self.ids.ex_inputer.text = ''
									self.ids.ex_inputer2.text = ''
									self.ids.ex_inputer3.text = ''
									self.ids.inputer.text = ""
									self.show_buttons_before_after('hide')
									self.dater_invisible()
									self.step = 0
									self.press = 499
								else:
									self.go()
									self.ids.inputer.text = ''
									self.show_buttons_before_after('hide')
									self.dater_invisible()
									self.step = 0
									self.ids.ex_inputer.text = ''
									self.ids.ex_inputer2.text = ''
									self.ids.ex_inputer3.text = ''
							else:
								self.ids.ex_inputer.text = ''
								self.ids.ex_inputer2.text = ''
								self.ids.ex_inputer3.text = ''
								self.ids.inputer.text = ""
								self.show_buttons_before_after('hide')
								self.dater_invisible()
								self.step = 0
								if sitrep == 'before':
									self.pos_day_month_visible(True)
									self.worktext = "Введите срок годности"
									self.press = 99
								else:
									global standartdate
									self.ids.inputer.focus = True
									self.worktext = 'Введите название артикула'
									self.standartdate = "0"
									self.press = 199

						else:
							popup("Внимание!", "В этом месяце нет столько дней")
							self.ids.ex_inputer.text = ""
							self.ids.ex_inputer2.text = ""
							self.press -= 1
					else:
						popup("Внимание!", "Вы вне диапазона!")
						self.ids.ex_inputer.text = ""
						self.ids.ex_inputer2.text = ""
						self.press -= 1
				else:
					popup("Внимание!", "Вы ввели буквы")
					self.ids.ex_inputer.text = ""
					self.ids.ex_inputer2.text = ""
					self.press -= 1
			else:
				popup("Внимание!", "Необходимый формат - ДДММ")
				self.ids.ex_inputer.text = ""
				self.ids.ex_inputer2.text = ""
				self.press -= 1
		else:
			popup("Внимание!", "Вы ввели символы!")
			self.ids.ex_inputer.text = ""
			self.ids.ex_inputer2.text = ""
			self.press -= 1

	def define_date(self):
		if len(self.standartdate) == 0:
			self.ids.inputer.text = ""
			self.pos_day_month_visible(True)
			self.worktext = "Введите срок годности" 
			self.press = 99
			popup("Внимание!", "Срок годности должен быть числом")
			return

		for each in self.standartdate:
			if each.isdigit() == False:
				self.ids.inputer.text = ""
				self.pos_day_month_visible(True)
				self.worktext = "Введите срок годности" 
				self.press = 99
				popup("Внимание!", "Срок годности должен быть числом")
				return

		if self.day_or_what == 'month':
			self.standartdate = self.standartdate + 'm'
		elif self.day_or_what == 'year':
			self.standartdate = self.standartdate + 'y'

		self.pos_day_month_visible(False)
		self.worktext = "Введите название артикула"
		self.ids.inputer.text = ""
		self.press = 199
		self.ids.inputer.focus = True

	def define_name(self):

		f = open("daysoflife.txt", "a")
		f.write(str((self.cuart + "$" + self.standartdate + "$")))
		f.close()

		f = open("artname.txt", "a")
		f.write(str((self.cuart + "$" + self.standartname + "$")))
		f.close()

		sync()

		self.go()

	def save_anyway(self, final):
		self.popup.dismiss()
		self.save(final, self.cuart)
		sell = "Срок годности до {}".format(final)
		popup("Сохранено", sell)
		self.worktext = "Введите артикул"
		self.ids.inputer.text = ""
		self.press = 0
		self.alarm()

	def wise(self):
		self.popup.dismiss()
		self.worktext = "Введите артикул"
		self.ids.inputer.text = ""
		self.press = 0


	def enter_prosrok(self, final):
		title = 'Внимание!'
		label = Label(text='Сохраняемый артикул просрочен,\n все равно сохранить?')
		btn1 = Button(text='Да', on_release=lambda x: self.save_anyway(final))
		btn2 = Button(text='Нет', on_release=lambda x: self.wise())

		fl = BoxLayout(orientation='vertical')
		fl.add_widget(label)
		bx = BoxLayout(orientation='horizontal')
		bx.add_widget(btn1)
		bx.add_widget(btn2)

		fl.add_widget(bx)

		self.popup = Popup(title=title,
		content=fl,
		size_hint=(None, None), size=(300, 200))
		self.popup.open()

	def go(self):
		month = self.cudate[0][2:]
		day = self.cudate[0][:2]

		c = date(int(self.cudate[1]), int(month), int(day))

		ex = self.standartdate
		if ex[len(ex)-1].upper() == "M":
			newex = ex.replace("M","")
			ex = newex.replace("m", "")

			c += relativedelta(months=int(ex))

			year = str(c.year)
			month = str(c.month)
			day = str(c.day)

			if len(month) < 2:
				month = '0'+month

			if len(day) < 2:
				day = '0'+day

			repres = '{}.{}.{}'.format(day, month, year)
			final = '{}{}{}'.format(day, month, year)

			###-----space------###

			todayer = date.today()

			if c <= todayer:
				self.enter_prosrok(final)
			else:
				self.save(final, self.cuart)
				sell = "Срок годности до {}".format(repres)
				popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0

		elif ex[len(ex)-1].upper() == "Y":
			newex = ex.replace("Y","")
			ex = newex.replace("y", "")

			c += relativedelta(years=int(ex))

			year = str(c.year)
			month = str(c.month)
			day = str(c.day)

			if len(month) < 2:
				month = '0'+month

			if len(day) < 2:
				day = '0'+day

			repres = '{}.{}.{}'.format(day, month, year)
			final = '{}{}{}'.format(day, month, year)

			todayer = date.today()

			if c <= todayer:
				self.enter_prosrok(final)
			else:
				self.save(final, self.cuart)
				sell = "Срок годности до {}".format(repres)
				popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0

		elif str(ex).isdigit() and int(ex) >= 0:
			ex = int(ex)
			c += timedelta(ex)
			year = str(c.year)
			month = str(c.month)
			day = str(c.day)

			if len(month) < 2:
				month = '0'+month

			if len(day) < 2:
				day = '0'+day

			sell = 'Срок годности до {}.{}.{}'.format(day, month, year)
			ent = '{}{}{}'.format(day, month, year)

			todayer = date.today()
			
			if c <= todayer:
				self.enter_prosrok(ent)
			else:
				self.save(ent, self.cuart)
				popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			
		else:
			popup("Внимание", "Некорректное количество дней")

	def check2(self, ask):
		try:
			dayz = ask[:2]
			month = ask[2:]       
			digidayz = int(dayz)
			digimonth = int(month)
			newmonth = "0%d" % (digimonth + 1)  
			realdayz = allmonth[month]
			if len(newmonth) == 2:
				result = allmonth[newmonth] - realdayz
			else:
				newmonthD = newmonth[1:]
				result = allmonth[newmonthD] - realdayz
			if digidayz <= result:
				return True
			else:
				return False
		except:
			return False

	def popup(self, title, text):
		popup = Popup(title=title,
		content=Label(text=text),
		size_hint=(None, None), size=(200, 100))
		popup.open()

	def save(self, ent, article):
		if len(ent) == 7:
			ent = "0" + ent

		hound = [i for i,x in enumerate(entries) if x==article]
		samer = False
		for each in hound:
			if entries[each-1] == ent:
				samer = True
		if samer:
			self.popup("Внимание!", "Эта дата уже записана для этого артикула")
			self.worktext = "Введите артикул"
			self.ids.inputer.text = ""
			self.press = 0
		else:
			f = open("saver.txt", "a")
			f.write(str((ent + "$" + article + "$")))
			f.close()
			sync()

##########################################################------Database------##############################3
	def create_new(self):
		sentence = "Заполните необходимые поля\n чтобы создать артикул"
		self.layout = FloatLayout(size=(self.width, self.height))
		self.inputi = TextInput(hint_text="Артикул", multiline=False, size_hint_x=.5, size_hint_y=0.1, pos_hint={"center_x":.5,"center_y":.6})
		self.inputi2 = TextInput(hint_text="Название", multiline=False, size_hint_x=.5, size_hint_y=0.1, pos_hint={"center_x":.5,"center_y":.45})
		self.inputi3 = TextInput(hint_text="Стандартный срок", multiline=False, size_hint_x=.5, size_hint_y=0.1, pos_hint={"center_x":.5,"center_y":.35})
		self.btn1 = Button(text="Создать", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size=0.035*self.height, pos_hint={"center_x":.5,"center_y":.2}, on_release=lambda x:self.art_create())
		self.lbl = Label(text=sentence, font_size=0.025*self.height, pos_hint={"center_x":.5,"center_y":.86})

		self.layout.add_widget(self.lbl)
		self.layout.add_widget(self.inputi)
		self.layout.add_widget(self.inputi2)
		self.layout.add_widget(self.inputi3)
		self.layout.add_widget(self.btn1)

		self.popup = Popup(title="Создание",
		content=self.layout,
		size_hint=(.8, .6))
		self.popup.open()

	def art_create(self):
		correct = False
		if self.inputi.text != "" and self.inputi.text.isdigit() and self.inputi2.text != "" and self.inputi3.text != "":
			if self.inputi3.text.isdigit():
				correct = True
			elif self.inputi3.text.lower()[-1] == "m":
				tester = []
				for each in self.inputi3.text:
					tester.append(each.lower())
				tester.remove("m")
				new = "".join(tester)
				if not new.isdigit():
					popup("Внимание!", "Срок годности должен быть числом\n дней или месяцев с буквой 'M' в конце")
					return
				else:
					correct = True
			else:
				popup("Внимание!", "Срок годности должен быть числом\n дней или месяцев с буквой 'M' в конце")
				return

			if correct == False:
				popup("Внимание!", "Срок годности должен быть числом\n дней или месяцев с буквой 'M' в конце")
				return
			else:
				if self.inputi.text in art_names:
					popup("Внимание!", "Этот артикул уже есть в базе данных")
					return
				else:
					f = open("artname.txt", "a")
					f.write(str((self.inputi.text + "$" + self.inputi2.text + "$")))
					f.close()

					f = open("daysoflife.txt", "a")
					f.write(str((self.inputi.text + "$" + self.inputi3.text + "$")))
					f.close()

					sync()

					self.popup.dismiss()
					self.get_them(0)


		else:
			popup("Внимание!", "Введите данные корректно")
			return

	def get_them(self, code):
			search = self.ids.searcher.text
			grid = self.ids.griddy
			grid.bind(minimum_height=grid.setter("height"))
			grid.clear_widgets()
			if len(art_names) == 0 and code == 0:
				popup("Внимание", "В базе данных нет записей")
			else:
				if code == 0:
					for each in art_names:
						top = "{} {}".format(each, art_names[each])
						if search.lower() in top.lower():
							self.info = "{} {}".format(each, art_names[each])
							self.btn = Button(id=each, text=self.info, size_hint_y=None, height=0.09*self.height, font_size=0.035*self.height)
							grid.add_widget(self.btn)
							self.btn.bind(on_release=self.infor)

	def popup(self, title, text):
		popup = Popup(title=title,
		content=Label(text=text),
		size_hint=(None, None), size=(200, 100))
		popup.open()

	def infor(self, button):
		global inf_art

		self.ids.mana.current = "information"

		numbers = []
		words = []
		do_we = False

		for each in button.text:
			if each.isdigit() and do_we == False:
				numbers.append(each)
			else:
				do_we = True
				words.append(each)

		inf_art = "".join(numbers)
		art_names[inf_art] = "".join(words)
		if art_names[inf_art][0] == " ":
			art_names[inf_art] = art_names[inf_art][1:]

		self.start_one()

###########################---INFORMATION---##################################
	def start_one(self):
		self.ids.ghost.text = art_names[inf_art]
		self.ids.ghost2.text = inf_art
		self.ids.ghost4.text = "Срок годности: {}".format(days_of_life[inf_art])

		self.grid = self.ids.ghost3
		self.grid.bind(minimum_height=self.grid.setter("height"))
		self.grid.clear_widgets()

		hound = [i for i,x in enumerate(entries) if x==inf_art]
		temper = [i-1 for i in hound]
		hound = []
		for each in temper:
			hound.append(entries[each])

		# Lets sort those dates!

		sorter = []

		for each in hound:
			year = each[4:]
			month = each[2:4]
			day = each[:2]
			exactday = date(int(year), int(month), int(day))
			sorter.append(exactday)

		sorter.sort()

		hound = []

		for each in sorter:
			year = str(each.year)
			month = str(each.month)
			day = str(each.day)


			if len(month) == 1:
				month = '0'+month
			if len(day) == 1:
				day = '0'+day


			hound.append('{}.{}.{}'.format(day, month, year[2:]))

		# We sorted dates in overview

		for each in hound:
			self.texter = "  До\n"+str(each)
			self.btn = Button(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size=0.035*self.height)
			self.grid.add_widget(self.btn)



	def init_edit(self):
		if self.ids.ghost2.text == "":
			pass
		else:
			self.letedit()
			self.ids.mana.current ='edit'

	def clearer(self):
		self.ids.ghost.text = "Нажмите обновить"
		self.ids.ghost2.text = ""
		self.ids.ghost4.text = ""
		self.ids.ghost3.text = ""

###########################---Edit---#########################################
	def del_ask(self):
		sentence = "Вы уверены что хотите безвозвратно\n удалить артикул {} ?".format(inf_art)

		self.layout = FloatLayout(size=(self.width, self.height))
		self.btn1 = Button(text="Удалить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size=0.035*self.height, pos_hint={"center_x":.5,"center_y":.34}, on_release=lambda x:self.art_delete())
		self.lbl = Label(text=sentence, font_size=0.025*self.height, pos_hint={"center_x":.5,"center_y":.86})

		self.layout.add_widget(self.lbl)
		self.layout.add_widget(self.btn1)

		self.popup = Popup(title="Удаление",
		content=self.layout,
		size_hint=(.8, .3))
		self.popup.open()
		self.get_them(0)

	def art_delete(self):
		self.popup.dismiss()

		# Lets delete from names

		f = open("artname.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = dawread.index(inf_art)
		del dawread[worker]
		del dawread[worker]

		with open("artname.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		#Lets delete from STANDART DATE

		f = open("daysoflife.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = dawread.index(inf_art)
		del dawread[worker]
		del dawread[worker]

		with open("daysoflife.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		#Finally lets delete all entries for it

		f = open("saver.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		hound = [i for i,x in enumerate(dawread) if x==inf_art]
		worker = []

		for each in hound:
			worker.append(each-1)

		worker = worker[::-1]

		for each in worker:
			del dawread[each]
			del dawread[each]

		with open("saver.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		sync()

		self.show_prosrok(False)
		self.alarm()

		self.clean()
		self.get_them(0)
		self.ids.mana.current = "database"


	def add_entry(self):
		sentence = "Добавьте дату артикулу\n{} вручную".format(inf_art)

		
		self.layout = FloatLayout(size=(self.width, self.height))
		self.inputi = TextInput(multiline=False, size_hint_x=.5, size_hint_y=0.2, pos_hint={"center_x":.5,"center_y":.61})
		self.btn1 = Button(text="Добавить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size=0.035*self.height, pos_hint={"center_x":.5,"center_y":.34}, on_release=lambda x:self.add_entry2())
		self.lbl = Label(text=sentence, font_size=0.025*self.height, pos_hint={"center_x":.5,"center_y":.86})

		self.inputi.bind(text=self.save_entry1)

		self.layout.add_widget(self.lbl)
		self.layout.add_widget(self.inputi)
		self.layout.add_widget(self.btn1)

		self.popup = Popup(title="Добавление",
		content=self.layout,
		size_hint=(.8, .3))
		self.popup.open()

	def save_anyway2(self, boomb):
		self.popup.dismiss()
		f = open("saver.txt", "a")
		f.write(str((boomb + "$" + inf_art + "$")))
		f.close()
		sync()
		self.letedit()
		self.popup2.dismiss()
		self.alarm()

	def wise2(self):
		self.popup2.dismiss()

	def enter_prosrok2(self, final):

		title = 'Внимание!'
		label = Label(text='Сохраняемый артикул просрочен,\n все равно сохранить?')
		btn1 = Button(text='Да', on_release=lambda x: self.save_anyway2(final))
		btn2 = Button(text='Нет', on_release=lambda x: self.wise2())

		fl = BoxLayout(orientation='vertical')
		fl.add_widget(label)
		bx = BoxLayout(orientation='horizontal')
		bx.add_widget(btn1)
		bx.add_widget(btn2)

		fl.add_widget(bx)

		self.popup2 = Popup(title=title,
		content=fl,
		size_hint=(None, None), size=(300, 200))
		self.popup2.open()

	def add_entry2(self):
		global new_date

		change = True
		boomb = "some"
		try:
			if new_date.isdigit():
				boomb = new_date
		except:
			change = False

		if change:
			if self.datetest(boomb):
				day = boomb[:2]
				month = boomb[2:4]
				year = boomb[4:]
				c = date(int(year), int(month), int(day))

				todayer = date.today()

				if c <= todayer:
					self.enter_prosrok2(boomb)
					return
			else:
				hound = [i for i,x in enumerate(entries) if x==inf_art]
				for each in hound:
					if entries[each-1] == boomb:
						popup("Внимание!", "Введенная дата уже записана")
						return

			f = open("saver.txt", "a")
			f.write(str((boomb + "$" + inf_art + "$")))
			f.close()
			sync()
			self.letedit()
			self.popup.dismiss()
		else:
			popup("Внимание!", "Вы ничего не ввели")

	def letedit(self):
		self.ids.name.text = art_names[inf_art]
		self.ids.article.text = inf_art
		self.ids.standartdate.text = days_of_life[inf_art]

		self.grid = self.ids.griddy2
		self.grid.bind(minimum_height=self.grid.setter("height"))
		self.grid.clear_widgets()
		
		hound = [i for i,x in enumerate(entries) if x==inf_art]
		leisu = []
		for each in hound:
			leisu.append(each-1)
		hound = []
		for each in leisu:
			hound.append(entries[each])

		#Lets sort dates in edit view

		sorter = []

		for each in hound:
			year = each[4:]
			month = each[2:4]
			day = each[:2]
			exactday = date(int(year), int(month), int(day))
			sorter.append(exactday)

		sorter.sort()

		hound = []

		for each in sorter:
			year = str(each.year)
			month = str(each.month)
			day = str(each.day)


			if len(month) == 1:
				month = '0'+month
			if len(day) == 1:
				day = '0'+day


			hound.append('{}.{}.{}'.format(day, month, year))

		# Should be sorted now

		for each in hound:
			self.texter = "  До\n"+str(each)
			self.btn = Button(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size=0.035*self.height)
			self.grid.add_widget(self.btn)
			self.btn.bind(on_release=self.entry_change)

	def clean(self):
		self.ids.name.text = ""
		self.ids.article.text = ""
		self.ids.standartdate.text = ""
		self.ids.griddy.clear_widgets()

	def change_popup_name(self):
		name = art_names[inf_art]
		ask = self.ids.name.text
		sentence = "Вы уверены что хотите внести изменения\n в артикул {}?".format(name)


		layout = FloatLayout(size=(self.width, self.height))
		btn1 = Button(id="one", text="Изменить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size=0.035*self.height, pos_hint={"center_x":.5,"center_y":.45}, on_release=lambda x:self.close_n_save_name())
		lbl = Label(text=sentence, font_size=0.025*self.height, pos_hint={"center_x":.5,"center_y":.82})

		layout.add_widget(lbl)
		layout.add_widget(btn1)



		if closer == False:
			self.popup = Popup(title="Внимание!",
			content=layout,
			size_hint=(.8, .3))
			self.popup.open()
		else:
			self.popup.dismiss()
			ch_closer()
			popup("Выполнено", "Изменения сохранены")
			self.get_them(0)

	def close_n_save_name(self):
		global inf_art

		name = art_names[inf_art]
		new_name = self.ids.name.text
		new_art = self.ids.article.text
		new_standartdate = self.ids.standartdate.text

		if new_name[0] == " ":
			new_name = new_name[1:]

		#Lets update name... And article in one place

		f = open("artname.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = dawread.index(inf_art)
		worker += 1
		dawread[worker] = new_name

		with open("artname.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		f = open("artname.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = dawread.index(inf_art)
		dawread[worker] = new_art

		with open("artname.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		# Now lets try to update DAYS of Life and art in one place ;)

		f = open("daysoflife.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = dawread.index(inf_art)
		worker += 1
		dawread[worker] = new_standartdate

		with open("daysoflife.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		if inf_art in days_of_life:
			f = open("daysoflife.txt", "r+")
			dawread = f.read()
			f.close()
			dawread = dawread.split("$")
			del dawread[-1]
			worker = dawread.index(inf_art)
			dawread[worker] = new_art

			with open("daysoflife.txt", "w") as f:
				for each in dawread:
					f.write(str(each + "$"))

		#Lets Update entries also...

		if inf_art in entries:
			f = open("saver.txt", "r+")
			dawread = f.read()
			f.close()
			dawread = dawread.split("$")
			del dawread[-1]
			worker = [i for i,x in enumerate(dawread) if x==inf_art]
			for each in worker:
				dawread[each] = new_art

			with open("saver.txt", "w") as f:
				for each in dawread:
					f.write(str(each + "$"))

		#Lets kill copies in NAMES if they are here
		f = open("artname.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = [i for i,x in enumerate(dawread) if x==new_art]

		if len(worker) > 1:
			del dawread[worker[0]]
			del dawread[worker[0]]

		with open("artname.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		#Lets kill copies in STANDARTDATES

		f = open("daysoflife.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = [i for i,x in enumerate(dawread) if x==new_art]
		if len(worker) > 1:
			del dawread[worker[0]]
			del dawread[worker[0]]

		with open("daysoflife.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		sync()

		inf_art = new_art

		ch_closer()
		self.change_popup_name()

	def entry_change(self, button):
		cont = []
		for each in button.text:
			if each.isdigit():
				cont.append(each)

		self.date = "".join(cont)

		sentence = "Вы можете изменить дату"
		
		self.layout = FloatLayout(size=(self.width, self.height))
		self.inputi = TextInput(id="newent", text=self.date, multiline=False, size_hint_x=.5, size_hint_y=0.15, pos_hint={"center_x":.5,"center_y":.7})
		self.btn1 = Button(text="Изменить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size=0.035*self.height, pos_hint={"center_x":.5,"center_y":.45}, on_release=lambda x:self.save_entry())
		self.btn2 = Button(text="Удалить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size=0.035*self.height, pos_hint={"center_x":.5,"center_y":.25}, on_release=lambda x:self.delete_entry())
		self.lbl = Label(text=sentence, font_size=0.025*self.height, pos_hint={"center_x":.5,"center_y":.85})

		self.inputi.bind(text=self.save_entry1)

		self.layout.add_widget(self.lbl)
		self.layout.add_widget(self.inputi)
		self.layout.add_widget(self.btn1)
		self.layout.add_widget(self.btn2)

		self.popup = Popup(title="Редактирование",
		content=self.layout,
		size_hint=(.8, .4))
		self.popup.open()

	def delete_entry(self):
		self.popup.dismiss()

		f = open("saver.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = [i for i,x in enumerate(dawread) if x==inf_art]

		for each in worker:
			if dawread[each-1] == self.date:
				del dawread[each-1]
				del dawread[each-1]
				break


		with open("saver.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		sync()
		self.show_prosrok(False)
		self.alarm()

		self.letedit()

	def save_entry1(self, *args):
		global new_date

		new_date = args[-1]

#######################################################################################
	def save_anyway3(self, boomb):
		f = open("saver.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = [i for i,x in enumerate(dawread) if x==inf_art]

		for each in worker:
			if dawread[each-1] == self.date:
				dawread[each-1] = boomb

		with open("saver.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		sync()

		self.popup.dismiss()
		self.popup2.dismiss()
		self.alarm()

		self.letedit()

	def wise3(self):
		self.popup2.dismiss()

	def enter_prosrok3(self, final):

		title = 'Внимание!'
		label = Label(text='Сохраняемый артикул просрочен,\n все равно сохранить?')
		btn1 = Button(text='Да', on_release=lambda x: self.save_anyway3(final))
		btn2 = Button(text='Нет', on_release=lambda x: self.wise3())

		fl = BoxLayout(orientation='vertical')
		fl.add_widget(label)
		bx = BoxLayout(orientation='horizontal')
		bx.add_widget(btn1)
		bx.add_widget(btn2)

		fl.add_widget(bx)

		self.popup2 = Popup(title=title,
		content=fl,
		size_hint=(None, None), size=(300, 200))
		self.popup2.open()
#######################################################################################

	def save_entry(self):
		global new_date

		change = True
		boomb = "some"
		try:
			if new_date.isdigit():
				boomb = new_date
		except:
			change = False


		if boomb != self.date and change == True:
			if self.datetest(boomb):
				hound = [i for i,x in enumerate(entries) if x==boomb]
				for each in hound:
					if entries[each+1] == inf_art:
						popup("Внимание!", "Эта дата уже записана")
						return

				day = boomb[:2]
				month = boomb[2:4]
				year = boomb[4:]
				c = date(int(year), int(month), int(day))

				todayer = date.today()

				if c <= todayer:
					self.enter_prosrok3(boomb)
					return

				self.popup.dismiss()

				f = open("saver.txt", "r+")
				dawread = f.read()
				f.close()
				dawread = dawread.split("$")
				del dawread[-1]
				worker = [i for i,x in enumerate(dawread) if x==inf_art]

				for each in worker:
					if dawread[each-1] == self.date:
						dawread[each-1] = boomb

				with open("saver.txt", "w") as f:
					for each in dawread:
						f.write(str(each + "$"))

				sync()

				self.show_prosrok(False)

				self.alarm()

				self.letedit()
		else:
			popup("Внимание!", "Вы не изменили дату")

	def datetest(self, date):
		ask = date[:4]
		year = date[4:]
		if ask.isalnum(): 
			if len(ask) == 4:
				if ask[0].isalpha() == False and ask[1].isalpha() == False and ask[2].isalpha() == False and ask[3].isalpha() == False:
					if int(ask[2:]) <= 12 and int(ask[2:]) >= 1 and int(ask[:2]) <= 31 and int(ask[:2]) >= 1:
						if self.check666(ask, year):
							return True
						else:
							popup("Внимание!", "В этом месяце нет столько дней")
					else:
						popup("Внимание!", "Вы вне диапазона!")
				else:
					popup("Внимание!", "Вы ввели буквы")
			else:
				popup("Внимание!", "Необходимый формат - ДДММ")
		else:
			popup("Внимание!", "Вы ввели символы!")

	def check666(self, ask, year):
		dayz = ask[:2]
		month = ask[2:]       
		digidayz = int(dayz)
		digimonth = int(month)
		newmonth = "0%d" % (digimonth + 1)  
		realdayz = allmonth[month]
		if len(newmonth) == 2:
			result = allmonth[newmonth] - realdayz
		else:
			newmonthD = newmonth[1:]
			result = allmonth[newmonthD] - realdayz
		if digidayz <= result and len(year) == 4:
			return True
		else:
			return False

###########################---Settings---#####################################

	def are_you_sure(self):
		title = "Внимание!!!"
		text = "Нажав на кнопку УДАЛИТЬ вы уничтожите\nвсю базу данных безвозвратно!"
		self.lay = FloatLayout(size=(self.width, self.height))
		self.btn1 = Button(background_normal="but_red.png", text="УДАЛИТЬ", size_hint_y=None, size_hint_x=None, height=0.13*self.height, width=0.8*self.width, font_size=0.035*self.height, pos_hint={"center_x":.5,"center_y":.34}, on_release=lambda x:self.exterminate())
		self.lbl = Label(text=text, font_size=0.025*self.height, pos_hint={"center_x":.5,"center_y":.86})

		self.lay.add_widget(self.lbl)
		self.lay.add_widget(self.btn1)

		self.poz = Popup(title=title,
		content=self.lay,
		size_hint=(.8, .3))
		self.poz.open()

	def exterminate(self):
		none = ""

		f = open("daysoflife.txt", "w")
		f.write(none)
		f.close()

		f = open("artname.txt", "w")
		f.write(none)
		f.close()

		f = open("saver.txt", "w")
		f.write(none)
		f.close()

		sync()

		self.poz.dismiss()
		self.show_prosrok(False)

		popup("Внимание", "База данных была полностью удалена")
		self.clearer()
		self.alarm()
		self.ids.griddy.clear_widgets()
		self.ids.griddy4.clear_widgets()

###########################---App_Classes---##################################
class ProtoApp(App):
	def on_start(self):
		mine = ''
		for obj in gc.get_objects(): #This way I could find an instance ;)
			if isinstance(obj, Core):
				mine = obj
				break

		Clock.schedule_once(mine.alarm, 2)

	def build(self):
		return Core()

class ScreenManagement(ScreenManager):
	pass

def sync():
	try:
		f = open("saver.txt", "r+")
		rawread = f.read()
		f.close()
		global entries
		entries = rawread.split("$")
	except:
		f = open("saver.txt", "w+")
		f.close()
	try:
		f = open("artname.txt", "r+")
		dawread = f.read()
		f.close()
		global art_names
		art_names = {}
		templ = dawread.split("$")
		counter = 0

		while counter < (len(templ)-1):
			art_names[templ[counter]] = templ[counter+1]
			counter += 2
	except:
		f = open("artname.txt", "w+")
		f.close()

	try:
		f = open("daysoflife.txt", "r+")
		dawread = f.read()
		f.close()
		global days_of_life
		days_of_life = {}
		templ = dawread.split("$")
		counter = 0

		while counter < (len(templ)-1):
			days_of_life[templ[counter]] = templ[counter+1]
			counter += 2
	except:
		f = open("daysoflife.txt", "w+")
		f.close()

Builder.load_string("""
#:import NoTransition kivy.uix.screenmanager.NoTransition

<SuppaLabel>:
	canvas.before:
		Color: 
			rgb: 0, .8, .4, 
		Rectangle: 
			pos: self.pos 
			size: self.size
	text: 'LMAO'
	size_hint_y: None
	height: root.container1
	font_size: root.container2

<Core>:
	orientation: "vertical"
	FloatLayout:
		canvas.before: 
			Color: 
				rgb: 1, .65, .18
			Rectangle:
				pos: self.pos 
				size: self.size

		size_hint_y: 10

		Image:
			source: 'head.jpg'
			size_hint: (1, 1)
			pos_hint: {"center_x": .5,"center_y": .5}

		Button:
			id: warner
			background_normal: ''
			background_color: 1, .35, .35, 1
			halign: 'center'
			valign: "middle"
			text: 'Есть просроченные артикулы'
			text_size: self.size
			size_hint: (.8, 1)
			font_size: sp(25)
			pos_hint: {"center_x": .4,"center_y": 2}
			on_press: root.ids.fi.state = 'normal'
			on_press: root.ids.se.state = 'normal'
			on_press: root.ids.th.state = 'normal'
			on_press: root.ids.fo.state = 'normal'

			on_press: root.ids.mana.current = "old_arts"
			on_press: root.alarm_out()
			on_press: root.put_trash()

		Button:
			canvas.before:
		        Color:
					rgba: 0, 0, 0, 1
				Line:
					width: 2
					rectangle: self.x, self.y, 0, self.height
			id: warner2
			background_normal: ''
			background_color: 1, .35, .35, 1
			halign: 'center'
			valign: "middle"
			text: 'X'
			text_size: self.size
			size_hint: (.2, 1)
			font_size: sp(25)
			pos_hint: {"center_x": .9,"center_y": 2}
			on_press: root.alarm_out()



	ScreenManagement:
		transition: NoTransition()
		id: mana
		size_hint_y: 82


		Screen:
			name: 'work'
			FloatLayout:
				canvas:
					Color: 
						rgb: 1, 1, 1

					Rectangle:
						source: 'back.png'
						size: self.size
						pos: self.pos
				Label:
					canvas.before:
						Color: 
							rgb: 0, .8, .4
						Rectangle:
							size: self.size
							pos: self.pos

					halign: 'center'
					valign: "middle"
					text: root.worktext
					text_size: self.size
					size_hint: (.8, .15)
					font_size: sp(25)
					pos_hint:{"center_x": .5,"center_y":.92}

				ToggleButton:
					allow_no_selection: False
					group: 'before_after'
					state: 'down'
					text: "От"
					size_hint: (.3, .06)
					pos_hint: root.pos_before_after1
					on_press: root.switch_before_after('before')

				ToggleButton:
					allow_no_selection: False
					group: 'before_after'
					text: "До"
					size_hint: (.3, .06)
					pos_hint: root.pos_before_after2
					on_press: root.switch_before_after('after')

				ToggleButton:
					allow_no_selection: False
					state: 'down'
					group: 'day_month_year'
					state: 'down'
					text: "Дни"
					size_hint: (.3, .06)
					pos_hint: root.pos_day_month_year1
					on_press: root.day_or_what_changer('day')

				ToggleButton:
					allow_no_selection: False
					group: 'day_month_year'
					text: "Месяцы"
					size_hint: (.3, .06)
					pos_hint: root.pos_day_month_year2
					on_press: root.day_or_what_changer('month')

				ToggleButton:
					allow_no_selection: False
					group: 'day_month_year'
					text: "Годы"
					size_hint: (.3, .06)
					pos_hint: root.pos_day_month_year3
					on_press: root.day_or_what_changer('year')


				TextInput:
					font_size: sp(65)
					id: inputer
					multiline: False
					size_hint: (.8, .15)
					pos_hint: root.g_input

				TextInput:
					font_size: sp(65)
					id: ex_inputer
					multiline: False
					size_hint: (.2, .15)
					pos_hint:root.ex_input1

				TextInput:
					font_size: sp(65)
					id: ex_inputer2
					multiline: False
					size_hint: (.2, .15)
					pos_hint: root.ex_input2

				TextInput:
					font_size: sp(65)
					id: ex_inputer3
					hint_text: root.yez
					multiline: False
					size_hint: (.4, .15)
					pos_hint: root.ex_input3


				Button:
					pos_hint: {'center_x': .72, 'center_y': .53}
					size_hint: (.24, .15)
					background_normal: "arrow_next.png"
					background_down: "butp.png"
					on_release:
						root.press += 1
						root.catch_art()


				Button:
					pos_hint: {'center_x': .5, 'center_y': .53}
					size_hint: (.24, .15)
					background_normal: "arrow_repeat.png"
					background_down: "butp.png"
					on_release:
						root.repeat()


				Button:
					pos_hint: {'center_x': .28, 'center_y': .53}
					size_hint: (.24, .15)
					background_normal: "arrow_previous.png"
					background_down: "butp.png"
					on_release: root.previous()
					on_release: root.dater_invisible()
					on_release: root.show_buttons_before_after('hide')
					on_release: root.ids.ex_inputer.text = ''
					on_release: root.ids.ex_inputer2.text = ''
					on_release: root.step = 0

				GridLayout:
					cols: 3
					size_hint_y: .4
					size_hint_x: .8
					pos_hint: {'center_x': .5, 'center_y': .25}
					canvas.before: 
						Color: 
							rgb: 0, .8, 0 
						Rectangle: 
							pos: self.pos 
							size: self.size
					Button:
						text: "1"
						on_release:
							root.type('1')
					Button:
						text: "2"
						on_release: root.type('2')
					Button:
						text: "3"
						on_release: root.type('3')
					Button:
						text: "4"
						on_release: root.type('4')
					Button:
						text: "5"
						on_release: root.type('5')
					Button:
						text: "6"
						on_release: root.type('6')
					Button:
						text: "7"
						on_release: root.type('7')
					Button:
						text: "8"
						on_release: root.type('8')
					Button:
						text: "9"
						on_release: root.type('9')
					Button:
						text: "CLS"
						on_release: root.type('CLS')
					Button:
						text: "0"
						on_release: root.type('0')
					Button:
						text: "<<"
						on_release: root.type('<<')


		Screen:
			name: 'database'
			FloatLayout:
				canvas:
					Rectangle:
						size: self.size
						pos: self.pos
						source: 'back.png'

			Button:
				pos_hint: {'center_x': .5, 'center_y': .1}
				size_hint: (.24, .15)
				background_normal: "plus.png"
				background_down: "butp.png"
				on_release:
					root.create_new()

			Button:
				pos_hint: {'center_x': .85, 'center_y': .9}
				size_hint: (.24, .15)
				background_normal: "find.png"
				background_down: "butp.png"
				on_release:
					root.get_them(0)

			TextInput:
				font_size: 28
				id: searcher
				multiline: False
				size_hint: (.7, .08)
				pos_hint:{"center_x":.40,"center_y":.9}

			ScrollView:
				size_hint_x: .95
				size_hint_y: .65
				pos_hint: {'center_x': .5, 'center_y': .5}
				GridLayout:
					id: griddy
					canvas:
						Rectangle:
							pos: self.pos
							size: self.size
							source: "cleanbl.png"
					spacing: 2
					cols: 1
					size_hint_y: None
					height: 0

		Screen:
			name: 'today'
			FloatLayout:
				canvas:
					Rectangle:
						size: self.size
						pos: self.pos
						source: 'back.png'

				Button:
					id: posrok_button
					text: "Просрок"
					size_hint: (.3, .06)
					background_normal: ''
					background_color: .92, 0, 0, 1
					pos_hint: root.prosrochka_button
					on_press: root.ids.fi.state = 'normal'
					on_press: root.ids.se.state = 'normal'
					on_press: root.ids.th.state = 'normal'
					on_press: root.ids.fo.state = 'normal'

					on_press: root.ids.mana.current = "old_arts"
					on_press: root.put_trash()

				ToggleButton:
					id: bom_bom_bom
					allow_no_selection: False
					state: 'down'
					group: 'which_trash'
					state: 'down'
					text: "Сегодня"
					size_hint: (.3, .06)
					pos_hint: {"center_x": .2,"center_y":.9}
					on_press: root.show_rangers(False)
					on_press: root.show_el(False)
					on_press: root.define_today_art('today')

				ToggleButton:
					id: bom_bom_bom2
					allow_no_selection: False
					group: 'which_trash'
					text: "Произвольно"
					size_hint: (.3, .06)
					pos_hint: {"center_x": .5,"center_y":.9}
					on_press: root.show_rangers(False)
					on_press: root.show_el(True)
					on_press: root.define_today_art('another')

				ToggleButton:
					id: bom_bom_bom3
					allow_no_selection: False
					group: 'which_trash'
					text: "Период"
					size_hint: (.3, .06)
					pos_hint: {"center_x": .8,"center_y":.9}
					on_press: root.show_rangers(True)
					on_press: root.show_el(False)
					on_press: root.define_today_art('range')

				TextInput:
					font_size: 28
					id: to_d1
					hint_text: 'ДД'
					multiline: False
					size_hint: (.11, .08)
					pos_hint: root.pos_el1
					on_text: root.extra_checker('dd')

				TextInput:
					font_size: 28
					id: to_d2
					hint_text: 'ММ'
					multiline: False
					size_hint: (.11, .08)
					pos_hint: root.pos_el2
					on_text: root.extra_checker('mm')

				TextInput:
					font_size: 28
					id: to_d3
					hint_text: root.current_year
					multiline: False
					size_hint: (.2, .08)
					pos_hint: root.pos_el3
					on_text: root.extra_checker('yy')
##################################################################################
				TextInput:
					font_size: 18
					id: to_range1
					hint_text: 'ДД'
					multiline: False
					size_hint: (.11, .05)
					pos_hint: root.ranger1
					on_text: root.extra_checker2('1dd')

				TextInput:
					font_size: 18
					id: to_range2
					hint_text: 'ММ'
					multiline: False
					size_hint: (.11, .05)
					pos_hint: root.ranger2
					on_text: root.extra_checker2('1mm')

				TextInput:
					font_size: 18
					id: to_range3
					hint_text: root.current_year
					multiline: False
					size_hint: (.2, .05)
					pos_hint: root.ranger3
					on_text: root.extra_checker2('1yy')

				TextInput:
					font_size: 18
					id: to_range4
					hint_text: 'ДД'
					multiline: False
					size_hint: (.11, .05)
					pos_hint: root.ranger4
					on_text: root.extra_checker2('2dd')

				TextInput:
					font_size: 18
					id: to_range5
					hint_text: 'ММ'
					multiline: False
					size_hint: (.11, .05)
					pos_hint: root.ranger5
					on_text: root.extra_checker2('2mm')

				TextInput:
					font_size: 18
					id: to_range6
					hint_text: root.current_year
					multiline: False
					size_hint: (.2, .05)
					pos_hint: root.ranger6
					on_text: root.extra_checker2('2yy')

				Button:
					font_size: 28
					text: "Найти"
					size_hint: (.31, .11)
					pos_hint: root.ranger7
					on_release: root.ranger_main()

######################################################################################

				Label:
					canvas.before: 
						Color: 
							rgb: 0, .8, 0 
						Rectangle: 
							pos: self.pos 
							size: self.size
					font_size: 18
					text: 'От:'
					size_hint: (.1, .05)
					pos_hint: root.ranger8

				Label:
					canvas.before: 
						Color: 
							rgb: 0, .8, 0 
						Rectangle: 
							pos: self.pos 
							size: self.size
					font_size: 18
					text: 'До:'
					size_hint: (.1, .05)
					pos_hint: root.ranger9

				Button:
					text: "Найти"
					size_hint: (.3, .08)
					pos_hint: root.pos_el4
					on_press: root.define_another_art()

				ScrollView:
					size_hint_x: .95
					size_hint_y: .72
					pos_hint: {'center_x': .5, 'center_y': .375}
					BoxLayout:
						orientation: "vertical"
						id: griddy4
						canvas:
							Rectangle:
								pos: self.pos
								size: self.size
								source: "cleanbl.png"
						spacing: 2
						cols: 1
						size_hint_y: None
						height: 0

				Label:
					pos_hint: {'center_x': .5, 'center_y': .5}
					text: root.sp_text
					font_size: sp(20)
					size_hint: (.8, .3)
					canvas.before: 
						Color: 
							rgba: root.col
						Rectangle:
							pos: self.pos 
							size: self.size

				Button:
					pos_hint: root.pos_el5
					size_hint: (.25, .2)
					background_normal: "trash.png"
					background_down: "butp.png"
					on_release:
						root.trash_out()

		Screen:
			name: 'information'
			FloatLayout:
				id: canvas
				canvas:
					Rectangle:
						size: self.size
						pos: self.pos
						source: 'back.png'

				Label:
					id: ghost
					size: self.texture_size
					text: "Нажмите обновить"
					font_size: sp(60)
					pos_hint:{"center_x":.5,"center_y":.88}

				Label:
					id: ghost2
					size: self.texture_size
					text: ""
					font_size: sp(30)
					pos_hint:{"center_x":.5,"center_y":.80}
				Label:
					id: ghost4
					size: self.texture_size
					text: ""
					font_size: sp(30)
					pos_hint:{"center_x":.5,"center_y":.75}

				ScrollView:
					size_hint_x: 0.9
					size_hint_y: 0.5
					pos_hint: {'center_x': .5, 'center_y': .45}
					GridLayout:
						id: ghost3
						canvas:
							Rectangle:
								pos: self.pos
								size: self.size
								source: "cleanbl.png"
						spacing: 2
						cols: 4
						size_hint_y: None
						height: 0

				Button:
					pos_hint: {'center_x': .8, 'center_y': .1}
					size_hint: (.24, .15)
					background_normal: "edit.png"
					background_down: "butp.png"
					on_release:
						root.init_edit()

				Button:
					pos_hint: {'center_x': .2, 'center_y': .1}
					size_hint: (.24, .15)
					background_normal: "arrow_previous.png"
					background_down: "butp.png"
					on_release: root.ids.mana.current = "database"


		Screen:
			name: 'edit'
			FloatLayout:
				id: canvas
				canvas:
					Rectangle:
						size: self.size
						pos: self.pos
						source: 'back.png'
				Label:
					size: self.texture_size
					text: "Редактирование"
					font_size: sp(40)
					pos_hint:{"center_x":.5,"center_y":.9}

				TextInput:
					id: name
					text: "Обновите информацию"
					multiline: False
					size_hint: (.5, .05)
					pos_hint:{"center_x":.3,"center_y":.8}

				TextInput:
					id: article
					text: "Обновите информацию"
					multiline: False
					size_hint: (.5, .05)
					pos_hint:{"center_x":.3,"center_y":.7}

				TextInput:
					id: standartdate
					text: "Обновите информацию"
					multiline: False
					size_hint: (.5, .05)
					pos_hint:{"center_x":.3,"center_y":.6}

				Button:
					text: "Сохранить"
					font_size: sp(22)
					pos_hint: {'center_x': .75, 'center_y': .7}
					size_hint: (.4, .10)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.change_popup_name()
				Button:
					text: "Добавить дату"
					font_size: sp(16)
					pos_hint: {'center_x': .75, 'center_y': .6}
					size_hint: (.4, .10)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.add_entry()

				Button:
					text: "Удалить артикул"
					font_size: sp(18)
					pos_hint: {'center_x': .75, 'center_y': .1}
					size_hint: (.5, .12)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.del_ask()

				ScrollView:
					size_hint_x: .95
					size_hint_y: .35
					pos_hint: {'center_x': .5, 'center_y': .35}
					GridLayout:
						id: griddy2
						canvas:
							Rectangle:
								pos: self.pos
								size: self.size
								source: "cleanbl.png"
						spacing: 2
						cols: 3
						size_hint_y: None
						height: 0

				Button:
					pos_hint: {'center_x': .2, 'center_y': .1}
					size_hint: (.24, .15)
					background_normal: "arrow_previous.png"
					background_down: "butp.png"
					on_release:
						root.start_one()
						root.ids.mana.current = "information"


		Screen:
			name: 'settings'
			FloatLayout:

				id: canvas
				canvas:
					Rectangle:
						size: self.size
						pos: self.pos
						source: 'back.png'

				Button:
					text: "Язык"
					font_size: sp(22)
					pos_hint: {'center_x': .5, 'center_y': .8}
					size_hint: (.65, .12)
					background_normal: "but.png"
					background_down: "butp.png"

				Button:
					text: "Синхронизировать"
					font_size: sp(22)
					pos_hint: {'center_x': .5, 'center_y': .7}
					size_hint: (.65, .12)
					background_normal: "but.png"
					background_down: "butp.png"

				Button:
					text: "Удалить базу данных"
					font_size: sp(22)
					pos_hint: {'center_x': .5, 'center_y': .6}
					size_hint: (.65, .12)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.are_you_sure()

		Screen:
			name: 'old_arts'
			FloatLayout:

				id: canvas
				canvas:
					Rectangle:
						size: self.size
						pos: self.pos
						source: 'back.png'


				ScrollView:
					size_hint_x: .95
					size_hint_y: .8
					pos_hint: {'center_x': .5, 'center_y': .55}
					BoxLayout:
						orientation: "vertical"
						id: griddy_trash
						canvas:
							Rectangle:
								pos: self.pos
								size: self.size
								source: "cleanbl.png"
						spacing: 2
						cols: 1
						size_hint_y: None
						height: 0


				Button:
					pos_hint: {'center_x':.5, 'center_y': .1}
					size_hint: (.25, .2)
					background_normal: "trash.png"
					background_down: "butp.png"
					on_release:
						root.old_trash_out()





	BoxLayout:
		size_hint_y: 8
		ToggleButton:
			id: fi
			allow_no_selection: False
			group: 'test'
			state: 'down'
			text: "WORK"
			on_press: root.ids.mana.current = "work"

		ToggleButton:
			id: se
			allow_no_selection: False
			group: 'test'
			text: 'DB'
			on_press: root.ids.mana.current = "database"

		ToggleButton:
			id: th
			allow_no_selection: False
			group: 'test'
			text: 'Today'
			on_press: root.show_rangers(False)
			on_press: root.ids.bom_bom_bom.state = 'down'
			on_press: root.ids.bom_bom_bom2.state = 'normal'
			on_press: root.ids.bom_bom_bom3.state = 'normal'
			on_press: root.show_el(False)
			on_press: root.define_today_art('today')

		ToggleButton:
			id: fo
			allow_no_selection: False
			group: 'test'
			text: 'Settings'
			on_press: root.ids.mana.current = "settings"
	""")

entries = []
art_names = {}
days_of_life = {}
last_art = None

def popup(title, text):
	popup = Popup(title=title,
	content=Label(text=text),
	size_hint=(None, None), size=(250, 200))
	popup.open()

closer = False
new_date = StringProperty("")

def ch_closer():
	global closer

	if closer == True:
		closer = False
	elif closer == False:
		closer = True

sync()

if __name__ == "__main__":
	ProtoApp().run()
