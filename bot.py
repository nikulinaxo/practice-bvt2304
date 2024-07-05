import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

import vacancies
import db

TOKEN = '7471656640:AAEGx0xXM_Q4-Ms0wITshLqMydMMfOY3NIA'

dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    if db.addUser(message.from_user.id):
        print("новый пользователь добавлен в базу данных")
    await message.answer(f"Привет, {message.from_user.first_name}!"
                         '\n\n'
                         f'Пример для поиска вакансий:\n{html.bold('/search Python разработчик Москва')}')


class Form(StatesGroup):
    job = State()
    sch = State()
    exp = State()

data = []

hiddenData = []

@dp.message(Command('search'))
async def search(message: Message, state: FSMContext):

    query = message.text[8::]

    data.append(query)
    hiddenData.append(query)

    schs = []

    schs.append([KeyboardButton(text='Полный день')])
    schs.append([KeyboardButton(text='Сменный график')])
    schs.append([KeyboardButton(text='Гибкий график')])
    schs.append([KeyboardButton(text='Удаленно')])
    schs.append([KeyboardButton(text='Вахта')])



    await message.answer(f'🔍 Ищем {query}\nУкажите график работы', reply_markup=ReplyKeyboardMarkup(keyboard=schs, one_time_keyboard=True, resize_keyboard=True))
    await state.set_state(Form.sch)


@dp.message(F.text, Form.sch)
async def getExp(message: Message, state: FSMContext):

    data.append(message.text)

    exp = []

    exp.append([KeyboardButton(text='Без опыта')])
    exp.append([KeyboardButton(text='От года до трех')])
    exp.append([KeyboardButton(text='От трех до шести')])
    exp.append([KeyboardButton(text='Более шести')])

    await message.answer(f'И требования к опыту...', reply_markup=ReplyKeyboardMarkup(keyboard=exp, one_time_keyboard=True, resize_keyboard=True))
    await state.set_state(Form.exp)

@dp.message(F.text, Form.exp)
async def final(message: Message, state: FSMContext):

    data.append(message.text)

    await message.answer(f"🔍 Ищем вакансии\n"
                         f"{data[0]}\n"
                         f"{data[1]}\n"
                         f"{data[2]}")

    await state.clear()

    match data[1]:
        case 'Полный день':
            data[1] = 'fullDay'
        case 'Сменный график':
            data[1] = 'shift'
        case 'Гибкий график':
            data[1] = 'flexible'
        case 'Удаленно':
            data[1] = 'remote'
        case 'Вахта':
            data[1] = 'flyInFlyOut'

    match data[2]:
        case 'Без опыта':
            data[2] = 'noExperience'
        case 'От года до трех':
            data[2] = 'between1And3'
        case 'От трех до шести':
            data[2] = 'between3And6'
        case 'Более шести':
            data[2] = 'moreThan6'

    for vac in vacancies.get(data[0], data[2], data[1]):

        btns = []

        btns.append([InlineKeyboardButton(text="Подробнее...", url=vac['url'])])



        await message.answer(html.bold(vac['name']) +
                             f'\n{html.italic('в г.' + vac['area'])}\n\nТребования: \n' +
                             html.code(vac['req']) +
                             f'\n\nЗарплата: {html.bold(vac['sal'])}', reply_markup=InlineKeyboardMarkup(inline_keyboard=btns))

    data.clear()


@dp.message(Command('stats'))
async def stats(message: Message):

    userCount = db.getUserCount()
    popular = db.getPopular()

    await message.answer(html.bold('Количество пользователей:'
                                   f'\n{userCount}'
                                   f'\n\nСамая популярная вакансия:'
                                   f'{html.italic(popular[0])}'
                                   f'\n{html.bold(popular[1])} вакансий'))


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

