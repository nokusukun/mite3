from mite3 import Mite, UI, Materialize
from mite3 import Query as q
from mite3 import ElementBuilder
import time
import json
import glob
import asyncio

class app(Mite):

	bookdetail = {
		"title"		:"Boku no Hero Academia 11",
		"pages"		:213,
		"format"	:"jpg",
	}

	bookmeta = {}

	languageMap = {}

	session = {
		"currentpage"	:1,
		"zoom"			:80,
	}




	@Mite.on_ready()
	async def on_ready(self):
		self.miteui = UI(self)
		self.textbox = self.miteui.element("bitch")
		self.header = self.miteui.element("header")
		self.textbox2 = self.miteui.element("bitchass")
		self.page = self.miteui.element("page-view")
		self.viewhole = self.miteui.element("viewport")
		self.mapbox = self.miteui.element("map-container")

		print("Binding Keyboard Shortcuts")
		query = q("~document").bind("keyup", "left", 'function(){{pagePrev();}}')
		query += q("~document").bind("keyup", "right", 'function(){{pageNext();}}')
		query.execute(self)
		print("App is now fully loaded")
		q(self.header).text("App is ready").execute(self)
		self.renderPageSlider("0", self.bookdetail["pages"])


	# Binds this function to these buttons on the 'onmouseover' event
	@Mite.event(["btn-nav-libr", "btn-nav-open", "btn-nav-sett"], "onmouseover")
	async def dummy(self):
		Materialize(self).toast("Function not implemented yet!", 1000)


	# Binds this function to this button on the 'onclick' event by default
	@Mite.event("btn-next")
	async def pageNext(self):
		if self.session['currentpage'] > self.bookdetail["pages"]:
			self.xj(Materialize.toast("You are on the last page.", 1000))
			return

		# self.mite.xj(pquery.fadeOut(self.page.id, 100))
		# time.sleep(0.1)

		self.session['currentpage'] += 1
		self.page.src = "data/{0}.{1}".format(str(self.session['currentpage']).zfill(3), self.bookdetail["format"])
		self.header.innerHTML = "{0}".format(self.bookdetail["title"])

		# Old functions pre miteJquery
		# self.mite.xj(pquery.fadeIn(self.page.id, 100))
		# self.mite.xj("$('#view-hole').focus();")


		chip = ElementBuilder("span").c("chip").text('Page {0}'.format(self.session['currentpage']))
		self.renderPageSlider(0, self.bookdetail["pages"])
		# chip = q(Materialize.chip).text('Page {0}'.format(self.session['currentpage']))
		query = q(self.miteui.element("page-pos-container")).append(chip) + \
				q(self.page).fadeIn(100) + \
				q(self.miteui.element("page-pos")).val(self.session['currentpage']) + \
				q("#view-hole").animate("{scrollTop: 0}", 200).focus()
		query.execute(self)




	@Mite.event("btn-prev")
	async def pagePrev(self):
		if self.session['currentpage'] < 2:
			self.xj(Materialize.toast("You are on the first page.", 1000))
			return

		q("#{}".format(self.page.id)).fadeOut(300).execute(self)

		self.session['currentpage'] -= 1
		self.page.src = "data/{0}.{1}".format(str(self.session['currentpage']).zfill(3), self.bookdetail["format"])
		self.header.innerHTML = "{0}".format(self.bookdetail["title"])
		q(self.header).append(
			q(Materialize.chip).addClass('new').text('Page {0}'.format(self.session['currentpage']))).execute(self)

		q(self.page).fadeIn(100).execute(self)
		q(self.miteui.element("view-hole")).focus().execute(self)


	@Mite.event("btn-zoom-in")
	async def zoomIn(self):
		self.session["zoom"] += 5;
		self.viewhole.style = "width: {0}%".format(self.session["zoom"])

	@Mite.event("btn-zoom-out")
	async def zoomOut(self):
		self.session["zoom"] -= 5;
		self.viewhole.style = "width: {0}%".format(self.session["zoom"])

	@Mite.event()
	async def jumpToPage(self, value):
		self.session['currentpage'] = int(value) - 1

	@Mite.event()
	async def nextBottom(self, value):
		print(value)
		pass

		
	def renderPageSlider(self, min, max):
		inp = ElementBuilder("input").id("page-pos").type("range").min(min).max(max).value(0).onchange("jumpToPage(this.value);pageNext()")
			
		self.miteui.element("page-pos-container").innerHTML = inp.html




	# DEMO STUFF
	def loadDemo():
		path = "views\\bnha\\"
		
		try:
			with open(path+"meta.txt") as f:
				self.bookmeta = json.loads(f.read())
		except:
			assert False, "Invalid Metadata"

		self.parseLangMaps(path)
		
		self.header.innerHTML = self.bookmeta["title"]
		self.page.src = "data/008.jpg"
		self.loadMap(self.languageMap["English"]["008.jpg"])



	def loadMap(mapData):
		script = "$('#map-container').prop('innerHTML',`{value}`);".format(value=mapData)
		self.xj(script);

		script = "$('#page-view').prop('usemap', '#map');"
		script += "$('img[usemap]').rwdImageMaps();"
		script += "$('area').addClass('tooltipped');"
		script += "$('area').attr('data-position', 'top');"
		script += "$('.tooltipped').tooltip({delay: 10});"
		script += "$('area').attr('onmouseover', 'moveTool(event)');"
		self.xj(script);

	def parseLangMaps(path):
		for name in glob.glob(path+"*.lang.txt"):
			with open(name) as f:
				map = [x.rstrip() for x in f.readlines()]
				data = {}
				line = 0
				language = ""

				while line < len(map) - 1:
					if map[line].startswith("[lang]"):
						language = map[line].replace("[lang]", "")
						print("Language Map: {0}".format(language))
						line += 1

					if map[line].startswith("[page]"):
						page = map[line].replace("[page]", "")
						print("\tPage: {0}".format(page))
						pagemap = []
						line += 1
						try:
							while not map[line].startswith("[page]"):
								print("\t\tMap: {0}".format(map[line]))
								pagemap.append(map[line].replace("data-text", "data-tooltip"))
								line += 1
						except:
							pass

						data[page] = "".join(pagemap)

			self.languageMap[language] = data
							


x= app().run(url="b:\\git-projects\\mitemite\\views\\main.html", title="Mite Manga Viewer Demo")
print("a")

