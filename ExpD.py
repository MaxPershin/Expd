"""This programm should let us do quick ExpD calculations"""

import os
from time import strftime
from time import sleep
clear = lambda: os.system('cls')
j = 0


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


entries = []
art_names = {}
days_of_life = {}
superexiter = False
#Logic block
yoga = True
x = True
def check(yoga, preask, article):
	while x:
		if yoga == True:
			ask = input("What is Start Date? DDMM or E/END/MON ")

			if ask.upper() == "END":
				shit = artch(article)
				ask2 = input("What is End Date? DDMM ")
				if ask2.upper() == "E":
					continue
				if ask2.isalnum(): 
					if len(ask2) == 4:
						if ask2[0].isalpha() == False and ask2[1].isalpha() == False and ask2[2].isalpha() == False and ask2[3].isalpha() == False:
							if int(ask2[2:]) <= 12 and int(ask2[2:]) >= 1 and int(ask2[:2]) <= 31 and int(ask2[:2]) >= 1:
								if check2(ask2):
									save(ask2, article, True)
									global superexiter
									superexiter = True
									break
								else:
									clear()
									print("This month have less days than you typed!")
									sleep(2)
									clear()
									if yoga == False:
										return "F"
							else:
								clear()
								print("You are out of range!!!")
								sleep(2)
								clear()
								if yoga == False:
									return "F"
						else:
							clear()
							print("You were typing letters!")
							sleep(2)
							clear()
							if yoga == False:
								return "F"
					else:
						clear()
						print("You should type in following format - DDMM!")
						sleep(2)
						clear()
						if yoga == False:
							return "F"
				else:
					clear()
					print("You entered symbols!")
					sleep(2)
					clear()
					if yoga == False:
						return "F"

		elif yoga == False:
			ask = preask
		if ask == "e" or ask == "E":
			clear()
			return "EXIT"
		else:
			if ask.isalnum(): 
				if len(ask) == 4:
					if ask[0].isalpha() == False and ask[1].isalpha() == False and ask[2].isalpha() == False and ask[3].isalpha() == False:
						if int(ask[2:]) <= 12 and int(ask[2:]) >= 1 and int(ask[:2]) <= 31 and int(ask[:2]) >= 1:
							if check2(ask):
								return ask
							else:
								clear()
								print("This month have less days than you typed!")
								sleep(2)
								clear()
								if yoga == False:
									return "F"
						else:
							clear()
							print("You are out of range!!!")
							sleep(2)
							clear()
							if yoga == False:
								return "F"
					else:
						clear()
						print("You were typing letters!")
						sleep(2)
						clear()
						if yoga == False:
							return "F"
				else:
					clear()
					print("You should type in following format - DDMM!")
					sleep(2)
					clear()
					if yoga == False:
						return "F"
			else:
				clear()
				print("You entered symbols!")
				sleep(2)
				clear()
				if yoga == False:
					return "F"

def check2(ask):
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

