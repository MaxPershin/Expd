#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '414')
Config.set('graphics', 'height', '736')
from zbarcam import ZBarCam

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
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior

from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
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
import threading

import json
import requests

from kivy.core.window import Window

year = int(strftime("%Y"))
if year % 4 == 0:
 	extra = 1
else:
 	extra = 0

allmonth = {"01": 0, "02": 31, "03": 59+extra, 
"04": 90+extra, "05": 120+extra, "06": 151+extra, 
"07": 181+extra, "08": 212+extra, "09": 243+extra,
"10": 273+extra, "11": 304+extra, "12": 334+extra, "13": 365+extra}

class MyWidget(ButtonBehavior, BoxLayout):

	def __init__(self, data, **kwargs):
		super(MyWidget, self).__init__(**kwargs)
		self.ids.name.text = data['name']
		self.ids.article.text = data['art']
		try:
			y, m, d = str(data['nearest_date']).split('-')
			self.ids.date.text = "{}.{}.{}".format(d, m, y)
		except:
			self.ids.date.text = "N/A"

		self.scale()


	def on_press(self, *args):
		pass

	def scale(self):
		self.ids.name.texture_update()
		real = self.ids.name.size[1]
		box = self.ids.name.texture_size[1]

		if real < box - 150:
			self.scale_down()

	def scale_down(self):
		self.ids.name.font_size -= 1
		return self.scale()

class SuppaLabel(Label):

	container1 = ObjectProperty(10)
	container2 = ObjectProperty(10)

class Reader(BoxLayout):
	hinter = ObjectProperty({"center_x": .5,"center_y": .9})

	def stop_cam(self, text):
		if text:
			for obj in gc.get_objects():
				try: #This way I could find an instance ;)
					if isinstance(obj, Core):
						mine = obj
						break
				except:
					pass

			mine.stop_cam(text)

class Core(BoxLayout):
	lang = 'ru'
	col = ObjectProperty((.1, .1, .1, .0))
	sp_text = ObjectProperty("")

	if lang == 'ru':
		worktext = ObjectProperty("Введите артикул")
	else:
		worktext = ObjectProperty("Enter Article")


	new_barcode = None
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

	pos_unknown_EAN = ObjectProperty({"center_x": -5,"center_y":.80})

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

	pos_init_cam = ObjectProperty({'center_x': .785, 'center_y': .68})

	container1 = ObjectProperty(10)
	container2 = ObjectProperty(10)

	day_or_what = ObjectProperty('day')

	stop_list =ObjectProperty([])

	shx_today_scroll = ObjectProperty(.95)
	shy_today_scroll = ObjectProperty(.72)
	ph_today_scroll = ObjectProperty({'center_x': .5, 'center_y': .5})

	ranger1 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger2 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger3 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger4 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger5 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger6 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger7 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger8 = ObjectProperty({"center_x":-5,"center_y":.795})
	ranger9 = ObjectProperty({"center_x":-5,"center_y":.795})
	group_home_nothing_color = ObjectProperty((.1, .1, .1, .0))

	prosrochka_button = ObjectProperty({"center_x": -5,"center_y":.9625})

	current_year = str(datetime.now().year)

	current_data = None
	current_user = ObjectProperty('')
	current_group = ObjectProperty('')
	current_password = None
	current_users_and_values = {}
	new_users = ''
	auth_key = "HqpU7WbJBeA4wN058kf9nPo9PZAAiUiEBrC3ZvP5"
	url = 'https://avocado-a066c.firebaseio.com/'
	buttons_color = (0, 0, 0, 1)

	r = None


	#translation

	def to_russian(self):
		self.t_delete = 'Удалить'
		self.t_ot = 'От'
		self.t_do = 'До'
		self.t_day = 'День'
		self.t_month = 'Месяц'
		self.t_year = 'Год'
		self.t_search = 'Поиск'
		self.t_today = 'Сегодня'
		self.t_random = 'Произвольно'
		self.t_period = 'Период'
		self.t_find = 'Найти'
		self.t_dd = 'ДД'
		self.t_mm = 'ММ'
		self.t_edit = 'Редактирование'
		self.t_save = 'Сохранить'
		self.t_add_date = 'Добавить дату'
		self.t_delete_article = 'Удалить артикул'
		self.t_delete_effects = 'Удалить эффекты'
		self.t_delete_database = 'Удалить базу данных'
		self.t_sync = 'Синхронизировать'
		self.t_language = 'Язык'
		self.t_exit = 'Выйти'
		self.t_group = 'группа'
		self.t_your_sync = 'Запланированные действия'
		self.t_expired = 'просрок'
		self.t_group_name = 'Название группы'
		self.t_password = 'Пароль'
		self.t_enter = 'Войти'
		self.t_create_group = 'Создать группу'
		self.t_create_user = 'Создать пользователя'
		self.t_create = 'Создать'
		self.t_user_name = 'Имя пользователя'
		self.t_we_have_expired = 'Найдены просроченные артикулы'
		self.t_manage_ean = 'Управление EAN'

	def to_english(self):
		self.t_delete = 'Delete'
		self.t_ot = 'from'
		self.t_do = 'until'
		self.t_day = 'Day'
		self.t_month = 'Month'
		self.t_year = 'Year'
		self.t_search = 'Search'
		self.t_today = 'Today'
		self.t_random = 'Arbitrarily'
		self.t_period = 'Period'
		self.t_find = 'Find'
		self.t_dd = 'DD'
		self.t_mm = 'MM'
		self.t_edit = 'Editing'
		self.t_save = 'Save'
		self.t_add_date = 'Add date'
		self.t_delete_article = 'Delete article'
		self.t_delete_effects = 'Delete effects'
		self.t_delete_database = 'Delete database'
		self.t_sync = 'Synchronize'
		self.t_language = 'Language'
		self.t_exit = 'Logout'
		self.t_group = 'group'
		self.t_your_sync = 'Actions to sync'
		self.t_expired = 'expired'
		self.t_group_name = 'Group Name'
		self.t_password = 'Password'
		self.t_enter = 'Login'
		self.t_create_group = 'Create group'
		self.t_create_user = 'Create User'
		self.t_create = 'Create'
		self.t_user_name = 'User name'
		self.t_we_have_expired = 'Expired articles found!'
		self.t_manage_ean = 'Manage EAN'
	
	if lang == 'ru':
		t_delete = ObjectProperty('Удалить')
		t_ot = ObjectProperty('От')
		t_do = ObjectProperty('До')
		t_day = ObjectProperty('День')
		t_month = ObjectProperty('Месяц')
		t_year = ObjectProperty('Год')
		t_search = ObjectProperty('Поиск')
		t_today = ObjectProperty('Сегодня')
		t_random = ObjectProperty('Произвольно')
		t_period = ObjectProperty('Период')
		t_find = ObjectProperty('Найти')
		t_dd = ObjectProperty('ДД')
		t_mm = ObjectProperty('ММ')
		t_edit = ObjectProperty('Редактирование')
		t_save = ObjectProperty('Сохранить')
		t_add_date = ObjectProperty('Добавить дату')
		t_delete_article = ObjectProperty('Удалить артикул')
		t_delete_effects = ObjectProperty('Удалить эффекты')
		t_delete_database = ObjectProperty('Удалить базу данных')
		t_sync = ObjectProperty('Синхронизировать')
		t_language = ObjectProperty('Язык')
		t_exit = ObjectProperty('Выйти')
		t_group = ObjectProperty('группа')
		t_your_sync = ObjectProperty('Запланированные действия')
		t_expired = ObjectProperty('просрок')
		t_group_name = ObjectProperty('Название группы')
		t_password = ObjectProperty('Пароль')
		t_enter = ObjectProperty('Войти')
		t_create_group = ObjectProperty('Создать группу')
		t_create_user = ObjectProperty('Создать пользователя')
		t_create = ObjectProperty('Создать')
		t_user_name = ObjectProperty('Имя пользователя')
		t_we_have_expired = ObjectProperty('Найдены просроченные артикулы')
		t_manage_ean = ObjectProperty('Управление EAN')


	else:
		t_delete = 'Delete'
		t_ot = ObjectProperty('from')
		t_do = ObjectProperty('until')
		t_day = ObjectProperty('Day')
		t_month = ObjectProperty('Month')
		t_year = ObjectProperty('Year')
		t_search = ObjectProperty('Search')
		t_today = ObjectProperty('Today')
		t_random = ObjectProperty('Arbitrarily')
		t_period = ObjectProperty('Period')
		t_find = ObjectProperty('Find')
		t_dd = ObjectProperty('DD')
		t_mm = ObjectProperty('MM')
		t_edit = ObjectProperty('Editing')
		t_save = ObjectProperty('Save')
		t_add_date = ObjectProperty('Add date')
		t_delete_article = ObjectProperty('Delete article')
		t_delete_effects = ObjectProperty('Delete effects')
		t_delete_database = ObjectProperty('Delete database')
		t_sync = ObjectProperty('Synchronize')
		t_language = ObjectProperty('Language')
		t_exit = ObjectProperty('Logout')
		t_group = ObjectProperty('group')
		t_your_sync = ObjectProperty('Actions to sync')
		t_expired = ObjectProperty('expired')
		t_group_name = ObjectProperty('Group Name')
		t_password = ObjectProperty('Password')
		t_enter = ObjectProperty('Login')
		t_create_group = ObjectProperty('Create group')
		t_create_user = ObjectProperty('Create User')
		t_create = ObjectProperty('Create')
		t_user_name = ObjectProperty('User name')
		t_we_have_expired = ObjectProperty('Expired articles found!')
		t_manage_ean = ObjectProperty('Manage EAN')

	def reshape_today_scroll(self, data):
		if data == 'today':
			self.shx_today_scroll = .95
			self.shy_today_scroll = .72
			self.ph_today_scroll = {'center_x': .5, 'center_y': .5}
		if data == 'any' or data == 'range':
			self.shx_today_scroll = .95
			self.shy_today_scroll = .72
			self.ph_today_scroll = {'center_x': .5, 'center_y': .375}

	def show_unknown_ean(self, action):
		if action == 'hide':
			self.pos_unknown_EAN = {"center_x": -5,"center_y":.92}
		else:
			self.pos_unknown_EAN = {"center_x": .5,"center_y":.80}
			self.ids.inputer.text = ''
			self.show_cam_button('hide')

	def go_cam(self):
		if self.r == None:
			self.r = Reader()
			self.ids.summertime.add_widget(self.r)
		else:
			self.r.hinter = {"center_x": .5,"center_y": .9}
			self.r.ids.zbarcam.start()

	def stop_cam(self, text):
		self.r.ids.zbarcam.stop()
		self.r.hinter = {"center_x": -2,"center_y": .9}
		if text != "NO":
			text = text.split("'")[1]
			self.compare_barcode(text)
		else:
			return

	def compare_barcode(self, texter):
		
		for each in art_bars:
			if texter in art_bars[each]:
				self.ids.inputer.text = str(each)
				return

		self.new_barcode = texter
		self.show_unknown_ean('show')

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
					self.stop_list.append((each[8:], 'deleteDate', each[:8]))
					self.set_stop_list()
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

			if self.lang == 'ru':
				popup("Внимание", "Данные были удалены")
			else:
				popup('Attention!', 'All data is deleted')

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
			if each[0] <= curent.date():
				just_list.append(each)

		new_kind = sorted(just_list, key=lambda x: x[0])

