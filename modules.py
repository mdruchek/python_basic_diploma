from configparser import ConfigParser
from typing import List


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

    __answers_key = ('cyty', 'price', 'distance', 'number_hotels', 'uploading_photos', 'number_photos')



    def __init__(self):
        self.__command: str = ''
        self.__command_number = 0
        self.__answers = dict()

    @property
    def command(self):
        return self.__command

    @command.setter
    def command(self, command):
        self.__command = command
        self.__command_number = 0
        self.__city: str = ''
        self.__price: List = [None, None]
        self.__distance: List = [None, None]
        self.__number_hotels: int = 0
        self.__uploading_photos: bool = False
        self.__number_photos: int = 0

    def get_question(self):
        if self.__command_number > len(UserSurvey.__survey_list[self.__command]):
            self.__command_number = 0
            return False
        question = UserSurvey.__questions[UserSurvey.__survey_list[self.__command_number]]
        self.__command_number += 1
        return question

    def set_answer(self, answer):
        self.__answers[self.__answers_key[self.__command_number] - 1] = answer

    def reset_answers(self):
        self.__answers = dict()
