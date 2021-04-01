import subprocess

import transliterate
from aiogram import types
import re
import datetime

# Если запускаете код отдельно от этого репозитория, то закомментируйте следующую строку:
from aiogrambot.misc import dp
from pyad import pyad

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# ... и замените её на:
# from misc import dp
pyad.set_defaults(ldap_server="domenname.corp", username="admin", password="adminpassword")  # от какого имени использовать АД


@dp.message_handler(content_types=types.ContentTypes.ANY, state="*")
async def all_other_messages(message: types.Message):
    user_message = message.text
    user_message = user_message.lower()  # привожу всё к мелким буквам
    if user_message == "кек":
        await message.answer("чебурек")
    elif re.search(r'\bсписок команд\b', user_message):  # СПисок команд
        await message.answer("""
        Писать можно маленькими и большими буквами
        1. Список команд
        ++++++++++++++++++++++++++++++++++++++++++
        2. Закажи ...
        3. Что в списке
        4. Отчисти список
        ++++++++++++++++++++++++++++++++++++++++++
        5. Разблокируй учётку ...(ФИО)
        6. Сбрось пароль ...(ФИО)
        7. Выключи учётку ...(ФИО)
        8. Включи учётку ...(ФИО)
        9. открой юсб ... ФИО
        ++++++++++++++++++++++++++++++++++++++++++
        10. Кто дежурит
        
        """)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif re.search(r'\bзакажи\b', user_message):  # СПисок команд
        res = []
        res.append(message.text)
        text = res[0]
        ogrizok = (text[text.find('закажи') + 6:])
        f = open('1.txt', 'a')
        f.write(ogrizok + "\n")
        f.close()
        await message.answer("ща куплю")
        # await message.reply("Этот бот принимает только текстовые сообщения!")
    elif re.search(r'\bчто в списке\b', user_message):
        f = open('1.txt', 'r')
        await message.answer("в списке покупок:  ")
        await message.answer(f.read())
        f.close()
    elif re.search(r'\bотчисти список\b', user_message):
        open('1.txt', 'w').close()
        await message.answer("список закупок теперь пуст")

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif re.search(r'\bразблокируй учётку\b', user_message):  # 'разблокируй учётку Фамилия Имя Отчество'
        res = []
        res.append(message.text)
        text = res[0]
        name = text[text.find('учётку') + 6:]
        try:
            user_ad = pyad.from_cn(name)
            user_ad.update_attribute("lockoutTime", "0")
            await message.answer("учётная запись " + name + " разблокирована ")
        except AttributeError:
            await message.answer("учётная запись " + name + " НЕ НАЙДЕНА !!! ")
    elif re.search(r'\bвыключи учётку\b', user_message):  # 'выключить учётку Фамилия Имя Отчество'
        res = []
        res.append(message.text)
        text = res[0]
        name = text[text.find('учётку') + 6:]
        try:
            user_ad = pyad.from_cn(name)

            user_ad.disable()
            await message.answer("учётная запись " + name + " выключена ")
        except AttributeError:
            await message.answer("учётная запись " + name + " НЕ НАЙДЕНА !!! ")
    elif re.search(r'\bвключи учётку\b', user_message):  # 'включить учётку Фамилия Имя Отчество'
        res = []
        res.append(message.text)
        text = res[0]
        name = text[text.find('учётку') + 6:]
        try:
            user_ad = pyad.from_cn(name)
            user_ad.enable()
            await message.answer("учётная запись " + name + " включена ")
        except AttributeError:
            await message.answer("учётная запись " + name + " НЕ НАЙДЕНА !!! ")
    elif re.search(r'\bсбрось пароль\b', user_message):  # сброс пароля
        res = []
        res.append(message.text)
        text = res[0]
        name = text[text.find('пароль') + 6:]
        try:
            user_ad = pyad.from_cn(name)
            user_ad.set_password("PASSWORD")  # сброс пароля
            await message.answer("учётная запись " + name + " теперь с паролем PASSWORD ")
        except AttributeError:
            await message.answer("учётная запись " + name + " НЕ НАЙДЕНА !!! ")

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif re.search(r'\bкто дежурит\b', user_message):
        now = datetime.datetime.now()
        f = open('АДРЕС ДО ФАЙЛИКА С ДЕРУЖРСТВАМИ', 'r')
        await message.answer(
            "сегодня " + now.strftime("%d-%m-%Y") + " от рождества Христова. \n " + "     Дежурства:  \n" + f.read())

        f.close()

    elif re.search(r'\bоткрой юсб\b', user_message):
        res = []
        res.append(message.text)
        text = res[0]
        name = text[text.find('юсб') + 4:]
        nameEng = transliterate.translit(name, reversed=True)  # инициалы на английском

        a = nameEng.split()
        nameEngTrans = (f'{a[0]}{a[1][0]}{a[2][0]}')
        nameEngTrans = nameEngTrans.replace("'", "")

        try:
            pscommand = 'Add-AdGroupMember -Identity "USB разрешены" -Members {}'.format(nameEngTrans)
            subprocess.Popen(['powershell.exe', pscommand], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            await message.answer(name, " теперь может использовать USB")
        except Exception:
            await message.answer("какие-то сложности")