def work(switch):
	exiting = False
	while x:
		j = True
		while j:
			global superexiter
			superexiter = False
			article = input("Please Enter Article: ")
			if article == "E" or article == "e":
				exiting = True
				break
			if article.isdigit():
				j = False
			else:
				print()
				print("Please enter digit Article!")
				print()
				sleep(2)
				clear()
		if exiting:
			start = "EXIT"
		else:
			start = check(True, "", article)
		if superexiter == True:
			continue
		if start == "EXIT":
			print()
			print("Exiting to main menu")
			print()
			sleep(1)
			break
		month = start[2:]
		day = int(start[:2])
		exactday = allmonth[month] + day
		clear()
		ex = artch(article)
		if ex[len(ex)-1].upper() == "M":
			newex = ex.replace("M","")
			newex2 = newex.replace("m", "")
			ex = newex2
			halfm = int(month) + int(ex)
			while halfm > 12:
				halfm -= 12
			newhalfm = str(halfm)
			halfm = newhalfm
			halfd = start[:2]
			if len(halfm) < 2:
				halfmm = "0"+ halfm
				halfm = halfmm
			final = halfd + halfm
			save(final, article, True)
			print("ExpD is BEFORE", final)
			print()
			continue
		elif str(ex).isdigit() == True and int(ex) > 0:
			ex = int(ex)
			ex = newcycle(ex)
			summing = exactday + ex
			if summing <= 32:
				a = 31 - summing
				dayf = 31 - a
				print("ExpD is BEFORE %0d.01" % dayf)
				print ()
				ent = "%0d01" % dayf
				save(ent, article, switch)
			elif summing <= (59+extra):
				a = (59+extra) - summing
				dayf = (28+extra) - a
				print("ExpD is BEFORE %0d.02" % dayf)
				print()
				ent = "%0d02" % dayf
				save(ent, article, switch)
			elif summing <= (90+extra):
				a = (90+extra) - summing
				dayf = 31 - a
				print("ExpD is BEFORE %0d.03" % dayf)
				print()
				ent = "%0d03" % dayf
				save(ent, article, switch)
			elif summing <= (120+extra):
				a = (120+extra) - summing
				dayf = 30 - a
				print("ExpD is BEFORE %0d.04" % dayf)
				print()
				ent = "%0d04" % dayf
				save(ent, article, switch)
			elif summing <= (151+extra):
				a = (151+extra) - summing
				dayf = 31 - a
				print("ExpD is BEFORE %0d.05" % dayf)
				print()
				ent = "%0d05" % dayf
				save(ent, article, switch)
			elif summing <= (181+extra):
				a = (181+extra) - summing
				dayf = 30 - a
				print("ExpD is BEFORE %0d.06" % dayf)
				print()
				ent = "%0d06" % dayf
				save(ent, article, switch)
			elif summing <= (212+extra):
				a = (212+extra) - summing
				dayf = 31 - a
				print("ExpD is BEFORE %0d.07" % dayf)
				print()
				ent = "%0d07" % dayf
				save(ent, article, switch)
			elif summing <= (243+extra):
				a = (243+extra) - summing
				dayf = 31 - a
				print("ExpD is BEFORE %0d.08" % dayf)
				print()
				ent = "%0d08" % dayf
				save(ent, article, switch)
			elif summing <= (273+extra):
				a = (273+extra) - summing
				dayf = 30 - a
				print("ExpD is BEFORE %0d.09" % dayf)
				print()
				ent = "%0d09" % dayf
				save(ent, article, switch)
			elif summing <= (304+extra):
				a = (304+extra) - summing
				dayf = 31 - a
				print("ExpD is BEFORE %0d.10" % dayf)
				print()
				ent = "%0d10" % dayf
				save(ent, article, switch)
			elif summing <= (334+extra):
				a = (334+extra) - summing
				dayf = 30 - a
				print("ExpD is BEFORE %0d.11" % dayf)
				print()
				ent = "%0d11" % dayf
				save(ent, article, switch)
			elif summing <= (365+extra):
				a = (365+extra) - summing
				dayf = 31 - a
				print("ExpD is BEFORE %0d.12" % dayf)
				print()
				ent = "%0d12" % dayf
				save(ent, article, switch)
			elif summing >= (365+extra):
				ov = summing - (365+extra)
				realanwser = cycle(ov)
				print(realanwser)
				if len(realanwser) != 19:
					ent = realanwser[15] + realanwser[16] + realanwser[18] + realanwser[19]
					save(ent, article, switch)
				else:
					ent = realanwser[15] + realanwser[17] + realanwser[18]
					save(ent, article, switch)
		else:
			print("You entered incorrect number of days!")

def newcycle(ov):
	switch = True
	while switch:
		if ov > 365:
			ov -= 365
		else:
			return ov

def cycle(ov):
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
		cycle(ov)

def save(ent, article, switch):
	if len(ent) == 3:
		ent = "0" + ent

	if switch:
		hound = [i for i,x in enumerate(entries) if x==article]
		samer = False
		for each in hound:
			if entries[each-1] == ent:
				samer = True
		if samer:
			print("This Article Already has this entry!")
			sleep(2)
		else:
			f = open("saver.txt", "a")
			f.write(str((ent + "$" + article + "$")))
			f.close()
			sync()
			print("Article", art_names[article], "added Successfully!")
			print()

def start():
	while True:
		clear()
		sync()
		print("MAIN MENU")
		print()
		print("Press 1 for Work Mode")
		print("Press 2 for View Mode")
		print("Press 3 for TODAY Utilization Mode")
		print("Press 4 for DATABASE change")
		print("Press 5 for TEMPTODAY")
		print("Press E for Exit")
		print()
		anwser = input("You choice: ")
		if anwser == "1":
			switch = True
			clear()
			work(switch)
		elif anwser == "2":
			clear()
			view()
		elif anwser == "3":
			clear()
			today()
		elif anwser == "4":
			clear()
			change_menu()
		elif anwser == "5":
			clear()
			temptoday()
		elif anwser == "e" or anwser == "E":
			print()
			print("Goodbye!")
			break
		else:
			print()
			print("Wrong input!")
			print()
			sleep(1)
			clear()

