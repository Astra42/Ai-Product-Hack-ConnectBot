import aiohttp

import asyncio


class Network:
    HOST = "http://localhost:8005"

    @staticmethod
    async def update_data(profile_id, data_dict={}):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{Network.HOST}/profile/{profile_id}",
                                json=data_dict) as response:
                if response.status == 200:
                    print("Данные обновлены успешно!")
                else:
                    print(f"Ошибка при отправке данных, статус: {response.status}")

    @staticmethod
    async def load_img(profile_id, image):
        async with aiohttp.ClientSession() as session:
            async with session.get(image.file_path) as response:
                image_data = await response.read()
                async with session.post(f"{Network.HOST}/profile/{profile_id}/load_img", data=image_data) as response:
                    if response.status == 200:
                        print("Данные обновлены успешно!")
                    else:
                        print(f"Ошибка при отправке данных, статус: {response.status}")

    @staticmethod
    async def get_specific_profile(profile_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{Network.HOST}/profile/{profile_id}") as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Ошибка при получении профиля, статус: {response.status}")
                    return None

    @staticmethod
    async def get_recommendation(profile_id, rec_num=0, refresh=True): #-> List[dict]
        #rec_num - индекс рекомендации в списке на беке
        async with aiohttp.ClientSession() as session:
            request = f"{Network.HOST}/profile/predict_for/{profile_id}/?rec_num={rec_num}&refresh={refresh}"
            async with session.get(request) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Ошибка при получении предсказания, статус: {response.status}")
                    return None
                
    @staticmethod
    async def get_recommendation_cnt(profile_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{Network.HOST}/profile/predict_for/{profile_id}/rec_cnt") as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Ошибка при получении профиля, статус: {response.status}")
                    return None

    @staticmethod
    async def get_inplementation(profile_id, inplement_num=0, refresh=True):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{Network.HOST}/profile/predict_for/{profile_id}/implement/?inplement_num={inplement_num}&refresh={refresh}") as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Ошибка при получении профиля, статус: {response.status}")
                    return None




# # \__NETWORK_REQUEST

# async def update_data(profile_id, data_dict={}):
#     async with aiohttp.ClientSession() as session:
#         async with session.post(f"http://localhost:8005/profile/{profile_id}",
#                                json=data_dict) as response:
#             if response.status == 200:
#                 print("Данные обновлены успешно!")
#             else:
#                 print(f"Ошибка при отправке данных, статус: {response.status}")


# async def load_img(profile_id, image):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(image.file_path) as response:
#             image_data = await response.read()
#             async with session.post(f"http://localhost:8005/profile/{profile_id}/load_img", data=image_data) as response:
#                 if response.status == 200:
#                     print("Данные обновлены успешно!")
#                 else:
#                     print(f"Ошибка при отправке данных, статус: {response.status}")

# async def get_specific_profile(profile_id):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(f"http://localhost:8005/profile/{profile_id}") as response:
#             if response.status == 200:
#                 return await response.text()
#             else:
#                 print(f"Ошибка при получении профиля, статус: {response.status}")
#                 return None


# async def get_recommendation(profile_id, rec_num=0, refresh=True): #-> List[dict]
#     #rec_num - индекс рекомендации в списке на беке
#     async with aiohttp.ClientSession() as session:
#         request = f"http://localhost:8005/profile/predict_for/{profile_id}/?rec_num={rec_num}&refresh={refresh}"
#         async with session.get(request) as response:
#             if response.status == 200:
#                 return await response.text()
#             else:
#                 print(f"Ошибка при получении предсказания, статус: {response.status}")
#                 return None
# async def get_recommendation_cnt(profile_id):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(f"http://localhost:8005/profile/predict_for/{profile_id}/rec_cnt") as response:
#             if response.status == 200:
#                 return await response.text()
#             else:
#                 print(f"Ошибка при получении профиля, статус: {response.status}")
#                 return None


# async def get_inplementation(profile_id, inplement_num=0, refresh=True):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(f"http://localhost:8005/profile/predict_for/{profile_id}/implement/?inplement_num={inplement_num}&refresh={refresh}") as response:
#             if response.status == 200:
#                 return await response.text()
#             else:
#                 print(f"Ошибка при получении профиля, статус: {response.status}")
#                 return None
# # NETWORK_REQUEST__/