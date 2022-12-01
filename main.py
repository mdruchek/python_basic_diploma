import modules
import telebot
import lowprice
import shelve

if __name__ == '__main__':
    token: str = modules.get_config_from_file(path='./config.ini', section='account', setting='token')
    my_bot: telebot.TeleBot = telebot.TeleBot(token)

    @my_bot.message_handler(commands=['lowprice'])
    def lowprice_command(message) -> None:
        """
        Функция для вывода самых дешёвых отелей
        """
        my_bot.reply_to(message, "В каком городе ищем?")

    @my_bot.message_handler(commands=['highprice'])
    def highprice_command(message) -> None:
        """
        Функция для вывода самых дорогих отелей
        """
        my_bot.reply_to(message, "В каком городе ищем?")

    @my_bot.message_handler(commands=['bestdeal'])
    def bestdeal_command(message) -> None:
        """
        Функция для вывода отелей, наиболее подходящих по цене и расположению от центра
        """
        my_bot.reply_to(message, "В каком городе ищем?")

    @my_bot.message_handler(commands=['history'])
    def history_command(message) -> None:
        """
        Функция для вывода вывод истории поиска отелей
        """
        my_bot.reply_to(message.from_user.id, "В каком городе ищем?")

    @my_bot.message_handler(commands=['help'])
    def help_command(message) -> None:
        """
        Функция для вывода справки по функциям
        """
        my_bot.reply_to(message, 'Привет меня зовут MDr, я могу подобрать отель для проживания.\n'
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

        if telegram_bot.command == '/lowprice':
            my_bot.reply_to(message, lowprice.Lowprice.get_location_city(message.text))
        else:
            my_bot.reply_to(message, 'функция в разработке')
        my_bot.reply_to(message, 'Я Вас не понимаю, введите /help')

    my_bot.infinity_poling()