def view():
	if len(entries) == 1:
		print()
		print("You have no entries")
		sleep(2)
		print()
		print("Heading back to menu")
		sleep(2)
		return
	else:
		enum = 0
		indie = 0
		lenner = len(entries)-2
		while indie < lenner:
			enum+=1
			print(enum, "Before", entries[indie], entries[indie+1], art_names[entries[indie+1]]) 
			indie+=2

	print()
	sleep(1)
	back = input("Are you ready to go back? Hit Enter ")
	print()
	print("Heading to main menu")
	print()
	sleep(1)

def sync():
	f = open("saver.txt", "r+")
	rawread = f.read()
	f.close()
	global entries
	entries = rawread.split("$")

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

def today():
	count = 0
	holder = []
	abol = todaynum+1
	res = fnum2text(abol) #res returns str "0204"

	if len(res) < 4:
		newres = "0%s" % res
	else:
		newres = res

	if newres in entries:
		print("Before", newres,":")
		print()

		lister = [i for i,x in enumerate(entries) if x==newres]

		for each in lister:
			holder.append(each+1)

		for each in holder:
			count+=1
			if days_of_life[entries[each]].isdigit():
				helper = fnum2text(abol - int(days_of_life[entries[each]]))
			else:
				helper = "NO DATA YET ;)"
			if len(helper) < 4:
				helper = "0%s" % helper
			print(count, entries[each], art_names[entries[each]], "FROM", helper)

		print()
		print()
		while True:
			wannadelete = input("Did you utilize those items? Y/N ")
			if wannadelete.upper() == "N":
				break
			elif wannadelete.upper() == "Y":
				f = open("saver.txt", "r+")
				rawread = f.read()
				f.close()

				rawread = rawread.split("$")
				del rawread[len(rawread)-1]

				deleter = []

				for each in lister:
					deleter.append(each)

				for each in holder:
					deleter.append(each)

				deleter.sort(reverse=True)

				for each in deleter:
					del rawread[each]

				f = open("saver.txt", "w")

				for each in rawread:
					f.write(str(each + "$"))

				f.close()

				sync()

				print()
				print("Entries Was Deleted")
				sleep(2)
				break



	else:
		print()
		print("You have nothing to utilize")
		sleep(2)
	print()
	anwser = input("Hit Enter to Go back to Menu: ")

def temptoday():
	while True:

		clear()
		asker = input("How many days forvard? ")
		if asker.upper() == "E":
			break
		r = int(asker)
		count = 0
		holder = []
		abol = todaynum+(r)
		res = fnum2text(abol) #res returns str "0204"

		print("You are watchin arts which are BEFORE", res)

		if len(res) < 4:
			newres = "0%s" % res
		else:
			newres = res

		if newres in entries:
			print("Before", newres,":")
			print()

			lister = [i for i,x in enumerate(entries) if x==newres]

			for each in lister:
				holder.append(each+1)

			for each in holder:
				count+=1
				if days_of_life[entries[each]].isdigit():
					helper = fnum2text(abol - int(days_of_life[entries[each]]))
				else:
					helper = "NO DATA YET ;)"
				if len(helper) < 4:
					helper = "0%s" % helper
				print(count, entries[each], art_names[entries[each]], "FROM", helper)

			print()
			print()
		if count == 0:
			print("No entries to this date")
			sleep(2)
		if count >= 1:
			xex = input("Want to Delete? Y? ")
			if xex.upper() == "Y":
				f = open("saver.txt", "r+")
				rawread = f.read()
				f.close()

				rawread = rawread.split("$")
				del rawread[len(rawread)-1]

				deleter = []

				for each in lister:
					deleter.append(each)

				for each in holder:
					deleter.append(each)

				deleter.sort(reverse=True)

				for each in deleter:
					del rawread[each]

				f = open("saver.txt", "w")

				for each in rawread:
					f.write(str(each + "$"))

				f.close()

				sync()

				print()
				print("Entries Was Deleted")
				sleep(2)
				break

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

