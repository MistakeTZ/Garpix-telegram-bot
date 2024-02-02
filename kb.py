from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from language import text, get_list


def start(lang) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=text("REGISTER", lang), callback_data="register")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def lang() -> InlineKeyboardMarkup:
    buttons = []
    for el in get_list():
        buttons.append([InlineKeyboardButton(text=el, callback_data=el)])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back(lang) -> InlineKeyboardMarkup:
    buttons = [
        [KeyboardButton(text=text("BACK", lang), callback_data="back")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def phone(lang) -> InlineKeyboardMarkup:
    buttons = [[KeyboardButton(text=text("PHONE", lang), request_contact=True)]]
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons, one_time_keyboard=True)


def confirm(lang) -> InlineKeyboardMarkup:
    buttons = [[KeyboardButton(text=text("CONFIRM", lang))]]
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons, one_time_keyboard=True)


def login(text) -> InlineKeyboardMarkup:
    buttons = [[KeyboardButton(text=text)]]
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons, one_time_keyboard=True)


def name(user) -> InlineKeyboardMarkup:
    if user.last_name == None:
        return None
    buttons = [[KeyboardButton(text=f"{user.first_name} {user.last_name}")]]
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons, one_time_keyboard=True)


def confirm_data(lang) -> InlineKeyboardMarkup:
    buttons = [
        [KeyboardButton(text=text("CONFIRM", lang), callback_data="confirm_user"),
         KeyboardButton(text=text("CREATE_NEW", lang), callback_data="create_new")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_promo(lang) -> InlineKeyboardMarkup:
    buttons = [
        [KeyboardButton(text=text("CONFIRM", lang), callback_data="confirm_promo"),
         KeyboardButton(text=text("AGAIN", lang), callback_data="new_promo")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)