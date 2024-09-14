import os, sys
from typing import Optional, Union

import aiofiles
import uvicorn
import traceback
import secrets
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File

from data_science.recsys.recsys import TextVectorizer_v2, RecSys
from data_science.recsys.user import User

from pprint import pprint

app = FastAPI()

# USERS = {
#     "1": User('1', "Алиса", "Увлекаюсь литературой про разведение Арбузов дома. По вечерам читаю про способы обёртки Ml решений. Работаю backend-разрабом на Java в Сбере", "12345", "Ищу людей кто шарит за ML и арбузы любит"),
#     "2": User('2', "Алина", "Увлекаюсь машинным обучением и анализом данных. Люблю кофе и шоколадные кексы.", "5678", "Ищу единомышленников для обсуждения последних тенденций в AI"),
#     "3": User('3', "Михаил", "Работаю в сфере NLP. Люблю читать научную фантастику и пробовать новые виды кофе.", "9012", "Ищу коллег для совместных проектов по обработке естественного языка"),
#     "4": User('4', "Елена", "Занимаюсь компьютерным зрением. Увлекаюсь фотографией и путешествиями.", "1111", "Ищу людей для обсуждения инноваций в CV"),
#     "5": User('5', "Дмитрий", "Разрабатываю рекомендательные системы. Люблю играть на гитаре и слушать рок-музыку.", "2222", "Ищу единомышленников для создания музыкального бота"),
#     "6": User('6', "Светлана", "Увлекаюсь анализом данных в финансах. Люблю йогу и здоровое питание.", "3333", "Ищу коллег для обсуждения финансовых моделей"),
#     "7": User('7', "Андрей", "Работаю над проектами по time series forecasting. Люблю исторические книги и настольные игры.", "4444", "Ищу людей для создания прогнозной модели погоды"),
#     "8": User('8', "Наталья", "Занимаюсь natural language processing. Увлекаюсь кулинарией и садоводством.", "5555", "Ищу коллег для разработки чат-бота для кулинарных рецептов"),
#     "9": User('9', "Владимир", "Разрабатываю системы для обработки больших данных. Люблю футбол и рыбалку.", "6666", "Ищу единомышленников для создания аналитической платформы для спорта"),
#     "10": User('10', "Ольга", "Увлекаюсь computer vision. Люблю путешествия и изучение новых языков.", "7777", "Ищу коллег для разработки системы распознавания объектов"),
#     "11": User('11', "Кирилл", "Работаю над проектами по reinforcement learning. Люблю читать научную литературу и заниматься бегом.", "8888", "Ищу людей для создания игрового бота"),
#     "12": User('12', "Мария", "Занимаюсь анализом данных в сфере здравоохранения. Люблю классическую музыку и рисование.", "9999", "Ищу коллег для разработки системы предиктивной медицины"),
#     "13": User('13', "Александр", "Увлекаюсь deep learning. Люблю исторические фильмы и коллекционирую монеты.", "0000", "Ищу единомышленников для создания системы распознавания монет"),
#     "14": User('14', "Юлия", "Работаю над проектами по sentiment analysis. Люблю современную литературу и танцы.", "1234", "Ищу коллег для разработки системы анализа отзывов"),
#     "15": User('15', "Павел", "Занимаюсь feature engineering. Люблю путешествия на велосипеде и фотографию.", "5678", "Ищу людей для создания системы прогнозирования погоды"),
#     "16": User('16', "Боб", "Я люблю Data Science, люблю чай и бананы. Меня зовут Ярик, хочу стать ML инженером", '1234', "Ищу человека, который любит банановый сок, чай с ромашкой и работает в СБЕРе"),
#     "17": User('17', "Макс", "Я люблю DS, увлекаюсь машинным обучением. Ем бананы и пью чай с ромашкой. Развиваюсь в NLP работаю в Сбере. ", "12345", "Ищу людей с именем Ярик. Или тех кто шарит за Ml, NLP"),
# } # user_id:User