def artch(article):

	j = True

	anwser = article
	if anwser in days_of_life:
		preex = days_of_life[anwser]
	else:
		while j:
			preex = input("We have no lifespan data of this ARTICLE, pleae enter its DAYS OF LIFE/MON: ")
			if preex[len(preex)-1].upper() == "M" or preex.isdigit():
				j = False
				f = open("daysoflife.txt", "a")
				f.write(str((anwser + "$" + preex + "$")))
				f.close()
				print()
				print("Now Article", anwser, "has standart lifespan setted to", preex)
				print()
				sleep(2)

	if anwser not in art_names:
		gettingname = input("We can't find its name in DATABASE, please enter ARTICLE NAME: ")
		f = open("artname.txt", "a")
		f.write(str((anwser + "$" + gettingname + "$")))
		f.close()
		print()
		print("Now Article", anwser, "has name", gettingname)
		print()
		sleep(2)

	sync()
	return preex

def change_menu():
	while True:
		clear()
		print ("Welcome to ExpD DATABASE")
		print()
		print("Press 1 for changing BEFORE entries")
		print("Press 2 for changing Article Name/Standart")
		print("Press 3 for VIEW Art")
		print("Press 4 for VIEW ALL ARTs")
		print("Press 5 to ADD new Article")
		print("Press 6 to Delete an Item")
		print("Press 7 to Delete ALL DATABASE")
		print()
		print("Press E for Exit to main menu")
		inputer = input("Enter value: ")
		if inputer == "E" or inputer == "e":
			break
		elif inputer.isdigit() == True:
			if inputer == "1":
				change_entries()
			elif inputer == "2":
				change_days_name()
			elif inputer == "3":
				artview()
			elif inputer == "4":
				viewallarts()
			elif inputer == "5":
				addnewart()
			elif inputer == "6":
				deleteart()
			elif inputer == "7":
				deleteALL()
			else:
				print()
				print("Enter correct number!")
				sleep(1)

def viewallarts():
	clear()
	print("Those ARTICLES is in a DATABASE:")
	print()
	for each in art_names:
		if each != "":
			print(each, art_names[each], "with ", days_of_life[each], "days")

	print()
	rower = input("Press ENTER to go back")

def addnewart():
	while True:
		clear()
		print("Here you can add a new article in a DATABASE")
		print()
		nart = input("Please enter new article (or E for exit): ")
		if nart.upper() == "E":
			break
		if nart in art_names:
			print()
			print("This article is already in DATABASE!")
			sleep(2)
			break
		elif nart not in art_names:
			nname = input("Please enter new article name: ")
			print()
			ndays = input("Please enter new days amount: ")

		f = open("artname.txt", "a")
		f.write(str((nart + "$" + nname + "$")))
		f.close()

		f = open("daysoflife.txt", "a")
		f.write(str((nart + "$" + ndays + "$")))
		f.close()

		sync()

		print("Article", nart, nname, "with", ndays, "added!")
		sleep(2)

def deleteart():
	while True:
		clear()
		print("In this Menu you can DELETE ARTICLE")
		print()
		dart = input("Enter article (or E): ")
		if dart.upper() == "E":
			break
		elif dart not in art_names:
			print()
			print("We dont have this art in DATABASE!")
			sleep (2)
		else:
			while True:
				print("ARE YOU SURE YOU WANT TO DELETE", dart, art_names[dart],"?")
				anwser = input("Y/N: ")
				if anwser.upper() == "N":
					break
				elif anwser.upper() != "Y" and anwser.upper() != "N":
					print("Wrong input!")
				else:
					if dart in entries:

						f = open("saver.txt", "r+")
						rawread = f.read()
						f.close()
						rawread = rawread.split("$")
						print(rawread)
						sleep(10)
						if rawread[len(rawread)-1] == " " or rawread[len(rawread)-1] == " ":
							del rawread[(len(rawread))-1]
						lister = [i for i,x in enumerate(rawread) if x==dart]
						listerz = []
						for each in lister:
							listerz.append(each-1)
						for each in listerz:
							lister.append(each)

						lister.sort(reverse=True)

						for each in lister:
							del rawread[each]
						f = open("saver.txt", "w")
						for each in rawread:
							f.write(str(each + "$"))
						f.close()


					f = open("artname.txt", "r+")
					rawread2 = f.read()
					f.close()
					rawread2 = rawread2.split("$")
					del rawread2[(len(rawread2))-1]
					indexer = rawread2.index(dart)
					indexer2 = indexer
					indexer2 += 1
					del rawread2[indexer2]
					del rawread2[indexer]
					f = open("artname.txt", "w")
					for each in rawread2:
						f.write(str(each + "$"))
					f.close()


					f = open("daysoflife.txt", "r+")
					rawread3 = f.read()
					f.close()
					rawread3 = rawread3.split("$")
					del rawread3[(len(rawread3))-1]
					indexer = rawread3.index(dart)
					indexer2 = indexer
					indexer2 += 1
					del rawread3[indexer2]
					del rawread3[indexer]
					f = open("daysoflife.txt", "w")
					for each in rawread3:
						f.write(str(each + "$"))
					f.close()

					print("Article", dart, art_names[dart], "has been deleted!")
					sleep(2)
					sync()
					break

