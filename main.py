import requests
from bs4 import BeautifulSoup
import telebot
import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])  # Запускаем бот
def welcome_start(message):
    bot.send_message(message.chat.id, 'Приветствую! Чтобы узнать праздник по дате нажмите /holiday \n')


@bot.message_handler(commands=['holiday', 'date'])  # Выводим список команд
def holiday(message):
    print(message.text)
    if message.text == '/holiday':
        bot.send_message(message.chat.id, 'Введите дату в формате "1 января"')

        @bot.message_handler(content_types=['text'])
        def holy(message):
            a = message.text
            url = 'https://www.calend.ru/holidays/belorus/'
            source = requests.get(url)
            soup = BeautifulSoup(source.text, 'lxml')
            table = soup.find('div', {'class': 'block datesList'})
            ul = table.find_all('li')
            dates = []
            for i in ul:
                elem = i.find('span', {'class': 'dataNum'})
                dates.append(elem.text[:-3])
            descrips = []
            for j in ul:
                desc = j.find('span', {'class': 'caption'})
                for h in desc:
                    descrips.append(h.text.strip())
            descrips = [x for x in descrips if x]
            descrips = [el for i, el in enumerate(descrips) if not i%2]
            final_dict = {}
            for i in range(len(dates)):
                final_dict[dates[i]] = descrips[i]

            print(final_dict)
            answer = 'В этот день праздников нет!'
            for name in final_dict.keys():
                if name == a:
                    answer = (final_dict[name])
            bot.send_message(message.chat.id, answer)


bot.polling()  # запускаем бота