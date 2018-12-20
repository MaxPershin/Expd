#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

from kivy.config import Config
Config.set('graphics', 'resizable', True)
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

year = int(strftime("%Y"))
if year % 4 == 0:
 	extra = 1
else:
 	extra = 0

allmonth = {"01": 0, "02": 31, "03": 59+extra, 
"04": 90+extra, "05": 120+extra, "06": 151+extra, 
"07": 181+extra, "08": 212+extra, "09": 243+extra,
"10": 273+extra, "11": 304+extra, "12": 334+extra, "13": 365+extra}

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
				if data == 'CLS':
					self.ids.ex_inputer2.text = ''
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
			tommorow = fnum2text(int(strftime("%j"))+1)
			if len(tommorow) < 4:
				tommorow = '0'+tommorow

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

	def define_today_art(self):
		tommorow = fnum2text(int(strftime("%j"))+1)
		if len(tommorow) < 4:
			tommorow = '0'+tommorow

		hound = [i for i,x in enumerate(entries) if x==tommorow]

		if len(hound) == 0:
			self.ids.mana.current = "today"
			self.ids.griddy4.clear_widgets()
			self.col = (.1, .1, .1, .3)
			self.sp_text ='Нет артикулов с \nистекающим сроком годности'
		else:
			self.col = (.1, .1, .1, .0)
			self.sp_text =''
			storage = []

			for each in hound:
				storage.append(entries[each+1])

			self.ids.inin.text = tommorow

			self.grid = self.ids.griddy4
			self.grid.bind(minimum_height=self.grid.setter("height"))
			self.grid.clear_widgets()

			for each in storage:
				self.texter = each + ' ' + art_names[each]
				self.btn = ToggleButton(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size=0.035*self.height)
				self.grid.add_widget(self.btn)
				self.btn.bind(on_press=self.check_status)

			self.ids.mana.current = "today"

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

		self.catch_art()

	def repeat(self):

		if last_art == None:
			popup("Внимание", "Нет прошлого артикула")
		else:
			self.ids.inputer.text = last_art

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

			global last_art
			last_art = self.ids.inputer.text
			self.cuart = article
			self.ids.inputer.text = ""
			self.worktext = "Введите дату производства\n или окончания срока ДДММ"

	def work2(self):
		global cudate
		global standartdate

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

							if self.cuart in days_of_life:
								self.standartdate = days_of_life[self.cuart]
								self.go()
								self.ids.inputer.text = ''
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
								self.dater_invisible()
								self.step = 0
								self.worktext = "Введите срок годности в днях или месяцах"
								self.press = 99

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
		for each in self.standartdate:
			if each.isdigit() == False and (each.upper() != "M"):
				self.ids.inputer.text = ""
				self.worktext = "Введите срок годности в днях или месяцах \n"+"Или укажите 0 для указания даты ДО" 
				self.press = 99
				popup("Внимание!", "Срок годности должен быть числом дней или месяцев с буквой 'M' в конце")
				return

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

			final = '{}{}'.format(day, month)

			self.save(final, self.cuart)
			sell = "Expd is before {}".format(final)
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

			sell = 'Срок годности до {}{}'.format(day, month)
			ent = '{}{}'.format(day, month)

			print('Фактически дата такова ', day, month, year)

			self.save(ent, self.cuart)
			popup("Сохранено", sell)
			self.worktext = "Введите артикул"
			self.ids.inputer.text = ""
			self.press = 0
			
		else:
			popup("Внимание", "Некорректное количество дней")

	def check2(self, ask):
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

	def popup(self, title, text):
		popup = Popup(title=title,
		content=Label(text=text),
		size_hint=(None, None), size=(200, 100))
		popup.open()

	def save(self, ent, article):
		if len(ent) == 3:
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
				print('WE DEFINE M In there')
				tester = []
				for each in self.inputi3.text:
					tester.append(each.lower())
				print(tester)
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
			month = each[2:]
			day = each[:2]
			exactday = allmonth[month] + int(day)
			sorter.append(exactday)

		sorter.sort()

		hound = []

		for each in sorter:
			temp = fnum2text(each)
			if len(temp) == 3:
				temp = '0'+temp
			hound.append(temp)

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
			month = each[2:]
			day = each[:2]
			exactday = allmonth[month] + int(day)
			sorter.append(exactday)

		sorter.sort()

		hound = []

		for each in sorter:
			temp = fnum2text(each)
			if len(temp) == 3:
				temp = '0'+temp
			hound.append(temp)

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

		self.letedit()

	def save_entry1(self, *args):
		global new_date

		new_date = args[-1]

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

				self.letedit()
		else:
			popup("Внимание!", "Вы не изменили дату")

	def datetest(self, date):
		ask = date
		if ask.isalnum(): 
			if len(ask) == 4:
				if ask[0].isalpha() == False and ask[1].isalpha() == False and ask[2].isalpha() == False and ask[3].isalpha() == False:
					if int(ask[2:]) <= 12 and int(ask[2:]) >= 1 and int(ask[:2]) <= 31 and int(ask[:2]) >= 1:
						if self.check666(ask):
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

	def check666(self, ask):
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

		popup("Внимание", "База данных была полностью удалена")
		self.clearer()
		self.ids.griddy.clear_widgets()
		self.ids.griddy4.clear_widgets()