def deleteALL():
	while True:
		clear()
		print("YOU ARE TRYING TO DELETE ALL ARTICLES AND ENTRIES!")
		anwser = input("Are you sure you want to do so? Y/N ")
		if anwser.upper() == "N":
			break
		elif anwser.upper() == "Y":
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
			print()
			print("Everything was DELETED")
			sleep(2)
			break

def change_entries():
	while True:
		clear()
		print("You can change final date for art or create one")
		print("Choose 1 to Create an Expd entry for ART that in base")
		print("Choose 2 to Upgrade exicting ExpD entry")
		print("Choose 3 to Delete exicting ExpD entry")

		anwser = input("Your choise (or E): ")
		if anwser.upper() == "E":
			break
		elif anwser == "1":
			clear()
			print("You choose to CREATE EXPD entry")
			print()
			endop = True
			while True:
				if endop == False:
					break
				article = input("enter article: ")
				if article.upper() == "E":
					break
				elif article not in art_names:
					print()
					print("We don't have it in DATABASE")
					sleep(2)
				elif article in art_names:
					while True:
						erroronsame = True
						if endop == False:
							break
						error = False
						print("Ok, wich date for", art_names[article], "we should add?")
						dater = input("Type BEFORE date: ")
						if dater.upper() == "E":
							break
						validation = check(False, dater)
						if validation == "F":
							print("Please enter correct date")
							continue

						indient = [i for i, x in enumerate(entries) if x==article]
						indient.sort()

						for each in indient:
							if entries[each-1] == validation:
								print("This article already have this EXPD!!!")
								sleep(2)
								erroronsame = False

						if erroronsame == False:
							continue

						f = open("saver.txt", "a")
						f.write(validation + "$" + article + "$")
						f.close()

						sync()

						endop = False
						print()
						print("We added new entry to", article)
						sleep(2)


		elif anwser == "2":
			clear()
			while True:
				print("You choose to Upgrade exicting EXPD")
				print()
				article = input("Which article we working with? ")
				if article.upper() == "E":
					break
				if article not in art_names:
					print("Article doesnt exict!")
					sleep(2)
					break
				if article not in entries:
					print("Article doesnt have any EXPD data yet")
					sleep(2)
					break

				enuart = [i for i, x in enumerate(entries) if x==article]
				enuexpd = []

				for each in enuart:
					enuexpd.append(each-1)

				lengther = len(enuexpd)

				print("You have", len(enuexpd), "EXPD enties for", article, art_names[article])
				print("Which should we change?")

				number = 0
				storage = []
				for x in range(lengther):
					number += 1
					print(number, entries[enuexpd[number-1]])
					storage.append(number)
					storage.append(entries[enuexpd[number-1]])

				while True:
					anwser = input("Press number from to choose: ")
					if not anwser.isdigit() or int(anwser) <= 0 or int(anwser) > number:
						print("Wrong input!!!")
					else:
						sindex = storage.index(int(anwser))
						worker = storage[sindex+1]

						print("So to what date you would like to change", worker, "?")
						newent = input("Enter a new date: ")
						newentchecked = check(False, newent)
						newent = newentchecked
						if newent == "F":
							print("Please enter corrent date!")
							continue

						f = open("saver.txt", "r+")
						reader = f.read()
						f.close()

						readerNEW = reader.split("$")
						reader = readerNEW

						tind = [i for i, x in enumerate(reader) if x==worker]

						for each in tind:
							if reader[each+1] == article:
								reader[each] = newent

						del reader[len(reader)-1]

						f = open("saver.txt", "w")
						for each in reader:
							f.write(each + "$")
						f.close()
						sync()
						print("Changed Successfully")
						sleep(2)
						break

		elif anwser == "3":
			clear()
			while True:
				print("You choose to DELETE and EXPD enrtry")
				article = input("Which article we working with? ")
				if article.upper() == "E":
					break
				if article not in art_names:
					print("Article doesnt exict!")
					sleep(2)
					break
				if article not in entries:
					print("Article doesnt have any EXPD data yet")
					sleep(2)
					break

				enuart = [i for i, x in enumerate(entries) if x==article]
				enuexpd = []

				for each in enuart:
					enuexpd.append(each-1)

				lengther = len(enuexpd)

				print("You have", len(enuexpd), "EXPD entries for", article, art_names[article])
				print("Which should we delete? ")

				number = 0
				storage = []
				for x in range(lengther):
					number += 1
					print(number, entries[enuexpd[number-1]])
					storage.append(number)
					storage.append(entries[enuexpd[number-1]])

				while True:
					anwser = input("Press number from to choose: ")
					if not anwser.isdigit() or int(anwser) <= 0 or int(anwser) > number:
						print("Wrong input!!!")
					else:
						sindex = storage.index(int(anwser))
						worker = storage[sindex+1]

						f = open("saver.txt", "r+")
						reader = f.read()
						f.close()

						readerNEW = reader.split("$")
						reader = readerNEW

						tind = [i for i, x in enumerate(reader) if x==worker]

						for each in tind:
							if reader[each+1] == article:
								del reader[each]
								del reader[each]

						del reader[len(reader)-1]

						f = open("saver.txt", "w")
						for each in reader:
							f.write(each + "$")
						f.close()
						sync()
						print("Deleted Successfully")
						sleep(2)
						break

