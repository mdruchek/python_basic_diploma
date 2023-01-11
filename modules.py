from configparser import ConfigParser
from typing import List, Dict, Union, Optional
import json
import requests
import datetime
import re


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
            print('Ключ принят.')
    return setting_in_file


class UserSurvey:
    """
    Класс опрос пользователя
    """

    def __init__(self):
        self.__command: str = ''
        self.__answers: dict = dict()
        self.__answers['price'] = [None, None]
        self.__answers['distance'] = [None, None]

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
        return self.__answers.get('city', False)

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

        return self.__answers.get('check_in_date_month', False)

    @property
    def check_in_date_day(self) -> int:
        """
        Геттер для вывода даты заезда (день)

        :return check_in_date_day: день даты заезда
        :rtype check_in_date_day: Union[int, bool]
        """

        return self.__answers.get('check_in_date_day', False)

    @property
    def check_out_date_year(self) -> int:
        """
        Геттер для вывода даты выезда (год)

        :return check_out_date_year: год дата выезда
        :rtype check_out_date_year: Union[int, bool]
        """
        return self.__answers.get('check_out_date_year', False)

    @property
    def check_out_date_month(self) -> int:
        """
        Геттер для вывода даты выезда (месяц)

        :return check_out_date_month: месяц даты выезда
        :rtype check_out_date_month: Union[int, bool]
        """
        return self.__answers.get('check_out_date_month', False)

    @property
    def check_out_date_day(self) -> int:
        """
        Геттер для вывода даты выезда (день)

        :return check_out_date_day: день даты выезда
        :rtype check_out_date_day: Union[int, bool]
        """
        return self.__answers.get('check_out_date_day', False)

    @property
    def price(self) -> List[Optional[int]]:
        """
        Геттер для вывода диапазона цен

        :return __answer['price']: диапазон цен
        :rtype __answer['price]: List[min, max]
        """
        return self.__answers.get('price', False)

    @property
    def distance(self) -> Union[List[Optional[int]], bool]:
        """
        Геттер для вывода диапазона расстояния от центра

        :return __answers['distance']: диапазон расстояния
        :rtype __answers['distance']: List[min, max]
        """
        return self.__answers.get('distance', False)

    @property
    def number_hotels(self) -> int:
        """
        Геттер для возврата количества выводимых ботом отелей

        :return __answers['number_hotels']: количество отелей
        :rtype __answers['number_hotels']: int
        """

        return self.__answers.get('number_hotels', False)

    @property
    def uploading_photos(self) -> str:
        """
        Геттер для вывода необходимости загрузки фото
        """
        return self.__answers.get('uploading_photos', False)

    @property
    def number_photos(self) -> int:
        """
        Геттер для вывода количества загружаемых фото
        """
        return self.__answers.get('number_photos', False)

    @property
    def answers(self) -> Dict:
        """
        Геттер для возврата словаря с ответами пользователя
        """
        return self.__answers

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
        Метод для обнуления словаря с вопросами и команды
        """

        self.__answers = dict()
        self.__command: str = ''


class Requests:
    """
    Класс, реализующий необходимые запросы к API

    Args:
        parameters_request (Dict): параматры запроса, из опроса пользователя
        sort (str): сортировка
        price_max (int): максимальная цена
        price_min (int): минимальная цена
    """

    def __init__(self, parameters_request, sort, price_max, price_min) -> None:
        self.__parameters_request = parameters_request
        self.__price_max = price_max
        self.__price_min = price_min

        self.__sort = sort
        self.__x_rapid_api_host = get_config_from_file(path='./config.ini', section='account', setting='x-rapidapi-key')
        self.__currency = 'USD'
        self.__locale = 'en_US'
        self.__location_dict: Dict = dict()
        self.__meta_data_dict: Dict = dict()
        self.__properties_list: List = []

    @property
    def properties_list(self) -> Union[List[dict], int]:
        """
        Геттер выполняет все запросы и возвращает список отелей

        :return Union[__properties_list, response_status_code...]: список отелей, либо статус ответа сервера (если статус не 200)
        :rtype Union[List[dict], int]
        """

        response_status_code_location_search = self.__get_location_search()
        if response_status_code_location_search != 200:
            return response_status_code_location_search

        response_status_code_meta_data = self.__get_meta_data()
        if response_status_code_meta_data != 200:
            return response_status_code_meta_data

        response_status_code_properties_list = self.__get_properties_list()
        if response_status_code_properties_list != 200:
            return response_status_code_properties_list

        response_status_code_details = self.__add_properties_details_dict()
        if response_status_code_details != 200:
            return response_status_code_details

        return self.__properties_list

    def __get_meta_data(self) -> int:
        """
        Метод выполняет запрос v2/get-meta-data
        Данные страны
        :return response.status_code: статус ответа сервера (если статус 200);
                либо 1, если словарь self.__location_dict не соттветствует ожидаемому
        :rtype: int
        """

        url: str = "https://hotels4.p.rapidapi.com/v2/get-meta-data"

        headers: Dict = {
            "X-RapidAPI-Key": self.__x_rapid_api_host,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response: requests = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            if self.__location_dict.get('hierarchyInfo', False):
                if self.__location_dict['hierarchyInfo'].get('country', False):
                    if self.__location_dict['hierarchyInfo']['country'].get('isoCode2', False):
                        self.__meta_data_dict: Dict = json.loads(response.text)[self.__location_dict['hierarchyInfo']['country']['isoCode2']]
                        return 200
            return 1
        return response.status_code

    def __get_location_search(self) -> int:
        """
        Метод выполняет запрос locations/v3/search
        Данные города

        :return response.status_code: статус ответа сервера
        :rtype: int
        """

        url: str = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring: Dict = {"q": self.__parameters_request['city']}

        headers: Dict = {
            "X-RapidAPI-Key": self.__x_rapid_api_host,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response: requests = requests.request("GET",
                                              url,
                                              headers=headers,
                                              params=querystring)

        if response.status_code == 200:
            locations_dict: Dict = json.loads(response.text)
            for location in locations_dict["sr"]:
                if location['type'] == 'CITY':
                    self.__location_dict = location
                    break
        return response.status_code

    def __get_properties_list(self) -> int:
        """
        Метод выполняет запрос properties/v2/list
        Поиск отелей

        :return response.status_code: статус ответа сервера; либо 1, если ничего нет соответствующее фильтрам
        :rtype: int
        """

        url: str = "https://hotels4.p.rapidapi.com/properties/v2/list"
        payload: Dict = {
            "currency": self.__currency,
            "eapid": self.__meta_data_dict["EAPID"],
            "locale": self.__locale,
            "siteId": self.__meta_data_dict['siteId'],
            "destination": {"regionId": self.__location_dict['gaiaId']},
            "checkInDate": {
                "day": self.__parameters_request['check_in_date_day'],
                "month": self.__parameters_request['check_in_date_month'],
                "year": self.__parameters_request['check_in_date_year']
            },
            "checkOutDate": {
                "day": self.__parameters_request['check_out_date_day'],
                "month": self.__parameters_request['check_out_date_month'],
                "year": self.__parameters_request['check_out_date_year']
            },
            "rooms": [
                {
                    "adults": 1,
                    "children": []
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": self.__parameters_request['number_hotels'],
            "sort": self.__sort,
            "filters": {
                "price": {
                    "max": self.__price_max,
                    "min": self.__price_min
                }
            }
        }

        headers: Dict = {
            "content-type": "application/json",
            "X-RapidAPI-Key": self.__x_rapid_api_host,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response: requests = requests.request("POST", url, json=payload, headers=headers)

        if response.status_code == 200:
            response_dict: Dict = json.loads(response.text)
            if response_dict.get('data', False):
                if response_dict['data'].get('propertySearch', False):
                    if response_dict['data']['propertySearch'].get('properties', False):
                        self.__properties_list = json.loads(response.text)['data']['propertySearch']['properties']
                        return 200

            if response_dict.get('errors', False):
                if response_dict['errors'][0].get('extensions', False):
                    if response_dict['errors'][0]['extensions'].get('event', False):
                        if response_dict['errors'][0]['extensions']['event'].get('message', False):
                            if response_dict['errors'][0]['extensions']['event']['message'] == 'Your filter options are not showing a match.':
                                return 1

        return response.status_code

    def __add_properties_details_dict(self) -> Optional[int]:
        """
        Метод выполняет запрос properties/v2/list
        Поиск подробностей по отелям.
        Добавляет детали к __properties_list.

        :return response.status_code: статус ответа сервера
        :rtype: int
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
            if response.status_code == 200:
                self.__properties_list[index_hotel]['detail'] = json.loads(response.text)
            else:
                return response.status_code
        return 200


