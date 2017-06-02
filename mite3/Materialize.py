from mite3.Query import Query
from mite3.Map import Map
from mite3.ElementBuilder import ElementBuilder


class Materialize():
	"""
		Will change this.
		I only created this for testing purposes.
	"""

	def __init__(self, mite):
		self.mite = mite

	def toast(self, message, timeout=1000):
		self.mite.xj('Materialize.toast(`{}`, {})'.format(message, timeout))

	card = '<div class="card"></div>'
	badge = '<span class="badge"></span>'
	chip = '<div class="chip"></div>' 