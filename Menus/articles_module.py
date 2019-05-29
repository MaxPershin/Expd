articles = []

#93999$26553242341/5241432$Boomber$8m/45$01092012/01012010%
#ean...barcode/............Name....stDa..expd.............

class Article():
	def __init__(self, ean, name):
		self.ean = ean
		self.name = name
		self.standart_date = []
		self.exp_d = []
		self.barcode = []

	def add_entry(self, date):
		self.exp_d.append(date)

	def add_barcode(self, bcode):
		self.barcode.append(bcode)

	def add_standart_date(self, date):
		self.standart_date.append(date)

def sync():
	try:
		f = open("newdata.txt", "r+")
		text = f.read()
		f.close()
		text = text[:-2]
	except:
		f = open("newdata.txt", "w+")
		f.close()
		return

	if len(text) == 0:
		return

	for each in text.split("%"):
		ean, name, stdate, entries, barcode = each.split('$')
		barcode = barcode.split('/')
		stdate = stdate.split('/')
		entries = entries.split('/')

		articles.append(Article(ean, name))

		if barcode != ['']:
			for each in barcode:
				articles[-1].add_barcode(each)

		if stdate != ['']:		
			for each in stdate:
				articles[-1].add_standart_date(each)

		if entries != ['']:
			for each in entries:
				articles[-1].add_entry(each)

def representArticles():
	sentence = ''
	for each in articles:
		sentence += each.ean + "$"
		sentence += each.name + '$'
		unsent = ''
		for x in each.standart_date:
			unsent += x + '/'

		unsent = unsent[:-1]

		sentence += unsent + "$"

		unsent = ''
		for x in each.exp_d:
			unsent += x + '/'

		unsent = unsent[:-1]

		sentence += unsent + "$"

		unsent = ''
		for x in each.barcode:
			unsent += x + '/'

		unsent = unsent[:-1]

		sentence += unsent

		sentence += '%'

	print(sentence)

representArticles()