########################-------------------------We have all what we want sorted now###############

		self.grid = self.ids.griddy_trash
		self.grid.bind(minimum_height=self.grid.setter("height"))
		self.grid.clear_widgets()

		last_date = ''

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


			if last_date != '{}{}{}'.format(each[0].day, each[0].month, each[0].year):
				last_date = '{}{}{}'.format(each[0].day, each[0].month, each[0].year)
				dayr = str(each[0].day)
				monthr = str(each[0].month)

				if len(dayr) < 2:
					dayr = '0'+dayr
				if len(monthr) < 2:
					monthr = '0'+monthr

				if self.lang == 'ru':
					m_label.text = 'Просрок до {}.{}.{}'.format(dayr, monthr, each[0].year)
				else:
					m_label.text = 'Expired at {}.{}.{}'.format(dayr, monthr, each[0].year)
				m_label.container1 = 0.06*self.height
				m_label.container2 = 0.035*self.height
				self.grid.add_widget(m_label)
			else:
				pass

			self.texter = str(counter)+'. ' + each[1] + ' ' + art_names[each[1]]
			self.btn = ToggleButton(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size="25sp")
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
			if self.lang == 'ru':
				popup('Внимание', 'Дата введена не корректно!')
			else:
				popup('Warning', 'Incorrect date!')
			return

		holder = {}

		this_date = True

		for x in range(len(entries)-1):
			if this_date:
				c = date(int(entries[x][4:]),int(entries[x][2:4]),int(entries[x][:2]))
				if c >= start_date and c <= end_date:
					if c in holder:
						holder[c].append(entries[x+1])
					else:
						holder[c] = [entries[x+1]]

					this_date = not this_date
				else:
					this_date = not this_date
					continue
			else:
				this_date = not this_date


		hope = []

		for key in sorted(holder.keys()):
			hope.append((key, holder[key]))


		if len(hope) == 0:
			return
		else:
			self.col = (.1, .1, .1, .0)
			self.sp_text =''

			self.grid = self.ids.griddy4
			self.grid.bind(minimum_height=self.grid.setter("height"))


			for each in hope:
				day = str(each[0].day)
				month = str(each[0].month)
				year = str(each[0].year)

				if len(day) < 2:
					day = '0'+day
				if len(month) < 2:
					month = '0'+month

				m_label = SuppaLabel()

				if self.lang == 'ru':
					m_label.text = 'Списать до {}.{}.{}'.format(day, month, year)
				else:
					m_label.text = 'Dispose until {}.{}.{}'.format(day, month, year)

				m_label.container1 = 0.06*self.height
				m_label.container2 = 0.035*self.height

				self.grid.add_widget(m_label)

				for eaz in each[1]:
					self.texter = eaz + ' ' + art_names[eaz]
					self.btn = Button(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size="25sp")
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

			self.pos_el5 = ({'center_x': .5, 'center_y': .08})

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

			if len(day) < 2:
				day = '0'+day
			if len(month) < 2:
				month = '0'+month 

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

			temp = []

			for each in hound:
				temp.append(dawread[each])
				if len(temp) == 2:
					self.stop_list.append((temp[0], 'deleteDate', temp[1]))
					self.set_stop_list()
					temp = []

				del dawread[each]

			with open("saver.txt", "w") as f:
				for each in dawread:
					f.write(str(each + "$"))

			sync()

			self.ids.griddy4.clear_widgets()

			self.define_today_art('today')

			self.found_arts = []

			if self.lang == 'ru':
				popup("Внимание", "Данные были удалены")
			else:
				popup('Attention', 'Data is deleted')

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
					if self.lang == 'ru':
						self.sp_text ='Нет артикулов'
					else:
						self.sp_text = 'No articles'
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

					if self.lang == 'ru':
						m_label.text = 'Списать до {}.{}.{}'.format(day, month, year)
					else:
						m_label.text = 'Dispose until {}.{}.{}'.format(day, month, year)

					m_label.container1 = 0.06*self.height
					m_label.container2 = 0.035*self.height


					self.grid.add_widget(m_label)


					for each in storage:
						self.texter = each + ' ' + art_names[each]
						self.btn = Button(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size="25sp")
						self.grid.add_widget(self.btn)

					self.ids.mana.current = "today"
					self.ids.to_d1.text = ''
					self.ids.to_d2.text = ''
					self.ids.to_d3.text = ''
			else:
				if self.lang == 'ru':
					popup("Внимание", "Вы ввели неверную дату")
				else:
					popup('Warning', 'You entered incorrect date')

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
				if self.lang == 'ru':
					self.sp_text ='Нет артикулов'
				else:
					self.sp_text = 'No articles'

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

				if self.lang == 'ru':
					m_label.text = 'Списать сегодня'
				else:
					m_label.text = 'Dispose today'

				m_label.container1 = 0.06*self.height
				m_label.container2 = 0.035*self.height


				self.grid.add_widget(m_label)


				for each in storage:
					self.texter = each + ' ' + art_names[each]
					self.btn = ToggleButton(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size="25sp")
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
		if self.lang == 'ru':
			self.worktext = 'Введите артикул'
		else:
			self.worktext = 'Enter Article'

		self.pos_day_month_visible(False)
		self.show_cam_button('show')

		self.catch_art()

	def repeat(self):

		if last_art == None:
			if self.lang == 'ru':
				popup("Внимание", "Нет прошлого артикула")
			else:
				popup('Warning', "You don't have previous article")
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
			if self.lang == 'ru':
				self.worktext = "Введите срок годности"
			else:
				self.worktext = 'Enter article shelf life' 
			self.press = 99

			if self.lang == 'ru':
				popup("Внимание!", "Срок годности должен быть числом")
				return
			else:
				popup("Warning!", "Article shelf life should be a number")
				return

		for each in self.standartdate:
			if each.isdigit() == False and (each.upper() != "M"):
				self.ids.inputer.text = ""
				self.pos_day_month_visible(True)
				if self.lang == 'ru':
					self.worktext = "Введите срок годности в днях или месяцах"
				else:
					self.worktext = "Please enter shelf life in days or month"
				self.press = 499
				if self.lang == 'ru':
					popup("Внимание!", "Срок годности должен быть числом дней или месяцев с буквой 'M' в конце")
				else:
					popup("Внимание!", "Shelf life should be a whole number of days or month")
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

			if self.lang == 'ru':
				popup("Ошибка", "Введите числовой артикул")
			else:
				popup('Error', 'Enter digital article')

			self.press -= 1
			return
		else:
			self.step = 1
			self.dater_visible()
			self.show_buttons_before_after('show')
			self.show_cam_button('hide')

			if self.new_barcode != None:
				self.save_ean(article)

			self.show_unknown_ean('hide')

			global last_art
			last_art = self.ids.inputer.text
			self.cuart = article
			self.ids.inputer.text = ""
			if self.lang == 'ru':
				self.worktext = "Введите дату производства\n или окончания срока"
			else:
				self.worktext = "Enter production date\n or expiry date"

	def save_ean(self, article):
		self.if_recreated(article, 'deleteEAN', self.new_barcode)
		f = open("barcode.txt", "a", newline='')
		f.write(str((article + "$" + self.new_barcode + "$")))
		f.close()
		self.new_barcode = None
		sync()

	def show_cam_button(self, action):
		if action == 'hide':
			self.pos_init_cam = {'center_x': -2, 'center_y': .8}
		else:
			self.pos_init_cam = {'center_x': .785, 'center_y': .68}
			self.show_unknown_ean('hide')

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

									if self.lang == 'ru':
										self.worktext = 'Введите срок годности'
									else:
										self.worktext = 'Enter shelf life'

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

									if self.lang == 'ru':
										self.worktext = "Введите срок годности"
									else:
										self.worktext = 'Enter shelf life'

									self.press = 99
								else:
									global standartdate
									self.ids.inputer.focus = True

									if self.lang == 'ru':	
										self.worktext = 'Введите название артикула'
									else:
										self.worktext = 'Enter article name'

									self.standartdate = "0"
									self.press = 199

						else:
							if self.lang == 'ru':
								popup("Внимание!", "В этом месяце нет столько дней")
							else:
								popup('Warning!', "That month doesn't have so much days")
							self.ids.ex_inputer.text = ""
							self.ids.ex_inputer2.text = ""
							self.press -= 1
					else:
						if self.lang == 'ru':
							popup("Внимание!", "Вы вне диапазона!")
						else:
							popup('Warning!', 'You are out of range!')
						self.ids.ex_inputer.text = ""
						self.ids.ex_inputer2.text = ""
						self.press -= 1
				else:
					if self.lang == 'ru':
						popup("Внимание!", "Вы ввели буквы")
					else:
						popup('Warning!', 'You entered literals')

					self.ids.ex_inputer.text = ""
					self.ids.ex_inputer2.text = ""
					self.press -= 1
			else:
				if self.lang == 'ru':
					popup("Внимание!", "Необходимый формат - ДДММ")
				else:
					popup('Warning!', 'Should be in DDMM format')

				self.ids.ex_inputer.text = ""
				self.ids.ex_inputer2.text = ""
				self.press -= 1
		else:
			if self.lang == 'ru':
				popup("Внимание!", "Вы ввели символы!")
			else:
				popup('Warning!', "You entered symbols!")

			self.ids.ex_inputer.text = ""
			self.ids.ex_inputer2.text = ""
			self.press -= 1

	def define_date(self):
		if len(self.standartdate) == 0:
			self.ids.inputer.text = ""
			self.pos_day_month_visible(True)
			if self.lang == 'ru':
				self.worktext = "Введите срок годности"
			else:
				self.worktext = 'Enter shelf life'
			self.press = 99

			if self.lang == 'ru':
				popup("Внимание!", "Срок годности должен быть числом")
			else:
				popup('Warning!', 'Shelf life should be a whole number')
			return

		for each in self.standartdate:
			if each.isdigit() == False:
				self.ids.inputer.text = ""
				self.pos_day_month_visible(True)

				if self.lang == 'ru':
					self.worktext = "Введите срок годности"
				else:
					self.worktext = 'Enter shelf life' 
				self.press = 99

				if self.lang == 'ru':
					popup("Внимание!", "Срок годности должен быть числом")
				else:
					popup('Warning!', 'Shelf life should be a whole number')
				return

		if self.day_or_what == 'month':
			self.standartdate = self.standartdate + 'm'
		elif self.day_or_what == 'year':
			self.standartdate = self.standartdate + 'y'

		self.pos_day_month_visible(False)

		if self.lang == 'ru':
			self.worktext = "Введите название артикула"
		else:
			self.worktext = 'Enter article name'

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

		self.if_recreated(self.cuart, 'deleteART', None)
		self.if_recreated(self.cuart, 'deleteDate', final)

		self.save(final, self.cuart)
		if self.lang == 'ru':
			sell = "Срок годности до {}".format(final)
			popup("Сохранено", sell)
			self.worktext = "Введите артикул"
		else:
			sell = "Best before {}".format(final)
			popup("Saved", sell)
			self.worktext = "Enter article"

		self.ids.inputer.text = ""
		self.press = 0
		self.show_cam_button('show')
		self.alarm()

	def wise(self):
		self.popup.dismiss()

		if self.lang == 'ru':
			self.worktext = "Введите артикул"
		else:
			self.worktext = 'Enter article'

		self.ids.inputer.text = ""
		self.press = 0
		self.show_cam_button('show')


	def enter_prosrok(self, final):
		if self.lang == 'ru':
			title = 'Внимание!'
			label = Label(text='Сохраняемый артикул просрочен,\n все равно сохранить?')
			btn1 = Button(text='Да', on_release=lambda x: self.save_anyway(final))
			btn2 = Button(text='Нет', on_release=lambda x: self.wise())
		else:
			title = 'Warning!'
			label = Label(text='This article is already expired,\n save it anyway?')
			btn1 = Button(text='Yes', on_release=lambda x: self.save_anyway(final))
			btn2 = Button(text='No', on_release=lambda x: self.wise())

		fl = BoxLayout(orientation='vertical')
		fl.add_widget(label)
		bx = BoxLayout(orientation='horizontal')
		bx.add_widget(btn1)
		bx.add_widget(btn2)

		fl.add_widget(bx)

		self.popup = Popup(title=title,
		content=fl,
		size_hint=(0.65, 0.25))
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

				self.if_recreated(self.cuart, 'deleteART', None)
				self.if_recreated(self.cuart, 'deleteDate', final)

				self.save(final, self.cuart)

				if self.lang == 'ru':
					sell = "Срок годности до {}".format(repres)
					popup("Сохранено", sell)
					self.worktext = "Введите артикул"
				else:
					sell = "Best before {}".format(repres)
					popup("Saved", sell)
					self.worktext = "Enter article"

				self.ids.inputer.text = ""
				self.press = 0
				self.show_cam_button('show')

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

				self.if_recreated(self.cuart, 'deleteART', None)
				self.if_recreated(self.cuart, 'deleteDate', final)

				self.save(final, self.cuart)
				if self.lang == 'ru':
					sell = "Срок годности до {}".format(repres)
					popup("Сохранено", sell)
					self.worktext = "Введите артикул"
				else:
					sell = "Best before {}".format(repres)
					popup("Saved", sell)
					self.worktext = "Enter article"

				self.ids.inputer.text = ""
				self.press = 0
				self.show_cam_button('show')

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

			if self.lang == 'ru':
				sell = 'Срок годности до {}.{}.{}'.format(day, month, year)
			else:
				sell = 'Best before {}.{}.{}'.format(day, month, year)

			ent = '{}{}{}'.format(day, month, year)

			todayer = date.today()
			
			if c <= todayer:
				self.enter_prosrok(ent)
			else:

				self.if_recreated(self.cuart, 'deleteART', None)
				self.if_recreated(self.cuart, 'deleteDate', ent)

				self.save(ent, self.cuart)
				if self.lang == 'ru':
					popup("Сохранено", sell)
					self.worktext = "Введите артикул"
				else:
					popup("Saved", sell)
					self.worktext = "Enter article"

				self.ids.inputer.text = ""
				self.press = 0
				self.show_cam_button('show')
			
		else:
			if self.lang == 'ru':
				popup("Внимание", "Некорректное количество дней")
			else:
				popup('Warning', 'Incorrect number of days')

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
		size_hint=(0.65, 0.25))
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
			if self.lang == 'ru':
				popup("Внимание!", "Эта дата уже записана для этого артикула")
				self.worktext = "Введите артикул"
			else:
				popup("Warning!", "This date is already exist")
				self.worktext = "Enter article"

			self.ids.inputer.text = ""
			self.press = 0
			self.show_cam_button('show')
		else:
			f = open("saver.txt", "a")
			f.write(str((ent + "$" + article + "$")))
			f.close()
			sync()

