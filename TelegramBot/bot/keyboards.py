from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, BotCommandScopeDefault

navigation_kb = [BotCommand(command='start', description='🚀Старт'),
            BotCommand(command='set_profile', description='📝Моя анкета'),
            BotCommand(command='search_interlocutor', description='🔎Поиск'),]
#BotCommand(command='change_language', description='⚙language')


hi_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🚀", callback_data="start_form")]])

fill_pls_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Заполнить!", callback_data="start_form")]])

back_to_profile = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📝Назад к анкете", callback_data="set_profile")]])
back_to_profile_target = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📝Назад к анкете", callback_data="set_profile"),
                                                                InlineKeyboardButton(text="🔎Искать!", callback_data="search_interlocutor")]])
def get_watch_next_kb_buttons():
    watch_next_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="✏Изменить кого ищу")],
                                  [KeyboardButton(text="🍺/🍷")],
                                  [KeyboardButton(text="🚀Далее")]],
                        resize_keyboard=True, one_time_keyboard=True)
    return watch_next_kb


def get_watch_next_kb(num: int):
    watch_next_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="✏Изменить кого ищу", callback_data="edit_target"),
                          InlineKeyboardButton(text="🍺/🍷", callback_data="like"),
                          InlineKeyboardButton(text="🚀Далее", callback_data=f"rec_{num}")]])

    return watch_next_kb


profile_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Поиск собеседника🔎", callback_data="search_interlocutor")],
                                                   [InlineKeyboardButton(text="⚙ Имя", callback_data="edit_name", ),
                                                    InlineKeyboardButton(text="⚙ О себе", callback_data="edit_about_me")],
                                                    [InlineKeyboardButton(text="⚙ СV", callback_data="edit_cv_path"),
                                                    InlineKeyboardButton(text="⚙ Кого ищу", callback_data="edit_target")]])









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
