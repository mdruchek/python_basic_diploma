import telebot


bot = telebot.TeleBot('5750439044:AAEfGHepjzNZWc67w5rTTh_H9TZX_WICzBY')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет".lower():
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text == "/hello word":
        bot.send_message(message.from_user.id, "hellow word")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)