##########################################################------Database------##############################3
	def create_new(self):
		if self.lang == 'ru':
			tit = 'Создание'
			sentence = "Заполните необходимые поля\n чтобы создать артикул"
			self.layout = FloatLayout(size=(self.width, self.height))
			self.inputi = TextInput(hint_text="Артикул", multiline=False, size_hint_x=.5, size_hint_y=0.1, pos_hint={"center_x":.5,"center_y":.6})
			self.inputi2 = TextInput(hint_text="Название", multiline=False, size_hint_x=.5, size_hint_y=0.1, pos_hint={"center_x":.5,"center_y":.45})
			self.inputi3 = TextInput(hint_text="Стандартный срок", multiline=False, size_hint_x=.5, size_hint_y=0.1, pos_hint={"center_x":.5,"center_y":.35})
			self.btn1 = Button(text="Создать", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.2}, on_release=lambda x:self.art_create())
		else:
			tit = 'Creation'
			sentence = "Please fill required fields\n to create article"
			self.layout = FloatLayout(size=(self.width, self.height))
			self.inputi = TextInput(hint_text="Article", multiline=False, size_hint_x=.5, size_hint_y=0.1, pos_hint={"center_x":.5,"center_y":.6})
			self.inputi2 = TextInput(hint_text="Name", multiline=False, size_hint_x=.5, size_hint_y=0.1, pos_hint={"center_x":.5,"center_y":.45})
			self.inputi3 = TextInput(hint_text="Shelf life", multiline=False, size_hint_x=.5, size_hint_y=0.1, pos_hint={"center_x":.5,"center_y":.35})
			self.btn1 = Button(text="Create", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.2}, on_release=lambda x:self.art_create())

		self.lbl = Label(text=sentence, text_size=(self.width, None), halign='center', font_size="20sp", pos_hint={"center_x":.5,"center_y":.86})

		self.layout.add_widget(self.lbl)
		self.layout.add_widget(self.inputi)
		self.layout.add_widget(self.inputi2)
		self.layout.add_widget(self.inputi3)
		self.layout.add_widget(self.btn1)

		self.popup = Popup(title=tit,
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
					if self.lang == 'ru':
						popup("Внимание!", "Срок годности должен быть числом\n дней, месяцев, или лет")
					else:
						popup("Warning!", "Shelf life should be a number of\n days, months or years")
					return
				else:
					correct = True
			else:
				if self.lang == 'ru':
					popup("Внимание!", "Срок годности должен быть числом\n дней, месяцев, или лет")
				else:
					popup("Warning!", "Shelf life should be a number of\n days, months or years")

				return

			if correct == False:
				if self.lang == 'ru':
					popup("Внимание!", "Срок годности должен быть числом\n дней, месяцев, или лет")
				else:
					popup("Warning!", "Shelf life should be a number of\n days, months or years")

				return
			else:
				if self.inputi.text in art_names:
					if self.lang == 'ru':
						popup("Внимание!", "Этот артикул уже есть в базе данных")
					else:
						popup('Warning!', 'This article is already in a database')
					return
				else:
					
					self.if_recreated(self.inputi.text, 'deleteART', None)

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
			if self.lang == 'ru':
				popup("Внимание!", "Введите данные корректно")
			else:
				popup('Warning!', 'Enter correct data!')
			return

	def if_recreated(self, article, typer, value):
		if typer == 'deleteART':
			return self.deleteART_check(article)

		elif typer == 'deleteDate':
			return self.deleteDate_check(article, value)

		elif typer == 'deleteEAN':
			return self.deleteEAN_check(article, value)

	def deleteEAN_check(self, article, value):
		tester = (article, 'deleteEAN', value)
		
		if tester in self.stop_list:
			self.stop_list.remove(tester)
			self.set_stop_list()
			return True


	def deleteDate_check(self, article, value):
		tester = (article, 'deleteDate', value)
		
		if tester in self.stop_list:
			self.stop_list.remove(tester)
			self.set_stop_list()
			return True

	def deleteART_check(self, article):
		tester = (article, 'deleteART', None)

		if tester in self.stop_list:
			self.stop_list.remove(tester)
			self.set_stop_list()
			return True

	def get_them(self, code):
			search = self.ids.searcher.text
			self.search_grid = self.ids.griddy
			self.search_grid.bind(minimum_height=self.search_grid.setter("height"))
			self.search_grid.clear_widgets()
			if len(art_names) == 0 and code == 0:
				if self.lang == 'ru':
					popup("Внимание", "В базе данных нет записей")
				else:
					popup('Warning', 'No entires in database')
			else:
				if code == 0:
					for each in art_names:
						top = "{} {}".format(each, art_names[each])
						if search.lower() in top.lower():

							date_storage = []

							if each in entries:

								hound = [i for i,x in enumerate(entries) if x==each]

								for eaz in hound:

									date_storage.append(entries[eaz-1])

								n_stor = []

								for d in date_storage:
									if d:
										m_year, m_month, m_day = d[4:],d[2:4],d[:2]

										n_stor.append(date(int(m_year), int(m_month), int(m_day)))

								n_stor = sorted(n_stor)
							else:
								n_stor = 'N/A'


							self.wi = MyWidget({'name':art_names[each],'art':each, 'nearest_date':n_stor[0]})
							self.search_grid.add_widget(self.wi)
							self.wi.bind(on_release=self.infor)

	def popup(self, title, text):
		popup = Popup(title=title,
		content=Label(text=text),
		size_hint=(0.65, 0.25))
		popup.open()

	def infor(self, button):
		global inf_art

		self.ids.mana.current = "information"

		numbers = []
		words = []
		do_we = False

		inf_art = button.ids.article.text

		'''
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
'''
		self.start_one()

###########################---INFORMATION---##################################

	def create_ean(self):
		n_ean = self.ean_input.text
		self.manage_ean_popup.dismiss()

		try:
			for each in art_bars[inf_art]:
				if each == n_ean:
					popup('Warning', 'This EAN is already in a list')
					return
		except:
			pass

		self.if_recreated(inf_art, 'deleteEAN', n_ean)

		f = open("barcode.txt", "a", newline='')
		f.write(str((inf_art + "$" + n_ean + "$")))
		f.close()
		sync()
		

	def new_ean(self):
		try:
			self.manage_ean_popup.dismiss()
		except:
			pass

		self.layout = FloatLayout(size=(self.width, self.height))

		self.button1 = Button(text='Creater', size_hint_y=None, size_hint_x=None,
					height=0.06*self.height, width=0.5*self.width, font_size="25sp",
					pos_hint={"center_x":.5,"center_y":.28}, halign='center',
					valign="middle", on_release=lambda x:self.create_ean())

		self.ean_input = TextInput(id='hola', multiline=False, size_hint_x=.75, size_hint_y=0.35, 
			pos_hint={"center_x":.5,"center_y":.7}, hint_text='Enter EAN', font_size='27sp') 

		self.layout.add_widget(self.button1)
		self.layout.add_widget(self.ean_input)

		self.manage_ean_popup = Popup(title='Manage Ean',
		content=self.layout,
		size_hint=(.8, .24))

		self.manage_ean_popup.open()

	def manage_eans(self):
		try:
			self.manage_ean_popup.dismiss()
		except:
			pass

		collection = []
		if inf_art not in art_bars:
			self.new_ean()
			return
		for each in art_bars[inf_art]:
			collection.append(each)


		layout = FloatLayout(size=(self.width, self.height))

		button1 = Button(text='Create', size_hint_y=None, size_hint_x=None,
					height=0.06*self.height, width=0.5*self.width, font_size="25sp",
					pos_hint={"center_x":.5,"center_y":.1}, halign='center',
					valign="middle", on_release=lambda x:self.new_ean())

		scrolly = ScrollView(size_hint_x= .95, size_hint_y= .8, pos_hint={'center_x': .5, 'center_y': .58})
		grid_for_scroll = GridLayout(id='ean_griddy', spacing=2, cols=1, size_hint_y=None, height=0)
		grid_for_scroll.bind(minimum_height=grid_for_scroll.setter("height"))


		for each in collection:
			self.btn = Button(text='{}'.format(each),
			size_hint_y=None, height=0.09*self.height,
			font_size="25sp")
			grid_for_scroll.add_widget(self.btn)
			self.btn.bind(on_release=self.change_ean)

		scrolly.add_widget(grid_for_scroll)
		layout.add_widget(scrolly)
		layout.add_widget(button1)

		self.manage_ean_popup = Popup(title='Manage Ean',
		content=layout,
		size_hint=(.8, .65))

		self.manage_ean_popup.open()

	def change2_ean(self, args):
		local = []
		
		if self.ean_input.text in art_bars[inf_art]:
			self.manage_ean_popup.dismiss()
			self.manage_eans()
			popup('Warning!', 'This EAN already there!')
			return

		self.change3_ean(args)

	def change3_ean(self, args):

		self.if_recreated(inf_art, 'deleteEAN', self.current_button)

		if args:
			self.stop_list.append((inf_art, 'deleteEAN', self.current_button))
			self.set_stop_list()

		f = open("barcode.txt", "r+")
		dawread = f.read()
		f.close()
		global art_bars
		art_bars = {}
		templ = dawread.split("$")[:-1]

		hound = [i for i,x in enumerate(templ) if x==inf_art]
		for each in hound:
			if templ[each+1] == self.current_button:
				templ[each+1] = self.ean_input.text

				with open("barcode.txt", "w") as f:
					for each in templ:
						f.write(str(each + "$"))
				sync()
				self.manage_ean_popup.dismiss()
				self.manage_eans()
				return

	def delete2_ean(self, *args):

		article = inf_art
		barcode = self.current_button

		self.if_recreated(article, 'deleteEAN', barcode)

		f = open("barcode.txt", "r+")
		dawread = f.read()
		f.close()
		global art_bars
		art_bars = {}
		templ = dawread.split("$")[:-1]

		hound = [i for i,x in enumerate(templ) if x==article]
		for each in hound:
			if templ[each+1] == barcode:
				del templ[each]
				del templ[each]

				with open("barcode.txt", "w") as f:
					for each in templ:
						f.write(str(each + "$"))

				if args[0]:
					self.stop_list.append((inf_art, 'deleteEAN', self.current_button))
					self.set_stop_list()

				sync()
				self.manage_ean_popup.dismiss()
				self.manage_eans()
				return


	def delete_ean(self, *argument):

		arg = ''
		if argument:
			arg = True

		self.manage_ean_popup.dismiss()

		self.layout = FloatLayout(size=(self.width, self.height))

		self.lbl = Label(text="You want to delete EAN?", font_size="25sp", 
				pos_hint={"center_x":.5,"center_y":.86})

		self.button1 = Button(text='Yes', size_hint_y=None, size_hint_x=None,
					height=0.06*self.height, width=0.5*self.width, font_size="25sp",
					pos_hint={"center_x":.5,"center_y":.42}, halign='center',
					valign="middle", on_release=lambda x:self.delete2_ean(arg))

		self.button2 = Button(text='No', size_hint_y=None, size_hint_x=None,
					height=0.06*self.height, width=0.5*self.width, font_size="25sp",
					pos_hint={"center_x":.5,"center_y":.18}, halign='center',
					valign="middle", on_release=lambda x:self.manage_eans())

		self.layout.add_widget(self.button1)
		self.layout.add_widget(self.button2)
		self.layout.add_widget(self.lbl)

		self.manage_ean_popup = Popup(title='Manage Ean',
		content=self.layout,
		size_hint=(.8, .35))

		self.manage_ean_popup.open()



	def change_ean(self, button):
		self.manage_ean_popup.dismiss()
		self.current_button = button.text

		self.layout = FloatLayout(size=(self.width, self.height))

		if self.lang == 'ru':
			change = 'Изменить'
			delete = 'Удалить'
			change_eve = 'Изменить для всех'
			delete_eve = 'Удалить для всех'
		else:
			change = 'Change'
			delete = 'Delete'
			change_eve = 'Change for everyone'
			delete_eve = 'Delete for everyone'

		if self.current_user:
			self.ean_input = TextInput(text=button.text, multiline=False, size_hint_x=.75, size_hint_y=0.15, 
			pos_hint={"center_x":.5,"center_y":.8}, hint_text='Enter EAN', font_size='27sp')

			self.button1 = Button(text=change, size_hint_y=None, size_hint_x=None,
						height=0.06*self.height, width=0.5*self.width, font_size="25sp",
						pos_hint={"center_x":.5,"center_y":.59}, halign='center',
						valign="middle", on_release=lambda x:self.change2_ean(False))

			self.button2 = Button(text=delete, size_hint_y=None, size_hint_x=None,
						height=0.06*self.height, width=0.5*self.width, font_size="25sp",
						pos_hint={"center_x":.5,"center_y":.44}, halign='center',
						valign="middle", on_release=lambda x:self.delete_ean())

			self.button3 = Button(text=change_eve, size_hint_y=None, size_hint_x=None,
						height=0.06*self.height, width=0.5*self.width, font_size="25sp",
						pos_hint={"center_x":.5,"center_y":.29}, halign='center',
						valign="middle", on_release=lambda x:self.change2_ean(True))

			self.button4 = Button(text=delete_eve, size_hint_y=None, size_hint_x=None,
						height=0.06*self.height, width=0.5*self.width, font_size="25sp",
						pos_hint={"center_x":.5,"center_y":.14}, halign='center',
						valign="middle", on_release=lambda x:self.delete_ean(True))

			self.layout.add_widget(self.button1)
			self.layout.add_widget(self.button2)
			self.layout.add_widget(self.button3)
			self.layout.add_widget(self.button4)
			self.layout.add_widget(self.ean_input)

			self.manage_ean_popup = Popup(title='Manage Ean',
			content=self.layout,
			size_hint=(.8, .5))

		else:
			self.ean_input = TextInput(text=button.text, multiline=False, size_hint_x=.75, size_hint_y=0.25, 
			pos_hint={"center_x":.5,"center_y":.7}, hint_text='Enter EAN', font_size='27sp')

			self.button1 = Button(text='Change', size_hint_y=None, size_hint_x=None,
						height=0.06*self.height, width=0.5*self.width, font_size="25sp",
						pos_hint={"center_x":.5,"center_y":.42}, halign='center',
						valign="middle", on_release=lambda x:self.change2_ean())

			self.button2 = Button(text='Delete', size_hint_y=None, size_hint_x=None,
						height=0.06*self.height, width=0.5*self.width, font_size="25sp",
						pos_hint={"center_x":.5,"center_y":.18}, halign='center',
						valign="middle", on_release=lambda x:self.delete_ean())

			self.layout.add_widget(self.button1)
			self.layout.add_widget(self.button2)
			self.layout.add_widget(self.ean_input)

			self.manage_ean_popup = Popup(title='Manage Ean',
			content=self.layout,
			size_hint=(.8, .35))

		self.manage_ean_popup.open()

	def show_all_eans(self):
		collection = []

		for ean, in_art in art_bars.items():
			if ean == inf_art:
				for eaz in art_bars[ean]:
					collection.append(eaz)

		layout = FloatLayout(size=(self.width, self.height))
		scrolly = ScrollView(size_hint_x= .95, size_hint_y= .95, pos_hint={'center_x': .5, 'center_y': .5})
		grid_for_scroll = GridLayout(id='ean_griddy', spacing=2, cols=1, size_hint_y=None, height=0)
		grid_for_scroll.bind(minimum_height=grid_for_scroll.setter("height"))


		for each in collection:
			grid_for_scroll.add_widget(Button(text='{}'.format(each), size_hint_y=None, height=0.09*self.height, font_size="25sp"))
		scrolly.add_widget(grid_for_scroll)
		layout.add_widget(scrolly)


		popup = Popup(title='EAN',
		content=layout,
		size_hint=(.8, .5))

		popup.open()

	def start_one(self):
		self.ids.ghost.text = art_names[inf_art]
		self.ids.ghost2.text = inf_art
		if self.lang == 'ru':
			sent = days_of_life[inf_art]
			if sent[-1] == 'm':
				sent = sent[:-1] + ' мес'
			elif sent[-1] == 'y':
				sent = sent[:-1] + ' лет'
			else:
				sent = sent + ' дней'

			self.ids.ghost4.text = "Срок годности: {}".format(sent)
		else:
			sent = days_of_life[inf_art]
			if sent[-1] == 'm':
				sent = sent[:-1] + ' mon'
			elif sent[-1] == 'y':
				sent = sent[:-1] + ' years'
			else:
				sent = sent + ' days'

			self.ids.ghost4.text = "Shelf life: {}".format(sent)

		## Collect Eans by value in dict ##
		collection = []

		try:
			self.ids.info_canvas.remove_widget(self.bob)
		except:
			pass

		self.btn = Button(text='...', size_hint_y=None, size_hint_x=None,
					height=0.06*self.height, width=0.1*self.width, font_size="25sp",
					pos_hint={"center_x":.92,"center_y":.7}, halign='center',
					valign="top", on_release=lambda x:self.show_all_eans())

		for ean, in_art in art_bars.items():
			if ean == inf_art:
				for eaz in art_bars[ean]:
					collection.append(eaz)

		if len(collection) == 0:
			if self.lang == 'ru':
				self.ids.ghost5.text = 'Нет привязанного EAN'
			else:
				self.ids.ghost5.text = 'No EANs'
		else:
			self.ids.ghost5.text = "EAN: {}".format(collection[0])
			if len(collection) > 1:
				self.bob = self.btn
				self.ids.info_canvas.add_widget(self.btn)

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
			if self.lang == 'ru':
				self.texter = "  До\n"+str(each)
			else:
				self.texter = "  Until\n"+str(each)
			self.btn = Button(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size="25sp")
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
		if self.lang == 'ru':
			sentence = "Вы уверены что хотите безвозвратно\n удалить артикул {} ?".format(inf_art)
			tit = 'Удаление'
			self.layout = FloatLayout(size=(self.width, self.height))
			self.btn1 = Button(text="Удалить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.45}, on_release=lambda x:self.art_delete())
			self.btn2 = Button(text="Удалить для всех", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.15}, on_release=lambda x:self.art_delete(True))
		else:
			sentence = "Do you want to permanently\n delete article {} ?".format(inf_art)
			tit = 'Deletion'
			self.layout = FloatLayout(size=(self.width, self.height))
			self.btn1 = Button(text="Delete", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.45}, on_release=lambda x:self.art_delete())
			self.btn2 = Button(text="Delete for everyone", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.15}, on_release=lambda x:self.art_delete(True))


		self.lbl = Label(text=sentence, font_size="25sp", pos_hint={"center_x":.5,"center_y":.86})

		self.layout.add_widget(self.lbl)
		self.layout.add_widget(self.btn1)
		if self.current_user:
			self.layout.add_widget(self.btn2)

		self.popup = Popup(title=tit,
		content=self.layout,
		size_hint=(.8, .3))
		self.popup.open()
		self.get_them(0)

	def art_delete(self, *args):
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

		#lets delete all eans

		f = open("barcode.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		hound = [i for i,x in enumerate(dawread) if x==inf_art]
		worker = []

		for each in hound:
			worker.append(each+1)

		worker = worker[::-1]


		for each in worker:
			del dawread[each-1]
			del dawread[each-1]

		with open("barcode.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		sync()

		if args:
			self.stop_list.append((inf_art, 'deleteART', None))
			self.set_stop_list()

		self.show_prosrok(False)
		self.alarm()

		self.clean()
		self.get_them(0)
		self.ids.mana.current = "database"


	def add_entry(self):
		if self.lang == 'ru':
			tit = 'Ручное добавление'
			sentence = "Добавьте дату артикулу\n{} вручную".format(inf_art)
			self.layout = FloatLayout(size=(self.width, self.height))
			self.inputi = TextInput(multiline=False, size_hint_x=.2, size_hint_y=0.2, pos_hint={"center_x":.2,"center_y":.61}, hint_text='День')
			self.inputi_2 = TextInput(multiline=False, size_hint_x=.2, size_hint_y=0.2, pos_hint={"center_x":.4,"center_y":.61}, hint_text='Месяц')
			self.inputi_3 = TextInput(multiline=False, size_hint_x=.4, size_hint_y=0.2, pos_hint={"center_x":.7,"center_y":.61}, hint_text='Год')
			self.btn1 = Button(text="Добавить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.34}, on_release=lambda x:self.add_entry2())
		else:
			tit = 'Manual addition'
			sentence = "Manually add date\n{} to article".format(inf_art)
			self.layout = FloatLayout(size=(self.width, self.height))
			self.inputi = TextInput(multiline=False, size_hint_x=.2, size_hint_y=0.2, pos_hint={"center_x":.2,"center_y":.61}, hint_text='Day')
			self.inputi_2 = TextInput(multiline=False, size_hint_x=.2, size_hint_y=0.2, pos_hint={"center_x":.4,"center_y":.61}, hint_text='Month')
			self.inputi_3 = TextInput(multiline=False, size_hint_x=.4, size_hint_y=0.2, pos_hint={"center_x":.7,"center_y":.61}, hint_text='Year')
			self.btn1 = Button(text="Add", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.34}, on_release=lambda x:self.add_entry2())

		self.lbl = Label(text=sentence, font_size="25sp", pos_hint={"center_x":.5,"center_y":.86})

		self.inputi.bind(focus=lambda x, y: self.clear_field(1, y))
		self.inputi_2.bind(focus=lambda x, y: self.clear_field(2, y))
		self.inputi_3.bind(focus=lambda x, y: self.clear_field(3, y))

		self.inputi.bind(text=lambda x, y: self.pass_it_up(1, y))
		self.inputi_2.bind(text=lambda x, y: self.pass_it_up(2, y))
		self.inputi_3.bind(text=lambda x, y: self.pass_it_up(3, y))

		self.layout.add_widget(self.lbl)
		self.layout.add_widget(self.inputi)
		self.layout.add_widget(self.inputi_2)
		self.layout.add_widget(self.inputi_3)
		self.layout.add_widget(self.btn1)

		self.popup = Popup(title=tit,
		content=self.layout,
		size_hint=(.8, .3))
		self.popup.open()

	def pass_it_up(self, *args):
		number, text = args

		if number == 1 and len(text) >= 2:
			self.inputi_2.focus = True
		elif number == 2 and len(text) >= 2:
			self.inputi_3.focus = True
		elif number == 3 and len(text) >= 4:
			self.inputi_3.focus = False

	def clear_field(self, *args):
		which_field, value = args
		if value:
			if which_field == 1:
				if len(self.inputi.text) >= 2:
					self.inputi.text = ''
			elif which_field == 2:
				if len(self.inputi_2.text) >= 2:
					self.inputi_2.text = ''
			else:
				if len(self.inputi_3.text) >= 4:
					self.inputi_3.text = ''

	def save_anyway2(self, boomb):
		self.popup.dismiss()

		self.if_recreated(inf_art, 'deleteART', None)
		self.if_recreated(inf_art, 'deleteDate', boomb)

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

		if self.lang == 'ru':
			title = 'Внимание!'
			label = Label(text='Сохраняемый артикул просрочен,\n все равно сохранить?')
			btn1 = Button(text='Да', on_release=lambda x: self.save_anyway2(final))
			btn2 = Button(text='Нет', on_release=lambda x: self.wise2())
		else:
			title = 'Warning!'
			label = Label(text='Date is expired,\n save it anyway?')
			btn1 = Button(text='Yes', on_release=lambda x: self.save_anyway2(final))
			btn2 = Button(text='No', on_release=lambda x: self.wise2())


		fl = BoxLayout(orientation='vertical')
		fl.add_widget(label)
		bx = BoxLayout(orientation='horizontal')
		bx.add_widget(btn1)
		bx.add_widget(btn2)

		fl.add_widget(bx)

		self.popup2 = Popup(title=title,
		content=fl,
		size_hint=(0.65, 0.25))
		self.popup2.open()

	def add_entry2(self):

		first = self.inputi.text
		second = self.inputi_2.text
		third = self.inputi_3.text

		if len(first) < 2:
			first = '0'+first
		if len(second) < 2:
			second = '0'+second

		new_date = '{}{}{}'.format(first, second, third)


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
						if self.lang == 'ru':
							popup("Внимание!", "Введенная дата уже записана")
						else:
							popup('Warning!', 'This date is already in database')

						self.inputi.text = ''
						self.inputi_2.text = ''
						self.inputi_3.text = ''
						return

				day = boomb[:2]
				month = boomb[2:4]
				year = boomb[4:]

				if len(year) < 4:
					if self.lang == 'ru':
						popup("Внимание!", "Введите 4-х значный год")
					else:
						popup('Warning!', 'Enter year in following format - yyyy')
					self.inputi.text = ''
					self.inputi_2.text = ''
					self.inputi_3.text = ''
					return

				c = date(int(year), int(month), int(day))

				todayer = date.today()

				if c <= todayer:
					self.enter_prosrok2(boomb)
					return
				else:

					self.if_recreated(inf_art, 'deleteDate', boomb)

					f = open("saver.txt", "a")
					f.write(str((boomb + "$" + inf_art + "$")))
					f.close()
					sync()
					self.letedit()
					self.popup.dismiss()
			else:
				if self.lang == 'ru':
					popup("Внимание!", "Ошибка ввода!")
				else:
					popup('Warning!', 'Input Error!')

				self.inputi.text = ''
				self.inputi_2.text = ''
				self.inputi_3.text = ''
				return
		else:
			if self.lang == 'ru':
				popup("Внимание!", "Вы ничего не ввели")
			else:
				popup('Warning!', 'You entered nothing')

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
			if self.lang == 'ru':
				self.texter = "  До\n"+str(each)
			else:
				self.texter = "  Until\n"+str(each)
			self.btn = Button(text=self.texter, size_hint_y=None, height=0.09*self.height, font_size="25sp")
			self.grid.add_widget(self.btn)
			self.btn.bind(on_release=self.entry_change)

	def clean(self):
		self.ids.name.text = ""
		self.ids.article.text = ""
		self.ids.standartdate.text = ""
		self.ids.griddy.clear_widgets()

	def change_popup_name(self, flag):
		name = art_names[inf_art]
		ask = self.ids.name.text

		if self.lang == 'ru':
			tit = "Внимание!"
			sentence = "Вы уверены что хотите внести изменения\n в артикул {}?".format(name)
			layout = FloatLayout(size=(self.width, self.height))
			btn1 = Button(id="one", text="Изменить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.45}, on_release=lambda x:self.changes_selector())
			btn2 = Button(id="one", text="Изменить для всех", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.15}, on_release=lambda x:self.changes_selector(True))
		else:
			tit = "Warning!"
			sentence = "Do you really want to\n change article {}?".format(name)
			layout = FloatLayout(size=(self.width, self.height))
			btn1 = Button(id="one", text="Change", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.45}, on_release=lambda x:self.changes_selector())
			btn2 = Button(id="one", text="Change for everyone", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.15}, on_release=lambda x:self.changes_selector(True))


		lbl = Label(text=sentence, font_size="25sp", pos_hint={"center_x":.5,"center_y":.82})

		layout.add_widget(lbl)
		layout.add_widget(btn1)
		if self.current_user:
			layout.add_widget(btn2)

		if closer == False:
			self.popup = Popup(title=tit,
			content=layout,
			size_hint=(.8, .3))
			self.popup.open()
		else:
			self.popup.dismiss()
			ch_closer()
			if flag:
				if self.lang == 'ru':
					popup("Выполнено", "Изменения сохранены")
				else:
					popup('Done', 'Changes saved')
				self.get_them(0)
			elif flag == None:
				if self.lang == 'ru':
					popup("Внимание", "Вы не ввели новых данных")
				else:
					popup('Warning', 'No new data found')
			elif flag == 'merge':
				pass
			else:
				if self.lang == 'ru':
					popup("Внимание", "Вы ввели некорректные данные")
				else:
					popup('Warning', 'Data is incorrect')

	def changes_selector(self, *args):

		name = self.ids.name.text
		article = self.ids.article.text
		st_date = self.ids.standartdate.text

		if name == art_names[inf_art] and article == inf_art and st_date == days_of_life[inf_art]:
			ch_closer()
			self.change_popup_name(None)
			return

		if not article.isdigit() or not st_date.isdigit():
			ch_closer()
			self.change_popup_name(False)
			return
		
		if article != inf_art:
			if article in art_names:
				self.popup.dismiss()
				self.merge_arts(article)
				return
			else:
				self.work_out_article(article, args)

		if name != art_names[inf_art]:
			self.work_out_name(name)

		if st_date != days_of_life[inf_art]:
			self.work_out_st_date(st_date, args)

		self.do_clean_stuff(article)

		ch_closer()
		self.change_popup_name(True)

	def do_clean_stuff(self, new_art):

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

	def work_out_st_date(self, st_date, *args):

		f = open("daysoflife.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = dawread.index(inf_art)
		worker += 1
		dawread[worker] = st_date

		with open("daysoflife.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		if args:
			self.stop_list.append((inf_art, 'changeSTD', st_date))
			self.set_stop_list()

		sync()

	def work_out_name(self, name):

		f = open("artname.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = dawread.index(inf_art)
		worker += 1
		dawread[worker] = name

		with open("artname.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		sync()

	def merge_arts(self, article):

		if self.lang == 'ru':
			title = 'Внимание!'
			label = Label(text='Артикул {} уже существует,\n объединить?'.format(article))
			btn1 = Button(text='Да', on_release=lambda x: self.do_merge(article))
			btn2 = Button(text='Нет', on_release=lambda x: self.dis_my_pop())
		else:
			title = 'Warning!'
			label = Label(text='Article {} is already exist,\n want to merge them?'.format(article))
			btn1 = Button(text='Yes', on_release=lambda x: self.do_merge(article))
			btn2 = Button(text='No', on_release=lambda x: self.dis_my_pop())


		fl = BoxLayout(orientation='vertical')
		fl.add_widget(label)
		bx = BoxLayout(orientation='horizontal')
		bx.add_widget(btn1)
		bx.add_widget(btn2)

		fl.add_widget(bx)

		self.my_pop = Popup(title=title,
		content=fl,
		size_hint=(0.65, 0.5))
		self.my_pop.open()

	def dis_my_pop(self):
		self.my_pop.dismiss()

	def do_merge(self, article):
		
		self.my_pop.dismiss()

		entries_copy = entries[:]

		del entries_copy[-1]

		index_list = [i for i,x in enumerate(entries_copy) if x == inf_art]

		for each in index_list:
			entries_copy[each] = article

		hub = []

		for x in range(0, len(entries_copy)-1, 2):
			hub.append((entries_copy[x], entries_copy[x+1]))

		entry = list(set(hub))

		entries_copy = []

		for each in entry:
			for eaz in each:
				entries_copy.append(eaz)


		with open("saver.txt", "w") as f:
			for each in entries_copy:
				f.write(str(each + "$"))

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

		sync()

		self.show_prosrok(False)
		self.alarm()

		self.clean()
		self.get_them(0)
		self.ids.mana.current = "database"


		if self.current_user:
			self.stop_list.append((inf_art, 'deleteART', None))
			self.set_stop_list()

		if self.lang == 'ru':
			text = 'Миграция артикула {} в {} успешно!'.format(inf_art, article)
			popup('Внимание!', text)
		else:
			text = 'Article {} migrated into {} successfully!'.format(inf_art, article)
			popup('Warning!', text)

	def work_out_article(self, article, *args):
		global inf_art

		f = open("artname.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = dawread.index(inf_art)
		dawread[worker] = article

		with open("artname.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		f = open("daysoflife.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = dawread.index(inf_art)
		dawread[worker] = article

		with open("daysoflife.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		f = open("saver.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = [i for i,x in enumerate(dawread) if x==inf_art]
		for each in worker:
			dawread[each] = article

		with open("saver.txt", "w") as f:
			for each in dawread:
				f.write(str(each + "$"))

		if args:
			self.stop_list.append((inf_art, 'deleteART', None))
			self.set_stop_list()

		sync()

		inf_art = article

	def entry_change(self, button):
		cont = []
		for each in button.text:
			if each.isdigit():
				cont.append(each)

		self.date = "".join(cont)

		day = self.date[:2]
		month = self.date[2:4]
		year = self.date[4:]

		if self.lang == 'ru':
			sentence = "Вы можете изменить дату"
		else:
			sentence = 'You can change date'

		if self.current_user:
			if self.lang == 'ru':
				tit = 'Редактирование'
				self.layout = FloatLayout(size=(self.width, self.height))
				self.inputi_4 = TextInput(text=day, multiline=False, size_hint_x=.2, size_hint_y=0.12, pos_hint={"center_x":.2,"center_y":.83}, hint_text='День')
				self.inputi_5 = TextInput(text=month, multiline=False, size_hint_x=.2, size_hint_y=0.12, pos_hint={"center_x":.4,"center_y":.83}, hint_text='Месяц')
				self.inputi_6 = TextInput(text=year, multiline=False, size_hint_x=.4, size_hint_y=0.12, pos_hint={"center_x":.7,"center_y":.83}, hint_text='Год')
				self.btn1 = Button(text="Изменить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.65}, on_release=lambda x:self.save_entry())
				self.btn1_2 = Button(text="Изменить для всех", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.48}, on_release=lambda x:self.save_entry(True))
				self.btn2 = Button(text="Удалить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.31}, on_release=lambda x:self.delete_entry())
				self.btn3 = Button(text="Удалить для всех", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.14}, on_release=lambda x:self.delete_entry(True))
			else:
				tit = 'Edit'
				self.layout = FloatLayout(size=(self.width, self.height))
				self.inputi_4 = TextInput(text=day, multiline=False, size_hint_x=.2, size_hint_y=0.12, pos_hint={"center_x":.2,"center_y":.83}, hint_text='Day')
				self.inputi_5 = TextInput(text=month, multiline=False, size_hint_x=.2, size_hint_y=0.12, pos_hint={"center_x":.4,"center_y":.83}, hint_text='Month')
				self.inputi_6 = TextInput(text=year, multiline=False, size_hint_x=.4, size_hint_y=0.12, pos_hint={"center_x":.7,"center_y":.83}, hint_text='Year')
				self.btn1 = Button(text="Change", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.65}, on_release=lambda x:self.save_entry())
				self.btn1_2 = Button(text="Change for everyone", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.48}, on_release=lambda x:self.save_entry(True))
				self.btn2 = Button(text="Delete", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.31}, on_release=lambda x:self.delete_entry())
				self.btn3 = Button(text="Delete for everyone", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.14}, on_release=lambda x:self.delete_entry(True))
						
			self.lbl = Label(text=sentence, font_size="25sp", pos_hint={"center_x":.5,"center_y":.95})
		else:
			if self.lang == 'ru':
				tit = 'Редактирование'
				self.layout = FloatLayout(size=(self.width, self.height))
				self.inputi_4 = TextInput(text=day, multiline=False, size_hint_x=.2, size_hint_y=0.15, pos_hint={"center_x":.2,"center_y":.63}, hint_text='День')
				self.inputi_5 = TextInput(text=month, multiline=False, size_hint_x=.2, size_hint_y=0.15, pos_hint={"center_x":.4,"center_y":.63}, hint_text='Месяц')
				self.inputi_6 = TextInput(text=year, multiline=False, size_hint_x=.4, size_hint_y=0.15, pos_hint={"center_x":.7,"center_y":.63}, hint_text='Год')
				self.btn1 = Button(text="Изменить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.40}, on_release=lambda x:self.save_entry())
				self.btn2 = Button(text="Удалить", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.16}, on_release=lambda x:self.delete_entry())
			else:
				tit = 'Edit'
				self.layout = FloatLayout(size=(self.width, self.height))
				self.inputi_4 = TextInput(text=day, multiline=False, size_hint_x=.2, size_hint_y=0.15, pos_hint={"center_x":.2,"center_y":.63}, hint_text='Day')
				self.inputi_5 = TextInput(text=month, multiline=False, size_hint_x=.2, size_hint_y=0.15, pos_hint={"center_x":.4,"center_y":.63}, hint_text='Month')
				self.inputi_6 = TextInput(text=year, multiline=False, size_hint_x=.4, size_hint_y=0.15, pos_hint={"center_x":.7,"center_y":.63}, hint_text='Year')
				self.btn1 = Button(text="Change", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.40}, on_release=lambda x:self.save_entry())
				self.btn2 = Button(text="Delete", size_hint_y=None, size_hint_x=None, height=0.06*self.height, width=0.6*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.16}, on_release=lambda x:self.delete_entry())


			self.lbl = Label(text=sentence, font_size="25sp", pos_hint={"center_x":.5,"center_y":.85})

		self.layout.add_widget(self.lbl)
		self.layout.add_widget(self.inputi_4)
		self.layout.add_widget(self.inputi_5)
		self.layout.add_widget(self.inputi_6)
		self.layout.add_widget(self.btn1)
		self.layout.add_widget(self.btn2)
		if self.current_user:
			self.layout.add_widget(self.btn3)
			self.layout.add_widget(self.btn1_2)

		self.inputi_4.bind(focus=lambda x, y: self.clear_field2(1, y))
		self.inputi_5.bind(focus=lambda x, y: self.clear_field2(2, y))
		self.inputi_6.bind(focus=lambda x, y: self.clear_field2(3, y))

		self.inputi_4.bind(text=lambda x, y: self.pass_it_up2(1, y))
		self.inputi_5.bind(text=lambda x, y: self.pass_it_up2(2, y))
		self.inputi_6.bind(text=lambda x, y: self.pass_it_up2(3, y))

		if self.current_user:
			self.popup = Popup(title=tit,
			content=self.layout,
			size_hint=(.8, .45))
			self.popup.open()
		else:
			self.popup = Popup(title=tit,
			content=self.layout,
			size_hint=(.8, .35))
			self.popup.open()

	def pass_it_up2(self, *args):
		number, text = args

		if number == 1 and len(text) >= 2:
			self.inputi_5.focus = True
		elif number == 2 and len(text) >= 2:
			self.inputi_6.focus = True
		elif number == 3 and len(text) >= 4:
			self.inputi_6.focus = False

	def clear_field2(self, *args):
		which_field, value = args
		if value:
			if which_field == 1:
				if len(self.inputi_4.text) >= 2:
					self.inputi_4.text = ''
			elif which_field == 2:
				if len(self.inputi_5.text) >= 2:
					self.inputi_5.text = ''
			else:
				if len(self.inputi_6.text) >= 4:
					self.inputi_6.text = ''

	def delete_entry(self, *args):
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


		if args:
			self.stop_list.append((inf_art, 'deleteDate', self.date))
			self.set_stop_list()

		sync()
		self.show_prosrok(False)
		self.alarm()

		self.letedit()

#######################################################################################
	def save_anyway3(self, boomb):
		f = open("saver.txt", "r+")
		dawread = f.read()
		f.close()
		dawread = dawread.split("$")
		del dawread[-1]
		worker = [i for i,x in enumerate(dawread) if x==inf_art]

		self.if_recreated(inf_art, 'deleteART', None)
		self.if_recreated(inf_art, 'deleteDate', self.date)

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

		if self.lang == 'ru':
			title = 'Внимание!'
			label = Label(text='Сохраняемый артикул просрочен,\n все равно сохранить?')
			btn1 = Button(text='Да', on_release=lambda x: self.save_anyway3(final))
			btn2 = Button(text='Нет', on_release=lambda x: self.wise3())
		else:
			title = 'Warning!'
			label = Label(text='Article is expired,\n save it anyway?')
			btn1 = Button(text='Yes', on_release=lambda x: self.save_anyway3(final))
			btn2 = Button(text='No', on_release=lambda x: self.wise3())

		fl = BoxLayout(orientation='vertical')
		fl.add_widget(label)
		bx = BoxLayout(orientation='horizontal')
		bx.add_widget(btn1)
		bx.add_widget(btn2)

		fl.add_widget(bx)

		self.popup2 = Popup(title=title,
		content=fl,
		size_hint=(0.65, 0.25))
		self.popup2.open()
#######################################################################################

	def save_entry(self, *args):

		day = self.inputi_4.text
		month = self.inputi_5.text
		year = self.inputi_6.text

		new_date = '{}{}{}'.format(day, month, year)

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
						if self.lang == 'ru':
							popup("Внимание!", "Эта дата уже записана")
						else:
							popup('Warning!', 'This day already in database')
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


				if args:
					self.stop_list.append((inf_art, 'deleteDate', self.date))
					self.set_stop_list()

				sync()

				self.show_prosrok(False)

				self.alarm()

				self.letedit()
		else:
			if self.lang == 'ru':
				popup("Внимание!", "Вы не изменили дату")
			else:
				popup('Warning!', 'Date is not changed')

	def datetest(self, date):
		ask = date[:4]
		year = date[4:]

		if len(year) < 4:
			if self.lang == 'ru':
				popup("Внимание!", "Укажите 4-х значный год")
			else:
				popup('Warning!', 'Year should have 4 digits')
			return
		if ask.isalnum(): 
			if len(ask) == 4:
				if ask[0].isalpha() == False and ask[1].isalpha() == False and ask[2].isalpha() == False and ask[3].isalpha() == False:
					if int(ask[2:]) <= 12 and int(ask[2:]) >= 1 and int(ask[:2]) <= 31 and int(ask[:2]) >= 1:
						if self.check666(ask, year):
							return True
						else:
							if self.lang == 'ru':
								popup("Внимание!", "В этом месяце нет столько дней")
							else:
								popup('Warning!', 'This month do not have so many days')
					else:
						if self.lang == 'ru':
							popup("Внимание!", "Вы вне диапазона!")
						else:
							popup('Warning!', 'You are out of range!')
				else:
					if self.lang == 'ru':
						popup("Внимание!", "Вы ввели буквы")
					else:
						popup('Warning!', 'You entered literals')
			else:
				if self.lang == 'ru':
					popup("Внимание!", "Необходимый формат - ДДММ")
				else:
					popup('Warning!', 'Required format - DDMM')
		else:
			if self.lang == 'ru':
				popup("Внимание!", "Вы ввели символы!")
			else:
				popup('Warning!', 'You entered symbols')

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

	def delete_effect(self):

		if self.lang == 'ru':
			title = "Внимание!!!"
			text = "Нажав на кнопку УДАЛИТЬ вы уничтожите\nвсе эффекты!"
			self.lay = FloatLayout(size=(self.width, self.height))
			self.btn1 = Button(background_normal="but_red.png", text="УДАЛИТЬ", size_hint_y=None, size_hint_x=None, height=0.13*self.height, width=0.8*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.34}, on_release=lambda x:self.exterminate_effect())
		else:
			title = "Warning!!!"
			text = "If you press DELETE button\nall effects will be deleted!"
			self.lay = FloatLayout(size=(self.width, self.height))
			self.btn1 = Button(background_normal="but_red.png", text="DELETE", size_hint_y=None, size_hint_x=None, height=0.13*self.height, width=0.8*self.width, font_size="25sp", pos_hint={"center_x":.5,"center_y":.34}, on_release=lambda x:self.exterminate_effect())


		self.lbl = Label(text=text, font_size="25sp", pos_hint={"center_x":.5,"center_y":.86})

		self.lay.add_widget(self.lbl)
		self.lay.add_widget(self.btn1)

		self.popup = Popup(title=title,
		content=self.lay,
		size_hint=(.8, .3))
		self.popup.open()

	def exterminate_effect(self):
		self.popup.dismiss()
		self.stop_list = []
		self.set_stop_list()

	def are_you_sure(self):

		if self.lang == 'ru':
			title = "Внимание!!!"
			text = "Нажав на кнопку УДАЛИТЬ вы уничтожите\nвсю базу данных безвозвратно!"
			self.lay = FloatLayout(size=(self.width, self.height))

			self.btn1 = Button(background_normal="but_red.png", text="УДАЛИТЬ",
			size_hint_y=None, size_hint_x=None, height=0.13*self.height,
			width=0.8*self.width, font_size="25sp",
			pos_hint={"center_x":.5,"center_y":.50}, on_release=lambda x:self.exterminate(False))

			self.btn2 = Button(background_normal="but_red.png", text="УДАЛИТЬ ДЛЯ ВСЕХ",
			size_hint_y=None, size_hint_x=None, height=0.13*self.height,
			width=0.8*self.width, font_size="25sp",
			pos_hint={"center_x":.5,"center_y":.17}, on_release=lambda x:self.exterminate(True))

		else:
			title = "Warning!!!"
			text = "If you press DELETE button\nwhole database will be deleted!"
			self.lay = FloatLayout(size=(self.width, self.height))

			self.btn1 = Button(background_normal="but_red.png",
				text="DELETE", size_hint_y=None, size_hint_x=None,
				height=0.13*self.height, width=0.8*self.width,
				font_size="25sp", pos_hint={"center_x":.5,"center_y":.34},
				on_release=lambda x:self.exterminate(False))

			self.btn2 = Button(background_normal="but_red.png", text="Delete for everyone",
			size_hint_y=None, size_hint_x=None, height=0.13*self.height,
			width=0.8*self.width, font_size="25sp",
			pos_hint={"center_x":.5,"center_y":.14}, on_release=lambda x:self.exterminate(True))


		self.lbl = Label(text=text, font_size="25sp", pos_hint={"center_x":.5,"center_y":.86})

		self.lay.add_widget(self.lbl)
		self.lay.add_widget(self.btn1)

		if self.current_user:
			self.lay.add_widget(self.btn2)
			hinter = (.95, .39)
		else:
			hinter = (.95, .28)
			self.btn1.pos_hint = {"center_x":.5,"center_y":.30}

		self.poz = Popup(title=title,
		content=self.lay,
		size_hint=hinter)
		self.poz.open()

	def exterminate_online(self):

		sent = '{"DaysOfLife": ' + '""' + '}'
		days_of_life = json.loads(sent)
		url = "https://avocado-a066c.firebaseio.com/{}.json".format(self.current_group)
		requests.patch(url=url, json=days_of_life)

		sent = '{"EAN": ' + '""' + '}'
		days_of_life = json.loads(sent)
		url = "https://avocado-a066c.firebaseio.com/{}.json".format(self.current_group)
		requests.patch(url=url, json=days_of_life)

		sent = '{"Names": ' + '""' + '}'
		days_of_life = json.loads(sent)
		url = "https://avocado-a066c.firebaseio.com/{}.json".format(self.current_group)
		requests.patch(url=url, json=days_of_life)

		sent = '{"Saver": ' + '""' + '}'
		days_of_life = json.loads(sent)
		url = "https://avocado-a066c.firebaseio.com/{}.json".format(self.current_group)
		requests.patch(url=url, json=days_of_life)

		data = self.read_from_base()
		judge = data['Users']

		for each in judge:

			text = '{'+ '"{}"'.format(each) + ': ""' + '}'

			to_database = json.loads(text)
			url = "https://avocado-a066c.firebaseio.com/{}/Users.json".format(self.current_group)
		
			try:
				requests.patch(url=url, json=to_database)
			except:
				if self.lang == 'ru':
					popup("Внимание!", "Нет интернет соединения")
				else:
					popup('Warning', 'Check your internet connection')

	def exterminate(self, global_wipe):

		if global_wipe:
			self.exterminate_online()

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

		f = open("barcode.txt", "w")
		f.write(none)
		f.close()

		sync()

		self.poz.dismiss()
		self.show_prosrok(False)

		if self.lang == 'ru':
			popup("Внимание", "База данных была полностью удалена")
		else:
			popup('Warning', 'Database is deleted')

		self.clearer()
		self.alarm()
		self.ids.griddy.clear_widgets()
		self.ids.griddy4.clear_widgets()

	#______________STOP_LIST_CODE________________#



	#______________HERE IS THE INTERNET SYNC CODE____________________#

	url = "https://avocado-a066c.firebaseio.com/.json"

	def exit_group(self):
		self.current_user = ''
		self.current_group = ''
		self.current_password = ''
		self.current_data = ''

		self.is_user_already_logged()

		with open('data.json', 'w') as outfile:
			json.dump('', outfile)

	def load_group_home(self):

		self.grid = self.ids.grid_internet_change
		self.grid.bind(minimum_height=self.grid.setter("height"))

		if len(self.stop_list) == 0:
			self.turn_on_nothing_group_home()
		else:
			self.group_home_nothing_color = (.1, .1, .1, .0)
			self.ids.nothing_to_show.text = ''
			self.grid.clear_widgets()
			for each in self.stop_list:
				if each[1] == 'deleteART':
					if self.lang == 'ru':
						self.texter = 'Удаление артикула [color=#04d3ff]{}[/color]'.format(each[0])
					else:
						self.texter = 'Delete article [color=#04d3ff]{}[/color]'.format(each[0])

				elif each[1] == 'deleteEAN':
					if self.lang == 'ru':
						self.texter = 'Удаление EAN [color=#04d3ff]{}[/color] \nАртикула [color=#04d3ff]{}[/color]'.format(each[2], each[0])
					else:
						self.texter = 'Delete EAN [color=#04d3ff]{}[/color] \nArticle [color=#04d3ff]{}[/color]'.format(each[2], each[0])

				else:
					if self.lang == 'ru':
						self.texter = 'Удаление даты [color=#04d3ff]{}[/color] \nАртикула [color=#04d3ff]{}[/color]'.format(each[2], each[0])
					else:
						self.texter = 'Delete date [color=#04d3ff]{}[/color] \nArticle [color=#04d3ff]{}[/color]'.format(each[2], each[0])	
				self.btn = Button(markup=True, halign='left', text=self.texter, size_hint_y=None, height=0.09*self.height, font_size="25sp", on_release=lambda x: self.popup_del_item_from_stop_list(x.text))
				self.grid.add_widget(self.btn)

	def popup_del_item_from_stop_list(self, data):

		if self.lang == 'ru':

			title = 'Внимание!'
			label = Label(text='Вы собираетесь удалить эффект,\nпродолжить?')
			btn1 = Button(text='Да', on_release=lambda x: self.del_item_from_stop_list(data))
			btn2 = Button(text='Нет', on_release=lambda x: self.close_this_one())
		else:
			title = 'Warning!'
			label = Label(text='You are about to delete an effect,\nproceed?')
			btn1 = Button(text='Yes', on_release=lambda x: self.del_item_from_stop_list(data))
			btn2 = Button(text='No', on_release=lambda x: self.close_this_one())

		fl = BoxLayout(orientation='vertical')
		fl.add_widget(label)
		bx = BoxLayout(orientation='horizontal')
		bx.add_widget(btn1)
		bx.add_widget(btn2)

		fl.add_widget(bx)

		self.popup = Popup(title=title,
		content=fl,
		size_hint=(0.65, 0.25))
		self.popup.open()

	def close_this_one(self):
		self.popup.dismiss()

	def del_item_from_stop_list(self, data):
		self.close_this_one()
		data = data.split()

		if data[1] == "артикула" or data[1] == 'article':
			article = (data[2].split("]")[1]).split('[')[0]

			self.stop_list.remove((article, 'deleteART', None))
			self.set_stop_list()
			self.load_group_home()

		elif data[1] == "EAN":

			article = data[4].split(']')[1].split('[')[0]
			ean = data[2].split(']')[1].split('[')[0]

			self.stop_list.remove((article, 'deleteEAN', ean))
			self.set_stop_list()
			self.load_group_home()

		else:
			date = (data[2].split("]")[1]).split('[')[0]
			article = (data[4].split(']')[1]).split('[')[0]

			self.stop_list.remove((article, 'deleteDate', date))
			self.set_stop_list()
			self.load_group_home()

	def turn_on_nothing_group_home(self):
		self.grid.clear_widgets()
		self.group_home_nothing_color = (.1, .1, .1, .3)
		if self.lang == 'ru':
			self.ids.nothing_to_show.text = 'Нет эффектов для применения'
		else:
			self.ids.nothing_to_show.text = 'No effects to apply'

	def while_loading(self):
		self.loading = self.ids.float_group_home
		self.loading_image = Image(source='load.png', size_hint=(1, 1))
		self.loading.add_widget(self.loading_image)

	def destroy_loading(self):
		self.ids.float_group_home.remove_widget(self.loading_image)

	def is_user_already_logged(self):
	
		if self.current_user:
			self.load_group_home()
			self.ids.mana.current = "group_home"
		else:
			self.ids.mana.current = "sync_data"

	def read_from_base_new_group(self):

		auth_key = "HqpU7WbJBeA4wN058kf9nPo9PZAAiUiEBrC3ZvP5"
		try:
			request = requests.get(self.url + "?auth=" + auth_key)
			anwser = request.json()
			return anwser
		except:
			if self.lang == 'ru':
				popup("Внимание!", "Нет интернет соединения")
			else:
				popup('Warning', 'Internet connection failed')

	def create_new_group(self, group_name, group_password):
		if not group_name or not group_password:
			if self.lang == 'ru':
				popup('Внимание!', 'Все поля обязательны к заполнению!')
			else:
				popup('Warning!', 'All fields required')
			return

		try:
			anwser = self.read_from_base_new_group()
		except:
			if self.lang == 'ru':
				popup("Внимание!", "Нет интернет соединения")
			else:
				popup('Warning', 'No internet connection')

		try:
			for each in anwser:
				if each == group_name:
					if self.lang == 'ru':
						popup('Внимание', 'Данная группа уже существует!')
					else:
						popup('Warning', 'Group already exist')
					return
		except:
			pass

		first_phrase = '{' + '"{}"'.format(group_name) + ': {' + '"Users": ' + '""' + ',' + '"Names":' + '""' + ', ' + '"DaysOfLife":' + '""' + ', ' + '"Saver":' + '""' + ', ' + '"EAN":' + '""' + ', ' + '"Password":' + '"{}"'.format(group_password) + '}}'
		try:
			self.write_to_base(first_phrase)
			self.ids.mana.current = 'new_group_nickname'
			self.current_group = group_name
			self.current_password = group_password
		except:
			pass

	def new_group_new_user(self, name):
		if self.create_user(name):
			self.current_user = name
			settings_data = {'group': self.current_group, 'user': name}
			self.set_settings(settings_data)
			self.ids.mana.current = 'group_home'

	def create_user(self, name):
		try:
			request = requests.get(self.url + '{}/Users.json'.format(self.current_group) +"?auth=" + self.auth_key)
			anwser = request.json()
			for each in anwser:
				pass

			text = '{'+ '"{}"'.format(name) + ': ""' + '}'

			to_database = json.loads(text)


			url = "https://avocado-a066c.firebaseio.com/{}/Users.json".format(self.current_group)

			requests.patch(url=url, json=to_database)
		except:
			return False

		return True

	def is_user_here(self, name):
		for each in self.current_data['Users']:
			if name == each:
				settings_data = {'group': self.current_group, 'user': name}
				self.set_settings(settings_data)
				self.current_user = name
				self.ids.mana.current = 'group_home'
				return

		return False

	def users_update(self):

		result = ''

		for each in self.current_users_and_values:
			result = result+'"'+each+'": '+'"'+self.current_users_and_values[each]+'",'

		result = '{' + result[:-1] + '}'

		self.new_users = result

	def try_to_log_in(self, group_name, password):

		if not group_name or not password:
			if self.lang == 'ru':
				popup('Внимание!', 'Все поля обязательны к заполнению!')
			else:
				popup('Warning!', 'All fields are required')
			return

		self.current_group = group_name
		self.current_password = password

		if self.read_from_base():
			if self.check_password():
				if not self.current_user:
					self.ids.group_password.text = ''
					self.ids.group_name.text = ''
					self.ids.mana.current = 'ask_nickname'
		

	def check_user_name(self):
		for each in self.current_data['Users']:
			if self.current_user == each:
				return True

		return False


	def check_password(self):
		
		if self.current_data['Password'] == self.current_password:
			return True
		else:
			if self.lang == 'ru':
				popup('Внимание', 'Неверный пароль!')
			else:
				popup('Warning', 'Wrong password!')

	def read_from_base(self):

		auth_key = "HqpU7WbJBeA4wN058kf9nPo9PZAAiUiEBrC3ZvP5"

		try:
			request = requests.get(self.url[:-5] + self.current_group + ".json" + "?auth=" + auth_key)
			anwser = request.json()
			raw = request.json()
			self.current_data = raw
			if anwser == None:
				if self.lang == 'ru':
					popup('Внимание!', 'Данной группы не существует!')
				else:
					popup('Warning!', 'Group do not exist')
				return False
		
			return anwser
		except:
			if self.lang == 'ru':
				popup("Внимание!", "Нет интернет соединения")
			else:
				popup('Warning', 'No internet connection')

	def write_to_base(self, text):

		try:
			to_database = json.loads(text)
			requests.patch(url=self.url, json=to_database)
		except:
			if self.lang == 'ru':
				popup("Внимание!", "Нет интернет соединения")
			else:
				popup('Warning', 'Check your internet connection')

	def create_digital_copy(self, names, days_of_life, saver, seans):

		try:

			sent = '{"DaysOfLife": ' + '"{}"'.format(days_of_life) + '}'
			days_of_life = json.loads(sent)
			url = "https://avocado-a066c.firebaseio.com/{}.json".format(self.current_group)
			requests.patch(url=url, json=days_of_life)


			sent = '{"Names": ' + '"{}"'.format(names) + '}'
			names = json.loads(sent)
			url = "https://avocado-a066c.firebaseio.com/{}.json".format(self.current_group)
			requests.patch(url=url, json=names)

			sent = '{"Saver": ' + '"{}"'.format(saver) + '}'
			saver = json.loads(sent)
			url = "https://avocado-a066c.firebaseio.com/{}.json".format(self.current_group)
			requests.patch(url=url, json=saver)

			sent = '{"EAN": ' + '"{}"'.format(seans) + '}'
			saver = json.loads(sent)
			url = "https://avocado-a066c.firebaseio.com/{}.json".format(self.current_group)
			requests.patch(url=url, json=saver)

		except:
			if self.lang == 'ru':
				popup("Внимание!", "Нет интернет соединения")
			else:
				popup('Warning', 'Check your internet connection')

	def stop_list_activity(self, days_server, names_server, saves_server, eans_server):
		
		for each in self.stop_list:

			if each[1] == 'deleteART':
				if each[0] in names_server:
					del names_server[names_server.index(each[0])+1]
					names_server.remove(each[0])
					del days_server[days_server.index(each[0])+1]
					del days_server[days_server.index(each[0])]

					if each[0] in saves_server:
						hound = [i for i, x in enumerate(saves_server) if x == each[0]]
						hound.reverse()
						for eaz in hound:
							del saves_server[eaz-1]
							del saves_server[eaz-1]

					if each[0] in eans_server:
						hound = [i for i, x in enumerate(eans_server) if x == each[0]]
						hound.reverse()
						for eaz in hound:
							del eans_server[eaz-1]
							del eans_server[eaz-1]

			if each[1] == 'deleteDate':
				value = each[2]
				art = each[0]

				if art in saves_server:
					hound = [i for i, x in enumerate(saves_server) if x == art]

					for eaz in hound:
						if saves_server[eaz-1] == value:
							del saves_server[eaz-1]
							del saves_server[eaz-1]
							break

			if each[1] == 'deleteEAN':
				value = each[2]
				art = each[0]

				if art in eans_server:
					hound = [i for i, x in enumerate(eans_server) if x == art]

					for eaz in hound:
						if eans_server[eaz-1] == value:
							del eans_server[eaz-1]
							del eans_server[eaz-1]
							break

	def send_stop_list(self, data):

		for each in data['Users']:
			if each == self.current_user:
				continue
			else:
				judge = data['Users'][each]
				hell = self.just_read_stop_list(judge)
				text = '{'+ '"{}"'.format(each) + ': "{}"'.format(self.stop_list + hell) + '}'

				to_database = json.loads(text)
				url = "https://avocado-a066c.firebaseio.com/{}/Users.json".format(self.current_group)
				try:
					requests.patch(url=url, json=to_database)
				except:
					if self.lang == 'ru':
						popup("Внимание!", "Нет интернет соединения")
					else:
						popup('Warning', 'Check your internet connection')

		self.stop_list = []
		self.set_stop_list()

	def just_read_stop_list(self, data):

		subject = data
		test = [x for x, in subject if x.isalnum() or x == ',']
		test = ''.join(test).split(',')

		mozzie = []
		temp = []
		for each in test:
			temp.append(each)
			if len(temp) == 3:
				mozzie.append((temp[0], temp[1], temp[2]))
				temp = []

		return mozzie

	def read_my_stop_list(self, data):

		subject = data['Users'][self.current_user]
		test = [x for x, in subject if x.isalnum() or x == ',']

		test = ''.join(test).split(',')

		mozzie = []
		temp = []
		for each in test:
			temp.append(each)
			if len(temp) == 3:
				mozzie.append((temp[0], temp[1], temp[2]))
				temp = []

		self.stop_my_data(mozzie)

		text = '{'+ '"{}"'.format(self.current_user) + ': ""' + '}'

		to_database = json.loads(text)
		url = "https://avocado-a066c.firebaseio.com/{}/Users.json".format(self.current_group)
		
		try:
			requests.patch(url=url, json=to_database)
		except:
			if self.lang == 'ru':
				popup("Внимание!", "Нет интернет соединения")
			else:
				popup('Warning', 'Check your internet connection')

	def stop_my_data(self, mozzie):

		f = open("daysoflife.txt", "r+")
		rawread = f.read()
		f.close()

		days_to_stop = rawread.split('$')[:-1]


		f = open("artname.txt", "r+")
		rawread = f.read()
		f.close()

		names_to_stop = rawread.split('$')[:-1]

		f = open("saver.txt", "r+")
		rawread = f.read()
		f.close()

		saves_to_stop = rawread.split('$')[:-1]

		f = open("barcode.txt", "r+")
		rawread = f.read()
		f.close()

		eans_to_stop = rawread.split('$')[:-1]

		for each in mozzie:

			if each[1] == 'deleteART':
				if each[0] in names_to_stop:
					del names_to_stop[names_to_stop.index(each[0])+1]
					names_to_stop.remove(each[0])
					del days_to_stop[days_to_stop.index(each[0])+1]
					del days_to_stop[days_to_stop.index(each[0])]

					if each[0] in saves_to_stop:
						hound = [i for i, x in enumerate(saves_to_stop) if x == each[0]]
						hound.reverse()
						for eaz in hound:
							del saves_to_stop[eaz-1]
							del saves_to_stop[eaz-1]

					if each[0] in eans_to_stop:
						hound = [i for i, x in enumerate(eans_to_stop) if x == each[0]]
						hound.reverse()
						for eaz in hound:
							del eans_to_stop[eaz-1]
							del eans_to_stop[eaz-1]

			if each[1] == 'deleteDate':
				value = each[2]
				art = each[0]

				if art in saves_to_stop:
					hound = [i for i, x in enumerate(saves_to_stop) if x == art]

					for eaz in hound:
						if saves_to_stop[eaz-1] == value:
							del saves_to_stop[eaz-1]
							del saves_to_stop[eaz-1]

			if each[1] == 'deleteEAN':
				value = each[2]
				art = each[0]

				if art in eans_to_stop:
					hound = [i for i, x in enumerate(eans_to_stop) if x == art]

					for eaz in hound:
						if eans_to_stop[eaz-1] == value:
							del eans_to_stop[eaz-1]
							del eans_to_stop[eaz-1]


		with open("artname.txt", "w+") as f:
			for x in names_to_stop:
				f.write(str(x + "$"))

		with open("daysoflife.txt", "w+") as f:
			for x in days_to_stop:
				f.write(str(x + "$"))

		with open("saver.txt", "w+") as f:
			for x in saves_to_stop:
				f.write(str(x + "$"))

		with open("barcode.txt", "w+") as f:
			for x in eans_to_stop:
				f.write(str(x + "$"))

		sync()
		
	def prepare_to_internet_sync(self):

		my_thread = threading.Thread(target=self.internet_sync)
		my_thread.start()

	def internet_sync(self):

		data = self.read_from_base()

		if data != None:
			days_of_life_from_server = data['DaysOfLife'].split('$')[:-1]
			names_from_server = data['Names'].split('$')[:-1]
			saves_from_server = data['Saver'].split('$')[:-1]
			eans_from_server = data['EAN'].split('$')[:-1]

			#stop list activity
			self.read_my_stop_list(data)
			self.stop_list_activity(days_of_life_from_server, names_from_server, saves_from_server, eans_from_server)
			self.send_stop_list(data)

			f = open("daysoflife.txt", "r+")
			rawread = f.read()
			f.close()

			days_of_life_local = rawread.split('$')[:-1]

			#_______--We updade date of life--___________#

			if len(days_of_life_local) == 0:
				updated_days_of_life = days_of_life_from_server[:]
			elif len(days_of_life_from_server) == 0:
				updated_days_of_life = days_of_life_local[:]
			else:
				updated_days_of_life = []

				articles_only = [i for i in days_of_life_local if days_of_life_local.index(i) % 2 == 0]

				updated_days_of_life = days_of_life_from_server[:]

				for each in articles_only:
					if each not in updated_days_of_life:
						updated_days_of_life.append(each)
						updated_days_of_life.append(days_of_life_local[days_of_life_local.index(each)+1])	

			#_______--We update names--_________________#

			f = open("artname.txt", "r+")
			rawread = f.read()
			f.close()

			names_local = rawread.split('$')[:-1]

			if (len(names_local)) == 0:
				updated_names = names_from_server
			elif len(names_from_server) == 0:
				updated_names = names_local
			else:
				articles_only = [i for i in names_local if names_local.index(i) % 2 == 0]

				updated_names = names_from_server


				for each in articles_only:
					if each not in updated_names:
						updated_names.append(each)
						updated_names.append(names_local[names_local.index(each)+1])

			alias = names_local[:]
			updated_names_to_phone = updated_names[:]

			for x in range(len(alias)-1):
				if x % 2 == 0 or x == 0:
					updated_names_to_phone[updated_names_to_phone.index(alias[x])+1] = alias[alias.index(alias[x])+1]

			#______--We update dates--________________#

			f = open("saver.txt", "r+")
			rawread = f.read()
			f.close()

			saves_local = rawread.split('$')[:-1]

			if len(saves_from_server) == 0:
				updated_saves = saves_local
			elif len(saves_local) == 0:
				updated_saves = saves_from_server
			else:

				saves_local += saves_from_server

				articles_only = []
				dates_only = []

				for x in range(len(saves_local)):
					if x % 2 != 0:
						articles_only.append(saves_local[x])
					else:
						dates_only.append(saves_local[x])

				final_hub = {}


				for x in range(len(articles_only)):
					
					if articles_only[x] not in final_hub:
						final_hub[articles_only[x]] = [dates_only[x]]
					else:
						old = final_hub[articles_only[x]]
						realm = dates_only[x]
						old.append(realm)
						old = list(set(old))
						final_hub[articles_only[x]] = old

				updated_saves = []

				for each in final_hub:
					for eaz in final_hub[each]:
						updated_saves.append(eaz)
						updated_saves.append(each)

			if len(updated_names) == 0:
				updated_names = ''
			if len(updated_days_of_life) == 0:
				updated_days_of_life = ''
			if len(updated_saves) == 0:
				updated_saves = ''

			# We update EANs 

			f = open("barcode.txt", "r+")
			rawread = f.read()
			f.close()

			eans_local = rawread.split('$')[:-1]

			if len(eans_from_server) == 0:
				updated_eans = eans_local
			elif len(eans_local) == 0:
				updated_eans = eans_from_server
			else:

				eans_local += eans_from_server

				articles_only = []
				eans_only = []

				for x in range(len(eans_local)):
					if x % 2 != 0:
						articles_only.append(eans_local[x])
					else:
						eans_only.append(eans_local[x])

				final_hub = {}


				for x in range(len(articles_only)):
					
					if articles_only[x] not in final_hub:
						final_hub[articles_only[x]] = [eans_only[x]]
					else:
						old = final_hub[articles_only[x]]
						realm = eans_only[x]
						old.append(realm)
						old = list(set(old))
						final_hub[articles_only[x]] = old

				updated_eans = []

				for each in final_hub:
					for eaz in final_hub[each]:
						updated_eans.append(eaz)
						updated_eans.append(each)

			if len(updated_names) == 0:
				updated_names = ''
			if len(updated_days_of_life) == 0:
				updated_days_of_life = ''
			if len(updated_saves) == 0:
				updated_saves = ''
			if len(updated_eans) == 0:
				updated_eans = ''

			with open("barcode.txt", "w") as f:
				for each in updated_eans:
					f.write(str(each + "$"))

			with open("artname.txt", "w") as f:
				for each in updated_names_to_phone:
					f.write(str(each + "$"))

			with open("daysoflife.txt", "w") as f:
				for each in updated_days_of_life:
					f.write(str(each + "$"))

			with open("saver.txt", "w") as f:
				for each in updated_saves:
					f.write(str(each + "$"))

			sync()
			updated_names = '$'.join(updated_names)+'$'
			updated_days_of_life = '$'.join(updated_days_of_life)+'$'
			updated_saves = '$'.join(updated_saves)+'$'
			updated_eans = '$'.join(updated_eans)+'$'

			if len(updated_names) == 1:
				updated_saves = ''
			if len(updated_days_of_life) == 1:
				updated_days_of_life = ''
			if len(updated_saves) == 1:
				updated_saves = ''
			if len(updated_eans) == 1:
				updated_eans = ''

			if updated_names == '$':
				updated_names = ''

			self.create_digital_copy(updated_names, updated_days_of_life, updated_saves, updated_eans)
			self.alarm()
			self.load_group_home()
			self.destroy_loading()
			self.search_grid.clear_widgets()
			#internet sync complete

	def dont_delete_user(self):
		self.popup.dismiss()

	def delete_user1(self):
		

		data = self.read_from_base()
		names = data['Users']
		del names[self.current_user]

		try:
			sent = '{"Users": ' + '""' + '}'
			saver = json.loads(sent)
			url = "https://avocado-a066c.firebaseio.com/{}.json".format(self.current_group)
			requests.patch(url=url, json=saver)
			
			
			for each in names:
				name = each
				val = names[each] 

				text = '{'+ '"{}"'.format(name) + ': "{}"'.format(val) + '}'

				to_database = json.loads(text)

				url = "https://avocado-a066c.firebaseio.com/{}/Users.json".format(self.current_group)

				requests.patch(url=url, json=to_database)

			self.popup.dismiss()	
			self.exit_group()
		except:
			if self.lang == 'ru':
				popup("Внимание!", "Нет интернет соединения")
				self.popup.dismiss()
			else:
				popup('Warning', 'Check your internet connection')

	def delete_user(self):

		if self.lang == 'ru':
			tit = 'Удаление'
			sentence = "Вы хотите удалить пользователя {}?".format(self.current_user)
			self.layout = FloatLayout(size=(self.width, self.height))

			self.btn1 = Button(text="Да", size_hint_y=.5, size_hint_x=.4, font_size="25sp",
				pos_hint={"center_x":.29,"center_y":.3}, on_release=lambda x:self.delete_user1())

			self.btn2 = Button(text="Нет", size_hint_y=.5, size_hint_x=.4, font_size="25sp",
				pos_hint={"center_x":.71,"center_y":.3}, on_release=lambda x:self.dont_delete_user())

		else:
			tit = 'Deletion'
			sentence = "Do you want to delete user {}?".format(self.current_user)
			self.layout = FloatLayout(size=(self.width, self.height))
			
			self.btn1 = Button(text="Yes", size_hint_y=.5, size_hint_x=.4, font_size="25sp",
				pos_hint={"center_x":.29,"center_y":.3}, on_release=lambda x:self.delete_user1())

			self.btn2 = Button(text="No", size_hint_y=.5, size_hint_x=.4, font_size="25sp",
				pos_hint={"center_x":.71,"center_y":.3}, on_release=lambda x:self.dont_delete_user())

		self.lbl = Label(text=sentence, font_size="25sp", pos_hint={"center_x":.5,"center_y":.86})

		self.layout.add_widget(self.lbl)
		self.layout.add_widget(self.btn1)
		self.layout.add_widget(self.btn2)

		self.popup = Popup(title=tit,
		content=self.layout,
		size_hint=(.85, .2))
		self.popup.open()

	def set_settings(self, data):

		with open('data.json', 'w') as outfile:
			json.dump(data, outfile)

	def get_settings(self, *args):

		try:
			with open('data.json') as data_file:

				data = json.loads(data_file.read())
				self.current_group = data['group']
				self.current_user = data['user']
		except:
			pass

		self.get_stop_list()

	def get_stop_list(self):
		try:
			with open('stop_list.txt', 'r') as f:
				data = f.read()
				data = data.split('$')
				del data[-1]
				
				for each in data:
					first,second,third = each.split(',')
					if third == 'None':
						third = None
					self.stop_list.append((first, second, third))
					

		except:
			f = open("stop_list.txt", "w+")
			f.close()

	def get_lang(self, *args):
		try:
			with open('lang.txt', 'r') as f:
				data = f.read()
				
				self.lang = data

				if self.lang == 'ru':
					self.to_russian()
					self.worktext = 'Введите артикул'
					self.ids.russian_button.state = 'down'
					self.ids.english_button.state = 'normal'
				else:
					self.to_english()
					self.worktext = 'Enter article'
					self.ids.russian_button.state = 'normal'
					self.ids.english_button.state = 'down'
		except:
			f = open("lang.txt", "w+")
			f.close()

			self.lang = 'ru'
			self.to_russian()

	def set_lang(self, data):
		with open("lang.txt", "w") as f:
			f.write(data)


	def set_stop_list(self):
		with open("stop_list.txt", "w") as f:
			for each in self.stop_list:
				f.write(str(each[0])+','+str(each[1])+ ','+ str(each[2]) + '$')

	def change_lang(self, data):
		self.previous()
		if data == 'ru':
			self.worktext = 'Введите артикул'
			self.dater_invisible()
			self.show_buttons_before_after('hide')
			self.ids.ex_inputer.text = ''
			self.ids.ex_inputer2.text = ''
			self.step = 0
			self.to_russian()
			self.new_barcode = None
		else:
			self.worktext = 'Enter article'
			self.dater_invisible()
			self.show_buttons_before_after('hide')
			self.ids.ex_inputer.text = ''
			self.ids.ex_inputer2.text = ''
			self.step = 0
			self.to_english()


