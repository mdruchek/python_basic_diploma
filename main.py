import telebot
from telebot import types
import modules
from modules import UserSurvey
from modules import Requests
from modules import MONTHS
import datetime
from calendar import monthrange
import math
from typing import List


token: str = modules.get_config_from_file(path='./config.ini', section='account', setting='token')
my_bot: telebot.TeleBot = telebot.TeleBot(token)
users_id = dict()


@my_bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def loading_hotels_command(message: types.Message) -> None:
    """
    Функция для загрузки отелей
    :param message: сообщение
    :type message: types.Message
    """

    markup = types.ReplyKeyboardRemove()
    users_id[message.from_user.id] = dict()
    users_id[message.from_user.id]['survey']: UserSurvey = UserSurvey()
    users_id[message.from_user.id]['survey'].command = message.text
    question: types.Message = my_bot.send_message(message.from_user.id, 'Введите город для поиска:', reply_markup=markup)
    my_bot.register_next_step_handler(question, check_in_date_year)


@my_bot.message_handler(commands=['history'])
def history_command(message: types.Message) -> None:
    """
    Функция для вывода вывод истории поиска отелей
    :param message: сообщение
    :type message: types.Message
    """
    pass
    """
    В работе
    """


@my_bot.message_handler(commands=['help', 'start'])
def help_command(message: types.Message) -> None:
    """
    Функция для вывода справки по функциям
    :param message: сообщение
    :type message: types.Message
    """
    my_bot.send_message(message.from_user.id, 'Привет меня зовут MDr, я могу подобрать отель для проживания.\n'
                                              'Я понимаю такие команды:\n'
                                              '/lowprice - вывод самых дешёвых отелей в городе\n'
                                              '/highprice - вывод самых дорогих отелей в городе\n'
                                              '/bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра\n'
                                              '/history - вывод истории поиска отелей')


@my_bot.message_handler(func=lambda m: True)
def any_text(message: types.Message) -> None:
    """
    Функция обработки остального текста
    :param message: сообщение
    :type message: types.Message
    """

    my_bot.send_message(message.from_user.id, 'Я Вас не понимаю, введите /help')


def check_in_date_year(message: types.Message) -> None:
    """
    Функция записывает город и спрашивает год даты заезда
    :param message: сообщение
    :type message: types.Message
    """

    users_id[message.from_user.id]['survey'].city = message.text
    markup = types.ReplyKeyboardRemove()
    my_bot.send_message(message.from_user.id,
                        'Введите дату заезда:',
                        reply_markup=markup)
    current_year = datetime.date.today().year
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembt_cur_year = types.KeyboardButton(str(current_year))
    itembt_next_year = types.KeyboardButton(str(current_year + 1))
    markup.add(itembt_cur_year, itembt_next_year)

    question = my_bot.send_message(message.from_user.id,
                                   'год',
                                   reply_markup=markup)

    my_bot.register_next_step_handler(question,  check_in_date_month)


def check_in_date_month(message: types.Message) -> None:
    """
    Функция записывает год даты заезда и спрашивает месяц даты заезда
    :param message: сообщение
    :type message: types.Message
    """

    users_id[message.from_user.id]['survey'].check_in_date_year = int(message.text)
    markup = get_ReplyKeyboardMarkup_month(year=int(message.text))

    question = my_bot.send_message(message.from_user.id,
                                 'месяц',
                                 reply_markup=markup)

    my_bot.register_next_step_handler(question, check_in_date_day)


def check_in_date_day(message: types.Message) -> None:
    """
    Функция записывает месяц заезда и спрашивает день заезда
    :param message: сообщение
    :type message: types.Message
    """

    users_id[message.from_user.id]['survey'].check_in_date_month = MONTHS.index(message.text) + 1
    markup = get_ReplyKeyboardMarkup_day(year=users_id[message.from_user.id]['survey'].check_in_date_year,
                                         month=MONTHS.index(message.text) + 1)

    question = my_bot.send_message(message.from_user.id,
                                   'день',
                                   reply_markup=markup)

    my_bot.register_next_step_handler(question, check_out_date_year)


def check_out_date_year(message: types.Message) -> None:
    """
    Функция записывает день заезда и спрашивает год выезда
    :param message: сообщение
    :type message: types.Message
    """

    users_id[message.from_user.id]['survey'].check_in_date_day = int(message.text)
    markup = types.ReplyKeyboardRemove()
    my_bot.send_message(message.from_user.id,
                        'Введите дату выезда:',
                        reply_markup=markup)
    current_year = datetime.date.today().year
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembt_cur_year = types.KeyboardButton(str(current_year))
    itembt_next_year = types.KeyboardButton(str(current_year + 1))
    markup.add(itembt_cur_year, itembt_next_year)

    question = my_bot.send_message(message.from_user.id,
                                 'год',
                                 reply_markup=markup)

    my_bot.register_next_step_handler(question, check_out_date_month)


