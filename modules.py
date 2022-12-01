from configparser import ConfigParser
import shelve
import os
from typing import Dict


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


class DataToShelve:
    """
    Класс для записи данных в файл с помощью модуля shelve
    """
    @classmethod
    def adding_data_to_shelve(cls, path: str, key: str, data: str) -> None:
        """
        Метод записи данных

        :param path: имя файла
        :type path: str

        :param key: ключ
        :type key: str

        :param data: данные
        :type data: str
        """
        shelve_buffer = shelve.open(path)
        shelve_buffer[key] = data
        shelve_buffer.close()

    @classmethod
    def read_data_from_shelve(cls, path: str, key: str) -> Dict:
        """
        Метод чтения данных

        :param path: имя файла
        :type path: str

        :param key: ключ
        :type key: str
        """
        shelve_buffer = shelve.open(path)
        data = shelve_buffer[key]
        shelve_buffer.close()
        return {key: data}

    @classmethod
    def remove_shelve(cls, path: str) -> None:
        """
        Метод удаления файла данных

        :param path: имя файла
        :type path: str
        """
        if os.path.exists(path):
            os.remove(path)