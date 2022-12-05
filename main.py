import telebot
from telebot import types
import modules
from modules import UserSurvey
from lowprice import Lowprice


if __name__ == '__main__':
    token: str = modules.get_config_from_file(path='./config.ini', section='account', setting='token')
    my_bot: telebot.TeleBot = telebot.TeleBot(token)
    users_id = dict()



    @my_bot.message_handler(commands=['lowprice'])
    def lowprice_command(message) -> None:
        """
        Функция для вывода самых дешёвых отелей
        """
        users_id[message.from_user.id] = UserSurvey()
        users_id[message.from_user.id].command = message.text
        my_bot.send_message(message.from_user.id, users_id[message.from_user.id].get_question())


    @my_bot.message_handler(commands=['highprice'])
    def highprice_command(message) -> None:
        """
        Функция для вывода самых дорогих отелей
        """
        my_bot.send_message(message.from_user.id, 'В каком городе ищем?')

    @my_bot.message_handler(commands=['bestdeal'])
    def bestdeal_command(message) -> None:
        """
        Функция для вывода отелей, наиболее подходящих по цене и расположению от центра
        """
        my_bot.send_message(message.from_user.id, 'В каком городе ищем?')

    @my_bot.message_handler(commands=['history'])
    def history_command(message) -> None:
        """
        Функция для вывода вывод истории поиска отелей
        """
        my_bot.send_message(message.from_user.id, 'В каком городе ищем?')

    @my_bot.message_handler(commands=['help'])
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
        if users_id[message.from_user.id].command_number != -1:
            users_id[message.from_user.id].set_answer(message.text)
            question = users_id[message.from_user.id].get_question()
            if question:
                if question == 'Загрузить фотографи?':
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    itembty = types.KeyboardButton('Да')
                    itembtn = types.KeyboardButton('Нет')
                    markup.add(itembty, itembtn)
                my_bot.send_message(message.from_user.id, question, reply_markup=markup)
            else:
                my_bot.send_message(message.from_user.id, users_id[message.from_user.id].city, reply_markup=markup)
        else:
            my_bot.send_message(message.from_user.id, 'Я Вас не понимаю, введиет /help', reply_markup=markup)

    my_bot.polling(non_stop=True)


