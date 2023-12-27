import telebot
from telebot import types
from database import Database, User

TOKEN = '6230049921:AAH9ivHfC3KVcRSvS-j8fn2Evom3-8zT_K4'
bot = telebot.TeleBot(TOKEN)
db = Database('profit_loss_bot.db')


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    if not db.user_exists(user_id):
        db.create_user(user_id)
    bot.send_message(user_id,
                     "Привет! Этот бот поможет вести учет прибыли и убытков. Используйте /profit и /loss для записи операций, а /report для получения статистики за день.")


@bot.message_handler(commands=['profit'])
def handle_profit(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Введите сумму прибыли:")
    bot.register_next_step_handler(message, process_profit_step)


def process_profit_step(message):
    try:
        user_id = message.chat.id
        amount = float(message.text)
        db.update_balance(user_id, amount)
        bot.send_message(user_id, f"Прибыль в размере {amount} успешно записана!")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")


@bot.message_handler(commands=['loss'])
def handle_loss(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Введите сумму убытка:")
    bot.register_next_step_handler(message, process_loss_step)


def process_loss_step(message):
    try:
        user_id = message.chat.id
        amount = float(message.text)
        db.update_balance(user_id, -amount)
        bot.send_message(user_id, f"Убыток в размере {amount} успешно записан!")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")


@bot.message_handler(commands=['report'])
def handle_report(message):
    user_id = message.chat.id
    balance = db.get_balance(user_id)
    bot.send_message(user_id, f"Ваш текущий баланс: {balance}")


if __name__ == '__main__':
    bot.polling(none_stop=True)
