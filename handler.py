from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ContentType
from aiogram.types.callback_query import CallbackQuery
from aiogram.methods.send_contact import SendContact

from language import text, get_list 
import kb
from user import get_user, update_user
import request
from table import get_promo


users = []

router = Router()
msgs = {}

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = get_user(message.from_user.id)
    user.mode = "none"

    await message.answer(text("START", user.lang), reply_markup=kb.start(user.lang))


@router.message(Command("language"))
async def command_language_handler(message: Message) -> None:
    user = get_user(message.from_user.id)
    user.mode = "none"
    await message.answer(text("CHANGE_LANG", user.lang), reply_markup=kb.lang())


for el in get_list():
    @router.callback_query(F.data == el)
    async def profile(clbck: CallbackQuery):
        user = get_user(clbck.from_user.id)
        user.mode = "none"

        await clbck.message.edit_reply_markup()
        update_user(user.id, lang=clbck.data)
        await clbck.message.answer(text("LANG_SUCCESS", user.lang))
        await clbck.message.answer(text("DEFAULT_MESSAGE", user.lang), reply_markup=kb.start(user.lang))

"""
@router.callback_query()
async def profile(clbck: CallbackQuery):
    await clbck.message.answer("Hi")

"""


@router.callback_query(F.data == "register")
async def profile(clbck: CallbackQuery):
    user = get_user(clbck.from_user.id)
    user.mode = "register"

    await clbck.message.edit_reply_markup()
    await clbck.message.answer(text("REGISTRATE", user.lang), reply_markup=kb.back(user.lang))


@router.callback_query(F.data == "back")
async def profile(clbck: CallbackQuery):
    user = get_user(clbck.from_user.id)
    user.mode = "none"

    await clbck.message.edit_reply_markup()
    await clbck.message.answer(text("DEFAULT_MESSAGE", user.lang), reply_markup=kb.start(user.lang))


@router.callback_query(F.data == "confirm_user")
async def profile(clbck: CallbackQuery):
    user = get_user(clbck.from_user.id)
    if user.mode != "confirmation_user":
        return
    user.mode = "none"

    await clbck.message.edit_reply_markup()
    promo = get_promo(user.promos[-1])

    if await request.check_promo(user.login, user.email, user.name, user.last_name, "1", promo["group_id"], promo["course_id"]):
        await clbck.message.answer(text("SUCCEFUL", user.lang, promo["course_name"]))
        await clbck.message.answer(text("LINK", user.lang, "*link*"), reply_markup=kb.back(user.lang))
    else:
        await clbck.message.answer(text("FAIL", user.lang), reply_markup=kb.back(user.lang))


@router.callback_query(F.data == "create_new")
async def profile(clbck: CallbackQuery):
    user = get_user(clbck.from_user.id)
    if user.mode != "confirmation_user":
        return
    user.mode = "login"

    await clbck.message.edit_reply_markup()
    await clbck.message.answer(text("LOGIN", user.lang), reply_markup=kb.login(clbck.message.from_user.username))


@router.callback_query(F.data == "confirm_promo")
async def profile(clbck: CallbackQuery):
    user = get_user(clbck.from_user.id)
    if user.mode != "confirmation_promo":
        return
    user.mode = "none"

    await clbck.message.edit_reply_markup()
    if user.callback != "" and user.email != "" and user.login != "" and user.name != "" and user.last_name != "":
        user.mode = "confirmation_user"
        await clbck.message.answer("<code>" + text("USER_DATA", user.lang, user.name, user.last_name, user.login,
                                user.email) + "</code>", reply_markup=kb.confirm_data(user.lang))
    else:
        user.mode = "login"
        await clbck.message.answer(text("LOGIN", user.lang), reply_markup=kb.login(clbck.message.from_user.username))


@router.callback_query(F.data == "new_promo")
async def profile(clbck: CallbackQuery):
    user = get_user(clbck.from_user.id)
    if user.mode != "confirmation_promo":
        return
    user.mode = "register"

    await clbck.message.edit_reply_markup()
    await clbck.message.answer(text("REGISTRATE", user.lang), reply_markup=kb.back(user.lang))


@router.message()
async def mes(message: Message) -> None:
    user = get_user(message.from_user.id)
    msg = message.text

    if user.mode == "register":

        promo = get_promo(msg)
        if promo != None:
            user.mode = "confirmation_promo"
            promos = user.promos
            if msg in promos:
                promos.remove(msg)
            promos.append(msg)
            update_user(user.id, promos=promos)
            await message.answer("<code>" + text("TABLE", user.lang, promo["promo"], "{}-{}".format(promo["start"], promo["end"]),
                                    promo["course_name"], promo["group_id"]) + "</code>", reply_markup=kb.confirm_promo(user.lang))
            #await message.answer(text("CONFIRMATE", user.lang), reply_markup=kb.confirm(user.lang))                     

        else:
            await message.answer(text("WRONG_PROMO", user.lang))
            await message.answer(text("REGISTRATE", user.lang), reply_markup=kb.back(user.lang))

    elif user.mode == "login":
        for i in msg:
            if "qwertyuiopasdfghjklzxcvbnm_-.@1234567890".find(i) == -1:
                await message.answer(text("WRONG_LOGIN", user.lang))
                await message.answer(text("LOGIN", user.lang), reply_markup=kb.login(message.from_user.username))
                return
        user.mode = "name"
        update_user(user.id, login=msg)
        await message.answer(text("NAME", user.lang), reply_markup=kb.name(message.from_user))

    elif user.mode == "name":
        a = msg.split()
        if len(a) != 2:
            await message.answer(text("NAME", user.lang), reply_markup=kb.name(message.from_user))
            return
        
        update_user(user.id, name=a[0], last_name=a[1])
        user.mode = "email"
        await message.answer(text("EMAIL", user.lang))
        # user.mode = "number"
        # await message.answer(text("WRITE_NUM", user.lang), reply_markup=kb.phone(user.lang))


    # elif user.mode == "number":
    #     if message.contact != None:
    #         update_user(user.id, callback=message.contact.phone_number)
    #     else:
    #         tel = msg.replace(" ", "").replace("+", "").replace("-", "").replace("(", "").replace(")", "")
    #         if len(tel) != 11:
    #             await message.answer(text("WRONG_NUM", user.lang))
    #             await message.answer(text("WRITE_NUM", user.lang), reply_markup=kb.phone(user.lang))
    #             return
    #         if tel[0] == "8":
    #             tel = "7" + tel[-10:]
    #         if not tel.isnumeric():
    #             await message.answer(text("WRONG_NUM", user.lang))
    #             await message.answer(text("WRITE_NUM", user.lang), reply_markup=kb.phone(user.lang))
    #             return
    #         update_user(user.id, callback=tel)
    #     user.mode = "email"
    #     await message.answer(text("EMAIL", user.lang))


    elif user.mode == "email":
        if len(msg.split("@")) == 2:
            if len(msg.split("@")[1].split(".")) >= 2:
                user.mode = "confirmation_user"
                update_user(user.id, email=msg)

                await message.answer("<code>" + text("USER_DATA", user.lang, user.name, user.last_name, user.login, user.callback,
                                        user.email) + "</code>", reply_markup=kb.confirm_data(user.lang))
                return
        await message.answer(text("WRONG_EMAIL", user.lang))
        await message.answer(text("EMAIL", user.lang))


def enter_info():
    pass