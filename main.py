import telebot
from telebot import types
import modules
from modules import UserSurvey
from modules import Requests
import datetime


if __name__ == '__main__':
    token: str = modules.get_config_from_file(path='./config.ini', section='account', setting='token')
    my_bot: telebot.TeleBot = telebot.TeleBot(token)
    users_id = dict()

    @my_bot.message_handler(commands=['lowprice'])
    def lowprice_command(message) -> None:
        """
        Функция для вывода самых дешёвых отелей
        """
        markup = types.ReplyKeyboardRemove()
        users_id[message.from_user.id] = dict()
        users_id[message.from_user.id]['survey']: UserSurvey = UserSurvey()
        users_id[message.from_user.id]['survey'].command = message.text
        my_bot.send_message(message.from_user.id, users_id[message.from_user.id]['survey'].get_question(), reply_markup=markup)


    @my_bot.message_handler(commands=['highprice'])
    def highprice_command(message) -> None:
        """
        Функция для вывода самых дорогих отелей
        """
        my_bot.send_message(message.from_user.id, 'В каком городе ищем?')
        """
        В работе
        """

    @my_bot.message_handler(commands=['bestdeal'])
    def bestdeal_command(message) -> None:
        """
        Функция для вывода отелей, наиболее подходящих по цене и расположению от центра
        """
        my_bot.send_message(message.from_user.id, 'В каком городе ищем?')
        """
        В работе
        """

    @my_bot.message_handler(commands=['history'])
    def history_command(message) -> None:
        """
        Функция для вывода вывод истории поиска отелей
        """
        my_bot.send_message(message.from_user.id, 'В каком городе ищем?')
        """
        В работе
        """

    @my_bot.message_handler(commands=['help', 'start'])
    def help_command(message) -> None:
        """
        Функция для вывода справки по функциям
        """
        my_bot.send_message(message.from_user.id, 'Привет меня зовут MDr, я могу подобрать отель для проживания.\n'
                                                  'Я понимаю такие команды:\n'
                                                  '/lowprice - вывод самых дешёвых отелей в городе\n'
                                                  '/highprice - вывод самых дорогих отелей в городе\n'
                                                  '/bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра\n'
                                                  '/history - вывод истории поиска отелей')

    @my_bot.message_handler(func=lambda text: True)
    def any_text(message) -> None:
        """
        Функция обработки остального текста
        """
        markup = types.ReplyKeyboardRemove()
        if users_id[message.from_user.id]['survey'].question_number != -1:
            users_id[message.from_user.id]['survey'].set_answer(message.text)
            question = users_id[message.from_user.id]['survey'].get_question()
            if question:
                if question == 'Загрузить фотографи?':
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    itembty = types.KeyboardButton('Да')
                    itembtn = types.KeyboardButton('Нет')
                    markup.add(itembty, itembtn)

                if 'год' in question:
                    current_year = datetime.date.today().year
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    itembt_cur_year = types.KeyboardButton(str(current_year))
                    itembt_next_year = types.KeyboardButton(str(current_year + 1))
                    markup.add(itembt_cur_year, itembt_next_year)

                if 'month' in question:
                    markup = types.ReplyKeyboardMarkup(row_resize_keyboard=True)
                    itembt_january = types.KeyboardButton('Январь')
                    itembt_february = types.KeyboardButton('Февраль')
                    itembt_march = types.KeyboardButton('Март')
                    itembt_april = types.KeyboardButton('Апрель')
                    itembt_may = types.KeyboardButton('Май')
                    itembt_june = types.KeyboardButton('Июнь')
                    itembt_july = types.KeyboardButton('Июль')
                    itembt_august = types.KeyboardButton('Август')
                    itembt_september = types.KeyboardButton('Сентябрь')
                    itembt_october = types.KeyboardButton('Октябрь')
                    itembt_november = types.KeyboardButton('Ноябрь')
                    itembt_december = types.KeyboardButton('Декабрь')
                    markup.row(itembt_january, itembt_february, itembt_march, itembt_april)
                    markup.row(itembt_may, itembt_june, itembt_july, itembt_august)
                    markup.row(itembt_september, itembt_october, itembt_november, itembt_december)

                if 'day' in question:
                    markup = types.ReplyKeyboardMarkup(row_resize_keyboard=True)
                    number_day = 0
                    for _ in range(5):
                        row_itembt = []
                        for __ in range(7):
                            number_day += 1
                            row_itembt.append(types.KeyboardButton(str(number_day)))
                        itembt1, itembt2, itembt3, itembt4, itembt5, itembt6, itembt7 = row_itembt
                        markup.row(itembt1, itembt2, itembt3, itembt4, itembt5, itembt6, itembt7)

                my_bot.send_message(message.from_user.id, question, reply_markup=markup)
            else:
                if users_id[message.from_user.id]['survey'].command in ['lowprice', 'bestdeal']:
                    sort = 'PRICE_LOW_TO_HIGH'
                if users_id[message.from_user.id]['survey'].command == 'highprice':
                    sort = 'PRICE_HIGH_TO_LOW'
                users_id[message.from_user.id]['request']: Requests = Requests(city=users_id[message.from_user.id]['survey'].city,
                                                                               check_in_date=users_id[message.from_user.id]['survey'].check_in_date,
                                                                               check_out_date=users_id[message.from_user.id]['survey'].check_out_date,
                                                                               result_size=users_id[message.from_user.id]['survey'].number_hotels,
                                                                               sort=sort)

                result_request = users_id[message.from_user.id]['request'].properties_list
                my_bot.send_message(message.from_user.id,
                                    'Вот что я нашёл для Вас:',
                                    reply_markup=types.ReplyKeyboardRemove())
                for hotel in result_request:
                    my_bot.send_message(message.from_user.id,
                                        'Отель: {name}\n'
                                        'Адрес: {address}'.format(name=hotel['name'],
                                                                  address=hotel['detail']['data']['propertyInfo']['summary']['location']['address']['firstAddressLine']))
        else:
            my_bot.send_message(message.from_user.id, 'Я Вас не понимаю, введиет /help', reply_markup=markup)

    my_bot.polling(non_stop=True)

