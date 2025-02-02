import telebot
import json
import random

TOKEN = ""

bot =telebot.TeleBot(TOKEN)


try:
    with open("user_data.json","r",encoding="utf-8") as file:
        user_dict =json.load(file)
except (FileNotFoundError,json.JSONDecoderError):
    user_dict = {}




@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id,f"Привет,{message.from_user.first_name}. Я - бот для прохождения карточек на английском языке!"
                                     "\n мой создатель - ."
                                     "\nИсходный код бота вы можете посмотреть по этой ссылке "
                                     "\n")

@bot.message_handler(commands=["addword"])
def addword(message):
    with open("user_data.json","r",encoding="utf-8") as file:
        user_dict =json.load(file)

    chat_id =message.chat.id
    user_dictonary =user_dict.get(chat_id,{})
    words =message.text.split()[1:]
    if len(words) ==2:
        word,translate =words[0].lower(),words[1].lower()
        user_dictonary[word] = translate
        user_dict[chat_id] = user_dictonary
        with open("user_data.json","w",encoding="utf-8") as file:
            json.dump(user_dict,file,ensure_ascii=False,indent=4)
        bot.send_message(message.chat.id,"Слово добавлено!")
    else:
        bot.send_message(message.chat.id,"Ошибка!Слово не добавлено.Возможно,вы неправильно пишете команду")



@bot.message_handler(commands=["learn"])
def learn(message):
    try:
        user_words =user_dict.get(str(message.chat.id),{})
        words_left =int(message.text.split()[1])
        ask_translation(message.chat.id,user_words,words_left)
    except (ValueError,IndexError):
        bot.send_message(message.chat.id,"Используй команду /learn ,а затем укажи число слов,для перевода"
                                         "\n Пример: /learn 5 (карточка на 5 слов)")
    except AttributeError:
        bot.send_message(message.chat.id,"Вы неправильно используете команду")
def ask_translation(chat_id,user_words,words_left):
    if words_left >0:
        random_word = random.choice(list(user_words.keys()))
        translation =user_words[random_word]
        bot.send_message(chat_id,f"Напиши перевод слова из твоего словаря: {random_word}")
        bot.register_next_step_handler_by_chat_id(chat_id,check_translation,translation,words_left -1)
    else:
        bot.send_message(chat_id,"Урок завершен")

def check_translation(message,translation,words_left):
    my_translation =message.text.strip().lower()
    if my_translation ==translation.lower():
        bot.send_message(message.chat.id,"Верно!Перевод верный")
    else:
        bot.send_message(message.chat.id,"Перевод неверный ):")
    ask_translation(message.chat.id,user_dict[str(message.chat.id)],words_left)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,"Привет!Этот бот создан для обучения английскому языку!"
                                     "\n его автор - "
                                     "\nсипоск команд:\n"
                                     "\n/start - переапуск бота"
                                     "\n/help - список команд\n"
                                     "\n/addword - добавление слова в словарь"
                                     "\n пример: /addword apple яблоко\n"
                                     "\n /learn - обучение по карточкам"
                                     "\n пример: /learn 5 (карточка на 5 слов)")


if __name__ == "__main__":
    bot.infinity_polling()
