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
    Класс опрос пользователя:
    Выдаёт по одному вопросу и записывает ответы в словарь

    Attributes:
        __questions (tuple): вопросы
        __survey_list (dict): содержит индексы вопросов (в __question), в соответствии с командой бота
        __answer_key (tuple): содержит ключи для записи вопросов в __answers (порядок соответствует порядку вопросов)
    """
    __questions: tuple = ('В каком городе ищем?',
                          'В каком диапазоне цен искать?',
                          'Какое расстояние от центра Вас устроит?',
                          'Сколько отелей вывести?',
                          'Загрузить фотографи?',
                          'Сколько фотографий загрузить?')

    __survey_list: dict = {'/lowprice': [0, 3, 4],
                           '/highprice': [0, 3, 4],
                           '/bestdeal': [0, 1, 2, 3, 4]}

    __answers_key: tuple = ('city', 'price', 'distance', 'number_hotels', 'uploading_photos', 'number_photos')

    def __init__(self):
        self.__command: str = ''
        self.__question_number: int = -1
        self.__answers: dict = dict()

    @property
    def command(self) -> str:
        """
        Геттер для вывода команды

        :return __command: команда бота
        :rtype __command: str
        """
        return self.__command

    @property
    def question_number(self):
        """
        Геттер для вывода номера вопроса

        :return :
        """
        return self.__question_number

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
        self.__question_number += 1
        if self.__question_number == len(UserSurvey.__survey_list[self.__command]):
            self.__question_number = -1
            return False
        question = UserSurvey.__questions[UserSurvey.__survey_list[self.__command][self.__question_number]]
        return question

    def set_answer(self, answer):
        self.__answers[self.__answers_key[UserSurvey.__survey_list[self.__command][self.__question_number]]] = answer

    def reset_answers(self):
        self.__answers = dict()


class Requests:

    def __init__(self, command, city, check_in_date, check_out_date, result_size):
        self._x_rapid_api_host = get_config_from_file(path='./config.ini', section='account', setting='x-rapidapi-key')

        if command == 'lowprice' or 'bestdeal':
            self.__sort = 'PRICE_LOW_TO_HIGH'
        if command == 'highprice':
            self.__sort = 'PRICE_HIGH_TO_LOW'
        self.__city = city
        self.__result_size = int(result_size)
        self.__location_dict = dict()
        self.__meta_data_dict = dict()
        self.__properties_list = []
        self.__properties_detail_dict = dict()

    @property
    def properties_list(self):
        self.__get_location_search()
        self.__get_meta_data()
        self.__get_properties_list()
        self.__add_properties_details_dict()

        with open('meta_data.json', 'w') as file:
            json.dump(self.__meta_data_dict, file, indent=4)

        with open('properties_list.json', 'a') as file:
            for proper in self.__properties_list:
                json.dump(proper, file, indent=4)

        return self.__properties_list

    def __get_meta_data(self):
        url = "https://hotels4.p.rapidapi.com/v2/get-meta-data"

        headers = {
            "X-RapidAPI-Key": self._x_rapid_api_host,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers)
        self.__meta_data_dict = json.loads(response.text)[self.__location_dict["hierarchyInfo"]["country"]["isoCode2"]]

    def __get_location_search(self):
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": self.__city}
        headers = {
            "X-RapidAPI-Key": self._x_rapid_api_host,
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

                self.__location_dict = location
                break

    def __get_properties_list(self):
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": self.__meta_data_dict['siteId'],
            "destination": {"regionId": self.__location_dict['gaiaId']},
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
            "resultsSize": self.__result_size,
            "sort": self.__sort,
            "filters": {}
        }

        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": self._x_rapid_api_host,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        self.__properties_list = json.loads(response.text)['data']['propertySearch']['properties']

    def __add_properties_details_dict(self):
        for hotel_properties in self.__properties_list:
            url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
            payload = {
                "currency": "USD",
                "eapid": 1,
                "locale": "en_US",
                "siteId": self.__meta_data_dict['siteId'],
                "propertyId": hotel_properties['id']
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": self._x_rapid_api_host,
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            }

            response = requests.request("POST", url, json=payload, headers=headers)
            hotel_details = json.loads(response.text)
            hotel_properties['details'] = hotel_details
