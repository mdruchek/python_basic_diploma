from configparser import ConfigParser
from typing import List, Dict
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
    def question_number(self) -> int:
        """
        Геттер для вывода номера вопроса

        :return __question_number: номер текущего вопроса
        :rtype __question_number: int
        """
        return self.__question_number

    @property
    def city(self) -> str:
        """
        Геттер для вывода города

        :return __ansvers['city']: город поиска
        :rtype __answers['city']: str
        """
        return self.__answers['city']

    @property
    def price(self) -> List:
        """
        Геттер для вывода диапазона цен

        :return __answer['price']: диапазон цен
        :rtype __answer['price]: List[min, max]
        """
        return self.__answers['price']

    @property
    def distance(self) -> List:
        """
        Геттер для вывода диапазона расстояния от центра

        :return __answers['distance']: диапазон расстояния
        :rtype __answers['distance']: List[min, max]
        """
        return self.__answers['distance']

    @property
    def number_hotels(self) -> str:
        """
        Геттер для возврата количества выводимых ботом отелей

        :return __answers['number_hotels']: количество отелей
        :rtype __answers['number_hotels']: str
        """

        return self.__answers['number_hotels']

    @property
    def uploading_photos(self):
        """
        Геттер для вывода необходимости загрузки фото
        """
        return self.__answers['uploading_photos']

    @property
    def number_photos(self) -> str:
        """
        Геттер для вывода количества загружаемых фото
        """
        return self.__answers['number_photos']

    @command.setter
    def command(self, command: str):
        """
        Сеттер для записи команды боту

        :param command (str): команда
        """
        self.reset_answers()
        self.__command = command

    def get_question(self):
        """
        Метод для выдачи вопросов по одному, по порядку в __questions, один за обращение к методу

        :return question: вопрос
        :rtype question: str
        """
        self.__question_number += 1
        if self.__question_number == len(UserSurvey.__survey_list[self.__command]):
            self.__question_number = -1
            return False
        question = UserSurvey.__questions[UserSurvey.__survey_list[self.__command][self.__question_number]]
        return question

    def set_answer(self, answer: str) -> None:
        """
        Метод записи ответов в __answers
        :param answer (str): ответ
        """

        self.__answers[self.__answers_key[UserSurvey.__survey_list[self.__command][self.__question_number]]] = answer

    def reset_answers(self) -> None:
        """
        Метод для обнуления словаря с вопросами
        """
        self.__answers = dict()


class Requests:
    """
    Класс, реализующий необходимые запросы к API

    Args:
        city (str): город для поиска
        check_in_date (?): дата заезда
        check_out_date (?): дата выезда
        result_size (str): количество результатов поиска
        sort (str): тип сортировки результатов запроса
    """

    def __init__(self, city: str, check_in_date: dict, check_out_date: dict, result_size: str, sort: str):
        self._x_rapid_api_host = get_config_from_file(path='./config.ini', section='account', setting='x-rapidapi-key')
        self.__city: str = city
        self.__check_in_date = check_in_date
        self.__check_out_date = check_out_date
        self.__result_size: int = int(result_size)
        self.__sort = sort

        self.__location_dict: Dict = dict()
        self.__meta_data_dict: Dict = dict()
        self.__properties_list: List = []

    @property
    def properties_list(self) -> List:
        """
        Геттер выполняет все запросы и возвращает список отелей

        :return __properties_list:
        """

        self.__get_location_search()
        self.__get_meta_data()
        self.__get_properties_list()
        self.__add_properties_details_dict()

        with open('meta_data.json', 'w') as file:
            json.dump(self.__meta_data_dict, file, indent=4)

        with open('properties_list.json', 'w') as file:
            json.dump(self.__properties_list, file, indent=4)

        return self.__properties_list

    def __get_meta_data(self) -> None:
        """
        Метод выполняет запрос v2/get-meta-data
        Данные страны
        """

        url: str = "https://hotels4.p.rapidapi.com/v2/get-meta-data"

        headers: Dict = {
            "X-RapidAPI-Key": self._x_rapid_api_host,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response: requests = requests.request("GET", url, headers=headers)
        self.__meta_data_dict: Dict = json.loads(response.text)[self.__location_dict["hierarchyInfo"]["country"]["isoCode2"]]

    def __get_location_search(self) -> None:
        """
        Метод выполняет запрос locations/v3/search
        Данные города
        """

        url: str = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring: Dict = {"q": self.__city}

        headers: Dict = {
            "X-RapidAPI-Key": self._x_rapid_api_host,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response: requests = requests.request("GET",
                                              url,
                                              headers=headers,
                                              params=querystring)

        locations_dict: Dict = json.loads(response.text)
        for location in locations_dict["sr"]:
            if location['type'] == 'CITY':

                with open('location_search_city_only.json', 'w') as file:
                    json.dump(location, file, indent=4)

                self.__location_dict = location
                break

    def __get_properties_list(self) -> None:
        """
        Метод выполняет запрос properties/v2/list
        Поиск отелей
        """

        url: str = "https://hotels4.p.rapidapi.com/properties/v2/list"
        payload: Dict = {
            "currency": "USD",
            "eapid": self.__meta_data_dict["EAPID"],
            "locale": "en_US",
            "siteId": self.__meta_data_dict['siteId'],
            "destination": {"regionId": self.__location_dict['gaiaId']},
            "checkInDate": {
                "day": self.__check_in_date['day'],
                "month": self.__check_in_date['month'],
                "year": self.__check_in_date['year']
            },
            "checkOutDate": {
                "day": self.__check_out_date['day'],
                "month": self.__check_out_date['month'],
                "year": self.__check_out_date['year']
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

        headers: Dict = {
            "content-type": "application/json",
            "X-RapidAPI-Key": self._x_rapid_api_host,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response: requests = requests.request("POST", url, json=payload, headers=headers)
        self.__properties_list = json.loads(response.text)['data']['propertySearch']['properties']

    def __add_properties_details_dict(self) -> None:
        """
        Метод выполняет запрос properties/v2/list
        Поиск подробностей по отелям.
        Добавляет детали к __properties_list.
        """

        for index_hotel, hotel_properties in enumerate(self.__properties_list):
            url: str = "https://hotels4.p.rapidapi.com/properties/v2/detail"

            payload: Dict = {
                "currency": "USD",
                "eapid": 1,
                "locale": "en_US",
                "siteId": self.__meta_data_dict['siteId'],
                "propertyId": hotel_properties['id']
            }

            headers: Dict = {
                "content-type": "application/json",
                "X-RapidAPI-Key": self._x_rapid_api_host,
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            }

            response: requests = requests.request("POST", url, json=payload, headers=headers)
            self.__properties_list[index_hotel]['detail'] = json.loads(response.text)