###########################---App_Classes---##################################
class ProtoApp(App):
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

<Core>:
	orientation: "vertical"
	BoxLayout:
		size_hint_y: 8
		canvas.before: 
			Color: 
				rgb: 0, .8, 0 
			Rectangle: 
				pos: self.pos 
				size: self.size
		Label:
			text: 'AVOCADO'

	ScreenManagement:
		transition: NoTransition()
		id: mana
		size_hint_y: 84


		Screen:
			name: 'work'
			FloatLayout:
				canvas:
					Rectangle:
						size: self.size
						pos: self.pos
						source: "work.png"
				Label:
					halign: 'center'
					valign: "middle"
					text: root.worktext
					text_size: self.size
					size_hint: (.8, .15)
					font_size: sp(25)
					pos_hint:{"center_x": .5,"center_y":.87}

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
						source: "clean.png"

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
				size_hint_x: .8
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
						source: "clean.png"
				TextInput:
					disabled: True
					id: inin
					multiline: False
					size_hint: (.33, .05*1.75)
					pos_hint:{"center_x":.5,"center_y":.9}
					font_size: sp(35)

				ScrollView:
					size_hint_x: .8
					size_hint_y: .65
					pos_hint: {'center_x': .5, 'center_y': .5}
					GridLayout:
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
					pos_hint: {'center_x': .5, 'center_y': .1}
					size_hint: (.24, .22)
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
						source: "clean.png"

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
						source: "clean.png"
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
					size_hint_x: .8
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
						source: "clean.png"

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






	BoxLayout:
		size_hint_y: 8
		ToggleButton:
			allow_no_selection: False
			group: 'test'
			state: 'down'
			text: "WORK"
			on_press: root.ids.mana.current = "work"

		ToggleButton:
			allow_no_selection: False
			group: 'test'
			text: 'DB'
			on_press: root.ids.mana.current = "database"

		ToggleButton:
			allow_no_selection: False
			group: 'test'
			text: 'Today'
			on_press: root.define_today_art()

		ToggleButton:
			allow_no_selection: False
			group: 'test'
			text: 'Settings'
			on_press: root.ids.mana.current = "settings"
	""")

entries = []
art_names = {}
days_of_life = {}
last_art = None


def fnum2text(nu):
	if nu <= 32:
		a = 31 - nu
		res = 31 - a			
		ent = "%0d01" % res
		return ent
	elif nu <= (59+extra):
		a = (59+extra) - nu
		res = (28+extra) - a			
		ent = "%0d02" % res
		return ent
	elif nu <= (90+extra):
		a = (90+extra) - nu
		res = 31 - a			
		ent = "%0d03" % res
		return ent
	elif nu <= (120+extra):
		a = (120+extra) - nu
		res = 30 - a			
		ent = "%0d04" % res
		return ent
	elif nu <= (151+extra):
		a = (151+extra) - nu
		res = 31 - a			
		ent = "%0d05" % res
		return ent
	elif nu <= (181+extra):
		a = (181+extra) - nu
		res = 30 - a			
		ent = "%0d06" % res
		return ent
	elif nu <= (212+extra):
		a = (212+extra) - nu
		res = 31 - a			
		ent = "%0d07" % res
		return ent
	elif nu <= (243+extra):
		a = (243+extra) - nu
		res = 31 - a			
		ent = "%0d08" % res
		return ent
	elif nu <= (273+extra):
		a = (273+extra) - nu
		res = 30 - a			
		ent = "%0d09" % res
		return ent
	elif nu <= (304+extra):
		a = (304+extra) - nu
		res = 31 - a			
		ent = "%0d10" % res
		return ent
	elif nu <= (334+extra):
		a = (334+extra) - nu
		res = 30 - a			
		ent = "%0d11" % res
		return ent
	elif nu <= (365+extra):
		a = (365+extra) - nu
		res = 31 - a			
		ent = "%0d12" % res
		return ent
	elif abol > (365+extra):
		count = 0
		res = 1			
		ent = "%0d01" % res
		return ent

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
