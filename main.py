import modules
from modules import DataToShelve
import telebot
from telebot import types
import lowprice
import os

if __name__ == '__main__':
    token: str = modules.get_config_from_file(path='./config.ini', section='account', setting='token')
    my_bot: telebot.TeleBot = telebot.TeleBot(token)
    DataToShelve.remove_shelve('./data_commands')

    @my_bot.message_handler(commands=['lowprice'])
    def lowprice_command(message) -> None:
        """
        Функция для вывода самых дешёвых отелей
        """
        DataToShelve.remove_shelve('data_commands')
        DataToShelve.adding_data_to_shelve(path='./data_commands', key='command', data=message.text)
        DataToShelve.adding_data_to_shelve(path='./data_commands', key='number_question', data='1')
        my_bot.send_message(message.from_user.id, 'В каком городе ищем?')


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

        if os.path.exists('./data_commands'):
            command = DataToShelve.read_data_from_shelve(path='./data_commands', key='command')['command']
            number_question: int = int(DataToShelve.read_data_from_shelve(path='./data_commands', key='number_question')['number_question'])
            number_question += 1
            print(number_question, type(number_question))
            if command['command'] == '/lowprice' and number_question == 1:
                number_question += 1
                DataToShelve.adding_data_to_shelve(path='./data_commands', key='number_question', data=str(number_question))
                my_bot.send_message(message.from_user.id, 'Cколько отелей вывести?')
        else:
            my_bot.send_message(message.from_user.id, 'Я Вас не понимаю, введиет /help')

    my_bot.polling(non_stop=True)


