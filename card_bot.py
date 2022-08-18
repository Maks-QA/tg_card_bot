# подключение библиотек
# В google colab добавить: !pip install pyTelegramBotAPI
# В google colab добавить: !pip install Faker
# для установки необходимо в файл requirements.text добавить строки
# 'PyTelegramBotApi'
# 'faker'

from telebot import TeleBot, types
from faker import Faker


bot = TeleBot(token='нужно вставить сюда свой токен', parse_mode='html') # создание бота

faker = Faker() # утилита для генерации номеров кредитных карт


# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    sti = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    
    bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Привет, <b>{0.first_name}</b>👻!\nЯ могу сгенерировать для тебя номер тестовой банковской карты.\nДля этого выбери, пожалуйста, тип карты:'.format(message.from_user, bot.get_me()), # текст сообщения
        parse_mode='html',
        reply_markup=card_type_keybaord,
    )


# объект клавиаутры
card_type_keybaord = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
card_type_keybaord.row(
    types.KeyboardButton(text='VISA🟦'),
    types.KeyboardButton(text='Mastercard🔴🟡'),
    types.KeyboardButton(text='Maestro🔴🔵'),
)



# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    # проверяем текст сообщения на совпадение с текстом какой либо из кнопок
    # в зависимости от типа карты присваем занчение переменной 'card_type'
    if message.text == 'VISA🟦':
        card_type = 'visa'
    elif message.text == 'Mastercard🔴🟡':
        card_type = 'mastercard'
    elif message.text == 'Maestro🔴🔵':
        card_type = 'maestro'
    else:
        # если текст не совпал ни с одной из кнопок 
        # выводим ошибку
        bot.send_message(
            chat_id=message.chat.id,
            text='Прости, я всего лишь робот и понимаю только запрограммированные кнопки 😔',
        )
        return

    # получаем номер тестовой карты выбранного типа
    # card_type может принимать одно из зачений ['maestro', 'mastercard', 'visa13', 'visa16', 'visa19',
    # 'amex', 'discover', 'diners', 'jcb15', 'jcb16']
    card_number = faker.credit_card_number(card_type)
    # и выводим пользователю
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Тестовая карта {card_type}:\n<code>{card_number}</code>'
    )


# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
