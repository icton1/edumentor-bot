from storage import get_user_info, set_user_info, get_users, del_user_info, set_mentor, get_mentors
from utils import create_new_user_document, get_scenario_state, set_scenario_state, set_scenario
from datetime import datetime
from markup import get_main_menu_markup
from telebot import types
from projectdata import categories
import time


def on_show_profile_callback(bot, call, _):
    # bot.answer_callback_query(call.id, "Answer is Yes")
    # bot.send_message(call.message.chat.id, "test")
    msg = ["Профиль:\n"]
    document = get_user_info(call.from_user.id)
    userinfo = document.get("userinfo", {})
    msg.append('Никнейм: {}'.format(userinfo.get(
        "botnickname", "информация отсутствует")))
    curYear = datetime.now().year
    userYear = userinfo.get("year")
    msg.append('Курс обучения: {}'.format((curYear - int(userYear))
                                          if userYear is not None else 'информация отсутствует'))
    msg.append('Факультет: {}'.format(userinfo.get(
        "department", "информация отсутствует")))
    msg.append('Группа: {}'.format(userinfo.get(
        "groupnumber", "информация отсутствует")))

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 2
    keyboard.add(types.InlineKeyboardButton(
        text="Вернуться назад", callback_data="on_main_menu_callback"))
    keyboard.add(types.InlineKeyboardButton(
        text="Удалить профиль", callback_data="on_delete_profile_callback"))
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id, text="\n".join(msg), reply_markup=keyboard)


def on_main_menu_callback(bot, call, _):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id, text="Главное меню",
                          reply_markup=get_main_menu_markup())


def on_delete_profile_callback(bot, call, _):
    del_user_info(call.from_user.id)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id, text="Профиль был успешно удален\n\nНачать все сначала?\nВведите /start")


def empty_callback(bot, call, _):
    pass


def on_create_mentor_callback(bot, call, _):
    # user_document = get_user_info(call.from_user.id)
    # set_scenario(user_document, "on_create_mentor_scenario")
    # set_scenario_state(user_document, "start")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 2
    for cat_name in categories.keys():
        keyboard.add(types.InlineKeyboardButton(
            text=cat_name,
            callback_data="on_create_mentor_field_callback:{}".format(cat_name)))

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="Вам надо выбрать дисциплину",
                          reply_markup=keyboard)


def on_create_mentor_field_callback(bot, call, param):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 2
    courses = categories.get(param, None)
    if courses is None:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Была выбрана дисциплина '{}'\nВ данный момент в этой дисциплине нет доступных тем".format(
                                  param)
                              )
    for course_key in courses.keys():
        keyboard.add(types.InlineKeyboardButton(
            text=courses[course_key],
            callback_data="on_create_mentor_course_callback:{}:{}".format(param, course_key)))

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="Была выбрана дисциплина '{}\nТеперь надо выбрать тему'".format(
                              param),
                          reply_markup=keyboard
                          )


def on_create_mentor_course_callback(bot, call, params):
    field, topic = params.split(":", maxsplit=2)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text="Вернуться на главное меню",
        callback_data="on_main_menu_callback"))
    topic_name = categories.get(field)
    if topic_name is not None:
        set_mentor(call.from_user.id, field, topic)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Поздравляем, теперь вы появились в списке менторов по теме {}'".format(
                                  topic_name.get(topic)),
                              reply_markup=keyboard
                              )
    else:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Что-то пошло не так",
                              reply_markup=keyboard
                              )


def on_list_all_mentors(bot, call, _):
    bot.send_message(call.message.chat.id,
                     "Список всех зарегистрированных менторов")
    mentors = get_mentors()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text="Вернуться на главное меню",
        callback_data="on_main_menu_callback"))
    print(mentors)
    for mentor in mentors:
        mentorInfo = get_user_info(mentor["user_id"])
        msg = []
        msg.append("Никнейм: " + mentorInfo["userinfo"]["botnickname"])
        msg.append("Факультет: " + mentorInfo["userinfo"]["department"])
        msg.append("Номер группы: " + mentorInfo["userinfo"]["groupnumber"])
        msg.append("Дисциплина: " + mentor["field"])
        msg.append("Тема: " + categories[mentor["field"]][mentor["topic"]])
        bot.send_message(call.message.chat.id, text="\n".join(msg))
        # time.sleep(0.2)
    bot.send_message(
        call.message.chat.id, "Главное меню", reply_markup=get_main_menu_markup()
    )


callbacks = {
    "on_show_profile_callback": on_show_profile_callback,
    "on_main_menu_callback": on_main_menu_callback,
    "on_delete_profile_callback": on_delete_profile_callback,
    "empty_callback": empty_callback,
    "on_create_mentor_callback": on_create_mentor_callback,
    "on_create_mentor_field_callback": on_create_mentor_field_callback,
    "on_create_mentor_course_callback": on_create_mentor_course_callback,
    "on_list_all_mentors": on_list_all_mentors
}