def artview():
	while True:
		name = False
		expd = False
		standDays = False

		clear()
		search = input("Enter Article you would like to VIEW (or E for exit): ")
		if search == "E" or search == "e":
			break
		elif search.isdigit():
			art = search
			if art in entries:
				expd = True
				lister = [i for i,x in enumerate(entries) if x==art]
				listers = []
				for each in lister:
					each -= 1
					listers.append(each)
					lislen = len(listers)
			if art in days_of_life:
				standDays = True
			if art in art_names:
				name = True

			if name == True and standDays == True:
				print()
				print("Article", art, "has name", art_names[art])
				print("And standart lifespan set to", days_of_life[art])
				print()
				if expd == True:
					print("Also it is has", lislen, "entries in ExpD list!")
					print()
					for each in range(lislen):
						print("Its BEFORE", entries[listers[each]])
				al = input("Press Any Key to continue... ")

def change_days_name():
	while True:
		clear()
		search = input("Enter Article you would like to change (or E for exit): ")
		if search == "E" or search == "e":
			break
		elif search.isdigit():
			art = search
			if art in days_of_life and art in art_names:
				print("You choose", art, "its standart DAYS value is", days_of_life[art], "and name is set to", art_names[art])
				print()
				anwser = input("Type 1 to enter new Standart Days or 2 to enter new name: ")
				if anwser.isdigit():
					if anwser == "1":
						clear()
						print("Current Standart Expire Days is", days_of_life[art])
						print()
						f = open("daysoflife.txt", "r+")
						dawread = f.read()
						f.close()
						dawread = dawread.split("$")
						worker = dawread.index(art)
						worker += 1
						newdays = input("Please Enter NEW Standart Days of Expiration: ")
						if newdays.isdigit():
							dawread[worker] = newdays
						f = open("daysoflife.txt", "w")
						for each in dawread:
							f.write(str(each + "$"))
						f.close()
						sync()
						print("Article", art, "STANDART Exp Days now Successfully set to", newdays)
						sleep(3)

					elif anwser == "2":
						clear()
						print("Current name for", art, "is", art_names[art])
						print()
						f = open("artname.txt", "r+")
						dawread = f.read()
						f.close()
						dawread = dawread.split("$")
						worker = dawread.index(art)
						worker += 1
						newname = input("Please Enter NEW Article name: ")
						dawread[worker] = newname
						f = open("artname.txt", "w")
						for each in dawread:
							f.write(str(each + "$"))
						f.close()
						sync()
						print("Article", art, "STANDART Name now set to", newname)
						sleep(3)
			else:
				print("Your Article is not in DATABASE")
				sleep(2)


welcome = "Welcome to ExpD - your Expiry Date Assistant"
print(welcome)
print()
sleep(1)
start()

"""Add more fixes and functions:
for v1.0


AFTER GUI!!! For v2.0
2. Create SHOULD BE IN TRASH menu - where user can see which should be already in trash

3. Create Feature where user can see which articles should be under GROSS INCOME rule TODAY

4. Create new input formats, as YEAR and MONTH, so users can input it without transforming into days
"""