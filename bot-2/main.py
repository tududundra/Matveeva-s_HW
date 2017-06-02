import telebot  # импортируем модуль pyTelegramBotAPI
import conf  # импортируем наш секретный токен
import flask
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()
import re
import random

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Приветики😁")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Этот бот умеет делать прикольный бред")


@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует на любое сообщение
def send_respon(message):
    f = open('full_data.txt', 'r', encoding='UTF-8')
    full_data = f.readlines()
    f.close()
    d = {}
    for st in full_data:
        st_1 = st.split(':')
        st_2 = st_1[1].strip('\n')
        d[st_1[0]] = st_2.split(',')
    message_arr = message.text.split()
    resp = ''
    random_word = ''
    for el in message_arr:
        el = el.strip('.,?!();:')
        print(el)
        ana = morph.parse(el)
        form = ana[0]
        PofS = form.tag.POS
        gram_1 = str(form.tag)
        gram_2 = re.sub(' ', ',', gram_1)
        gram = gram_2.split(',')
        print(gram)
        if 'NOUN' in gram:
            gram.remove('NOUN')
            if 'anim' in gram:
                gram.remove('anim')
                if 'femn' in gram:
                    gram.remove('femn')
                    random_word = random.choice(d['NOUN, anim, femn'])
                elif 'masc' in gram:
                    gram.remove('masc')
                    random_word = random.choice(d['NOUN, anim, masc'])
                elif 'neut' in gram:
                    gram.remove('neut')
                    random_word = random.choice(d['NOUN, anim, neut'])
            else:
                gram.remove('inan')
                if 'femn' in gram:
                    gram.remove('femn')
                    random_word = random.choice(d['NOUN, inan, femn'])
                elif 'masc' in gram:
                    gram.remove('masc')
                    random_word = random.choice(d['NOUN, inan, masc'])
                elif 'neut' in gram:
                    gram.remove('neut')
                    random_word = random.choice(d['NOUN, inan, neut'])
        elif PofS == None:
            resp = resp + el + ' '
        elif 'VERB' in gram:
            gram.remove('VERB')
            if 'perf' in gram:
                gram.remove('perf')
                if 'intr' in gram:
                    gram.remove('intr')
                    random_word = random.choice(d['VERB, perf, intr'])
                elif 'tran' in gram:
                    gram.remove('tran')
                    random_word = random.choice(d['VERB, perf, tran'])
            elif 'impf' in gram:
                gram.remove('impf')
                if 'intr' in gram:
                    gram.remove('intr')
                    random_word = random.choice(d['VERB, impf, intr'])
                elif 'tran' in gram:
                    gram.remove('tran')
                    random_word = random.choice(d['VERB, impf, tran'])
        elif 'INFN' in gram:
            gram.remove('INFN')
            if 'perf' in gram:
                gram.remove('perf')
                if 'intr' in gram:
                    gram.remove('intr')
                    random_word = random.choice(d['INFN, perf, intr'])
                elif 'tran' in gram:
                    gram.remove('tran')
                    random_word = random.choice(d['INFN, perf, tran'])
            elif 'impf' in gram:
                gram.remove('impf')
                if 'intr' in gram:
                    gram.remove('intr')
                    random_word = random.choice(d['INFN, impf, intr'])
                elif 'tran' in gram:
                    gram.remove('tran')
                    random_word = random.choice(d['INFN, impf, tran'])
        else:
            gram.remove(PofS)
            random_word = random.choice(d[PofS])
            print(random_word)
        word_morph = morph.parse(random_word)
        i = 0
        if gram != []:
            gram_fin = set(gram)
            new_word = word_morph[i].inflect(gram_fin)
            #print(new_word)
            if new_word == None:
                resp = resp + random_word + ' '
            else:
                needed_word = new_word.word
                #print(needed_word)
                resp = resp + needed_word + ' '
        else:
            print('я сюда дошел')
            resp = resp + random_word + ' '
    full_resp = resp.capitalize()
    print(full_resp)
    bot.send_message(message.chat.id, full_resp)


# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)