###########################---App_Classes---##################################
class ProtoApp(App):
	def on_start(self):
		mine = ''
		for obj in gc.get_objects(): #This way I could find an instance ;)
			if isinstance(obj, Core):
				mine = obj
				break

		Clock.schedule_once(mine.get_lang, 0.1)
		Clock.schedule_once(mine.alarm, 2)
		Clock.schedule_once(mine.get_settings, 1)

	def build(self):
		self.coreid = Core()
		return self.coreid

class ScreenManagement(ScreenManager):
	pass



def sync():
	try:
		f = open("barcode.txt", "r+")
		dawread = f.read()
		f.close()
		global art_bars
		art_bars = {}
		templ = dawread.split("$")
		counter = 0
		while counter < (len(templ)-1):
			
			if templ[counter] in art_bars:
				art_bars[templ[counter]].append(templ[counter+1])
			else:
				lister = []
				lister.append(templ[counter+1])
				art_bars[templ[counter]] = lister
			counter += 2

	except:
		f = open("barcode.txt", "w+")
		f.close()

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
#:import ZBarSymbol pyzbar.pyzbar.ZBarSymbol

<MyWidget>:
	canvas.before:
		Color: 
			rgb: 0, 0, 0 
		Rectangle: 
			pos: self.pos 
			size: self.size

	size_hint_x: .8
	size_hint_y: 1
	pos_hint: {"center_x":.5,"center_y":.2}

	orientation: "horizontal"
	cols: 2
	spacing: 1
	padding: 1

	BoxLayout:
		orientation: "vertical"
		raws: 2
		size_hint_x: .3
		spacing: 1
		Label:
			id: article
			canvas.before:
				Color: 
					rgb: .694, .812, .439 
				Rectangle: 
					pos: self.pos 
					size: self.size

			text: ''
			font_size: "21sp"
			pos_hint:{"center_x": .5,"center_y":.5}

		Label:
			id: date
			canvas.before:
				Color: 
					rgb: .694, .812, .439 
				Rectangle: 
					pos: self.pos 
					size: self.size
			text: 'N/A'
			font_size: "21sp"
			pos_hint:{"center_x": .5,"center_y":.5}
	Label:
		id: name
		canvas.before:
			Color: 
				rgb: .694, .812, .439 
			Rectangle: 
				pos: self.pos 
				size: self.size


		
		text: ''
		text_size: self.width - 8, None
		valign: 'top'
		halign: 'left'
		font_size: '40sp'
		pos_hint:{"center_x": .5,"center_y":.5}
		size_hint_x: .7


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

