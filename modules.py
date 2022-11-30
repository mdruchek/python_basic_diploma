import configparser
import os
import functools
from typing import Callable


def checking_existence_file(func) -> Callable:
    """
    Декоратор для проверки существования файла
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if os.path.exists(kwargs['path']):
            result: Callable = func(*args, **kwargs)
            return result
        else:
            config = configparser.ConfigParser()
            with open('config.ini', 'w') as file_config:
                token = input('Конфигурационный файл "config.ini" отсутствует,\n'
                              'чтобы его создать введите токен Телеграмм-бота: ')
                config['account'] = {'token_bot': token}
                config.write(file_config)
    return wrapper


@checking_existence_file
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
    config = configparser.ConfigParser()
    config.read(path)
    setting_in_file: str = config.get(section, setting)
    return setting_in_file


