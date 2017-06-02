from mite3 import Mite, UI, Materialize
from mite3 import Query as Q
from mite3 import ElementBuilder as E


class app(Mite):


	@Mite.on.preinit()
	def preload(self):
		"""
		This is not a coroutine. I.E. if there's blocking code here
			the application will hang.

		Allows you to modify the DOM before the events gets binded.
			i.e.: You can build the entire UI in python.
		"""
		# create a MiteUI instance for further DOM access capability
		self.miteui = UI(self)

		# You can set this as E("div", id="app-container") as well.
		ui = E("div").id("app-container")
		ui.style("display: flex; flex-direction: column; justify-content: center; width: 30%")

		ui.inner( E("span").id("hoverme").text("Click the button below or hover over me!")
				+ E("button").id("btn-action").text("Click"))
		
		
		# Create a query to the UI appending the body element we just made to
		# the document.
		query = Q("body").html(ui)

		#execute the query using this app as the argument.
		query.execute(self)


	# This gets executed when Mite is finished initalizing the application.
	@Mite.on.ready()
	async def onready(self):
		print("Application is Ready!")
		pass


	# Assign this function on the 'onmouseover' event on the element with the 'hoverme' id.
	@Mite.on.event("hoverme", "onmouseover")
	async def hover_text(self):
		Q("#hoverme").text("You hovered over me!").execute(self)


	# Assign this function to the 'btn-action' element on 
	@Mite.on.event("btn-action")
	async def change_text(self):

		# You can nest queries by adding them.
		query =  Q("#hoverme").text("You clicked the button")
		query += Q("#app-container").append(
					E("input").id("name").placeholder("Enter name here") +
					E("button").id("btn-greet").onclick(Q.event_compile(self.greet)).inner("Click me!")
			)

		query.execute(self)


	# This doesn't assign the function to anything, but it can be called
	# by anyone in the UI
	@Mite.on.event()
	async def greet(self):
		print("greet event")
		# Retrieves the value of the name textbox
		name = self.miteui.element("name").prop("value")
		print(name)
		Q("#hoverme").text("Hello there {}!".format(name)).execute(self)


if __name__ == "__main__":
	# Run the app
	app().run(url="views\\app.html", title="My App")