<Reader>:
	orientation: 'vertical'
	pos_hint: root.hinter
	canvas.before: 
		Color: 
			rgb: 1, .65, .18
		Rectangle:
			pos: self.pos 
			size: self.size

	ZBarCam:
		id: zbarcam
		code_types: ZBarSymbol.QRCODE, ZBarSymbol.EAN13

	Button:
		text: 'exit'
		pos_hint: {"center_x": .5,"center_y": 1}
		size_hint: (.4, .1)
		font_size: '25sp'
		on_release: root.stop_cam("NO")

	Label:
		size_hint: None, None
		size: self.texture_size[0], 50
		text: ', '.join([str(symbol.data) for symbol in zbarcam.symbols])
		on_text: root.stop_cam(self.text)

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
			source: 'head.png'
			size_hint: (1, 1)
			pos_hint: {"center_x": .5,"center_y": .5}

		Button:
			id: warner
			border: 0,0,0,0
			background_normal: ''
			background_color: 1, .35, .35, 1
			halign: 'center'
			valign: "middle"
			text: root.t_we_have_expired
			text_size: self.size
			size_hint: (.8, 1)
			font_size: "25sp"
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
			border: 0,0,0,0
			background_normal: ''
			background_color: 1, .35, .35, 1
			halign: 'center'
			valign: "middle"
			text: 'X'
			text_size: self.size
			size_hint: (.2, 1)
			font_size: "25sp"
			pos_hint: {"center_x": .9,"center_y": 2}
			on_press: root.alarm_out()



	ScreenManagement:
		transition: NoTransition()
		id: mana
		size_hint_y: 82


		Screen:
			name: 'work'
			FloatLayout:
				id: summertime
				canvas:
					Color: 	
						rgb: .886, .949, .671

					Rectangle:
						size: self.size
						pos: self.pos


				Label:
					canvas.before:
						Color: 
							rgba: 0, .8, .4, 0
						Rectangle:
							size: self.size
							pos: self.pos

					color: 255, 255, 255, 1
					halign: 'center'
					valign: "middle"
					text: root.worktext
					text_size: self.size
					size_hint: (.8, .15)
					font_size: "25sp"
					pos_hint:{"center_x": .5,"center_y":.92}

				Label:
					canvas.before:
						Color: 
							rgb: 0, .8, .4
						Rectangle:
							size: self.size
							pos: self.pos

					halign: 'center'
					valign: "middle"
					text: 'Неизвестный EAN! Введите артикул для ассоциации'
					text_size: self.size
					size_hint: (.8, .07)
					font_size: "15sp"
					pos_hint: root.pos_unknown_EAN

				ToggleButton:
					allow_no_selection: False
					group: 'before_after'
					state: 'down'
					text: root.t_ot
					size_hint: (.3, .06)
					background_down: 'w_b.png'
					pos_hint: root.pos_before_after1
					on_press: root.switch_before_after('before')

				ToggleButton:
					allow_no_selection: False
					group: 'before_after'
					text: root.t_do
					size_hint: (.3, .06)
					background_down: 'w_b.png'
					pos_hint: root.pos_before_after2
					on_press: root.switch_before_after('after')

				ToggleButton:
					allow_no_selection: False
					state: 'down'
					group: 'day_month_year'
					state: 'down'
					text: root.t_day
					size_hint: (.3, .06)
					background_down: 'w_b.png'
					pos_hint: root.pos_day_month_year1
					on_press: root.day_or_what_changer('day')

				ToggleButton:
					allow_no_selection: False
					group: 'day_month_year'
					text: root.t_month
					size_hint: (.3, .06)
					background_down: 'w_b.png'
					pos_hint: root.pos_day_month_year2
					on_press: root.day_or_what_changer('month')

				ToggleButton:
					allow_no_selection: False
					group: 'day_month_year'
					text: root.t_year
					size_hint: (.3, .06)
					background_down: 'w_b.png'
					pos_hint: root.pos_day_month_year3
					on_press: root.day_or_what_changer('year')


				TextInput:
					font_size: "65sp"
					id: inputer
					multiline: False
					size_hint: (.8, .15)
					pos_hint: root.g_input

				TextInput:
					font_size: "65sp"
					id: ex_inputer
					multiline: False
					size_hint: (.2, .15)
					pos_hint:root.ex_input1

				TextInput:
					font_size: "65sp"
					id: ex_inputer2
					multiline: False
					size_hint: (.2, .15)
					pos_hint: root.ex_input2

				TextInput:
					font_size: "65sp"
					id: ex_inputer3
					hint_text: root.yez
					multiline: False
					size_hint: (.4, .15)
					pos_hint: root.ex_input3


				Button:
					font_name: 'mp.ttf'
					text: '>'
					font_size: '70sp'
					border: 0,0,0,0
					pos_hint: {'center_x': .72, 'center_y': .53}
					size_hint: (.24, .15)
					background_normal: "edit.png"
					background_down: "edit.png"
					on_release:
						root.press += 1
						root.catch_art()


				Button:
					font_name: 'mp.ttf'
					text: 'R'
					font_size: '70sp'
					border: 0,0,0,0
					pos_hint: {'center_x': .5, 'center_y': .53}
					size_hint: (.24, .15)
					background_normal: "edit.png"
					background_down: "edit.png"
					on_release:
						root.repeat()

				
				Button:
					background_down: 'w_b.png'
					color: 1,1,1,1
					font_size: '90sp'
					text: "A"
					font_name: 'mp.ttf'
					pos_hint: root.pos_init_cam
					size_hint: (.23, .148)
					on_release:
						root.go_cam()


				Button:
					font_name: 'mp.ttf'
					text: '<'
					font_size: '70sp'
					pos_hint: {'center_x': .28, 'center_y': .53}
					border: 0,0,0,0
					size_hint: (.24, .15)
					background_normal: "edit.png"
					background_down: "edit.png"
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
					canvas: 
						Color: 
							rgba: root.buttons_color
						Rectangle: 
							pos: self.pos 
							size: self.size
					Button:
						text: "1"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('1')
					Button:
						text: "2"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('2')
					Button:
						text: "3"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('3')
					Button:
						text: "4"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('4')
					Button:
						text: "5"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('5')
					Button:
						text: "6"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('6')
					Button:
						text: "7"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('7')
					Button:
						text: "8"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('8')
					Button:
						text: "9"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('9')
					Button:
						text: "CLS"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('CLS')
					Button:
						text: "0"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('0')
					Button:
						text: "<<"
						background_down: 'w_b.png'
						font_size: '40sp'
						on_release: root.type('<<')


		Screen:
			name: 'database'
			FloatLayout:
				canvas:
					Color: 	
						rgb: .886, .949, .671

					Rectangle:
						size: self.size
						pos: self.pos
						
			Label:

				halign: 'center'
				valign: "middle"
				text: 'База данных'
				text_size: self.size
				size_hint: (.8, .07)
				color: 0, 0, 0, 1
				font_size: "28sp"
				pos_hint: {'center_x': .5, 'center_y': .93}

			Button:
				text: '+'
				font_name: 'mp.ttf'
				font_size: '75sp'
				border: 0,0,0,0
				pos_hint: {'center_x': .5, 'center_y': .07}
				size_hint: (.24, .15)
				background_normal: "edit.png"
				background_down: "edit.png"
				on_release:
					root.create_new()

			Button:
				pos_hint: {'center_x': .848, 'center_y': .8}
				size_hint: (.2, .113)
				text: 's'
				font_name: 'mp.ttf'
				font_size: '60sp'
				background_normal: 'w_b.png'
				on_release:
					root.get_them(0)

			TextInput:
				font_size: "28sp"
				hint_text: root.t_search
				id: searcher
				multiline: False
				size_hint: (.7, .11)
				pos_hint:{"center_x":.40,"center_y":.8}

			ScrollView:
				size_hint_x: .95
				size_hint_y: .58
				pos_hint: {'center_x': .5, 'center_y': .435}
				GridLayout:
					id: griddy
					canvas:
						Rectangle:
							pos: self.pos
							size: self.size
							source: "cleanbl.png"

					row_default_height: root.height/6 #row size control
					spacing: 2
					cols: 1
					size_hint_y: None
					height: 0

		Screen:
			name: 'today'
			FloatLayout:
				canvas:
					Color: 	
						rgb: .886, .949, .671
					Rectangle:
						size: self.size
						pos: self.pos
						source: 'back.png'

				Label:
					halign: 'center'
					valign: "middle"
					text: 'Сроки годности'
					text_size: self.size
					size_hint: (.8, .07)
					color: 0, 0, 0, 1
					font_size: "28sp"
					pos_hint: {'center_x': .5, 'center_y': .965}

				Button:
					id: posrok_button
					border: 0,0,0,0
					text: root.t_expired
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

				#togglers
				ToggleButton:
					id: bom_bom_bom
					allow_no_selection: False
					state: 'down'
					background_down: 'w_b.png'
					group: 'which_trash'
					state: 'down'
					text: root.t_today
					size_hint: (.3, .06)
					pos_hint: {"center_x": .2,"center_y":.9}
					on_press: root.show_rangers(False)
					on_press: root.show_el(False)
					on_press: root.define_today_art('today')
					on_press: root.reshape_today_scroll('today')

				ToggleButton:
					id: bom_bom_bom2
					allow_no_selection: False
					group: 'which_trash'
					background_down: 'w_b.png'
					text: root.t_random
					size_hint: (.3, .06)
					pos_hint: {"center_x": .5,"center_y":.9}
					on_press: root.show_rangers(False)
					on_press: root.show_el(True)
					on_press: root.define_today_art('another')
					on_press: root.reshape_today_scroll('any')

				ToggleButton:
					id: bom_bom_bom3
					allow_no_selection: False
					group: 'which_trash'
					background_down: 'w_b.png'
					text: root.t_period
					size_hint: (.3, .06)
					pos_hint: {"center_x": .8,"center_y":.9}
					on_press: root.show_rangers(True)
					on_press: root.show_el(False)
					on_press: root.define_today_art('range')
					on_press: root.reshape_today_scroll('range')

				TextInput:
					font_size: "28sp"
					id: to_d1
					hint_text: root.t_dd
					multiline: False
					size_hint: (.11, .08)
					pos_hint: root.pos_el1
					on_text: root.extra_checker('dd')

				TextInput:
					font_size: "28sp"
					id: to_d2
					hint_text: root.t_mm
					multiline: False
					size_hint: (.11, .08)
					pos_hint: root.pos_el2
					on_text: root.extra_checker('mm')

				TextInput:
					font_size: "28sp"
					id: to_d3
					hint_text: root.current_year
					multiline: False
					size_hint: (.2, .08)
					pos_hint: root.pos_el3
					on_text: root.extra_checker('yy')