class CheckingUserResponses:
    """
    Класс для проверки ответов пользователя

    Attributes:
        RESPONSE_TOUSER (Dict): ответы пользователю, в случае ввода не корректных данных
    """

    RESPONSE_TO_USER: Dict = {'year': 'Год должен содержать четыре цыфры, введите ещё раз',
                              'month': 'Месяц ввели не корректно, попробуйте ещё раз',
                              'day': 'Не верно ввели день, введите ещё раз',
                              'city': 'Название города должно состоять из букв латинского алфавита',
                              'price-distance': 'Нужно ввести две цифры через тире',
                              'yn': 'Да или Нет?',
                              'number': 'Не корректный ввод!'}

    @classmethod
    def checking_user_responses(cls, text: str, type_text: str) -> bool:
        """
        Метод для проверки сообщений пользователя

        :param text: проверяемое сообщение пользователя
        :type text: str

        :param type_text: шаблон, по которому необходимо проверять сообщение пользователя
        :type type_text: str

        :rtype: bool
        """

        if type_text == 'city':
            if re.fullmatch(r'[a-z, A-Z]*[ -][a-z, A-Z]*|[a-z, A-Z]*', text):
                return True
        if type_text == 'year':
            if text.isdigit() and len(text) == 4 and int(text) >= datetime.date.today().year:
                return True
        if type_text == 'day':
            if text.isdigit() and 0 < len(text) < 3 and 0 < int(text) < 32:
                return True
        if type_text == 'month':
            if text.lower() in MONTHS:
                return True
        if type_text == 'price-distance':
            if re.fullmatch(r'\d*-\d*', text):
                return True
        if type_text == 'number':
            if re.fullmatch(r'\d*', text):
                return True
        if type_text == 'yn':
            if text.lower() == 'да' or text.lower() == 'нет':
                return True

        return False
