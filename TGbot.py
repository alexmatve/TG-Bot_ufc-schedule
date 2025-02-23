import telebot
from telebot import types
from data_mining import df
import pandas as pd
import random
import urllib

bot = telebot.TeleBot('7566720309:AAEYv2k1YRVBGFwBSSRUFB1rV-XMBc7tkbo')


@bot.message_handler(commands=['help'])
def help_info(message):
    messange_to_send = "/event - получить информацию про конкретный инвент"


@bot.message_handler(commands=['event'])
def event_info(message):
    events = df.index

    markup = types.InlineKeyboardMarkup()
    for event in events:
        markup.add(types.InlineKeyboardButton(event, callback_data=event))
    markup.add(types.InlineKeyboardButton('Сделать ставку',
                                          url='https://verdictmma.com'))
    bot.send_message(message.chat.id, 'Choose an event', reply_markup=markup)

    # with open('out.jpg', 'wb') as f:
    #     url = 'https://sun9-3.userapi.com/s/v1/ig2/0cSFNhutXvFfaCnoqBPw9QbZ99sBlsHwhGtIbP5DwlthYwapSU4_JIi2ug6OLw4PfPJddnm1iiovHJLAyxuE3zYk.jpg?quality=95&crop=0,0,577,654&as=32x36,48x54,72x82,108x122,160x181,240x272,360x408,480x544,540x612,577x654&from=bu&u=qsXK6b7IJCmytPiu5BKPccs-HsgD8RCCFYr9dIzH2Zk&cs=577x654'
    #     f.write(urllib.request.urlopen(url).read())
    with open('card.jpg', 'rb') as image:
        bot.send_photo(message.chat.id, image)


@bot.callback_query_handler(func=lambda callback: True)
def get_info_event(callback):
    markup = types.InlineKeyboardMarkup()
    message_to_send = f"*{callback.data.upper()}*"
    date = df.loc[callback.data, 'date']
    main_card = df.loc[callback.data, 'main_card']
    prelims = df.loc[callback.data, 'prelims']
    events = df.loc[callback.data, 'events']
    message_to_send += f"\n_Date: \n{date}_"
    if events is None:
        message_to_send += "\n\n*MAIN CARD:* \n" + "• " + "\n• ".join(
            main_card) + "\n\n*PRELIMS:* \n" + "• " + "\n• ".join(prelims)
    else:
        message_to_send += "\n\n*FIGHT CARD:* \n" + "• " + "\n• ".join(events)
    bot.send_message(callback.message.chat.id, message_to_send, parse_mode='Markdown')
    markup.add(types.InlineKeyboardButton('Сделать ставку',
                                          url='https://verdictmma.com'))
    with open(f'stickers/{random.randint(1, 49)}.webm', 'rb') as stick:
        bot.send_sticker(callback.message.chat.id, stick, reply_markup=markup)


bot.polling(none_stop=True)
