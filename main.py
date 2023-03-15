import dotenv
import os
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import parsesgas


dotenv.load_dotenv()

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


URL = 'https://auto.ria.com/uk/toplivo/ivano-frankovsk/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.77'}
HOST = 'https://auto.ria.com/uk/toplivo/ivano-frankovsk'

def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("OKKO")
    btn2 = types.KeyboardButton("WOG")
    btn3 = types.KeyboardButton("АВІАС")
    btn4 = types.KeyboardButton("УКРНАФТА")
    markup.add(btn1, btn2, btn3, btn4)

    start_mess = "Виберіть заправку"
    bot.send_message(message.chat.id, start_mess, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def gas_prices(message):
    html = get_html(URL)
    prices_gas = parsesgas.get_content(html.text)

    PRICES_OKKO = prices_gas[0]
    PRICES_WOG = prices_gas[1]
    PRICES_AVIAS = prices_gas[2]
    PRICES_UKRNAFTA = prices_gas[4]

    gas_select_okko = types.InlineKeyboardMarkup()
    bt1_okko = types.InlineKeyboardButton("а-95+", callback_data='a-95+OKKO')
    bt2_okko = types.InlineKeyboardButton("а-95", callback_data='a-95OKKO')
    bt3_okko = types.InlineKeyboardButton("а-92", callback_data='a-92OKKO')
    bt4_okko = types.InlineKeyboardButton("дп", callback_data='дпOKKO')
    bt5_okko = types.InlineKeyboardButton("газ", callback_data='газOKKO')
    gas_select_okko.add(bt1_okko, bt2_okko, bt3_okko, bt4_okko, bt5_okko)

    gas_select_wog = types.InlineKeyboardMarkup()
    bt1_wog = types.InlineKeyboardButton("а-95+", callback_data='a-95+WOG')
    bt2_wog = types.InlineKeyboardButton("а-95", callback_data='a-95WOG')
    bt3_wog = types.InlineKeyboardButton("а-92", callback_data='a-92WOG')
    bt4_wog = types.InlineKeyboardButton("дп", callback_data='дпWOG')
    bt5_wog = types.InlineKeyboardButton("газ", callback_data='газWOG')
    gas_select_wog.add(bt1_wog, bt2_wog, bt3_wog, bt4_wog, bt5_wog)

    gas_select_avias = types.InlineKeyboardMarkup()
    bt1_avias = types.InlineKeyboardButton("а-95+", callback_data='a-95+AVIAS')
    bt2_avias = types.InlineKeyboardButton("а-95", callback_data='a-95AVIAS')
    bt3_avias = types.InlineKeyboardButton("а-92", callback_data='a-92AVIAS')
    bt4_avias = types.InlineKeyboardButton("дп", callback_data='дпAVIAS')
    bt5_avias = types.InlineKeyboardButton("газ", callback_data='газAVIAS')
    gas_select_avias.add(bt1_avias, bt2_avias, bt3_avias, bt4_avias, bt5_avias)

    gas_select_ukrnafta = types.InlineKeyboardMarkup()
    bt1_ukrnafta = types.InlineKeyboardButton("a-95+", callback_data="a-95+UKRNAFTA")
    bt2_ukrnafta = types.InlineKeyboardButton("a-95", callback_data="a-95UKRNAFTA")
    bt3_ukrnafta = types.InlineKeyboardButton("a-92", callback_data="a-92UKRNAFTA")
    bt4_ukrnafta = types.InlineKeyboardButton("дп", callback_data="дпUKRNAFTA")
    bt5_ukrnafta = types.InlineKeyboardButton("газ", callback_data="газUKRNAFTA")
    gas_select_ukrnafta.add(bt1_ukrnafta, bt2_ukrnafta, bt3_ukrnafta, bt4_ukrnafta, bt5_ukrnafta)

    get_message_bot = message.text.strip().lower()
    if get_message_bot == "okko" or get_message_bot == "окко":
        bot.send_message(message.chat.id, 'Вибери бензіну на {}'.format(message.text), reply_markup=gas_select_okko)
    elif get_message_bot == "wog":
        bot.send_message(message.chat.id, 'Вибери бензіну на {}'.format(message.text), reply_markup=gas_select_wog)
    elif get_message_bot == "авіас":
        bot.send_message(message.chat.id, 'Вибери бензіну на {}'.format(message.text), reply_markup=gas_select_avias)
    elif get_message_bot == "urknafta" or get_message_bot == "укрнафта":
        bot.send_message(message.chat.id, 'Вибери бензіну на {}'.format(message.text), reply_markup=gas_select_ukrnafta)
    else:
        bot.send_message(message.chat.id, 'Давай нормальне питання')
    #print(PRICES)
    #bot.send_message(message.chat.id, 'Вибери бензіну на {}'.format(message.text), reply_markup=gas_select)

    @bot.callback_query_handler(func=lambda call:True)
    def call_back(call):
        if call.data == "a-95+OKKO":
            bot.send_message(call.message.chat.id, PRICES_OKKO['a-95+'])
        elif call.data == "a-95+WOG":
            bot.send_message(call.message.chat.id, PRICES_WOG['a-95+'])
        elif call.data == "a-95+AVIAS":
            bot.send_message(call.message.chat.id, PRICES_AVIAS['a-95+'])
        elif call.data == "a-95+UKRNAFTA":
            bot.send_message(call.message.chat.id, PRICES_UKRNAFTA['a-95+'])
        elif call.data == "a-95OKKO":
            bot.send_message(call.message.chat.id, PRICES_OKKO['a-95'])
        elif call.data == "a-95WOG":
            bot.send_message(call.message.chat.id, PRICES_WOG['a-95'])
        elif call.data == "a-95AVIAS":
            bot.send_message(call.message.chat.id, PRICES_AVIAS['a-95'])
        elif call.data == "a-95UKRNAFTA":
            bot.send_message(call.message.chat.id, PRICES_UKRNAFTA['a-95'])
        elif call.data == "a-92OKKO":
            bot.send_message(call.message.chat.id, PRICES_OKKO['a-92'])
        elif call.data == "a-92WOG":
            bot.send_message(call.message.chat.id, PRICES_WOG['a-92'])
        elif call.data == "a-92AVIAS":
            bot.send_message(call.message.chat.id, PRICES_AVIAS['a-92'])
        elif call.data == "a-92UKRNAFTA":
            bot.send_message(call.message.chat.id, PRICES_UKRNAFTA['a-92'])
        elif call.data == "дпOKKO":
            bot.send_message(call.message.chat.id, PRICES_OKKO['дп'])
        elif call.data == "дпWOG":
            bot.send_message(call.message.chat.id, PRICES_WOG['дп'])
        elif call.data == "дпAVIAS":
            bot.send_message(call.message.chat.id, PRICES_AVIAS['дп'])
        elif call.data == "дпUKRNAFTA":
            bot.send_message(call.message.chat.id, PRICES_UKRNAFTA['дп'])
        elif call.data == "газOKKO":
            bot.send_message(call.message.chat.id, PRICES_OKKO['газ'])
        elif call.data == "газWOG":
            bot.send_message(call.message.chat.id, PRICES_WOG['газ'])
        elif call.data == "газAVIAS":
            bot.send_message(call.message.chat.id, PRICES_AVIAS['газ'])
        elif call.data == "газUKRNAFTA":
            bot.send_message(call.message.chat.id, PRICES_UKRNAFTA['газ'])



bot.polling()