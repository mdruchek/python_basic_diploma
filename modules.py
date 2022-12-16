from configparser import ConfigParser
from typing import List, Dict, Union, Optional
import json
import requests


MONTHS = ('январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
          'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь')


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
    """

    def __init__(self):
        self.__command: str = ''
        # self.__question_number: int = -1
        self.__answers: dict = dict()

    def __str__(self):
        return str(self.__answers)

    @property
    def command(self) -> str:
        """
        Геттер для вывода команды

        :return __command: команда бота
        :rtype __command: str
        """
        return self.__command

    @property
    def city(self) -> str:
        """
        Геттер для вывода города

        :return __ansvers['city']: город поиска
        :rtype __answers['city']: str
        """
        return self.__answers['city']

    @property
    def check_in_date_year(self) -> int:
        """
        Геттер для вывода даты заезда (год)

        :return check_in_date_year: год даты заезда
        :rtype check_in_date_year: Union[int, bool]
        """

        return self.__answers.get('check_in_date_year', False)

    @property
    def check_in_date_month(self) -> int:
        """
        Геттер для вывода даты заезда (месяц)

        :return check_in_date_month: месяц даты заезда
        :rtype check_in_date_month: Union[int, bool]
        """

        return self.__answers['check_in_date_month']

    @property
    def check_in_date_day(self) -> int:
        """
        Геттер для вывода даты заезда (день)

        :return check_in_date_day: день даты заезда
        :rtype check_in_date_day: Union[int, bool]
        """

        return self.__answers['check_in_date_day']

    @property
    def check_out_date_year(self) -> int:
        """
        Геттер для вывода даты выезда (год)

        :return check_out_date_year: год дата выезда
        :rtype check_out_date_year: Union[int, bool]
        """
        return self.__answers['check_out_date_year']

    @property
    def check_out_date_month(self) -> int:
        """
        Геттер для вывода даты выезда (месяц)

        :return check_out_date_month: месяц даты выезда
        :rtype check_out_date_month: Union[int, bool]
        """
        return self.__answers['check_out_date_month']

    @property
    def check_out_date_day(self) -> int:
        """
        Геттер для вывода даты выезда (день)

        :return check_out_date_day: день даты выезда
        :rtype check_out_date_day: Union[int, bool]
        """
        return self.__answers['check_out_date_day']

    @property
    def price(self) -> List[int]:
        """
        Геттер для вывода диапазона цен

        :return __answer['price']: диапазон цен
        :rtype __answer['price]: List[min, max]
        """
        return self.__answers['price']

    @property
    def distance(self) -> List[int]:
        """
        Геттер для вывода диапазона расстояния от центра

        :return __answers['distance']: диапазон расстояния
        :rtype __answers['distance']: List[min, max]
        """
        return self.__answers['distance']

    @property
    def number_hotels(self) -> int:
        """
        Геттер для возврата количества выводимых ботом отелей

        :return __answers['number_hotels']: количество отелей
        :rtype __answers['number_hotels']: int
        """

        return self.__answers['number_hotels']

    @property
    def uploading_photos(self) -> str:
        """
        Геттер для вывода необходимости загрузки фото
        """
        return self.__answers['uploading_photos']

    @property
    def number_photos(self) -> int:
        """
        Геттер для вывода количества загружаемых фото
        """
        return self.__answers['number_photos']

    @command.setter
    def command(self, command: str) -> None:
        """
        Сеттер для записи команды боту

        :param command (str): команда
        """
        self.reset_answers()
        self.__command = command

    @city.setter
    def city(self, city) -> None:
        """
        Сеттер для записи города
        :param city (str): город

        """
        self.__answers['city'] = city

    @check_in_date_year.setter
    def check_in_date_year(self, check_in_date_year: int) -> None:
        """
        Сеттер для записи года даты заезда
        :param check_in_date_year (int): год даты заезда
        """

        self.__answers['check_in_date_year'] = check_in_date_year

    @check_in_date_month.setter
    def check_in_date_month(self, check_in_date_month: int) -> None:
        """
        Сеттер для записи месяца даты заезда
        :param check_in_date_month (int): месяц даты заезда
        """

        self.__answers['check_in_date_month'] = check_in_date_month

    @check_in_date_day.setter
    def check_in_date_day(self, check_in_date_day: int) -> None:
        """
        Сеттер для записи дня даты заезда
        :param check_in_date_day (int): день даты заезда
        """
        self.__answers['check_in_date_day'] = check_in_date_day

    @check_out_date_year.setter
    def check_out_date_year(self, check_out_date_year: int) -> None:
        """
        Сеттер для записи года даты выезда
        :param check_out_date_year (int): год даты выезда
        """

        self.__answers['check_out_date_year'] = check_out_date_year

    @check_out_date_month.setter
    def check_out_date_month(self, check_out_date_month: int) -> None:
        """
        Сеттер для записи месяца даты выезда
        :param check_out_date_month (int): месяц даты выезда
        """

        self.__answers['check_out_date_month'] = check_out_date_month

    @check_out_date_day.setter
    def check_out_date_day(self, check_out_date_day: int) -> None:
        """
        Сеттер для записи дня даты выезда
        :param check_out_date_day (int):
        """

        self.__answers['check_out_date_day'] = check_out_date_day

    @price.setter
    def price(self, price: List[int]) -> None:
        """
        Сеттер для записи диапазона цен
        :param price List(int): диапазон цены
        """

        self.__answers['price'] = price

    @distance.setter
    def distance(self, distance: List[int]) -> None:
        """
        Сеттер для записи диапазона расстояния
        :param distance List(int): диапазон расстояния
        """

        self.__answers['distance'] = distance

    @number_hotels.setter
    def number_hotels(self, number_hotels: int) -> None:
        """
        Сеттер для записи количества отелей
        :param number_hotels (int): количество отелей
        """

        self.__answers['number_hotels'] = number_hotels

    @uploading_photos.setter
    def uploading_photos(self, uploading_photos: str) -> None:
        """
        Сеттер для записи необходимости загрузки фото
        :param uploading_photos (str): загрузка фото (да, нет)
        """

        self.__answers['uploading_photos'] = uploading_photos

    @number_photos.setter
    def number_photos(self, number_photos: int) -> None:
        """
        Сеттер для записи количества загружаемых фото
        :param number_photos (str): количество фото
        """

        self.__answers['number_photos'] = number_photos

    def reset_answers(self) -> None:
        """
        Метод для обнуления словаря с вопросами
        """
        self.__answers = dict()


class Requests:
    """
    Класс, реализующий необходимые запросы к API

    Args:
        arguments_request (Dict[Optional[int, str, List[int]]]): аргументы запроса
    """

    def __init__(self, city, check_in_date_day, check_in_date_month, check_in_date_year,
                 check_out_date_day, check_out_date_month, check_out_date_year,
                 number_hotels, sort) -> None:
        self.__city = city
        self.__check_in_date_day = check_in_date_day
        self.__check_in_date_month = check_in_date_month
        self.__check_in_date_year = check_in_date_year
        self.__check_out_date_day = check_out_date_day
        self.__check_out_date_month = check_out_date_month
        self.__check_out_date_year = check_out_date_year
        self.__number_hotels = number_hotels

        self.__sort = sort
        self.__x_rapid_api_host = get_config_from_file(path='./config.ini', section='account', setting='x-rapidapi-key')
        self.__currency = 'USD'
        self.__locale = 'en_US'
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
            "X-RapidAPI-Key": self.__x_rapid_api_host,
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
            "X-RapidAPI-Key": self.__x_rapid_api_host,
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
            "currency": self.__currency,
            "eapid": self.__meta_data_dict["EAPID"],
            "locale": self.__locale,
            "siteId": self.__meta_data_dict['siteId'],
            "destination": {"regionId": self.__location_dict['gaiaId']},
            "checkInDate": {
                "day": self.__check_in_date_day,
                "month": self.__check_in_date_month,
                "year": self.__check_in_date_year
            },
            "checkOutDate": {
                "day": self.__check_out_date_day,
                "month": self.__check_out_date_month,
                "year": self.__check_out_date_year
            },
            "rooms": [
                {
                    "adults": 1,
                    "children": []
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": self.__number_hotels,
            "sort": self.__sort,
            "filters": {}
        }

        headers: Dict = {
            "content-type": "application/json",
            "X-RapidAPI-Key": self.__x_rapid_api_host,
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
                "currency": self.__currency,
                "eapid": self.__meta_data_dict["EAPID"],
                "locale": self.__locale,
                "siteId": self.__meta_data_dict['siteId'],
                "propertyId": hotel_properties['id']
            }

            headers: Dict = {
                "content-type": "application/json",
                "X-RapidAPI-Key": self.__x_rapid_api_host,
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            }

            response: requests = requests.request("POST", url, json=payload, headers=headers)
            self.__properties_list[index_hotel]['detail'] = json.loads(response.text)
