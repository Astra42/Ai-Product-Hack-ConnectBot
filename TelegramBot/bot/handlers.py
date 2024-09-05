from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import aiohttp#ассинх аналог requests
import bot.keyboards as kb


router = Router()
USERS = {}  # id:User

class Form(StatesGroup):
    name = State()
    about_me = State()
    cv_path = State()
    target = State()

async def update_data(profile_id, data_dict={}):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://localhost:8001/profile/{profile_id}",
                               json=data_dict) as response:
            if response.status == 200:
                print("Данные обновлены успешно!")
            else:
                print(f"Ошибка при отправке данных, статус: {response.status}")

async def get_specific_profile(profile_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://localhost:8001/profile/{profile_id}") as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Ошибка при получении профиля, статус: {response.status}")
                return None


@router.message(CommandStart())
async def start(message: Message):
    hi_str = """Привет! 👋
Это бот коннектор!🤖
Здесь ты можешь поделиться своими интересами🧙‍, увлечениями🤸‍
и описать какого собседника ты хочешь найти 🤠
"""
    await message.answer(hi_str, reply_markup=kb.hi_kb)


@router.callback_query(F.data == 'start_form')
async def greeting(callback: CallbackQuery, state: FSMContext):
    # -------------BD: create user ------------
    user_id = callback.message.from_user.id
    await update_data(user_id)
    # -----------------------------------------
    await state.set_state(Form.name)
    print(f"Added new user {USERS}")
    meet_msg = """Давай познакомимся, как тебя зовут?"""
    await callback.message.answer(meet_msg)


@router.message(Form.name)
async def who_are_you(message: Message, state: FSMContext):
    # -------------BD: fill name ------------
    user_id = message.from_user.id
    await update_data(user_id, {"name": message.text})
    # -----------------------------------------
    await state.update_data(name=message.text)
    await state.set_state(Form.about_me)
    about_msg = """Расскажи о себе, может ты любишь пиво-смузи или управляешь банановой республикой?"""
    await message.answer(about_msg)


@router.message(Form.about_me)
async def get_cv(message: Message, state: FSMContext):
    # -------------BD: fill about_me ------------
    user_id = message.from_user.id
    await update_data(user_id, {"about_me": message.text})
    # -----------------------------------------
    await state.update_data(about_me=message.text)
    await state.set_state(Form.cv_path)
    cv_msg = """Супер! 
Чтобы мы смогли получше тебя узнать, ты можешь дать нам больше подробностей"""
    await message.answer(cv_msg)


@router.message(Form.cv_path)
async def get_target(message: Message, state: FSMContext):
    # -------------BD: fill cv ------------
    user_id = message.from_user.id
    await update_data(user_id, {"cv_path": message.text})
    # -----------------------------------------
    await state.update_data(cv_path=message.text)
    await state.set_state(Form.target)
    target_msg = """Опиши в свободной форме собеседника, которого ты хочешь найти"""
    await message.answer(target_msg)


@router.message(Command("set_profile"))
@router.message(Form.target)
async def ask_confirmation(message: Message, state: FSMContext):
    # -------------BD: fill target ------------
    user_id = message.from_user.id
    await update_data(user_id, {"target": message.text})
    # -----------------------------------------
    user_dict = await get_specific_profile(user_id)
    print(user_dict)
    print(user_dict, type(user_dict))

    user_dict = eval(eval(user_dict))
    print(user_dict, type(user_dict))

    profile_str =f"{user_dict['name']}\n"+\
        f"🧐Обо мне:\n{user_dict['about_me']}\n"+\
        f"📝CV ссылка:\n{user_dict['cv_path']}\n"+\
        f"🔎Ищу:\n{user_dict['target']}"

    await message.answer(profile_str)

    # await state.update_data(target=message.text)
    # await state.set_state(Form.target)
    # target_msg = """Опиши в свободной форме собеседника, которого ты хочешь найти"""
    # await message.answer(target_msg)


@router.callback_query(F.data == 't_shirt')
async def catalog(callback: CallbackQuery):
    await callback.answer("Вы выбрали категорию футболок")
    await callback.message.answer("Вы выбрали категорию футболок")





# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.answer('Привет', reply_markup=kb.main)
#     await message.reply('Как дела')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет', reply_markup=kb.main)
    await message.reply('Как дела')

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("Вы нажали на кнопку помощи")

@router.message(F.text == 'У меня всё хорошо')
async def nice(message: Message):
    await message.answer("Я очень рад")

@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer("Выберите категорию товара", reply_markup=kb.catalog)

@router.callback_query(F.data == 't_shirt')
async def catalog(callback: CallbackQuery):
    await callback.answer("Вы выбрали категорию футболок")
    await callback.message.answer("Вы выбрали категорию футболок")

# @router.message(Command('register'))
# async def register(message: Message, state: FSMContext):
#     await state.set_state(Register.name)
#     await message.answer("Введите ваше имя")
#
# @router.message(Register.name)
# async def register_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(Register.age)
#     await message.answer("Введите ваш возраст")
#
# @router.message(Register.age)
# async def register_age(message: Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await state.set_state(Register.number)
#     await message.answer("Отправьте ваш номер телефона", reply_markup=kb.get_number)
#
# @router.message(Register.number, F.contact)
# async def register_number(message: Message, state: FSMContext):
#     await state.update_data(number=message.contact)
#     data =await state.get_data()
#     await message.answer(f"Ваше имя : {data['name']} \n номер {data['number']}\n лет {data['age']}")
#
#
