# -*- coding: utf-8 -*-
from storage import get_user_info, set_user_info, get_users, del_user_info
from utils import create_new_user_document, get_scenario_state, set_scenario_state, set_scenario
from markup import get_main_menu_markup
from telebot import types
from strings import text
from datetime import datetime
import re


class Names:
    names = "names"


def on_start_scenario(bot, message):
    c = Names()
    c.waiting_creation_confirm = "waiting_creation_confirm"
    c.on_start_scenario = "on_start_scenario"
    c.asked_for_nickname = "asked_for_nickname"
    c.yes_i_agree = "Да, давай заведем профиль"
    c.no_disagree = "Нет, отказываюсь"
    c.asked_for_year = "asked_for_year"
    c.asked_for_department = "asked_for_department"
    c.asked_for_groupnumber = "asked_for_groupnumber"
    c.completed_onstart = "completed_onstart"

    def waiting_creation_confirm(userDocument):
        markup = types.ReplyKeyboardRemove(selective=False)
        if message.text == c.yes_i_agree:
            set_scenario_state(userDocument, c.asked_for_nickname)
            bot.send_message(message.chat.id, text(
                "add_nickname_intro"), reply_markup=markup)
            bot.send_message(
                message.chat.id, "Ник может содержать буквы, цифры и пробел")
        elif message.text == c.no_disagree:
            del_user_info(message.from_user.id)
            bot.send_message(
                message.chat.id, "Очень жаль, еще увидимся!", reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup()
            item1 = types.KeyboardButton(c.yes_i_agree)
            item2 = types.KeyboardButton(c.no_disagree)
            markup.row(item1, item2)
            bot.send_message(
                message.chat.id, "Вы возможно случайно отправили сообщение, пожалуйста, используйте кнопки внизу", reply_markup=markup
            )
        return

    def asked_for_nickname(userDocument):
        nickname = message.text.strip()
        # result = re.match(r'^[\w ]+$', nickname)
        result = re.fullmatch(r'^[\w ]+$', nickname)
        if result is not None:
            userDocument["userinfo"]["botnickname"] = message.text
            set_user_info(message.from_user.id, userDocument)
            set_scenario_state(userDocument, c.asked_for_year)
            bot.send_message(message.chat.id, "Никнейм успешно задан: " +
                             userDocument["userinfo"]["botnickname"])
            markup = types.ReplyKeyboardMarkup()
            item1 = types.KeyboardButton(1)
            item2 = types.KeyboardButton(2)
            item3 = types.KeyboardButton(3)
            markup.row(item1, item2, item3)
            item4 = types.KeyboardButton(4)
            item5 = types.KeyboardButton(5)
            item6 = types.KeyboardButton(6)
            markup.row(item4, item5, item6)
            bot.send_message(
                message.chat.id, "Укажите пожалуйста курс обучения", reply_markup=markup)
        else:
            bot.send_message(
                message.chat.id, "Неправильный формат, повторите еще")
        return

    def asked_for_year(userDocument):
        markup = types.ReplyKeyboardRemove(selective=False)
        year = message.text.strip()
        result = re.fullmatch(r'^[0-6]$', year)
        if result is not None:
            curYear = datetime.now().year
            userDocument["userinfo"]["year"] = curYear - int(year)
            set_user_info(message.from_user.id, userDocument)
            set_scenario_state(userDocument, c.asked_for_department)
            bot.send_message(message.chat.id, "Курс обучения успешно задан - " +
                             str(curYear -
                                 int(userDocument["userinfo"]["year"])))
            bot.send_message(
                message.chat.id, "Введите название своего факультета в свободной форме", reply_markup=markup)
        else:
            bot.send_message(
                message.chat.id, "Неправильный формат, повторите еще", reply_markup=markup)
        return

    def asked_for_department(userDocument):
        markup = types.ReplyKeyboardRemove(selective=False)
        department = message.text.strip()
        if department:
            userDocument["userinfo"]["department"] = department
            set_user_info(message.from_user.id, userDocument)
            set_scenario_state(userDocument, c.asked_for_groupnumber)
            bot.send_message(message.chat.id, "Факультут успешно задан - " +
                             userDocument["userinfo"]["department"])
            bot.send_message(
                message.chat.id, "Введите название номер/название своей группы", reply_markup=markup)
        else:
            bot.send_message(
                message.chat.id, "Неправильный формат, повторите еще", reply_markup=markup)
        return

    def asked_for_groupnumber(userDocument):
        groupnumber = message.text.strip()
        if groupnumber:
            userDocument["userinfo"]["groupnumber"] = groupnumber
            set_user_info(message.from_user.id, userDocument)
            set_scenario_state(userDocument, c.completed_onstart)
            set_scenario(userDocument, "on_main_menu_scenario")
            bot.send_message(message.chat.id, "Номер группы успешно задан - " +
                             userDocument["userinfo"]["groupnumber"])
            bot.send_message(
                message.chat.id, "Супер, вы отлично справились с формой регистрации)\nP.S. Не каждый человек выдержит это испытание (* ^ ω ^)")
            bot.send_message(
                message.chat.id, "Теперь ты находишься в главном меню, ниже есть кнопочки, на них можно поклацать =)", reply_markup=get_main_menu_markup()
            )
        else:
            bot.send_message(
                message.chat.id, "Неправильный формат, повторите еще")
        return

    userDocument = get_user_info(message.from_user.id)

    if userDocument is None:
        newDocument = create_new_user_document(message)
        set_scenario(newDocument, c.on_start_scenario)
        set_scenario_state(newDocument, c.waiting_creation_confirm)

        # set_user_info(message.from_user.id, newDocument)
        markup = types.ReplyKeyboardMarkup()
        item1 = types.KeyboardButton(c.yes_i_agree)
        item2 = types.KeyboardButton(c.no_disagree)
        markup.row(item1, item2)

        bot.send_message(
            message.chat.id, text("first_time"),
            reply_markup=markup)

        return

    inner_scenarios = {
        "waiting_creation_confirm": waiting_creation_confirm,
        "asked_for_nickname": asked_for_nickname,
        "asked_for_year": asked_for_year,
        "asked_for_department": asked_for_department,
        "asked_for_groupnumber": asked_for_groupnumber

    }
    scenario_state = get_scenario_state(userDocument)
    print(scenario_state)
    bot.send_message(message.chat.id, "Запуск сценария " + scenario_state)
    inner_scenarios[scenario_state](userDocument)


def on_main_menu_scenario(bot, message):

    bot.send_message(message.chat.id, "Главное меню",
                     reply_markup=get_main_menu_markup())


def on_create_mentor_scenario(bot, message):
    pass


def on_search_for_mentor_scenario(bot, message):
    pass


scenarios = {
    "on_start_scenario": on_start_scenario,
    "on_main_menu_scenario": on_main_menu_scenario,
    "on_create_mentor_scenario": on_create_mentor_scenario,
    "on_search_for_mentor_scenario": on_search_for_mentor_scenario,
}
