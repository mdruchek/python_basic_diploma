import modules


class Lowprice:
	"""
	Класс содержит методы для функции lowprice телеграмм бота
	"""

	__found_hotels_list = []

	@property
	def found_hotels_list(self):
		return Lowprice.__found_hotels_list

	@classmethod
	def get_properties_list(cls, city, result_size):
		Lowprice.__found_hotels = modules.Requests.properties_list(city=city,
																   check_in_date=None,
																   check_out_date=None,
																   result_size=result_size,
																   sort='PRICE_LOW_TO_HIGH')