import secret_file
import telebot
import flask
import re

WEBHOOK_URL_BASE = "https://{}:{}".format(secret_file.WEBHOOK_HOST, secret_file.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(secret_file.TOKEN)

bot = telebot.TeleBot(secret_file.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
app = flask.Flask(__name__)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, который считает количсетво слов в вашем сообщении.")


@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует на любое сообщение
def send_len(message):
    outline = message.text
    outline = re.sub('[!-().?/|\;:]+', '', outline)
    outline = re.sub(' +', ' ', outline)
    outline = re.findall(r'\w+', outline)
    #message_arr = outline.split(' ')
    reply = len(outline)
    bot.send_message(message.chat.id, 'В вашем сообщении {} слов.'.format(reply))


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


if __name__ == '__main__':
    bot.polling(none_stop=True)
