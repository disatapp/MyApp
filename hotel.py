import webapp2
from google.appengine.ext import ndb
import db_models
import json
# http://eecs.oregonstate.edu/ecampus-video/player/player.php?id=99
class Hotel(webapp2.RequestHandler):
	def post(self):
		# Creates a Hotel entity

		# POST Body Variables:
		# name - Required. Hotel name
		# customers[] - Array of customer ids
		# rooms[] - Array of Hotel rooms
		
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable"
			return

		new_hotel = db_models.Hotel()
		name = self.request.get('name', default_value=None)
		customers = self.request.get_all('customers[]', default_value=None)
		rooms = self.request.get_all('rooms[]', default_value=None)
		if name:
			new_hotel.name = name
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"

		if customers:
			for customer in customers:
				new_hotel.customers.append(ndb.Key(db_models.Customer, int(customer)))
		if rooms:
			new_hotel.rooms = rooms
		for room in new_hotel.rooms:
			print room
		key = new_hotel.put()
		out = new_hotel.to_dict()
		self.response.write(json.dumps(out))
		return

class HotelCustomers(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status_message = 406
			self.response.status_message = "Not Acceptable"
		hotel = None
		customer = None
		if 'cid' in kwargs:
			hotel = ndb.Key(db_models.Hotel, int(kwargs['hid'])).get()
			if not hotel:
				self.response.status = 404
				self.response.status_message = "Hotel Not Found"
				return
		if 'mid' in kwargs:
			customer = ndb.Key(db_models.Customer, int(kwargs['cid']))
			if not customer: 
				# Does this need to me Hotel??
				self.response.status = 404
				self.response.status_message = "Customer Not Found"
				return
			if customer not in hotel.customers:
				hotel.customers.append(customer)
				hotel.put()
		self.response.write(json.dumps(hotel.to_dict()))
		return