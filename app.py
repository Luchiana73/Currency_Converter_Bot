import telebot
from config import TOKEN, keys
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Добро пожаловать в бота обмена валюты! Следуйте этой инструкции.' \
           ' \n Для начала работы введите через пробел:' \
           ' \n- Валюту, которую вы хотите обменять (например, доллар) ' \
           ' \n- Валюту, в которую вы хотите обменять (например, евро) ' \
           ' \n- Сумму для обмена (в цифрах) ' \
           ' \n- Подтвердите операцию\n \
Чтобы увидеть список доступных валют, используйте команду: /currency'

    bot.reply_to(message, text)


@bot.message_handler(commands=['currency'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверно введены параметры. Убедитесь, что вы ввели три значения: '
                               'валюту 1, валюту 2 и сумму.')
        base, quote, amount = values

        total_base = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Произошла ошибка. Проверьте введенные данные и попробуйте снова. \n{e}')
    except ConnectionError:
        bot.reply_to(message,
                     'Произошла ошибка сети. Пожалуйста, проверьте ваше интернет-соединение и попробуйте снова.')
    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
