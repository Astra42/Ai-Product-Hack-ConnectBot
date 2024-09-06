from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, BotCommandScopeDefault

navigation_kb = [BotCommand(command='start', description='🚀Старт'),
            BotCommand(command='set_profile', description='📝Моя анкета'),
            BotCommand(command='search_interlocutor', description='🔎Поиск'),]
#BotCommand(command='change_language', description='⚙language')


hi_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🚀", callback_data="start_form")]])

fill_pls_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="заполнить!", callback_data="start_form")]])

edited_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад к анкете", )]])


profile_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Поиск собеседника🔎", callback_data="search_interlocutor")],
                                                   [InlineKeyboardButton(text="⚙Имя", callback_data="edit_name", ),
                                                    InlineKeyboardButton(text="⚙О себе", callback_data="edit_about_me")],
                                                    [InlineKeyboardButton(text="⚙СV", callback_data="edit_cv_path"),
                                                    InlineKeyboardButton(text="⚙Кого ищу", callback_data="edit_target")]])



main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Каталог")],
                                     [KeyboardButton(text="кнопка1")],
                                     [KeyboardButton(text="кнопка2"),
                                      KeyboardButton(text="мяв")]],
                           resize_keyboard=True,
                           input_field_placeholder="Выбери пункт меню")

catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Футболки", callback_data="t_shirt"),
                                                 InlineKeyboardButton(text="Пижама", callback_data="pajama")]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]],
                                 resize_keyboard=True)
