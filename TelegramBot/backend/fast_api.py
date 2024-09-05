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


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8001)