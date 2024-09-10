import os.path

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import aiohttp #ассинх аналог requests
import keyboards as kb

import asyncio
from typing import Union, Optional

router = Router()

class Form(StatesGroup): #Состояния для заполнения формы
    name = State()
    about_me = State()
    cv_path = State()
    target = State()

class Editing(StatesGroup):#Состояния для редактирования
    edit_name = State()
    edit_about_me = State()
    edit_cv_path = State()
    edit_target = State()

# \__DELETE_ALL
# Хранение сообщений пользователя и блокировка для синхронизации доступа
user_messages = {} # dict[user: list[message_id]]
user_messages_lock = asyncio.Lock()


async def extract_data_from_message_or_callback(
    message_or_callback: Union[Message, CallbackQuery]
):
    if isinstance(message_or_callback, CallbackQuery): 
        user_id = message_or_callback.from_user.id
        bot = message_or_callback.bot
        message_id = message_or_callback.message.message_id
    elif isinstance(message_or_callback, Message):
        user_id = message_or_callback.from_user.id
        bot = message_or_callback.bot
        message_id = message_or_callback.message_id
    else:
        raise Exception(f"delete_all_messages: Wrong type of message_or_callback {message_or_callback=}")

    return bot, user_id, message_id


async def delete_all_messages(
        message_or_callback: Union[Message, CallbackQuery],
        primary_user_message: Optional[Union[Message, CallbackQuery]] = None
    ) -> None:    
    bot, user_id, _ = await extract_data_from_message_or_callback(message_or_callback)
    
    if primary_user_message is not None:
        _, user_id, _ = await extract_data_from_message_or_callback(primary_user_message)
    global user_messages_lock, user_messages

    print(f'delete_all_messages:{user_id=}')
    async with user_messages_lock:  # Используем блокировку при доступе к user_messages
        print(f'\delete_all_messages: {type(message_or_callback)=} | {user_messages[user_id]=}')

        if user_id in user_messages:
            for message_id in user_messages[user_id]:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=message_id)
                except:
                    pass
            user_messages[user_id] = []
        print(f'/delete_all_messages: {type(message_or_callback)=} | {user_messages[user_id]=} {user_id=}')

async def save_message_id(
        message_or_callback: Union[Message, CallbackQuery],
        primary_user_message: Optional[Union[Message, CallbackQuery]] = None
    ):
    _, user_id, message_id = await extract_data_from_message_or_callback(message_or_callback)
    if primary_user_message is not None:
        _, user_id, _ = await extract_data_from_message_or_callback(primary_user_message)
    
    global user_messages_lock, user_messages
    
    async with user_messages_lock:  # Используем блокировку при доступе к user_messages
        # print(f'\save_message_id: {type(message_or_callback)=} | {user_messages[user_id]=}')
        if user_id not in user_messages:
            user_messages[user_id] = []
        user_messages[user_id].append(message_id)
    
        print(f'/save_message_id: {type(message_or_callback)=} | {user_messages[user_id]=} {user_id=}')

# DELETE_ALL__/ 


# \__NETWORK_REQUEST

async def update_data(profile_id, data_dict={}):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://localhost:8005/profile/{profile_id}",
                               json=data_dict) as response:
            if response.status == 200:
                print("Данные обновлены успешно!")
            else:
                print(f"Ошибка при отправке данных, статус: {response.status}")


async def load_img(profile_id, image):
    async with aiohttp.ClientSession() as session:
        async with session.get(image.file_path) as response:
            image_data = await response.read()
            async with session.post(f"http://localhost:8005/profile/{profile_id}/load_img", data=image_data) as response:
                if response.status == 200:
                    print("Данные обновлены успешно!")
                else:
                    print(f"Ошибка при отправке данных, статус: {response.status}")

