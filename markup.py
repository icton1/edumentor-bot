from telebot import types


def get_main_menu_markup():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text="Посмотреть свой профиль", callback_data="on_show_profile_callback"))
    keyboard.add(types.InlineKeyboardButton(
        text="Найти ментора", callback_data="on_list_all_mentors"))
    keyboard.add(types.InlineKeyboardButton(
        text="Стать ментором", callback_data="on_create_mentor_callback"))
    keyboard.add(types.InlineKeyboardButton(
        text="Удалить свой профиль", callback_data="on_delete_profile_callback"))
    return keyboard
