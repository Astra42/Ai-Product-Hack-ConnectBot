from typing import Any, Dict, List

from langchain.chains import LLMChain
from langchain_community.llms import YandexGPT
from langchain_core.prompts import PromptTemplate

yandex_dict = {
    "api_key": "YOUR-API-KEY",
    "model_uri": "YOUR-MODEL-URI",
    "folder_id": "YOUR-FOLDER-ID",
}


def get_summarisation_from_github_projects(
    github_repos: List[Dict[str, Any]], yandex_dict: Dict[str, str], n=150
) -> str:
    """
    Возвращает суммаризацию по информации о github репозиториях.

    :param github_repos: список json'ов с данными о репозиториях.
    :param yandex_dict: словарь с реквизитами для YandexGPT (api_key, model_uri, folder_id)
    :param n: максимальное количество слов в суммаризации.
    :return: Текст суммаризации.
    """

    llm = YandexGPT(**yandex_dict)
    template = """
    Перед тобой описание github проектов: {github_repos}. Суммаризуй информацию об этих проектах, используй ДО {n} слов, 
    не забудь указать область или тематику каждого проекта и его стек, если есть. Не используй нумерацию, перечисление проектов и отделение строк, 
    просто верни связный текст без своих комментариев. НЕ УКАЗЫВАЙ НАЗВАНИЯ репозиториев. Начни как: 'Темы: ...'
    """
    prompt = PromptTemplate.from_template(template)

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    text = llm_chain.invoke({"github_repos": github_repos, "n": n})["text"]
    return text


def get_summarisation_from_json_description(
    main_json: Dict[str, Any], yandex_dict: Dict[str, str], n=150
) -> str:
    """
    Возвращает суммаризацию по информации из json, в котором содержиться информация о человеке.

    :param main_json: json с данными о человеке.
    :param yandex_dict: словарь с реквизитами для YandexGPT (api_key, model_uri, folder_id)
    :param n: максимальное количество слов в суммаризации.
    :return: Текст суммаризации.
    """

    llm = YandexGPT(**yandex_dict)
    template = """
    Перед тобой описание человека в json формате. Суммаризуй эту информацию, используй ДО {n} слов. выдели только самое главное.
    Не используй нумерацию, перечисление проектов и отделение строк, просто верни связный текст без своих комментариев. 
    Описание: {description}
    """
    prompt = PromptTemplate.from_template(template)

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    text = llm_chain.invoke({"description": main_json, "n": n})["text"]
    return text


def get_summarisation_from_resume(
    cv_text: str, yandex_dict: Dict[str, str], n=150
) -> str:
    """
    Возвращает суммаризацию по тексту резюме, которое спарсили.

    :param cv_text: строка, получившаяся после парсинга pdf.
    :param yandex_dict: словарь с реквизитами для YandexGPT (api_key, model_uri, folder_id)
    :param n: максимальное количество слов в суммаризации.
    :return: Текст суммаризации.
    """

    llm = YandexGPT(**yandex_dict)
    template = """Перед тобой текст резюме, ты должен выделить из этого текста главную информацию: области работы, стек, навыки, опыт и т.д. и 
    составить связный текст. НЕ ВКЛЮЧАЙ В ОТВЕТ имя, возраст и другую персональную информацию, но выдели в тексте все самое важное.
    Верни в ответе до {n} слов. Не используй нумерацию, перечисление и отделение строк, просто верни связный текст без своих комментариев.
    Текст резюме: {cv_text}
    """
    prompt = PromptTemplate.from_template(template)

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    text = llm_chain.invoke({"cv_text": cv_text, "n": n})["text"]
    return text