async def get_specific_profile(profile_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://localhost:8005/profile/{profile_id}") as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Ошибка при получении профиля, статус: {response.status}")
                return None


async def get_recommendation(profile_id, rec_num=0, refresh=True): #-> List[dict]
    #rec_num - индекс рекомендации в списке на беке
    async with aiohttp.ClientSession() as session:
        request = f"http://localhost:8005/profile/predict_for/{profile_id}/?rec_num={rec_num}&refresh={refresh}"
        async with session.get(request) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Ошибка при получении предсказания, статус: {response.status}")
                return None
async def get_recommendation_cnt(profile_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://localhost:8005/profile/predict_for/{profile_id}/rec_cnt") as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Ошибка при получении профиля, статус: {response.status}")
                return None
# NETWORK_REQUEST__/


# \__RECOMMENDS
#Хранение указателя на порядковый номер просматриваемой анкеты
user_pointers = {} # dict[user: number_of_recomendred_profile]
user_pointers_lock = asyncio.Lock()
# __RECOMMENDS/



@router.message(Command('search_interlocutor_from_menu'))
@router.message(F.text.regexp(r'^\/\d+$'))# если это команды по типу /1 /6 (пишет пользователь)
# @router.callback_query(F.data.startswith('rec_'))# если это коллбеки по типу rec_1 rec_6 (Кнопка далее)
@router.callback_query(F.data == 'search_interlocutor')
@router.message(F.text == '🚀Далее')
@router.message(Command('🚀Далее'))
async def catalog(message: Message, state: FSMContext):
    await state.set_state(None)  # Сразу зануляем все стейты
    print('ВОШЕЛ В КАТОЛОГ')
    # await save_message_id(message)
    # await delete_all_messages(message)
    user_id = message.from_user.id
    #Еще ни разу не пользовался рекомендациями или решил обновиться
    print('user_pointers', user_pointers)
    print(message)
    text = message.text if isinstance(message, Message) else message.data
    if (user_id not in user_pointers.keys() or text.startswith(('search_', '/search_'))) and text != '🚀Далее':
        print('Ни разу не был')
        recommendation = await get_recommendation(user_id)
        if recommendation == '404':
            await answer_by_msg_or_clb(message, "Упс, кажется, Ваша анкета пуста 🙈", reply_markup=kb.fill_pls_kb)
        async with user_pointers_lock:
            user_pointers[user_id] = 1#Указатель на первой анкете

        content = await get_profile_str(1, eval(recommendation))
        await answer_by_msg_or_clb(message, content, reply_markup=kb.get_watch_next_kb_buttons()) # kb.get_watch_next_kb(1)

    # Переключается по анкетам
    else:
        rec_cnt_row = await get_recommendation_cnt(user_id)#Получаем количество рекомендаций на сервере
        rec_cnt = int(eval(rec_cnt_row.replace("len=", "")))
        print(rec_cnt)
        print('Был')
        if text != '🚀Далее':
            text = message.text if isinstance(message, Message) else message.data
            serial_rec_num = int(text.replace('rec_', '').replace('/', ''))#кейс если мы пришли через
        else:
            serial_rec_num = user_pointers[user_id] + 1

        if serial_rec_num > rec_cnt or serial_rec_num < 1:  # recommendation == '404':
            await answer_by_msg_or_clb(message, "На этом всё! 🙈 ", reply_markup=kb.back_to_profile)
            async with user_pointers_lock:
                user_pointers[user_id] = rec_cnt
        else:
            async with user_pointers_lock:
                user_pointers[user_id] = serial_rec_num

            recommendation = await get_recommendation(user_id, rec_num=user_pointers[user_id] - 1, refresh=False)

            content = await get_profile_str(user_pointers[user_id], eval(recommendation))
            await answer_by_msg_or_clb(
                message, content,
                reply_markup=kb.get_watch_next_kb_buttons())# kb.get_watch_next_kb(num=user_pointers[user_id])



@router.message(Command('set_profile'))
@router.callback_query((F.data == 'set_profile'))
async def ask_confirmation(message: Message, state: FSMContext):
    await state.set_state(None)#Сразу зануляем все стейты
    await delete_all_messages(message, message)
    # await delete_all_messages(message.bot, message.from_user.id)    

    user_id = message.from_user.id
    user_dict = await get_specific_profile(user_id)
    if user_dict == '404':
        sent_message = await message.answer("Упс, кажется Ваша анкета пуста 🙈", reply_markup=kb.fill_pls_kb)
    else:
        print(user_dict, type(user_dict))
        print(eval(user_dict), type(eval(user_dict)))

        user_dict = eval(eval(user_dict))
        print(user_dict, type(user_dict))
        print(f'{type(user_dict)=}\n{user_dict=}')

        profile_str =f"{user_dict['name']}, твоя анкета:\n\n"+\
            f"🧐 Обо мне:\n{user_dict['about_me']}\n\n"+\
            f"📝 CV ссылка:\n{user_dict['cv_path']}\n\n"+\
            f"🔎 Ищу:\n{user_dict['target']}"
        try: # Здесь под message скрывается коллебк - обрабатываем его
            sent_message = await message.message.answer(profile_str, reply_markup=kb.profile_kb)
        except Exception: # если не угадали - это обычный message
            sent_message = await message.answer(profile_str, reply_markup=kb.profile_kb)

    await save_message_id(sent_message, message)



@router.message(CommandStart())
async def start(message: Message):
    hi_str = """Привет! 👋
Это бот коннектор! 🤖
Здесь ты можешь поделиться своими интересами 🧙‍, увлечениями 🤸‍
и описать какого собседника ты хочешь найти 🤠
"""
    # print(f"start:{message=}")
    # await save_message_id(message)
    # await delete_all_messages(message)

    sent_message = await message.answer(hi_str, reply_markup=kb.hi_kb)
    await save_message_id(sent_message, message)
    

#------------------------------------------- 1 - name ----------------
@router.callback_query((F.data == 'start_form')) # Первое знакомство: получить имя
async def greeting(callback: CallbackQuery, state: FSMContext):
    await save_message_id(callback, callback)
    await delete_all_messages(callback, callback)

    # -------------BD: create user ------------
    user_id = callback.message.from_user.id
    await update_data(user_id)
    # -----------------------------------------
    await state.set_state(Form.name)
    meet_msg = """Давай познакомимся, как тебя зовут?"""
    sent_message = await callback.message.answer(meet_msg)
    print(f'greeting: {type(sent_message)=}')
    await save_message_id(sent_message, callback)
    


@router.callback_query(F.data == "edit_name") # Редактировать имя - вопрос
async def edit_name(callback: CallbackQuery, state: FSMContext):
    # print(f'{callback=}')
    await delete_all_messages(callback, callback)

    await state.set_state(Editing.edit_name)
    sent_message = await callback.message.answer(f"""Новое имя: """)
    await save_message_id(sent_message, callback)


@router.message(Editing.edit_name) # Редактировать имя - переход в меню
async def edit_name(message: Message, state: FSMContext):
    await save_message_id(message, message)
    await delete_all_messages(message, message)
    await state.set_state(None)

    # -------------BD: fill name ------------
    user_id = message.from_user.id
    await update_data(user_id, {"name": message.text})
    # -----------------------------------------
    # await message.answer(f"""Новое имя: {callback.message.text}""")

    sent_message = await message.answer('Супер! Записано! ✏', reply_markup=kb.back_to_profile)
    await save_message_id(sent_message, message)

#------------------------------------------- 2 - about ----------------
@router.message(Form.name)
async def who_are_you(message: Message, state: FSMContext):
    await save_message_id(message, message)
    await delete_all_messages(message, message)

    # -------------BD: fill name ------------
    user_id = message.from_user.id
    await update_data(user_id, {"name": message.text})
    # -----------------------------------------

    await state.update_data(name=message.text)
    await state.set_state(Form.about_me)
    about_msg = """Расскажи о себе, может ты любишь пиво-смузи или управляешь банановой республикой?"""
    sent_message = await message.answer(about_msg)
    await save_message_id(sent_message, message)


@router.callback_query(F.data == "edit_about_me") # Редактировать Обо мне - вопрос
async def edit_name(callback: CallbackQuery, state: FSMContext):
    # await save_message_id(callback, callback)
    await delete_all_messages(callback, callback)
    
    await state.set_state(Editing.edit_about_me)
    sent_message = await callback.message.answer("""Изменить о себе:""")
    await save_message_id(sent_message, callback)


@router.message(Editing.edit_about_me) # Редактировать Обо мне - переход в меню
async def edit_name(message: Message, state: FSMContext):
    await save_message_id(message, message)
    await delete_all_messages(message, message)
    await state.set_state(None)
    # -------------BD: fill about_me ------------
    user_id = message.from_user.id
    await update_data(user_id, {"about_me": message.text})
    # -----------------------------------------
    sent_message = await message.answer('Супер! Записано! ✏', reply_markup=kb.back_to_profile)
    await save_message_id(sent_message, message)



#------------------------------------------- 3 - CV ----------------
@router.message(Form.about_me)
async def get_cv(message: Message, state: FSMContext):
    await save_message_id(message, message)
    await delete_all_messages(message, message)

    # -------------BD: fill about_me ------------
    user_id = message.from_user.id
    await update_data(user_id, {"about_me": message.text})
    # -----------------------------------------
    await state.update_data(about_me=message.text)
    await state.set_state(Form.cv_path)
    cv_msg = """Супер! 
Чтобы мы смогли получше тебя узнать, ты можешь дать нам больше подробностей"""
    sent_message = await message.answer(cv_msg)
    await save_message_id(sent_message, message)


@router.callback_query(F.data == "edit_cv_path") # Редактировать CV - вопрос
async def edit_name(callback: CallbackQuery, state: FSMContext):
    # await save_message_id(callback)
    await delete_all_messages(callback, callback)
    await state.set_state(Editing.edit_cv_path)
    sent_message = await callback.message.answer("""Изменить ссылку на CV:""")
    await save_message_id(sent_message, callback)


@router.message(Editing.edit_cv_path) # Редактировать CV - переход в меню
async def edit_name(message: Message, state: FSMContext):
    await save_message_id(message, message)
    # await delete_all_messages(message, message)
    # -------------BD: fill about_me ------------
    user_id = message.from_user.id
    await state.set_state(None)
    await update_data(user_id, {"cv_path": message.text})
    # -----------------------------------------
    sent_message = await message.answer('Супер! Записано! ✏', reply_markup=kb.back_to_profile)
    await save_message_id(sent_message, message)


#------------------------------------------- 4 Target ----------------
@router.message(Form.cv_path)
async def get_target(message: Message, state: FSMContext):
    await save_message_id(message, message)
    await delete_all_messages(message, message)

    # -------------BD: fill cv ------------
    user_id = message.from_user.id
    await update_data(user_id, {"cv_path": message.text})
    # -----------------------------------------
    await state.update_data(cv_path=message.text)
    await state.set_state(None)
    await state.set_state(Form.target)
    target_msg = """Опиши в свободной форме собеседника, которого ты хочешь найти"""
    sent_message = await message.answer(target_msg)
    await save_message_id(sent_message, message)



@router.message(F.text == '✏Изменить кого ищу')
@router.callback_query(F.data == "edit_target")  # Редактировать таргет - вопрос
async def edit_name(callback: CallbackQuery, state: FSMContext):
    # await save_message_id(callback, callback)
    await delete_all_messages(callback, callback)
    await state.set_state(Editing.edit_target)
    sent_message = await answer_by_msg_or_clb(callback, "Изменить кого ищу:")#await callback.message.answer()
    print(sent_message)
    await save_message_id(sent_message, callback)


@router.message(Editing.edit_target)  # Редактировать таргет - переход в меню
async def edit_name(message: Message, state: FSMContext):
    await save_message_id(message, message)
    await state.set_state(None)
    # -------------BD: fill таргет ------------
    user_id = message.from_user.id
    await update_data(user_id, {"target": message.text})
    # -----------------------------------------
    sent_message = await message.answer('Супер! Записано!✏', reply_markup=kb.back_to_profile_target)
    await save_message_id(sent_message, message)


@router.message(Form.target)
async def set_target(message: Message, state: FSMContext):
    await save_message_id(message, message)
    await delete_all_messages(message, message)
    # -------------BD: fill target ------------
    if message.text != "/set_profile":
        user_id = message.from_user.id
        await update_data(user_id, {"target": message.text})
    # -----------------------------------------
    await state.update_data(target=message.text)
    await state.set_state(None)
    await ask_confirmation(message, state)

async def get_profile_str(rec_num, user_dict: dict):
    return "-" * 10 + '\n' + \
    f"/{rec_num}" + '\n'\
    f"{user_dict['name']}\n\n" + \
    f"🧐 About:\n{user_dict['about_me']}\n\n" + \
    f"📝 CV ссылка:\n{user_dict['cv_path']}\n\n"

async def answer_by_msg_or_clb(message: Optional[Union[Message, CallbackQuery]], content:str,  reply_markup=None):
    if isinstance(message, CallbackQuery):
        return await message.message.answer(content, reply_markup=reply_markup)
    else:
        return await message.answer(content, reply_markup=reply_markup)


#--------------------ФОТО------------------
@router.message(F.photo)
async def download_photo(message: Message):
    media_path = f"media"
    os.makedirs(media_path, mode=0o777, exist_ok=True)
    await message.bot.download(
        message.photo[-1],
        destination=os.path.join(media_path, f"{message.from_user.id}.jpg")
    )



# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.answer('Привет', reply_markup=kb.main)
#     await message.reply('Как дела')


# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.answer('Привет', reply_markup=kb.main)
#     await message.reply('Как дела')

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
