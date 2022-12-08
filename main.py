import telebot
from telebot import types
import modules
from modules import UserSurvey
from modules import Requests


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
        if users_id[message.from_user.id]['survey'].command_number != -1:
            users_id[message.from_user.id]['survey'].set_answer(message.text)
            question = users_id[message.from_user.id]['survey'].get_question()
            if question:
                if question == 'Загрузить фотографи?':
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    itembty = types.KeyboardButton('Да')
                    itembtn = types.KeyboardButton('Нет')
                    markup.add(itembty, itembtn)
                my_bot.send_message(message.from_user.id, question, reply_markup=markup)
            else:
                users_id[message.from_user.id]['request']: Requests = Requests(command=users_id[message.from_user.id]['survey'].command,
                                                                               city=users_id[message.from_user.id]['survey'].city,
                                                                               check_in_date=None,
                                                                               check_out_date=None,
                                                                               result_size=users_id[message.from_user.id]['survey'].number_hotels)

                result_request = users_id[message.from_user.id]['request'].properties_list()
                my_bot.send_message(message.from_user.id, 'Вот что я нашёл для Вас:')
                for hotel in result_request:
                    my_bot.send_message(message.from_user.id, 'Отель: {name}'.format(name=hotel['mane']))
        else:
            my_bot.send_message(message.from_user.id, 'Я Вас не понимаю, введиет /help', reply_markup=markup)

    my_bot.polling(non_stop=True)


