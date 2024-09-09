import base64
from typing import Any, Dict

import requests

TOKEN = ""


def extract_username(github_url: str) -> str:
    """
    Извлекает имя пользователя из URL GitHub.

    :param github_url: Ссылка на профиль пользователя GitHub.
    :return: Имя пользователя, извлеченное из ссылки.
    """
    github_url = github_url.split("?")[0]  # убираем параметры запроса
    github_url = github_url.rstrip("/")
    username = github_url.split("/")[-1]
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
        return "no README found"


def get_data(github_url: str) -> Dict[str, Any]:
    """
    Собирает информацию о пользователе GitHub и его публичных репозиториях.

    :param github_url: Ссылка на профиль пользователя GitHub.
    :return: Словарь с данными о пользователе и его репозиториях. Включает логин, био и информацию по каждому репозиторию.
    """
    username = extract_username(github_url)

    headers = {"Authorization": f"token {TOKEN}"}

    user_response = requests.get(
        f"https://api.github.com/users/{username}", headers=headers
    )
    user_data = user_response.json()

    repos_response = requests.get(user_data["repos_url"], headers=headers)
    repos_data = repos_response.json()

    github_repos = []
    for repo in repos_data:
        repo_data = {
            "name": repo["name"],
            "description": repo.get("description", "no description")
            .replace("\r", "")
            .replace("\n", ""),
            "language": repo.get("language", "no language specified"),
            "readme": get_readme(username, repo["name"], headers).replace("\n", " "),
            "link": repo["html_url"],
        }
        github_repos.append(repo_data)

    data = {
        "github_username": user_data["login"],
        # "github_name": user_data.get("name", ""),
        "github_bio": user_data.get("bio", ""),
        "github_link": github_url,
        # "github_location": user_data.get("location", ""),
        # "github_number_of_public_repos": user_data["public_repos"],
        "github_repos": github_repos,
    }

    return data