def check_out_date_month(message: types.Message) -> None:
    """
    Функция записывает год выезда и спрашивает месяц выезда
    :param message: сообщение
    :type message: types.Message
    """

    users_id[message.from_user.id]['survey'].check_out_date_year = int(message.text)
    markup = get_ReplyKeyboardMarkup_month(year=int(message.text))

    question = my_bot.send_message(message.from_user.id,
                                 'месяц',
                                 reply_markup=markup)

    my_bot.register_next_step_handler(question, check_out_date_day)


def check_out_date_day(message: types.Message) -> None:
    """
    Функция записывает месяц выезда и спрашивает день выезда
    :param message: сообщение
    :type message: types.Message
    """
    users_id[message.from_user.id]['survey'].check_out_date_month = MONTHS.index(message.text) + 1
    markup = get_ReplyKeyboardMarkup_day(year=users_id[message.from_user.id]['survey'].check_out_date_year,
                                                                    month=MONTHS.index(message.text) + 1)

    question = my_bot.send_message(message.from_user.id,
                                 'день',
                                 reply_markup=markup)

    if users_id[message.from_user.id]['survey'].command in ['/lowprice', '/highprice']:
        my_bot.register_next_step_handler(question, number_hotels, question.text)
    if users_id[message.from_user.id]['survey'].command == ['/bestdeal']:
        my_bot.register_next_step_handler(question, price)


def price(message: types.Message) -> None:
    """
    Функция запрашивает цену и записывает день выезда
    :param message: сообщение
    :type message: types.Message
    """

    users_id[message.from_user.id]['survey'].check_out_date_day = int(message.text)
    markup = types.ReplyKeyboardRemove()
    question = my_bot.send_message(message.from_user.id,
                                 'Введите диапазон цен (через тире)',
                                 reply_markup=markup)
    my_bot.register_next_step_handler(question, distance)


def distance(message: types.Message) -> None:
    """
    Функция записывает цену и спрашивает расстояние до центра
    :param message: сообщение
    :type message: types.Message
    """

    users_id[message.from_user.id]['survey'].price = message.text
    markup = types.ReplyKeyboardRemove()
    question = my_bot.send_message(message.from_user.id,
                                 'Введите расстояние от центра (через тире)',
                                 reply_markup=markup)
    my_bot.register_next_step_handler(question, number_hotels, question.text)


def number_hotels(message: types.Message, question: str) -> None:
    """
    Функция записывает цену или день выезда (в зависимосте от предыдущего вопроса questuon)
    и запрашивает количество результаттов
    :param message: сообщение
    :type message: types.Message

    :param question: предыдущий вопрос
    :type question: str
    """

    if 'расстояние' in question:
        users_id[message.from_user.id]['survey'].distance = message.text
    if 'день' in question:
        users_id[message.from_user.id]['survey'].check_out_date_day = int(message.text)
    markup = types.ReplyKeyboardRemove()
    question = my_bot.send_message(message.from_user.id,
                                 'Введите количество вариантов',
                                 reply_markup=markup)
    my_bot.register_next_step_handler(question, uploading_photos)


