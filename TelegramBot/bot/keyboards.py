from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, BotCommandScopeDefault

navigation_kb = [BotCommand(command='set_profile', description='📝Моя анкета'),
            BotCommand(command='search_interlocutor', description='🔎Поиск'),]
#BotCommand(command='change_language', description='⚙language')


hi_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🚀", callback_data="start_form")]])


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
