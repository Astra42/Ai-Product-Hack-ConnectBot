# V0 (примитивный) деплой 

Коротко опишу как поднять весь продукт использую простые инструменты!

## Клонируем репу с гита к себе 

`git clone https://github.com/Astra42/Ai-Product-Hack-ConnectBot.git`

Знакомимся со структурой папок и модулей 


## Создаем python окружение 

Подойдет питон 3.9 - в дальнейшим буду сокращать до `python3`

`python3 -m venv env`

Активируем 

`source env/bin/activate`

Скачиваем и устанавливаем нужные зависимости

`pip install -r requirements`


## Запуск в фоновом режиме 

Будем исползовать консольную утилиту `tmux` - [команды](https://www.ditig.com/publications/tmux-cheat-sheet)

Нам понадобится немного 

`tmux ls` - проверять активные сеансы

`tmux new-session -s session_name` - создать сессию

`tmux attach-session -t session_name` - подключиться к существующей сессии

Внутри сессии, что бы скролить нужно вбить 

`ctrl + B`  + `[`

Чтобы выйти из сессии

`ctrl + B` + `D`

На этом все.

### Теперь нужно запустить  бекенд с ручками + бд 

`tmux new-session -s route_`

Включить окружение + перейти в нужное корень + запустить бек

`cd TelegramBot/backend`

`python3 fast_api.py`

Выйти из `tmux`


### Поднятие телеграм бота


Аналогично,

запуск из `TelegramBot/backend` 
скрипт `main.py`


## Секретики

Не забываем положить секретики в нужные места 

* телеграм токен

* yagpt/chatGPT токены - будущее 



----


# V1 Переход на докер + docker compose 

TODO