def uploading_photos(message: types.Message) -> None:
    """
    Функция записывает количество результатов и запрашивает загрузить ли фото
    :param message: сообщение
    :type message: types.Message
    """

    users_id[message.from_user.id]['survey'].number_hotels = int(message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembty = types.KeyboardButton('Да')
    itembtn = types.KeyboardButton('Нет')
    markup.add(itembty, itembtn)
    question = my_bot.send_message(message.from_user.id,
                                 'Фото загрузить?',
                                 reply_markup=markup)
    my_bot.register_next_step_handler(question, request, question.text)


def number_photos(message: types.Message) -> None:
    """
    Функция записывает ответ о необходимости загрузки фото и запрашивает количество фото
    :param message: сообщение
    :type message: types.Message
    """

    users_id[message.from_user.id]['survey'].uploading_photos = message.text
    markup = types.ReplyKeyboardRemove()
    question = my_bot.send_message(message.from_user.id,
                                 'Сколько?',
                                 reply_markup=markup)
    my_bot.register_next_step_handler(question, request, question.text)


def request(message: types.Message, question: str) -> None:
    """
    Функция записывает необходимость загрузки фото или количество фото в зависимости от question,
    формирует запрос и выводит результат
    :param message: сообщение
    :type message: types.Message

    :param question: предыдущий вопрос
    :type question: str
    """

    if 'Фото' in question:
        users_id[message.from_user.id]['survey'].uploading_photos = message.text
    if 'сколько' in question:
        users_id[message.from_user.id]['survey'].number_photos = int(message.text)

    if users_id[message.from_user.id]['survey'].command in ['/lowprice', '/bestdeal']:
        sort_request_results = 'PRICE_LOW_TO_HIGH'
    if users_id[message.from_user.id]['survey'].command == '/highprice':
        sort_request_results = 'PRICE_HIGH_TO_LOW'

    users_id[message.from_user.id]['request']: Requests = Requests(city=users_id[message.from_user.id]['survey'].city,
                                                                   check_in_date_day=users_id[message.from_user.id]['survey'].check_in_date_day,
                                                                   check_in_date_month=users_id[message.from_user.id]['survey'].check_in_date_month,
                                                                   check_in_date_year=users_id[message.from_user.id]['survey'].check_in_date_year,
                                                                   check_out_date_day=users_id[message.from_user.id]['survey'].check_out_date_day,
                                                                   check_out_date_month=users_id[message.from_user.id]['survey'].check_out_date_month,
                                                                   check_out_date_year=users_id[message.from_user.id]['survey'].check_out_date_year,
                                                                   number_hotels=users_id[message.from_user.id]['survey'].number_hotels,
                                                                   sort=sort_request_results)

    result_request = users_id[message.from_user.id]['request'].properties_list

    my_bot.send_message(message.from_user.id,
                        'Вот что я нашёл для Вас:',
                        reply_markup=types.ReplyKeyboardRemove())

    for hotel in result_request:
        my_bot.send_message(message.from_user.id,
                            'Отель: {name}\n'
                            'Адрес: {address}\n'
                            'Расстояние до центра: {distance_value} {distance_unit}\n'
                            'Полная стоимость: {amount}'.format(name=hotel['name'],
                                                                address=hotel['detail']['data']['propertyInfo']['summary']['location']['address']['firstAddressLine'],
                                                                distance_value=hotel['destinationInfo']['distanceFromDestination']['value'],
                                                                distance_unit=hotel['destinationInfo']['distanceFromDestination']['unit'],
                                                                amount=hotel['price']['lead']['formatted']))


def get_ReplyKeyboardMarkup_month(year: int) -> types.ReplyKeyboardMarkup:
    """
    Функция возвращает клавиатуру выбора месяца
    :param year: год
    :type year: str

    :return: клавиатура выбора месяца
    :rtype: types.ReplyKeyboardMarkup
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    current_year = datetime.date.today().year
    if current_year == year:
        month: int = datetime.date.today().month
    else:
        month: int = 1
    number_month: int = 13 - month
    number_rows_keyboard: int = math.ceil(number_month / 4)
    for _ in range(number_rows_keyboard):
        row_itembt: List = []
        for __ in range(4):
            row_itembt.append(types.KeyboardButton(MONTHS[month - 1]))
            month += 1
            if month == 13:
                break
        if len(row_itembt) == 4:
            itembt1, itembt2, itembt3, itembt4 = row_itembt
            markup.row(itembt1, itembt2, itembt3, itembt4)
        elif len(row_itembt) == 3:
            itembt1, itembt2, itembt3 = row_itembt
            markup.row(itembt1, itembt2, itembt3)
        elif len(row_itembt) == 2:
            itembt1, itembt2, itembt3 = row_itembt
            markup.row(itembt1, itembt2)
        else:
            markup.row(row_itembt[0])
    return markup


def get_ReplyKeyboardMarkup_day(year: int, month: int) -> types.ReplyKeyboardMarkup:
    """
    Функция возвращает клавиатуру выбора дня
    :param year: год
    :type year: str

    :param month: месяц
    :type month: str

    :return: клавиатура выбора месяца
    :rtype: types.ReplyKeyboardMarkup
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    current_year: int = datetime.date.today().year
    current_month: int = datetime.date.today().month
    if current_month == month and current_year == year:
        day: int = datetime.date.today().day
    else:
        day: int = 1
    number_days: int = monthrange(year, month)[1] - day
    number_rows_keyboard: int = math.ceil(number_days / 7)
    for _ in range(number_rows_keyboard):
        row_itembt: List = []
        for __ in range(7):
            row_itembt.append(types.KeyboardButton(str(day)))
            day += 1
            if day == monthrange(year, month)[1] + 1:
                break
        if len(row_itembt) == 7:
            itembt1, itembt2, itembt3, itembt4, itembt5, itembt6, itembt7 = row_itembt
            markup.row(itembt1, itembt2, itembt3, itembt4, itembt5, itembt6, itembt7)
        elif len(row_itembt) == 6:
            itembt1, itembt2, itembt3, itembt4, itembt5, itembt6 = row_itembt

            markup.row(itembt1, itembt2, itembt3, itembt4, itembt5, itembt6)
        elif len(row_itembt) == 5:
            itembt1, itembt2, itembt3, itembt4, itembt5 = row_itembt
            markup.row(itembt1, itembt2, itembt3, itembt4, itembt5)
        elif len(row_itembt) == 4:
            itembt1, itembt2, itembt3, itembt4 = row_itembt
            markup.row(itembt1, itembt2, itembt3, itembt4)
        elif len(row_itembt) == 3:
            itembt1, itembt2, itembt3 = row_itembt
            markup.row(itembt1, itembt2, itembt3)
        elif len(row_itembt) == 2:
            itembt1, itembt2 = row_itembt
            markup.row(itembt1, itembt2)
        else:
            markup.row(row_itembt[0])
    return markup


my_bot.polling(non_stop=True)

