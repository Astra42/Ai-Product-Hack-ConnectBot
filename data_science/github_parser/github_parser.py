import base64
import os
import sys
from typing import Any, Dict

import requests


# /Ai-Product-Hack-ConnectBot/data_science/github_parser/github_parser.py -> /Ai-Product-Hack-ConnectBot/
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from data_science.github_parser.secrets import GITHUB_TOKEN

def extract_username(github_url: str) -> str:
    """
    Извлекает имя пользователя из URL GitHub.

    :param github_url: Ссылка на профиль пользователя GitHub.
    :return: Имя пользователя, извлеченное из ссылки.
    """
    github_url = github_url.split("?")[0]  # убираем параметры запроса
    github_url = github_url.rstrip("/")
    username = os.path.basename(github_url)
    return username


def get_readme(username: str, repo_name: str, headers: Dict[str, str]) -> str:
    """
    Получает содержимое файла README.md для указанного репозитория пользователя.

    :param username: Имя пользователя на GitHub.
    :param repo_name: Название репозитория.
    :param headers: Заголовки для авторизации при запросе.
    :return: Содержимое файла README.md в виде строки, или 'no README found', если файл не найден.
    """
    readme_url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    readme_response = requests.get(readme_url, headers=headers)
    if readme_response.status_code == 200:
        readme_data = readme_response.json()
        readme_content = base64.b64decode(readme_data["content"]).decode("utf-8")
        return readme_content
    else:
        return ""


def get_data_from_github_link(github_url: str) -> Dict[str, Any]:
    """
    Собирает информацию о пользователе GitHub и его публичных репозиториях.

    :param github_url: Ссылка на профиль пользователя GitHub.
    :return: Словарь с данными о пользователе и его репозиториях. Включает логин, био и информацию по каждому репозиторию.
    {
        "github_username": str,
        "github_bio": str,
        "github_link": github_url,
        "github_repos": [
            {"name": str1, "description": str1, "language": str1, "readme": str1, "link": str1},
            {"name": str2, "description": str2, "language": str2, "readme": str2, "link": str2},
            ...
        ]
    }
    """
    username = extract_username(github_url)

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    user_response = requests.get(
        f"https://api.github.com/users/{username}", headers=headers
    )
    user_data = user_response.json()

    print(f'get_data_from_github_link: {user_data=}')
    # почему основные поля достаются из проектов, а не из основного описания??? 

    repos_response = requests.get(user_data["repos_url"], headers=headers)
    github_repos = []
    try:
        repos_data = repos_response.json()

        for repo in repos_data:
            repo_data = {
                "name": repo["name"],
                "description": repo.get("description", "no description")
                # .replace("\r", "")
                # .replace("\n", "")
                ,
                "language": repo.get("language", "no language specified"),
                "readme": get_readme(username, repo["name"], headers),#.replace("\n", " "),
                "link": repo["html_url"],
            }
            github_repos.append(repo_data)
    except Exception as e:
        print(f'get_data_from_github_link:{e=}') 

    data = {
        "github_username": user_data["login"],
        # "github_name": user_data.get("name", ""),
        "github_bio": user_data.get("bio", ""),#.replace("\r", "").replace("\n", ""),
        "github_link": github_url,
        # "github_location": user_data.get("location", ""),
        # "github_number_of_public_repos": user_data["public_repos"],
        "github_repos": github_repos,
    }


    return data



if __name__ == "__main__":
    githbu_url = "https://github.com/avalur"
    print(f'{githbu_url=}')

    github_resp = get_data_from_github_link(githbu_url)

    print(f'{github_resp=}')



    """
    https://api.github.com/users/avalur

    {
        "login": "avalur",
        "id": 5484105,
        "node_id": "MDQ6VXNlcjU0ODQxMDU=",
        "avatar_url": "https://avatars.githubusercontent.com/u/5484105?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/avalur",
        "html_url": "https://github.com/avalur",
        "followers_url": "https://api.github.com/users/avalur/followers",
        "following_url": "https://api.github.com/users/avalur/following{/other_user}",
        "gists_url": "https://api.github.com/users/avalur/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/avalur/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/avalur/subscriptions",
        "organizations_url": "https://api.github.com/users/avalur/orgs",
        "repos_url": "https://api.github.com/users/avalur/repos",
        "events_url": "https://api.github.com/users/avalur/events{/privacy}",
        "received_events_url": "https://api.github.com/users/avalur/received_events",
        "type": "User",
        "site_admin": false,
        "name": "Alexander Avdiushenko",
        "company": "JetBrains",
        "blog": "",
        "location": "Cyprus",
        "email": null,
        "hireable": null,
        "bio": "Project Manager and Data Scientist with 8+ years of experience in data science, analysis, and educational programs for the IT industry.",
        "twitter_username": null,
        "public_repos": 14,
        "public_gists": 0,
        "followers": 36,
        "following": 6,
        "created_at": "2013-09-18T06:28:33Z",
        "updated_at": "2024-08-16T09:53:36Z"
    }
    """