USERS = {
    "1": User('1', "Алиса", "Увлекаюсь литературой про разведение Арбузов дома. По вечерам читаю про способы обёртки Ml решений. Работаю backend-разрабом на Java в Сбере", "12345", "Ищу людей кто шарит за ML и арбузы любит"),
    "2": User('2', "Алина", "Увлекаюсь машинным обучением и анализом данных. Люблю кофе и шоколадные кексы.", "5678", "Ищу единомышленников для обсуждения последних тенденций в AI"),
    "3": User('3', "Михаил", "Работаю в сфере NLP. Люблю читать научную фантастику и пробовать новые виды кофе.", "9012", "Ищу коллег для совместных проектов по обработке естественного языка"),
    "4": User('4', "Елена", "Занимаюсь компьютерным зрением. Увлекаюсь фотографией и путешествиями.", "1111", "Ищу людей для обсуждения инноваций в CV"),
    "5": User('5', "Дмитрий", "Разрабатываю рекомендательные системы. Люблю играть на гитаре и слушать рок-музыку.", "2222", "Ищу единомышленников для создания музыкального бота"),
    "6": User('6', "Светлана", "Увлекаюсь анализом данных в финансах. Люблю йогу и здоровое питание.", "3333", "Ищу коллег для обсуждения финансовых моделей"),
    "7": User('7', "Андрей", "Работаю над проектами по time series forecasting. Люблю исторические книги и настольные игры.", "4444", "Ищу людей для создания прогнозной модели погоды"),
    "8": User('8', "Наталья", "Занимаюсь natural language processing. Увлекаюсь кулинарией и садоводством.", "5555", "Ищу коллег для разработки чат-бота для кулинарных рецептов"),
    "9": User('9', "Владимир", "Разрабатываю системы для обработки больших данных. Люблю футбол и рыбалку.", "6666", "Ищу единомышленников для создания аналитической платформы для спорта"),
    "10": User('10', "Ольга", "Увлекаюсь computer vision. Люблю путешествия и изучение новых языков.", "7777", "Ищу коллег для разработки системы распознавания объектов"),
    "11": User('11', "Кирилл", "Работаю над проектами по reinforcement learning. Люблю читать научную литературу и заниматься бегом.", "8888", "Ищу людей для создания игрового бота"),
    "12": User('12', "Мария", "Занимаюсь анализом данных в сфере здравоохранения. Люблю классическую музыку и рисование.", "9999", "Ищу коллег для разработки системы предиктивной медицины"),
    "13": User('13', "Александр", "Увлекаюсь deep learning. Люблю исторические фильмы и коллекционирую монеты.", "0000", "Ищу единомышленников для создания системы распознавания монет"),
    "14": User('14', "Юлия", "Работаю над проектами по sentiment analysis. Люблю современную литературу и танцы.", "1234", "Ищу коллег для разработки системы анализа отзывов"),
    "15": User('15', "Павел", "Занимаюсь feature engineering. Люблю путешествия на велосипеде и фотографию.", "5678", "Ищу людей для создания системы прогнозирования погоды"),
    "16": User('16', "Боб", "Я люблю Data Science, люблю чай и бананы. Меня зовут Ярик, хочу стать ML инженером", '1234', "Ищу человека, который любит банановый сок, чай с ромашкой и работает в СБЕРе"),
    "17": User('17', "Макс", "Я люблю DS, увлекаюсь машинным обучением. Ем бананы и пью чай с ромашкой. Развиваюсь в NLP работаю в Сбере. ", "12345", "Ищу людей с именем Ярик. Или тех кто шарит за Ml, NLP"),
    "18": User('18', "Bob", "I live in New York. I am a web-designer and an artist. I use tools such as Figma, Photoshop, and Canva. I love animals", "1337", "I'm looking for a girlfriend"),
    "19": User('19', "Liza", "As a graphic designer living in London, I thrive on creativity and innovation. My toolkit includes Illustrator, InDesign, and Procreate. I'm passionate about creating visually stunning designs that tell stories through typography and color. In my free time, I enjoy attending art exhibitions and practicing yoga.", "1338", "I'm looking for a boyfriend"),
    "20": User('20', "Анна", "Я обожаю проводить время на свежем воздухе, гулять по лесам и заниматься фотографией природы. Увлекаюсь ботаникой и изучением местной флоры.", "12343", "Ищу единомышленников для совместных походов и прогулок на природе."),
    "21": User('21', "Дмитрий", "Я профессиональный повар и страстный любитель кулинарии. Люблю экспериментировать с новыми рецептами и делиться своими кулинарными шедеврами.", "12343", "Ищу людей, которые любят готовить и хотят обмениваться рецептами и кулинарными секретами."),
    "22": User('22', "Ольга", "Я обожаю путешествовать и открывать для себя новые культуры. Посетила более 20 стран и всегда готова к новым приключениям.", "12343", "Ищу попутчиков для совместных поездок и интересных путешествий."),
    "23": User('23', "Алексей", "Я занимаюсь бегом и фитнесом. В свободное время участвую в марафонах и спортивных мероприятиях.", "12343", "Ищу партнёров по тренировкам и людей, которые хотят вести активный образ жизни."),
    "24": User('24', "Мария", "Я люблю читать и обсуждать книги. Предпочитаю художественную литературу и научную фантастику.", "12343", "Ищу собеседников для обсуждения книг и обмена рекомендациями."),
    "25": User('25', "Сергей", "Я играю на гитаре и пишу собственные песни. Музыка — это моя страсть, и я всегда ищу вдохновение.", "12343", "Ищу музыкантов для создания группы и совместных музыкальных проектов."),
    "26": User('26', "Екатерина", "Я изучаю искусство и историю искусства. Люблю посещать выставки и музеи, а также заниматься живописью.", "12343", "Ищу людей, которые интересуются искусством и хотят делиться своими впечатлениями."),
    "27": User('27', "Игорь", "Я работаю в IT и увлекаюсь новыми технологиями. Люблю разрабатывать приложения и изучать программирование.", "12343", "Ищу коллег и единомышленников для обмена опытом и совместных проектов."),
    "28": User('28', "Наталья", "Я интересуюсь философией и психологией. Часто размышляю о жизни и смысле существования.", "12343", "Ищу людей для глубоких бесед и обсуждения философских идей."),
    "29": User('29', "Павел", "Я активно занимаюсь волонтерством и помогаю нуждающимся. Верю в силу сообщества и взаимопомощи.", "12343", "Ищу единомышленников для участия в волонтерских проектах и акциях."),
    "30": User('30', "Татьяна", "Я увлекаюсь садоводством и выращиванием растений. Люблю работать в саду и наблюдать за тем, как растут мои любимые цветы и овощи.", "12343", "Ищу единомышленников для обмена опытом и советами по садоводству."),
    "31": User('31', "Андрей", "Я страстный любитель кино. Смотрю фильмы разных жанров и эпох, от классики до современных блокбастеров.", "12343", "Ищу людей, которые любят обсуждать фильмы и делиться впечатлениями.")
} # user_id:User


