import json
import re
import time
from typing import Dict, Generator, List, Optional

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_links(text: str, max_records: int) -> Generator[str, None, None]:
    """
    Генератор для получения ссылок на резюме по заданному текстовому запросу.

    :param text: Текст для поиска резюме.
    :param max_records: Максимальное количество резюме для парсинга.
    :return: Генератор ссылок на резюме.
    """
    records_fetched = 0
    for page in range(1, 100):
        try:
            url = f"https://hh.ru/search/resume?text={text}&area=113&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&page={page}"
            headers = {"User-Agent": "User-Agent"}
            data = requests.get(url, headers=headers, timeout=5)
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, "lxml")
            for a in soup.find_all("a", attrs={"data-qa": "serp-item__title"}):
                yield f"https://hh.ru{a.attrs['href'].split('?')[0]}"
                records_fetched += 1
                if records_fetched >= max_records:
                    return
        except Exception as e:
            print(f"Error fetching links: {e}")


def get_all_jobs(soup: BeautifulSoup) -> List[str]:
    """
    Извлекает информацию о предыдущих местах работы из HTML-кода резюме.

    :param soup: Объект BeautifulSoup, представляющий страницу с резюме.
    :return: Список строк с описанием должностей и обязанностей.
    """
    experience_blocks = soup.find_all(
        "div", {"data-sentry-component": "ResumeExperience"}
    )
    jobs = []
    for block in experience_blocks:
        position = block.find("div", {"data-qa": "resume-block-experience-position"})
        if position:
            position = position.get_text(strip=True)
        else:
            position = ""

        description = block.find(
            "div", {"data-qa": "resume-block-experience-description"}
        )
        if description:
            description = description.get_text(separator=" ", strip=True)
            description = description.replace("\n", " ").replace("  ", " ")
        else:
            description = ""
        if position and description:
            jobs.append(f"{position}: {description}")
    return jobs


def get_education(soup: BeautifulSoup) -> List[str]:
    """
    Извлекает информацию об образовании из HTML-кода резюме.

    :param soup: Объект BeautifulSoup, представляющий страницу с резюме.
    :return: Список строк с информацией об учебных заведениях и специальностях.
    """
    education_blocks = soup.find_all("div", {"data-qa": "resume-block-education-item"})
    education_list = []

    for block in education_blocks:
        university = block.find("div", {"data-qa": "resume-block-education-name"})
        if university:
            university = university.get_text(strip=True)
        else:
            university = ""
        specialization = block.find(
            "div", {"data-qa": "resume-block-education-organization"}
        )
        if specialization:
            specialization = (
                specialization.get_text(separator=" ", strip=True)
                .replace(", ,", ",")
                .strip()
            )
        else:
            specialization = ""
        if university and specialization:
            education_list.append(f"{university}: {specialization}")

    return education_list


def get_tags(soup: BeautifulSoup) -> List[str]:
    """
    Извлекает теги (навыки) из HTML-кода резюме.

    :param soup: Объект BeautifulSoup, представляющий страницу с резюме.
    :return: Список тегов (навыков).
    """
    try:
        tags = [
            tag.text
            for tag in soup.find(attrs={"class": "bloko-tag-list"}).find_all(
                attrs={"class": "bloko-tag__section_text"}
            )
        ]
    except Exception as ex:
        print(ex)
        tags = []
    return tags


def get_single_text_block(s) -> str:
    """
    Извлекает текст из HTML-блока, если он существует.

    :param s: HTML-блок.
    :return: Текст блока или пустая строка, если блок не найден.
    """
    return s.text if s else ""


def get_data(link: str) -> Optional[Dict[str, any]]:
    """
    Парсит данные резюме по ссылке.

    :param link: Ссылка на резюме.
    :return: Словарь с данными резюме или None в случае ошибки.
    {
        "position": str,
        "age": str,
        "gender": str,
        "job_search_status": str,
        "about": str,
        "jobs": [str1, str2, ...],
        "tags": [str1, str2, ...],
        "eduacation": [str1, str2, ...],
        "link": str
    }
    """
    try:
        data = requests.get(link, headers={"User-Agent": "User-Agent"})
        if data.status_code != 200:
            return None

        soup = BeautifulSoup(data.content, "lxml")
        resume = {
            "position": get_single_text_block(
                soup.find(attrs={"class": "resume-block__title-text"})
            ),
            "age": re.sub(
                r"\D",
                "",
                get_single_text_block(
                    soup.find(attrs={"data-qa": "resume-personal-age"})
                ),
            ).replace("\xa0", ""),
            "gender": get_single_text_block(
                soup.find(attrs={"data-qa": "resume-personal-gender"})
            ),
            "job_search_status": get_single_text_block(
                soup.find(attrs={"data-qa": "job-search-status"})
            ).replace("\xa0", " "),
            "about": get_single_text_block(
                soup.find(attrs={"data-qa": "resume-block-skills-content"})
            ).replace("\n", " "),
            "jobs": get_all_jobs(soup),
            "tags": get_tags(soup),
            "education": get_education(soup),
            "link": link,
        }
        return resume
    except Exception as e:
        print(f"Error fetching resume data: {e}")
        return None


def parse_resumes(search_text: str, max_records: int) -> None:
    """
    Парсит резюме по заданному текстовому запросу и сохраняет их в файл JSON.

    :param search_text: Текст для поиска резюме.
    :param max_records: Максимальное количество резюме для парсинга.
    :return: None
    """
    resume_results = []
    count = 0
    for link in tqdm(get_links(search_text, max_records)):
        resume = get_data(link)
        if resume:
            resume_results.append(resume)
        time.sleep(1)
        count += 1
        if count >= 2000:
            break

    with open(
        f"./data/{(search_text).replace(" ", "_")}_resumes.json", "w", encoding="utf-8"
    ) as f:
        json.dump(resume_results, f, ensure_ascii=False, indent=4)

    print(f"Parsing is finished. {len(resume_results)} resumes found.")


if __name__ == "__main__":
    parse_resumes("data scientist", 50)
    parse_resumes("frontend", 50)
    parse_resumes("backend", 50)
    parse_resumes("analyst", 50)
