import telebot
import wikipedia
import requests
from translate import Translator
from telebot import types

from gtts import gTTS
import os


bot = telebot.TeleBot("6601561153:AAF_ZqRm1LBAPmYbnds-S1OfjinRdjS3dlo")

wikipedia.set_lang("ru")


def getWiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split(".")
        wikimas = wikimas[:-1]
        wikitext2 = ""
        for i in wikimas:
            if not ("==" in i):
                if len(i.strip()) > 3:
                    wikitext2 += i + "."
            else:
                break
       
        return wikitext2
    except Exception as e:
        return "Не смог найти, напиши моему создателю: @dbryanya"


@bot.message_handler(commands=["start"])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Запрос вики")
    item2 = types.KeyboardButton("Цитата")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id, "Бот заработал! Готов на ваше растерзание", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(m):
    if m.text.strip() == "Запрос вики":
        messg = bot.send_message(m.chat.id, "Ваш запрос:")
        bot.register_next_step_handler(messg, paper_wiki)
    elif m.text.strip() == "Цитата":
        category = ''
        api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
        response = requests.get(api_url, headers={'X-Api-Key': 'gToZ4BofFqsFMInOtNXU4Q==sVsz22kvfyQ7WBGk'})
        if response.status_code == requests.codes.ok:
            # print(response.text)
            # txt = response.text
            # txt1 = eval(txt)[0]
            # translator = Translator(from_lang="English", to_lang="Russian")
            # txt_En1 = translator.translate(txt1["quote"])
            # txt_En2 = txt1["author"]
            # txt_En3 = txt1["category"]
            # print(str(translator.translate(txt_En1)))

            tts = gTTS(text="Привет", lang="ru")
            tts.save("speech.mp3")

            bot.send_voice(m.chat.id, open("speech.mp3", "rb"))

            os.remove("speech.mp3")


            # bot.send_message(m.chat.id, (txt_En1))
            # bot.send_message(m.chat.id, translator.translate(txt_En2))
            # bot.send_message(m.chat.id, translator.translate(txt_En3))
        else:
            print("Error:", response.status_code, response.text)

def paper_wiki(m):
    bot.send_message(m.chat.id, getWiki(m.text))

bot.polling(none_stop=True, interval=0)
