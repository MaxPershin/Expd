from kivy.config import Config
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '414')
Config.set('graphics', 'height', '736')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
import os
from time import strftime
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button

year = int(strftime("%Y"))
if year % 4 == 0:
	extra = 1
else:
	extra = 0

todaynum = int(strftime("%j"))
#We define actual month start days here:

allmonth = {"01": 0, "02": 31, "03": 59+extra, 
"04": 90+extra, "05": 120+extra, "06": 151+extra, 
"07": 181+extra, "08": 212+extra, "09": 243+extra,
"10": 273+extra, "11": 304+extra, "12": 334+extra, "13": 365+extra}

Builder.load_string("""
<MenuScreen>:
	canvas:
		Rectangle:
			size: self.size
			pos: self.pos
			source: "main.png"
	Button:
		text: "Work Mode"
		font_size: sp(40)
		size_hint: (.8, .15)
		pos_hint: {'center_x': .5, 'center_y': .35}
		background_normal: "but.png"
		background_down: "butp.png"
		on_press:
			root.manager.current = "work"

	Button:
		text: "Database"
		font_size: sp(40)
		pos_hint: {'center_x': .5, 'center_y': .23}
		size_hint: (.8, .15)
		background_normal: "but.png"
		background_down: "butp.png"
		on_release:
			root.manager.current = "database"

<WorkScreen>:
	canvas:
		Rectangle:
			size: self.size
			pos: self.pos
			source: "work.png"
	Label:
		size: self.texture_size
		text: root.worktext
		font_size: sp(25)
		pos_hint:{"center_x":.5,"center_y":.88}

	TextInput:
		id: inputer
		multiline: False
		size_hint: (.5, .05)
		pos_hint:{"center_x":.5,"center_y":.65}

	Button:
		text: "Ввод"
		font_size: sp(35)
		pos_hint: {'center_x': .5, 'center_y': .5}
		size_hint: (.8, .15)
		background_normal: "but.png"
		background_down: "butp.png"
		on_release:
			root.press += 1
			root.catch_art()

	Button:
		text: "В меню"
		font_size: sp(35)
		pos_hint: {'center_x': .5, 'center_y': .1}
		size_hint: (.8, .15)
		background_normal: "but.png"
		background_down: "butp.png"
		on_release:
			root.manager.current = "menu"
			inputer.text = ""
			root.worktext = "Введите артикул"
			root.press = 0
<DataBase>:
	canvas:
		Rectangle:
			size: self.size
			pos: self.pos
			source: "clean.png"
	Button:
		text: "В меню"
		font_size: sp(35)
		pos_hint: {'center_x': .5, 'center_y': .1}
		size_hint: (.8, .15)
		background_normal: "but.png"
		background_down: "butp.png"
		on_release:
			root.get_them(1)
			root.manager.current = "menu"
	Button:
		text: "Поиск"
		font_size: sp(35)
		pos_hint: {'center_x': .75, 'center_y': .85}
		size_hint: (.4, .12)
		background_normal: "but.png"
		background_down: "butp.png"
		on_release:
			root.get_them(0)

	TextInput:
		id: searcher
		multiline: False
		size_hint: (.5, .05)
		pos_hint:{"center_x":.3,"center_y":.85}

	ScrollView:
		size_hint_x: .8
		size_hint_y: .6
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
<Information>:
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

		Label:
			canvas.before:
				Color:
					rgba: 0.3, 0.43, 0.24, 1
				Rectangle:
					pos: self.pos
					size: self.size
			id: ghost3
			size: self.texture_size
			size_hint_y: 0.4
			size_hint_x: 0.6
			text: ""
			font_size: sp(30)
			pos_hint:{"center_x":.5,"center_y":.5}
		

		Button:
			text: "Обновить"
			font_size: sp(22)
			pos_hint: {'center_x': .25, 'center_y': .2}
			size_hint: (.5, .12)
			background_normal: "but.png"
			background_down: "butp.png"
			on_release:
				root.start_one()

		Button:
			text: "Редактировать"
			font_size: sp(22)
			pos_hint: {'center_x': .75, 'center_y': .2}
			size_hint: (.5, .12)
			background_normal: "but.png"
			background_down: "butp.png"
			on_release:
				root.init_edit()

		Button:
			text: "Назад"
			font_size: sp(35)
			pos_hint: {'center_x': .5, 'center_y': .1}
			size_hint: (.4, .12)
			background_normal: "but.png"
			background_down: "butp.png"
			on_release:
				root.clearer()
				root.manager.current = "database"

<Editions>:
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
			disabled: root.blocked
			text: "Обновите информацию"
			multiline: False
			size_hint: (.5, .05)
			pos_hint:{"center_x":.3,"center_y":.8}

		TextInput:
			id: article
			disabled: root.blocked
			text: "Обновите информацию"
			multiline: False
			size_hint: (.5, .05)
			pos_hint:{"center_x":.3,"center_y":.7}

		TextInput:
			id: standartdate
			disabled: root.blocked
			text: "Обновите информацию"
			multiline: False
			size_hint: (.5, .05)
			pos_hint:{"center_x":.3,"center_y":.6}

		Button:
			text: "Сохранить"
			disabled: root.blocked
			font_size: sp(22)
			pos_hint: {'center_x': .75, 'center_y': .6}
			size_hint: (.4, .10)
			background_normal: "but.png"
			background_down: "butp.png"
			on_release:
				root.change_popup_name()

		ScrollView:
			size_hint_x: .8
			size_hint_y: .8
			pos_hint: {'center_x': .5, 'center_y': .1}
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

		Button:
			text: "Назад"
			font_size: sp(22)
			pos_hint: {'center_x': .75, 'center_y': .1}
			size_hint: (.5, .12)
			background_normal: "but.png"
			background_down: "butp.png"
			on_release:
				root.blocked = True
				root.clean()
				root.manager.current = "information"
		Button:
			text: "Обновить"
			font_size: sp(22)
			pos_hint: {'center_x': .25, 'center_y': .1}
			size_hint: (.5, .12)
			background_normal: "but.png"
			background_down: "butp.png"
			on_release:
				root.blocked = False
				root.letedit()

	""")