RECOMENDATIONS = {
    "7": [{'name': "Аль Пачино", 'about_me':"Один из выдающихся актёров 20-века. По вечерам выращивает бананы и кодит пет-проект с Ml начинкой", "cv_path":"12345"},
          {'name': "Марлон Брандо", 'about_me':"Легендарный актёр 20-века. По утрам делает зарядку, разводит бананы и кодит пет-проект с NLP начинкой", "cv_path":"12345"}]
}   # id:List[user desc like dict]

N_GRAMMS = {} # user_id: [[(2, 10), (11, 14)], [(21, 40)]] Список -> анкета -> N-граммы


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
            if attr in ['id', 'name', 'about_me', 'cv_path', 'target', 'hh_cv', 'github_cv']:
                setattr(USERS[profile_id], attr, value)
        return profile_id

    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return 'Ошибка:\n', traceback.format_exc()


@app.get("/profile/{profile_id}")
async def update_profile(profile_id: str):
    if profile_id in USERS.keys():
        # print(str(USERS[profile_id]))
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
    pprint(f'back:predict:{profile_id=}\n{USERS=}')
    
    if profile_id not in USERS.keys():
        return status.HTTP_404_NOT_FOUND
    if refresh or profile_id not in RECOMENDATIONS.keys(): # Если пользователя нет - генерим рекомендации и даём самую первую
        # print(str(USERS[profile_id]))
        print("Ищем похожих для пользователя", profile_id)
        top_dict = await get_top_all(profile_id)
        # print('top_dict', top_dict)
        RECOMENDATIONS[profile_id] = top_dict
        return RECOMENDATIONS[profile_id][0]
    else: # Если пользователь есть - просто даём реку по индексу
        print(RECOMENDATIONS, profile_id)
        if(0 <= rec_num < len(RECOMENDATIONS[profile_id])):
            return RECOMENDATIONS[profile_id][rec_num]
        print("Запрошен несуществующий индекс")
        return status.HTTP_404_NOT_FOUND



@app.get("/profile/predict_for/{profile_id}/implement")
async def implement(profile_id: str,
                    inplement_num: Optional[int] = 0,
                    refresh: Optional[bool] = True):
    # print(f'back:implement:{RECOMENDATIONS=}')
    if profile_id not in RECOMENDATIONS.keys():
        return status.HTTP_404_NOT_FOUND

    if refresh or profile_id not in N_GRAMMS.keys():
        print(f"\n\n Вызова метода get_implementation в end_point с параметром {profile_id} \n\n")
        result = await get_implementation(profile_id)
        N_GRAMMS[profile_id] = result
        return N_GRAMMS[profile_id][0]
    else:
        if 0 <= inplement_num < len(N_GRAMMS[profile_id]):
            return N_GRAMMS[profile_id][inplement_num]
        print("Запрошен несуществующий индекс")
        return status.HTTP_404_NOT_FOUND


@app.get("/profile/predict_for/{profile_id}/rec_cnt")
async def predict(profile_id: str):
    # print(RECOMENDATIONS)
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


async def get_implementation(profile_id: str, n_gramm_split:int = 2):
    print("\n\nВызываем метод get_implementation\n\n")

    pprint(f"backend:get_implementation:\n{USERS=}")
    return recsys.get_implementation(RECOMENDATIONS[profile_id], USERS, profile_id, n_gramm_split)



if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8005)