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
from time import sleep

from kivy.properties import StringProperty, NumericProperty
from kivy.uix.popup import Popup



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
		font_size: 35
		size_hint: (.8, .15)
		pos_hint: {'center_x': .5, 'center_y': .35}
		background_normal: "but.png"
		background_down: "butp.png"
		on_press:
			root.manager.current = "work"

	Button:
		text: "Database"
		font_size: 35
		pos_hint: {'center_x': .5, 'center_y': .23}
		size_hint: (.8, .15)
		background_normal: "but.png"
		background_down: "butp.png"

<WorkScreen>:
	canvas:
		Rectangle:
			size: self.size
			pos: self.pos
			source: "work.png"
	Label:
		size: self.texture_size
		text: root.worktext
		font_size: 40
		pos_hint:{"center_x":.5,"center_y":.88}

	TextInput:
		id: inputer
		multiline: False
		size_hint: (.5, .05)
		pos_hint:{"center_x":.5,"center_y":.65}

	Button:
		text: "Ввод"
		font_size: 35
		pos_hint: {'center_x': .5, 'center_y': .5}
		size_hint: (.8, .15)
		background_normal: "but.png"
		background_down: "butp.png"
		on_press:
			root.press += 1
			root.catch_art()

	Button:
		text: "В меню"
		font_size: 35
		pos_hint: {'center_x': .5, 'center_y': .1}
		size_hint: (.8, .15)
		background_normal: "but.png"
		background_down: "butp.png"
		on_press:
			root.manager.current = "menu"
			inputer.text = ""
			root.worktext = "Введите артикул"
			root.press = 0

	""")

class MenuScreen(Screen):
	pass

class WorkScreen(Screen):
	worktext = StringProperty("Введите артикул")
	press = NumericProperty(0)
	cuart = ""
	cudate = ""

	def catch_art(self):
		if self.press == 1:
			self.work()
		elif self.press == 2:
			self.work2()

	def work(self):
		global cuart
		article = self.ids.inputer.text
		if not article.isdigit():
			self.ids.inputer.text = ""
			self.popup("Ошибка", "Введите числовой артикул")
			self.press -= 1
			return
		else:
			cuart = article
			self.ids.inputer.text = ""
			self.worktext = "Введите дату производства ДДММ"

	def work2(self):
		global cudate
		article = cuart
		ask = self.ids.inputer.text
		if ask.isalnum(): 
			if len(ask) == 4:
				if ask[0].isalpha() == False and ask[1].isalpha() == False and ask[2].isalpha() == False and ask[3].isalpha() == False:
					if int(ask[2:]) <= 12 and int(ask[2:]) >= 1 and int(ask[:2]) <= 31 and int(ask[:2]) >= 1:
						if self.check2(ask):
							cudate = ask
							### You stoped THERE. Its CHECK thing, and NEXT is artch. nice job ;)
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

sm = ScreenManager(transition=FadeTransition())
sm.add_widget(MenuScreen(name="menu"))
sm.add_widget(WorkScreen(name="work"))

entries = []
art_names = {}
days_of_life = {}

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