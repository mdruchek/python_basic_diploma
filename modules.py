from configparser import ConfigParser
from typing import List
import json
import requests


def get_config_from_file(path: str, section: str, setting: str):
    """
    Функция чтения параметров из конфигурационного файла

    :param path: имя файла
    :type path: str

    :param section: секция в конфигурационном файле
    :type section: str

    :param setting: настройка в конфигурационном файле
    :type setting: str

    :return setting_in_file: настройка в файле .ini
    :rtype setting_in_file: str
    """

    config: ConfigParser = ConfigParser()
    config.read(path)
    setting_in_file: str = config.get(section, setting, fallback=False)
    if not setting_in_file:
        setting_in_file = input('В файле {path} отсутствует ключ {setting},\n'
                                'введите его для записи: '.format(path=path[2:],
                                                                  setting=setting))

        if not config.has_section(section):
            config.add_section(section)
        config.set(section, setting, setting_in_file)
        with open(path, 'w') as file_config:
            config.write(file_config)
    return setting_in_file


class UserSurvey:
    """
    Класс опрос пользователя
    """
    __questions = ('В каком городе ищем?',
                   'В каком диапазоне цен искать?',
                   'Какое расстояние от центра Вас устроит?',
                   'Сколько отелей вывести?',
                   'Загрузить фотографи?',
                   'Сколько фотографий загрузить?')

    __survey_list = {'/lowprice': [0, 3, 4],
                     '/highprice': [0, 3, 4],
                     '/bestdeal': [0, 1, 2, 3, 4]}

    __answers_key = ('city', 'price', 'distance', 'number_hotels', 'uploading_photos', 'number_photos')

    def __init__(self):
        self.__command: str = ''
        self.__command_number = -1
        self.__answers = dict()

    @property
    def command(self):
        return self.__command

    @property
    def command_number(self):
        return self.__command_number

    @property
    def city(self):
        return self.__answers['city']

    @property
    def price(self):
        return self.__answers['price']

    @property
    def distance(self):
        return self.__answers['distance']

    @property
    def number_hotels(self):
        return self.__answers['number_hotels']

    @property
    def uploading_photos(self):
        return self.__answers['uploading_photos']

    @property
    def number_photos(self):
        return self.__answers['number_photos']

    @command.setter
    def command(self, command):
        self.reset_answers()
        self.__command = command

    def get_question(self):
        self.__command_number += 1
        if self.__command_number == len(UserSurvey.__survey_list[self.__command]):
            self.__command_number = -1
            return False
        question = UserSurvey.__questions[UserSurvey.__survey_list[self.__command][self.__command_number]]
        return question

    def set_answer(self, answer):
        self.__answers[self.__answers_key[UserSurvey.__survey_list[self.__command][self.__command_number]]] = answer

    def reset_answers(self):
        self.__answers = dict()


class Requests:
    __x_rapid_api_host = get_config_from_file(path='./config.ini', section='account', setting='x-rapidapi-key')

    @classmethod
    def get_meta_data(cls, city):
        url = "https://hotels4.p.rapidapi.com/v2/get-meta-data"

        headers = {
            "X-RapidAPI-Key": Requests.__x_rapid_api_host,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)
        location_dict = Requests.get_location_search(city=city)
        meta_data_dict = json.loads(response.text)[location_dict["hierarchyInfo"]["country"]["isoCode2"]]

        with open('meta_data.json', 'w') as file:
            json.dump(meta_data_dict, file, indent=4)

        return meta_data_dict, location_dict

    @classmethod
    def get_location_search(cls, city):

        url = "https://hotels4.p.rapidapi.com/locations/v3/search"

        querystring = {"q": city}

        headers = {
            "X-RapidAPI-Key": Requests.__x_rapid_api_host,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response = requests.request("GET",
                                    url,
                                    headers=headers,
                                    params=querystring)

        locations_dict = json.loads(response.text)

        for location in locations_dict["sr"]:
            if location['type'] == 'CITY':

                with open('location_search_city_only.json', 'w') as file:
                    json.dump(location, file, indent=4)

                return location

    @classmethod
    def properties_list(cls, city, check_in_date, check_out_date, result_size, sort):
        meta_data_dict, location_dict = Requests.get_meta_data(city=city)
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": meta_data_dict['siteId'],
            "destination": {"regionId": location_dict['gaiaId']},
            "checkInDate": {
                "day": 20,
                "month": 12,
                "year": 2022
            },
            "checkOutDate": {
                "day": 21,
                "month": 12,
                "year": 2022
            },
            "rooms": [
                {
                    "adults": 1,
                    "children": []
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": int(result_size),
            "sort": sort,
            "filters": {}
        }

        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": Requests.__x_rapid_api_host,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("POST", url, json=payload, headers=headers)

        properties_list = json.loads(response.text)['data']['propertySearch']['properties']

        with open('properties_list.json', 'w') as file:
            json.dump(properties_list, file, indent=4)

        return properties_list