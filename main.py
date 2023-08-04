import telebot as telebot
from pyTONPublicAPI import pyTONPublicAPI
from telebot.apihelper import approve_chat_join_request

BOT_TOKEN = 'YourBotToken'
bot = telebot.TeleBot(BOT_TOKEN)


def approve(message):
    global chat_id
    user_id = message.from_user.id
    address = message.text
    client = pyTONPublicAPI()
    is_premium = message.from_user.is_premium
    try:
        balanse = client.get_address_balance(address=address)
        if balanse > 0 or is_premium:
            bot.send_message(user_id, 'Твоя заявка одобрена')
            approve_chat_join_request(token=BOT_TOKEN, chat_id=chat_id, user_id=user_id)
        else:
            msg = bot.send_message(user_id, 'На твоем аккаунте нет  Telegram Premium,'
                                            'а на кошельке нет нужной NFT. повторите '
                                            'попытку после покупки Telegram Premium '
                                            'или пополнения кошелька')
            bot.register_next_step_handler(msg, test)
    except Exception:
        msg = bot.send_message(user_id, 'Неверный адрес кошелька. Повторите попытку')
        bot.register_next_step_handler(msg, test)


@bot.chat_join_request_handler()
def main(message: telebot.types.ChatJoinRequest):
    global chat_id
    chat_id = message.chat.id
    msg = bot.send_message(message.user_chat_id,
                           'Привет, ты подал заявку на закрытый чат. Чтобы тебя принять, '
                           'привяжи свой TON кошелек к боту. '
                           'Этого будет достаточно, чтобы твоя заявка была одобрена. '
                           'Если на нём будет найдена минимум 1 NFT из нижеуказанных '
                           'коллекций, либо активируй Telegram Premium')
    bot.register_next_step_handler(msg, test)


bot.infinity_polling(allowed_updates=telebot.util.update_types)
