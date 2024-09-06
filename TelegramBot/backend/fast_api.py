import os
import uvicorn
import traceback
import secrets
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File

class User:
    def __init__(self, id: str):
        self.id = id
        self.name = None
        self.about_me = None
        self.cv_path = None
        self.target = None

    def __make_attrs_like_dict(self):
        return vars(self)

    def __str__(self):
        return str(self.__make_attrs_like_dict())

    def __repr__(self):
        return str(self.__make_attrs_like_dict())


app = FastAPI()

USERS = {}  # id:User

@app.post("/profile/{profile_id}")
async def update_profile(profile_id: str, update_data: dict):
    print('update_data', update_data)
    if isinstance(update_data, str):
        update_data = eval(update_data)
    try:
        if profile_id not in USERS.keys():
            USERS[profile_id] = User(profile_id)
        for attr, value in update_data.items():
            if attr in ['id', 'name', 'about_me', 'cv_path', 'target']:
                setattr(USERS[profile_id], attr, value)
        return profile_id

    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return 'Ошибка:\n', traceback.format_exc()


@app.get("/profile/{profile_id}")
async def update_profile(profile_id: str):
    if profile_id in USERS.keys():
        print(str(USERS[profile_id]))
        return str(USERS[profile_id])
    return status.HTTP_404_NOT_FOUND

@app.get("/profiles")
async def update_profile():
    print(str(USERS))
    return USERS

@app.get("/profile/predict_for/{profile_id}")
async def predict(profile_id: str):
    if profile_id not in USERS.keys():
        return status.HTTP_404_NOT_FOUND

    print(str(USERS[profile_id]))
    print("Ищем похожих для пользователя", profile_id)
    top_dict = await get_top_5(profile_id)
    return top_dict




async def get_top_5(profile_id: str):
    """Тут DS логика. Пользователи лежат в словаре USERS (profile_id: класс User)"""
    return [
    {
        'id': 1,
        'name': 'Алексей Иванов',
        'about_me': 'Опытный разработчик на Python с 5 летним стажем.',
        'cv_path': '/path/to/cv_alexei.pdf',
        # 'target': 'Ищу тех, кто разбирается в карбюраторах'
    },
    {
        'id': 2,
        'name': 'Елена Петрова',
        'about_me': 'Молодой и перспективный дизайнер UI/UX.',
        'cv_path': '/path/to/cv_elena.pdf',
        # 'target': 'Ведущих дизайнеров'
    },
    {
        'id': 3,
        'name': 'Райн Гослинг',
        'about_me': 'Специалист по технике с опытом работы в крупных компаниях.',
        'cv_path': '/path/to/cv_rain.pdf',
        # 'target': 'Людей кто поможет мигрировать с Notion'
    },
    {
        'id': 4,
        'name': 'Ольга Васильева',
        'about_me': 'Опытный аналитик данных с навыками машинного обучения.',
        'cv_path': '/path/to/cv_olga.pdf',
        # 'target': 'Хочу переехать в ml. Ищу ml-щиков'
    },
    {
        'id': 5,
        'name': 'Дмитрий Михайлов',
        'about_me': 'Молодой и перспективный разработчик мобильных приложений.',
        'cv_path': '/path/to/cv_dmitriy.pdf',
        # 'target': 'Ищу людей с фамилией Михайлов'
    }
]



if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8001)