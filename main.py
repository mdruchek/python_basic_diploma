import modules
import telebot
import lowprice


def telegram_bot(token):
    my_bot: telebot.TeleBot = telebot.TeleBot(token)
    telegram_bot.command_message_id = 0
    telegram_bot.command = None

    @my_bot.message_handler(commands=['lowprice'])
    def lowprice_command(message) -> None:
        """
        Функция для вывода самых дешёвых отелей
        """
        telegram_bot.command = message.text
        telegram_bot.command_message_id = message.id
        my_bot.send_message(message.from_user.id, "В каком городе ищем?")


    @my_bot.message_handler(commands=['highprice'])
    def highprice_command(message) -> None:
        """
        Функция для вывода самых дорогих отелей
        """
        telegram_bot.command_message_id = message.id
        telegram_bot.command = message.text
        my_bot.send_message(message.from_user.id, "В каком городе ищем?")



    @my_bot.message_handler(commands=['bestdeal'])
    def bestdeal_command(message) -> None:
        """
        Функция для вывода отелей, наиболее подходящих по цене и расположению от центра
        """
        telegram_bot.command_message_id = message.id
        telegram_bot.command = message.text
        my_bot.send_message(message.from_user.id, "В каком городе ищем?")


    @my_bot.message_handler(commands=['history'])
    def history_command(message) -> None:
        """
        Функция для вывода вывод истории поиска отелей
        """
        telegram_bot.command_message_id = message.id
        telegram_bot.command = message.text
        my_bot.send_message(message.from_user.id, "В каком городе ищем?")


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
        if message.id == telegram_bot.command_message_id + 2:
            if telegram_bot.command == '/lowprice':
                my_bot.send_message(message.from_user.id, lowprice.Lowprice.get_location_city(message.text))
            else:
                my_bot.send_message(message.from_user.id, 'функция в разработке')
        else:
            my_bot.send_message(message.from_user.id, 'Я Вас не понимаю, введите /help')


    my_bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    token: str = modules.get_config_from_file(path='./config.ini', section='account', setting='token')
    telegram_bot(token)