class MenuScreen(Screen):
	pass

class WorkScreen(Screen):
	worktext = StringProperty("Введите артикул")
	press = NumericProperty(0)
	cuart = ""
	cudate = ""
	standartdate = ""
	standartname = ""

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
		article = self.ids.inputer.text
		if not article.isdigit():
			self.ids.inputer.text = ""
			self.popup("Ошибка", "Введите числовой артикул")
			self.press -= 1
			return
		else:
			self.cuart = article
			self.ids.inputer.text = ""
			self.worktext = "Введите дату производства\n или окончания срока ДДММ"

	def work2(self):
		global cudate
		global standartdate

		article = self.cuart
		ask = self.ids.inputer.text
		if ask.isalnum(): 
			if len(ask) == 4:
				if ask[0].isalpha() == False and ask[1].isalpha() == False and ask[2].isalpha() == False and ask[3].isalpha() == False:
					if int(ask[2:]) <= 12 and int(ask[2:]) >= 1 and int(ask[:2]) <= 31 and int(ask[:2]) >= 1:
						if self.check2(ask):
							self.cudate = ask

							if self.cuart in days_of_life:
								self.standartdate = days_of_life[self.cuart]
								self.go()
							else:
								self.ids.inputer.text = ""
								self.worktext = "Введите срок годности в днях или месяцах \n"+"Или введите 0 чтобы указать дату окончания срока"
								self.press = 99

						else:
							self.popup("Внимание!", "В этом месяце нет столько дней")
							self.ids.inputer.text = ""
							self.press -= 1
					else:
						self.popup("Внимание!", "Вы вне диапазона!")
						self.ids.inputer.text = ""
						self.press -= 1
				else:
					self.popup("Внимание!", "Вы ввели буквы")
					self.ids.inputer.text = ""
					self.press -= 1
			else:
				self.popup("Внимание!", "Необходимый формат - ДДММ")
				self.ids.inputer.text = ""
				self.press -= 1
		else:
			self.popup("Внимание!", "Вы ввели символы!")
			self.ids.inputer.text = ""
			self.press -= 1

	def define_date(self):
		for each in self.standartdate:
			if each.isdigit() == False and (each.upper() != "M"):
				self.ids.inputer.text = ""
				self.worktext = "Введите срок годности в днях или месяцах \n"+"Или укажите 0 для указания даты ДО" 
				self.press = 99
				self.popup("Внимание!", "Срок годности должен быть числом дней или месяцев с буквой 'M' в конце")
				return
		f = open("daysoflife.txt", "a")
		f.write(str((self.cuart + "$" + self.standartdate + "$")))
		f.close()

		sync()

		self.worktext = "Введите название артикула"
		self.ids.inputer.text = ""
		self.press = 199

	def define_name(self):
		f = open("artname.txt", "a")
		f.write(str((self.cuart + "$" + self.standartname + "$")))
		f.close()

		sync()

		self.go()

	def go(self):
		month = self.cudate[2:]
		day = self.cudate[:2]
		exactday = allmonth[month] + int(day)
		ex = self.standartdate
		if ex[len(ex)-1].upper() == "M":
			newex = ex.replace("M","")
			newex2 = newex.replace("m", "")
			ex = newex2
			halfm = int(month) + int(ex)
			while halfm > 12:
				halfm -= 12
			newhalfm = str(halfm)
			halfm = newhalfm
			halfd = self.cudate[:2]
			if len(halfm) < 2:
				halfmm = "0"+ halfm
				halfm = halfmm
			final = halfd + halfm
			self.save(final, self.cuart)
			sell = "Expd is before {}".format(final)
			self.popup("Сохранено", sell)
			self.worktext = "Введите артикул"
			self.ids.inputer.text = ""
			self.press = 0

		elif str(ex).isdigit() == True and int(ex) >= 0:
			ex = int(ex)
			ex = self.newcycle(ex)
			summing = exactday + ex
			if summing <= 32:
				a = 31 - summing
				dayf = 31 - a
				sell = "ExpD is BEFORE %0d.01" % dayf
				ent = "%0d01" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing <= (59+extra):
				a = (59+extra) - summing
				dayf = (28+extra) - a
				sell = "ExpD is BEFORE %0d.02" % dayf
				ent = "%0d02" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing <= (90+extra):
				a = (90+extra) - summing
				dayf = 31 - a
				sell = "ExpD is BEFORE %0d.03" % dayf
				ent = "%0d03" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing <= (120+extra):
				a = (120+extra) - summing
				dayf = 30 - a
				sell = "ExpD is BEFORE %0d.04" % dayf
				ent = "%0d04" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing <= (151+extra):
				a = (151+extra) - summing
				dayf = 31 - a
				sell = "ExpD is BEFORE %0d.05" % dayf
				ent = "%0d05" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing <= (181+extra):
				a = (181+extra) - summing
				dayf = 30 - a
				sell = "ExpD is BEFORE %0d.06" % dayf
				ent = "%0d06" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing <= (212+extra):
				a = (212+extra) - summing
				dayf = 31 - a
				sell = "ExpD is BEFORE %0d.07" % dayf
				ent = "%0d07" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing <= (243+extra):
				a = (243+extra) - summing
				dayf = 31 - a
				sell = "ExpD is BEFORE %0d.08" % dayf
				ent = "%0d08" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing <= (273+extra):
				a = (273+extra) - summing
				dayf = 30 - a
				sell = "ExpD is BEFORE %0d.09" % dayf
				ent = "%0d09" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing <= (304+extra):
				a = (304+extra) - summing
				dayf = 31 - a
				sell = "ExpD is BEFORE %0d.10" % dayf
				ent = "%0d10" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing <= (334+extra):
				a = (334+extra) - summing
				dayf = 30 - a
				sell = "ExpD is BEFORE %0d.11" % dayf
				ent = "%0d11" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing <= (365+extra):
				a = (365+extra) - summing
				dayf = 31 - a
				sell = "ExpD is BEFORE %0d.12" % dayf
				ent = "%0d12" % dayf
				self.save(ent, self.cuart)
				self.popup("Сохранено", sell)
				self.worktext = "Введите артикул"
				self.ids.inputer.text = ""
				self.press = 0
			elif summing >= (365+extra):
				ov = summing - (365+extra)
				realanwser = self.cycle(ov)
				if len(realanwser) != 19:
					ent = realanwser[15] + realanwser[16] + realanwser[18] + realanwser[19]
					self.save(ent, self.cuart)
					self.popup("Сохранено", realanwser)
					self.worktext = "Введите артикул"
					self.ids.inputer.text = ""
					self.press = 0
					sync()
				else:
					ent = realanwser[15] + realanwser[17] + realanwser[18]
					self.save(ent, self.cuart)
					self.popup("Сохранено", realanwser)
					self.worktext = "Введите артикул"
					self.ids.inputer.text = ""
					self.press = 0
					sync()
		else:
			self.popup("Внимание", "Некорректное количество дней")

	def cycle(self, ov):
		if ov < 32:
			a = 31 - ov
			dayf = 31 - a
			return "ExpD is BEFORE %0d.01" % dayf
		elif ov < (59+extra):
			a = (59+extra) - ov
			dayf = (28+extra) - a
			return "ExpD is BEFORE %0d.02" % dayf
		elif ov < (90+extra):
			a = (90+extra) - ov
			dayf = 31 - a
			return "ExpD is BEFORE %0d.03" % dayf
		elif ov < (120+extra):
			a = (120+extra) - ov
			dayf = 30 - a
			return "ExpD is BEFORE %0d.04" % dayf
		elif ov < (151+extra):
			a = (151+extra) - ov
			dayf = 31 - a
			return "ExpD is BEFORE %0d.05" % dayf
		elif ov < (181+extra):
			a = (181+extra) - ov
			dayf = 30 - a
			return "ExpD is BEFORE %0d.06" % dayf
		elif ov < (212+extra):
			a = (212+extra) - ov
			dayf = 31 - a
			return "ExpD is BEFORE %0d.07" % dayf
		elif ov < (243+extra):
			a = (243+extra) - ov
			dayf = 31 - a
			return "ExpD is BEFORE %0d.08" % dayf
		elif ov < (273+extra):
			a = (273+extra) - ov
			dayf = 30 - a
			return "ExpD is BEFORE %0d.09" % dayf
		elif ov < (304+extra):
			a = (304+extra) - ov
			dayf = 31 - a
			return "ExpD is BEFORE %0d.10" % dayf
		elif ov < (334+extra):
			a = (334+extra) - ov
			dayf = 30 - a
			return "ExpD is BEFORE %0d.11" % dayf
		elif ov < (365+extra):
			a = (365+extra) - ov
			dayf = 31 - a
			return "ExpD is BEFORE %0d.12" % dayf
		elif ov >= (365+extra):
			ov - (365+extra)
			self.cycle(ov)

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

		self.short = False

	def newcycle(self, ov):
		switch = True
		while switch:
			if ov > 365:
				ov -= 365
			else:
				return ov

