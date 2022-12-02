import json
import requests
import modules


class Lowprice:
	"""
	Класс содержит методы для функции lowprice телеграмм бота
	"""
	@classmethod
	def get_location_city(cls, city):
		url = "https://hotels4.p.rapidapi.com/locations/v3/search"

		querystring = {"q": city}

		x_rapid_apy_key = modules.get_config_from_file(path='./config.ini', section='account', setting='X-RapidAPI-Key')

		headers = {
			"X-RapidAPI-Key": x_rapid_apy_key,
			"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
		}

		response = requests.request("GET", url, headers=headers, params=querystring)
		return response