##################################################################################
				TextInput:
					font_size: "18sp"
					id: to_range1
					hint_text: root.t_dd
					multiline: False
					size_hint: (.11, .05)
					pos_hint: root.ranger1
					on_text: root.extra_checker2('1dd')

				TextInput:
					font_size: "18sp"
					id: to_range2
					hint_text: root.t_mm
					multiline: False
					size_hint: (.11, .05)
					pos_hint: root.ranger2
					on_text: root.extra_checker2('1mm')

				TextInput:
					font_size: "18sp"
					id: to_range3
					hint_text: root.current_year
					multiline: False
					size_hint: (.2, .05)
					pos_hint: root.ranger3
					on_text: root.extra_checker2('1yy')

				TextInput:
					font_size: "18sp"
					id: to_range4
					hint_text: root.t_dd
					multiline: False
					size_hint: (.11, .05)
					pos_hint: root.ranger4
					on_text: root.extra_checker2('2dd')

				TextInput:
					font_size: "18sp"
					id: to_range5
					hint_text: root.t_mm
					multiline: False
					size_hint: (.11, .05)
					pos_hint: root.ranger5
					on_text: root.extra_checker2('2mm')

				TextInput:
					font_size: "18sp"
					id: to_range6
					hint_text: root.current_year
					multiline: False
					size_hint: (.2, .05)
					pos_hint: root.ranger6
					on_text: root.extra_checker2('2yy')

				Button:
					font_size: "60sp"
					font_name: 'mp.ttf'
					text: 's'
					background_down: 'w_b.png'
					size_hint: (.31, .11)
					pos_hint: root.ranger7
					on_release: root.ranger_main()