class DataBase(Screen):

	def get_them(self, code):
			search = self.ids.searcher.text
			grid = self.ids.griddy
			grid.bind(minimum_height=grid.setter("height"))
			grid.clear_widgets()
			if len(art_names) == 0 and code == 0:
				self.popup("Внимание", "В базе данных нет записей")
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

		self.manager.current = "information"

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

class Information(Screen):
	def start_one(self):
		self.ids.ghost.text = art_names[inf_art]
		self.ids.ghost2.text = inf_art
		self.ids.ghost4.text = "Срок годности: {}".format(days_of_life[inf_art])


		hound = [i for i,x in enumerate(entries) if x==inf_art]
		temper = [i-1 for i in hound]
		hound = []
		for each in temper:
			hound.append(entries[each])

		newfag = " \n".join(hound)
		self.ids.ghost3.text = newfag

	def init_edit(self):
		if self.ids.ghost2.text == "":
			pass
		else:
			self.manager.current = "edition"

	def clearer(self):
		self.ids.ghost.text = "Нажмите обновить"
		self.ids.ghost2.text = ""
		self.ids.ghost4.text = ""
		self.ids.ghost3.text = ""

class Editions(Screen):

	blocked = BooleanProperty(True)

	def letedit(self):
		self.ids.name.text = art_names[inf_art]
		self.ids.article.text = inf_art
		self.ids.standartdate.text = days_of_life[inf_art]

		self.grid = self.ids.griddy
		self.grid.bind(minimum_height=self.grid.setter("height"))
		self.grid.clear_widgets()
		
		hound = [i for i,x in enumerate(entries) if x==inf_art]
		leisu = []
		for each in hound:
			leisu.append(each-1)
		hound = []
		for each in leisu:
			hound.append(entries[each])

		for each in hound:
			self.texter = "  До\n"+str(each)
			self.btn = Button(id=each, text=self.texter, size_hint_y=None, height=0.09*self.height, font_size=0.035*self.height)
			self.grid.add_widget(self.btn)

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

		sync()

		inf_art = new_art
		print(inf_art)

		ch_closer()
		self.change_popup_name()

	def change_popup_art(self):
		pass

	def change_popup_date(self):
		pass

inf_art = StringProperty("z")

sm = ScreenManager(transition=FadeTransition())
sm.add_widget(MenuScreen(name="menu"))
sm.add_widget(WorkScreen(name="work"))
sm.add_widget(DataBase(name="database"))
sm.add_widget(Information(name="information"))
sm.add_widget(Editions(name="edition"))



entries = []
art_names = {}
days_of_life = {}

def popup(title, text):
	popup = Popup(title=title,
	content=Label(text=text),
	size_hint=(None, None), size=(200, 100))
	popup.open()

closer = False

def ch_closer():
	global closer

	if closer == True:
		closer = False
	elif closer == False:
		closer = True

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

sync()

class TestApp(App):
	def build(self):
		return sm

if __name__ == "__main__":
	TestApp().run()