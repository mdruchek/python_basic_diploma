from configparser import ConfigParser


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
