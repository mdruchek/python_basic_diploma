import configparser
import os
import functools
from typing import Callable


def checking_existence_file(path: str) -> Callable:
    """
    Декоратор для проверки существования файла
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if os.path.exists(path):
                    result: Callable = func(*args, **kwargs)
                    return result
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                print('Ошибка: Файл "{file}" не найден в корневой папке программы'.format(file=path[2:]))
        return wrapper
    return decorator


@checking_existence_file(path='./config.ini')
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