######################################################################################

				Label:
					canvas.before: 
						Color:
							rgb: .58, .84, 0 
						Rectangle:
							pos: self.pos 
							size: self.size
					font_size: "18sp"
					text: root.t_ot + ':'
					size_hint: (.1, .05)
					pos_hint: root.ranger8

				Label:
					canvas.before: 
						Color: 
							rgb: .58, .84, 0
						Rectangle: 
							pos: self.pos 
							size: self.size
					font_size: "18sp"
					text: root.t_do + ':'
					size_hint: (.1, .05)
					pos_hint: root.ranger9

				Button:
					font_name: 'mp.ttf'
					text: 's'
					font_size: '60sp'
					size_hint: (.3, .08)
					background_down: 'w_b.png'
					pos_hint: root.pos_el4
					on_press: root.define_another_art()

				ScrollView:
					size_hint_x: root.shx_today_scroll
					size_hint_y: root.shy_today_scroll
					pos_hint: root.ph_today_scroll
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
					font_size: "20sp"
					size_hint: (.8, .3)
					canvas.before: 
						Color: 
							rgba: root.col
						Rectangle:
							pos: self.pos 
							size: self.size


				#bookmark
				Button:
					background_down: 'w_b.png'
					font_name: 'mp.ttf'
					text: 'I'
					font_size: '60sp'
					pos_hint: root.pos_el5
					size_hint: (.3, .113)
					on_release:
						root.trash_out()

		Screen:
			name: 'information'
			FloatLayout:
				id: info_canvas
				canvas:
					Color: 	
						rgb: .886, .949, .671
					Rectangle:
						size: self.size
						pos: self.pos
						

				Label:
					id: ghost
					size: self.texture_size
					text: "Нажмите обновить"
					font_size: "60sp"
					pos_hint:{"center_x":.5,"center_y":.88}

				Label:
					id: ghost2
					size: self.texture_size
					text: ""
					font_size: "30sp"
					pos_hint:{"center_x":.5,"center_y":.80}
				Label:
					id: ghost4
					size: self.texture_size
					text: ""
					font_size: "30sp"
					pos_hint:{"center_x":.5,"center_y":.75}
				Label:
					id: ghost5
					size: self.texture_size
					text: ''
					font_size: "30sp"
					pos_hint: {"center_x":.5, "center_y":.70}

				ScrollView:
					size_hint_x: 0.9
					size_hint_y: 0.48
					pos_hint: {'center_x': .5, 'center_y': .41}
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
					border: 0,0,0,0
					pos_hint: {'center_x': .8, 'center_y': .1}
					size_hint: (.24, .15)
					background_normal: "edit.png"
					background_down: "butp.png"
					on_release:
						root.init_edit()

				Button:
					border: 0,0,0,0
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
					Color: 	
						rgb: .886, .949, .671
					Rectangle:
						size: self.size
						pos: self.pos
						
				Label:
					size: self.texture_size
					text: root.t_edit
					font_size: "40sp"
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
					border: 0,0,0,0
					text: root.t_save
					font_size: "22sp"
					pos_hint: {'center_x': .75, 'center_y': .8}
					size_hint: (.4, .10)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.change_popup_name(True)
				Button:
					border: 0,0,0,0
					text: root.t_add_date
					font_size: "16sp"
					pos_hint: {'center_x': .75, 'center_y': .7}
					size_hint: (.4, .10)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.add_entry()
				Button:
					border: 0,0,0,0
					text: root.t_manage_ean
					font_size: "16sp"
					pos_hint: {'center_x': .75, 'center_y': .6}
					size_hint: (.4, .10)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.manage_eans()

				Button:
					border: 0,0,0,0
					text: root.t_delete_article
					font_size: "18sp"
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
					border: 0,0,0,0
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
					Color: 	
						rgb: .886, .949, .671
					Rectangle:
						size: self.size
						pos: self.pos

				Label:		
					halign: 'center'
					valign: "middle"
					text: 'Настройки'
					text_size: self.size
					size_hint: (.8, .07)
					color: 0, 0, 0, 1
					font_size: "28sp"
					pos_hint: {'center_x': .5, 'center_y': .93}

				Button:
					border: 0,0,0,0
					text: root.t_language
					font_size: "22sp"
					pos_hint: {'center_x': .5, 'center_y': .8}
					size_hint: (.65, .12)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release: root.ids.mana.current = "language"

				Button:
					border: 0,0,0,0
					text: root.t_sync
					font_size: "22sp"
					pos_hint: {'center_x': .5, 'center_y': .68}
					size_hint: (.65, .12)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.is_user_already_logged()

				Button:
					border: 0,0,0,0
					text: root.t_delete_database
					font_size: "22sp"
					pos_hint: {'center_x': .5, 'center_y': .56}
					size_hint: (.65, .12)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.are_you_sure()

				Button:
					border: 0,0,0,0
					text: root.t_delete_effects
					font_size: "22sp"
					pos_hint: {'center_x': .5, 'center_y': .44}
					size_hint: (.65, .12)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.delete_effect()

		Screen:
			name: 'old_arts'
			FloatLayout:

				id: canvas
				canvas:
					Color: 	
						rgb: .886, .949, .671
					Rectangle:
						size: self.size
						pos: self.pos
						


				ScrollView:
					size_hint_x: .95
					size_hint_y: .8
					pos_hint: {'center_x': .5, 'center_y': .55}
					BoxLayout:
						orientation: "vertical"
						id: griddy_trash
						canvas:
							Color: 	
								rgb: .886, .949, .671
							Rectangle:
								pos: self.pos
								size: self.size
						spacing: 2
						cols: 1
						size_hint_y: None
						height: 0


				Button:
					border: 0,0,0,0
					pos_hint: {'center_x':.5, 'center_y': .1}
					size_hint: (.25, .2)
					background_normal: "trash.png"
					background_down: "butp.png"
					on_release:
						root.old_trash_out()

		Screen:
			name: 'sync_data'

			FloatLayout:
				id: canvas
				canvas:
					Color: 	
						rgb: .886, .949, .671
					Rectangle:
						size: self.size
						pos: self.pos
						


				TextInput:
					font_size: "24sp"
					id: group_name
					hint_text: root.t_group_name
					multiline: False
					size_hint: (.8, .08)
					pos_hint: {'center_x': .5, 'center_y': .75}

				TextInput:
					font_size: "24sp"
					id: group_password
					password: True
					hint_text: root.t_password
					multiline: False
					size_hint: (.8, .08)
					pos_hint: {'center_x': .5, 'center_y': .65}

				Button:
					border: 0,0,0,0
					text: root.t_enter
					font_size: "22sp"
					pos_hint: {'center_x': .5, 'center_y': .5}
					size_hint: (.65, .1)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.try_to_log_in(group_name.text, group_password.text)

				Button:
					border: 0,0,0,0
					text: root.t_create_group
					font_size: "22sp"
					pos_hint: {'center_x': .5, 'center_y': .4}
					size_hint: (.65, .1)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release:
						root.create_new_group(group_name.text, group_password.text)

		Screen:
			name: 'new_group_nickname'

			FloatLayout:
				id: canvas
				canvas:
					Color: 	
						rgb: .886, .949, .671
					Rectangle:
						size: self.size
						pos: self.pos
						

			TextInput:

				font_size: "24sp"
				id: new_nickname
				hint_text: root.t_create_user
				multiline: False
				size_hint: (.8, .08)
				pos_hint: {'center_x': .5, 'center_y': .75}

			Button:

				text: root.t_create
				border: 0,0,0,0
				font_size: "22sp"
				pos_hint: {'center_x': .5, 'center_y': .65}
				size_hint: (.65, .1)
				background_normal: "but.png"
				background_down: "butp.png"
				on_release:
					root.new_group_new_user(new_nickname.text)

		Screen:
			name: 'ask_nickname'

			FloatLayout:
				id: canvas
				canvas:
					Color: 	
						rgb: .886, .949, .671
					Rectangle:
						size: self.size
						pos: self.pos
						

			TextInput:

				font_size: "24sp"
				id: nickname
				hint_text: root.t_user_name
				multiline: False
				size_hint: (.8, .08)
				pos_hint: {'center_x': .5, 'center_y': .75}

			Button:

				text: root.t_enter
				border: 0,0,0,0
				font_size: "22sp"
				pos_hint: {'center_x': .5, 'center_y': .65}
				size_hint: (.65, .1)
				background_normal: "but.png"
				background_down: "butp.png"
				on_release:
					root.is_user_here(nickname.text)

			Button:

				text: root.t_create
				border: 0,0,0,0
				font_size: "22sp"
				pos_hint: {'center_x': .5, 'center_y': .55}
				size_hint: (.65, .1)
				background_normal: "but.png"
				background_down: "butp.png"
				on_release:
					root.new_group_new_user(nickname.text)

		Screen:
			name: 'group_home'

			FloatLayout:
				id: float_group_home
				canvas:
					Color: 	
						rgb: .886, .949, .671
					Rectangle:
						size: self.size
						pos: self.pos
						

				Label:
					id: nothing_to_show
					canvas.before:
						Color: 
							rgba: root.group_home_nothing_color 
						Rectangle:
							pos: self.pos 
							size: self.size

					size_hint: (.95, .5)
					pos_hint:{"center_x":.5,"center_y":.5}
					font_size: "25sp"

				Label:
					canvas.before:
						Color: 
							rgba: .53, .70, .18, .3 
						Rectangle:
							pos: self.pos 
							size: self.size

					size_hint: (1, .15)
					pos_hint:{"center_x":.5,"center_y":.9}


				Label:
					canvas.before:
						Color: 
							rgba: .53, .70, .18, .3 
						Rectangle:
							pos: self.pos 
							size: self.size

					size_hint: (1, .05)
					pos_hint:{"center_x":.5,"center_y":.79}
					text: root.t_your_sync
					color: 1,0,1,1
					font_size: "25sp"

				ScrollView:
					size_hint_x: .95
					size_hint_y: .5
					pos_hint: {'center_x': .5, 'center_y': .5}
					BoxLayout:
						orientation: "vertical"
						id: grid_internet_change
						canvas:
							Color: 	
								rgb: .886, .949, .671
							Rectangle:
								pos: self.pos
								size: self.size
								
						spacing: 2
						cols: 1
						size_hint_y: None
						height: 0

				Label:
					size: self.texture_size
					text: root.current_group
					font_size: "40sp"
					pos_hint:{"center_x":.5,"center_y":.9}

				Label:
					size: self.texture_size
					text: root.t_group
					color: 1,0,1,1
					font_size: "25sp"
					pos_hint:{"center_x":.5,"center_y":.95}

				Label:
					size: self.texture_size
					text: root.current_user
					color: 1,0,1,1
					font_size: "21sp"
					pos_hint:{"center_x":.5,"center_y":.85}

				Button:
					text: root.t_sync
					border: 0,0,0,0
					font_size: "22sp"
					pos_hint: {'center_x': .5, 'center_y': .19}
					size_hint: (.65, .1)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release: root.prepare_to_internet_sync()
					on_release: root.while_loading()

				Button:
					text: root.t_exit
					border: 0,0,0,0
					font_size: "22sp"
					pos_hint: {'center_x': .32, 'center_y': .09}
					size_hint: (.325, .1)
					background_normal: "but.png"
					background_down: "butp.png"
					on_release: root.exit_group()

				Button:
					text: root.t_delete
					border: 0,0,0,0
					font_size: "22sp"
					pos_hint: {'center_x': .68, 'center_y': .09}
					size_hint: (.325, .1)
					background_normal: "but_red.png"
					background_down: "butp.png"
					on_release: root.delete_user()

		Screen:
			name: 'language'

			FloatLayout:
				canvas:
					Color: 	
						rgb: .886, .949, .671
					Rectangle:
						size: self.size
						pos: self.pos
						

				ToggleButton:
					id: russian_button
					allow_no_selection: False
					group: 'lang_lang'
					state: 'down'
					text: 'Русский'
					pos_hint: {'center_x': .5, 'center_y': .79}
					size_hint: (.65, .1)
					on_press: root.lang = 'ru'
					on_press: root.change_lang('ru')
					on_press: root.set_lang('ru')


				ToggleButton:
					id: english_button
					allow_no_selection: False
					group: 'lang_lang'
					text: 'English'
					pos_hint: {'center_x': .5, 'center_y': .89}
					size_hint: (.65, .1)
					on_press: root.lang = 'eng'
					on_press: root.change_lang('eng')
					on_press: root.set_lang('eng')



	BoxLayout:
		size_hint_y: 8
		canvas.before:
			Color: 
				rgba: .733, .855, .463, .95
			Rectangle:
				pos: self.pos 
				size: self.size

		ToggleButton:
			id: fi
			border: 0,0,0,0
			allow_no_selection: False
			background_normal: 'work_1.png'
			background_down: 'work_2.png'
			group: 'test'
			state: 'down'
			on_press: root.ids.mana.current = "work"

		ToggleButton:
			id: se
			border: 0,0,0,0
			allow_no_selection: False
			background_normal: 'DB_1.png'
			background_down: 'DB_2.png'
			group: 'test'
			on_press: root.ids.mana.current = "database"

		ToggleButton:
			id: th
			border: 0,0,0,0
			allow_no_selection: False
			background_normal: 'today_1.png'
			background_down: 'today_2.png'
			group: 'test'
			on_press: root.show_rangers(False)
			on_press: root.ids.bom_bom_bom.state = 'down'
			on_press: root.ids.bom_bom_bom2.state = 'normal'
			on_press: root.ids.bom_bom_bom3.state = 'normal'
			on_press: root.show_el(False)
			on_press: root.reshape_today_scroll('today')
			on_press: root.define_today_art('today')

		ToggleButton:
			id: fo
			border: 0,0,0,0
			allow_no_selection: False
			background_normal: 'settings_1.png'
			background_down: 'settings_2.png'
			group: 'test'
			on_press: root.ids.mana.current = "settings"
	""")

art_bars = {}
entries = []
art_names = {}
days_of_life = {}
last_art = None

def popup(title, text):
	popup = Popup(title=title,
	content=Label(text=text),
	size_hint=(0.65, 0.25))
	popup.open()

closer = False
new_date = ObjectProperty("")

def ch_closer():
	global closer

	if closer == True:
		closer = False
	elif closer == False:
		closer = True

sync()

if __name__ == "__main__":
	ProtoApp().run()
