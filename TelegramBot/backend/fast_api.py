import os, sys
from typing import Optional, Union

import aiofiles
import uvicorn
import traceback
import secrets
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File

from data_science.recsys.recsys import TextVectorizer_v2, RecSys
from data_science.recsys.user import User

app = FastAPI()



USERS = { 
    "1": User(1, "Боб", "Я люблю Data Science, люблю чай и бананы. Меня зовут Ярик, хочу стать ML инженером", '1234', "Ищу человека, который любит банановый сок, чай с ромашкой и работает в СБЕРе"),
    "2": User(2, "Макс", "Я люблю DS, увлекаюсь машинным обучением. Ем бананы и пью чай с ромашкой. Развиваюсь в NLP работаю в Сбере. ", "12345", "Ищу людей с именем Ярик. Или тех кто шарит за Ml, NLP"),
    "3": User(3, "Алиса", "Увлекаюсь литературой про разведение Арбузов дома. По вечерам читаю про способы обёртки Ml решений. Работаю backend-разрабом на Java в Сбере", "12345", "Ищу людей кто шарит за ML и арбузы любит")
}  # id:User


RECOMENDATIONS = {
    "7": [{'name': "Аль Пачино", 'about_me':"Один из выдающихся актёров 20-века. По вечерам выращивает бананы и кодит пет-проект с Ml начинкой"},
          {'name': "Марлон Брандо", 'about_me':"Легендарный актёр 20-века. По утрам делает зарядку, разводит бананы и кодит пет-проект с NLP начинкой"}]
}   # id:List[user desc like dict]



model_vectorizer = TextVectorizer_v2("intfloat/multilingual-e5-large-instruct")
recsys = RecSys(model_vectorizer)


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
async def predict(profile_id: str,
                  rec_num: Optional[int] = 0,
                  refresh: Optional[bool] = True):
    if profile_id not in USERS.keys():
        return status.HTTP_404_NOT_FOUND
    if refresh or profile_id not in RECOMENDATIONS.keys(): # Если пользователя нет - генерим рекомендации и даём самую первую
        print(str(USERS[profile_id]))
        print("Ищем похожих для пользователя", profile_id)
        top_dict = await get_top_all(profile_id)
        print('top_dict', top_dict)
        RECOMENDATIONS[profile_id] = top_dict
        return RECOMENDATIONS[profile_id][0]
    else: # Если пользователь есть - просто даём реку по индексу
        print(RECOMENDATIONS, profile_id)
        if(0 <= rec_num < len(RECOMENDATIONS[profile_id])):
            return RECOMENDATIONS[profile_id][rec_num]
        print("Запрошен несуществующий индекс")
        return status.HTTP_404_NOT_FOUND

@app.get("/profile/predict_for/{profile_id}/rec_cnt")
async def predict(profile_id: str):
    print(RECOMENDATIONS)
    if profile_id not in RECOMENDATIONS.keys():
        return status.HTTP_404_NOT_FOUND
    return f"len={len(RECOMENDATIONS[profile_id])}"


@app.post("/profile/{profile_id}/load_img")
async def upload_image(profile_id: str, image: UploadFile = File(...)):
    if profile_id not in USERS.keys():
        return status.HTTP_404_NOT_FOUND
    media_path = f"./media"
    os.makedirs(media_path, exist_ok=False)
    async with aiofiles.open(os.path.join(media_path, f'{profile_id}.jpg'), mode='wb') as out_file:
        content = await image.read()
        await out_file.write(content)
    return {"status": "success"}


async def get_top_all(profile_id: str):
    """Тут DS логика. Пользователи лежат в словаре USERS (profile_id: класс User)"""
    return recsys.get_score_by_forms(USERS, profile_id)

#     return [
#     {
#         'id': 1,
#         'name': 'Алексей Иванов',
#         'about_me': 'Опытный разработчик на Python с 5 летним стажем.',
#         # 'cv_path': '/path/to/cv_alexei.pdf',
#         # 'target': 'Ищу тех, кто разбирается в карбюраторах'
#     },
#     {
#         'id': 2,
#         'name': 'Елена Петрова',
#         'about_me': 'Молодой и перспективный дизайнер UI/UX.',
#         # 'cv_path': '/path/to/cv_elena.pdf',
#         # 'target': 'Ведущих дизайнеров'
#     },
#     {
#         'id': 3,
#         'name': 'Райн Гослинг',
#         'about_me': 'Специалист по технике с опытом работы в крупных компаниях.',
#         # 'cv_path': '/path/to/cv_rain.pdf',
#         # 'target': 'Людей кто поможет мигрировать с Notion'
#     },
#     {
#         'id': 4,
#         'name': 'Ольга Васильева',
#         'about_me': 'Опытный аналитик данных с навыками машинного обучения.',
#         # 'cv_path': '/path/to/cv_olga.pdf',
#         # 'target': 'Хочу переехать в ml. Ищу ml-щиков'
#     },
#     {
#         'id': 5,
#         'name': 'Дмитрий Михайлов',
#         'about_me': 'Молодой и перспективный разработчик мобильных приложений.',
#         # 'cv_path': '/path/to/cv_dmitriy.pdf',
#         # 'target': 'Ищу людей с фамилией Михайлов'
#     }
# ]

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8005)