import lowprice
import modules
import telebot


if __name__ == '__main__':
    token: str = modules.get_config_from_file(path='./config.ini', section='account', setting='token_bot')
    my_bot: telebot.TeleBot = telebot.TeleBot(token)

    @my_bot.message_handler(content_types=['text'])
    def get_text_messages(message) -> None:
        """
        Функция обмена текстовыми сообщениями Телеграмм-бота
        """
        if message.text == "/help":
            my_bot.send_message(message.from_user.id,
                              "Привет меня зовут MDr, я могу подобрать отель для проживания.\n"
                              "Я понимаю такие команды:\n"
                              "/lowprice - вывод самых дешёвых отелей в городе\n"
                              "/highprice - вывод самых дорогих отелей в городе\n"
                              "/bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра\n"
                              "/history - вывод истории поиска отелей\n")
        elif message.text == '/lowprice':
            lowprice.lowprice_function_bot()
        elif message.text == '/highprice':
            my_bot.send_message(message.from_user.id, 'Функция в разработке.')
        elif message.text == '/bestdeal':
            my_bot.send_message(message.from_user.id, 'Функция в разработке.')
        elif message.text == '/history':
            my_bot.send_message(message.from_user.id, 'Функция в разработке.')
        else:
            my_bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


    my_bot.polling(none_stop=True, interval=0)