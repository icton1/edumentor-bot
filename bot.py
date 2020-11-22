from settings import TOKEN, bot
from storage import set_user_info, get_user_info, get_users, clear_storage
from utils import create_new_user_document, get_current_scenario,  set_scenario
from strings import text
from scenarios import scenarios, on_start_scenario
from callbacks import callbacks, on_show_profile_callback
from markup import get_main_menu_markup
from telebot import types


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, text("start_message"))
    state_manager(message)


@bot.message_handler(commands=['users'])
def show_all_users(message):
    usernames = [element["userinfo"]["username"]
                 for element in get_users()]

    bot.send_message(message.chat.id, ", ".join(usernames))


@bot.message_handler(commands=["main"])
def main_scenario(message):
    user_document = get_user_info(message.from_user.id)
    set_scenario(user_document, "on_main_menu_scenario")
    markup = get_main_menu_markup()
    bot.send_message(message.chat.id, text="Главное меню", reply_markup=markup)


@bot.message_handler(commands=['cleardb'])
def clear_db(message):
    clear_storage()
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(
        message.chat.id, "База данных была сброшена", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_manager(call):
    chat_id = call.message.chat.id
    splitted = call.data.split(":", maxsplit=1)
    callback_name = splitted[0]
    callback_params = splitted[1] if len(splitted) != 1 else None
    # bot.send_message(chat_id, "Получен callback: " +
    #  call.data + "\nЗапуск коллбэка " + callback_name)
    try:
        callbacks[callback_name](bot, call, callback_params)
    except KeyError:
        print("Error: key error callbacks[] - " + callback_name)


@bot.message_handler(content_types=['text'])
def state_manager(message):
    scenario_name = get_current_scenario(message)
    # bot.send_message(message.chat.id, "Запуск сценария " + scenario_name)
    try:
        scenarios[scenario_name](bot, message)
    except KeyError:
        print("Error: key error scenarios[] - " + scenario_name)


bot.polling()
