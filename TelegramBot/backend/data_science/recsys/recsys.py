import torch
from sentence_transformers import SentenceTransformer
import nltk
from nltk.corpus import stopwords
from nltk import ngrams
from typing import List, Union, Optional
import re

nltk.download('stopwords')


class TextVectorizer_v2:
    def __init__(self, model_checkpoint: str) -> None:

        """
        Инициализатор класса TextVectorizer_v2

        Аргументы:
            model_checkpoint: str - путь к чекпойнту SentenceTransformer

        """

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(model_checkpoint).to(self.device)

    def __preprocess(self, texts: list[str]) -> list[str]:
        """
        Закрытый метод предобработки текста

        Аргументы:
            texts: list[str]

        Возвращает:
            list[str]
        """
        return [txt.replace("\n", "") for txt in texts]

    def vectorize(self, form: Union[dict, list]) -> torch.Tensor:
        """
        Метод векторизации текста

        Аргументы:
            form: dict

        Возвращает:
            torch.Tensor (N, 1024)
        """

        if isinstance(form, dict):
            sentences = self.__preprocess([form[key] for key in tuple(form.keys())])

            with torch.no_grad():
                sentence_embeddings = self.model.encode(sentences, convert_to_tensor=True,
                                                        normalize_embeddings=True).to(self.device).cpu()

            return {key: sentence_embeddings[i] for i, key in enumerate(tuple(form.keys()))}

        elif isinstance(form, list):
            sentences = self.__preprocess(form)
            with torch.no_grad():
                sentence_embeddings = self.model.encode(sentences, convert_to_tensor=True,
                                                        normalize_embeddings=True).to(self.device).cpu()

            return sentence_embeddings

        return None


class RecSys:
    def __init__(self, model):
        """
        Инициализатор класса

        Аргументы:
            model: TextVectorizer_v2 - модель для векторизации текста
        """
        self.model = model
        self.stop_words = list(stopwords.words('russian')) + list(stopwords.words('english'))

    def __preprocess_forms(self, database: dict) -> dict:
        """
        Закрытый метод предобработки формы

        Аргументы:
            database: dict - словарь пользователей

        Возвращает:
            dict - словарь пользователей с предобработанными полями "hh_cv" и "github_cv"
        """
        db = database.copy()

        result = {}

        try:
            db.pop("7136022904")
        except:
            pass

        # Делаем пред обработку для поля "hh_cv" и "github_cv" и удаление людей у которых есть незаполненные поля
        for idx in db.keys():
            # if all(db[idx].make_attrs_like_dict().values()):
            # проверка на отсутствие "hh_cv"
            if (isinstance(db[idx].hh_cv, dict)==False) or (db[idx].hh_cv is  None) or (db[idx].hh_cv == 'None') or (db[idx].hh_cv == None):
                db[idx].hh_cv = db[idx].about_me
            else:
                print(db[idx].hh_cv)
                db[idx].hh_cv = " ".join([str(db[idx].hh_cv[tags]) for tags in db[idx].hh_cv if
                                          tags in ["position", "job_search_status", "about", "tags"] \
                                          and db[idx].hh_cv[tags] is not None])

            # проверка на отсутствие "github_cv"
            if (isinstance(db[idx].github_cv, dict) == False) or (db[idx].github_cv is None) or (db[idx].github_cv == 'None') or ( db[idx].github_cv == None):
                db[idx].github_cv = db[idx].about_me

            else:
                db[idx].github_cv = " ".join([str(db[idx].github_cv[tags]) for tags in db[idx].github_cv if db[idx].github_cv[tags] is not None])

            result[idx] = db[idx]
        return result

    def get_score_by_forms(self, USERS: dict, id_current: int) -> List:
        """
        Метод получения списка самых похожих пользователей на целевого пользователя

        Аргументы:
            USERS: dict - словарь пользователей
            id_current: int - id целевого пользователя

        Возвращает:
            List[dict] - список словарей, содержащих имя, текст о себе, путь к cv
        """
        db = USERS.copy()

        db = self.__preprocess_forms(db)

        # Делаем предобработку для поля "hh_cv"

        # Векторизуем целевого юзера поле "target"
        current_form_target = self.model.vectorize([db[id_current].target])

        # Векторизуем целевого юзера поле "hh_cv"
        current_hh_cv = self.model.vectorize([db[id_current].hh_cv])

        # Векторизуем целевого юзера поле "about_me"
        current_about_me = self.model.vectorize([db[id_current].about_me])

        # Векторизуем целевого юзера поле "github_cv"
        current_github_cv = self.model.vectorize([db[id_current].github_cv])

        # удаление целевого юзера
        db.pop(id_current)

        print('ЖОПА\n\n\n\n')
        print(id_current)
        print(db)

        # Векторизуем у остальных юзеров поле "about_me"
        other_forms_about_me = self.model.vectorize([db[key].about_me for key in db.keys()])

        # Векторизуем у остальных юзеров поле "hh_cv"
        other_forms_hh_cv = self.model.vectorize([db[key].hh_cv for key in db.keys()])

        # Векторизуем у остальных юзеров поле "github_cv"
        other_forms_github_cv = self.model.vectorize([db[key].github_cv for key in db.keys()])

        # Список индексов юзеров
        list_indexes_users = list(db.keys())

        # №1 - расстояние между целевым юзером и остальными юзерами
        # current - target
        # other - (about_me + hh_cv) / 2
        score_first = \
        self.__get_distance(current_form_target, torch.stack([other_forms_about_me, other_forms_hh_cv]).mean(axis=0))[0]

        # №2 - расстояние между целевым юзером и остальными юзерами
        # current - about_me
        # other - about_me
        score_second = self.__get_distance(current_about_me, other_forms_about_me)[0]

        # №3 - расстояние между целевым юзером и остальными юзерами
        # current - hh_cv
        # other - hh_cv
        score_third = self.__get_distance(current_hh_cv, other_forms_hh_cv)[0]

        # №4 - расстояние между целевым юзером и остальными юзерами
        # current - github_cv
        # other - github_cv
        score_fourth = self.__get_distance(current_github_cv, other_forms_github_cv)[0]

        # Считаем среднее между score about_me и hh_cv
        score_fifth = torch.stack([score_second, score_third, score_fourth]).mean(axis=0)

        score = (score_first * 0.7) + (score_fifth * 0.3)

        values, indices = torch.topk(score, k=score.shape[0])  # min(5, score.shape[0])

        return [{"id": db[list_indexes_users[idx]].id, "name": db[list_indexes_users[idx]].name, "about_me": db[list_indexes_users[idx]].about_me,
                 "cv_path": db[list_indexes_users[idx]].cv_path} for idx in indices]

    def get_implementation(self, RECOMENDATIONS: list, USERS: dict, id_current: int, n_gramm_split: int):
        """
        RECOMENDATIONS - список словарей, где каждый словарь это анкета (поля name, about_me, cv_path)

        USERS - словарь пользователей

        id_current - id текущего юзера

        return

        Список n-gramm к анкетам рекомендаций [[(...),(...),(...)], [(...),(...),(...)]]
        """

        result = []

        # Получаем поле "кого ищем" у целевого юзера
        current_target = USERS[id_current].target

        # очищаем поле "кого ищем" у целевого юзера
        clear_current_target = " ".join(
            [word for word in current_target.split() if word.lower() not in self.stop_words])

        ngramm_target = [" ".join(ngramm) for ngramm in
                         list(ngrams(clear_current_target.split(), n_gramm_split))[::n_gramm_split]]

        # Предобработка для поиска срезов
        ngramm_search_target = [ngramm for ngramm in
                                list(ngrams(clear_current_target.split(), n_gramm_split))[::n_gramm_split]]
        slice_list_target = [re.search(f"{ngramm[0]}.*{ngramm[-1]}", current_target).span() for ngramm in
                             ngramm_search_target]

        # Векторизуем n-gramm целевого юзера
        ngramm_target_emb = self.model.vectorize(ngramm_target)

        print("\n\Векторизовали целевого юзера\n\n")

        for user in RECOMENDATIONS:
            # Получаем текст "о себе" других пользователей
            user_about_me = user['about_me']
            print('user_about_me', user_about_me)

            # очищаем текст "о себе" у других пользователей
            clear_user_about_me = " ".join(
                [word for word in user_about_me.split() if word.lower() not in self.stop_words])

            ngramm_user = [" ".join(ngramm) for ngramm in
                           list(ngrams(clear_user_about_me.split(), n_gramm_split))[::n_gramm_split]]

            # Предобработка для поиска срезов
            ngramm_search_user = [ngramm for ngramm in
                                  list(ngrams(clear_user_about_me.split(), n_gramm_split))[::n_gramm_split]]
            slice_list_user = [re.search(f"{ngramm[0]}.*{ngramm[-1]}", user_about_me).span() for ngramm in
                               ngramm_search_user]

            # Векторизуем n-gramm других юзеров
            ngramm_user_emb = self.model.vectorize(ngramm_user)

            # По столбцам близость i-ой n-grammы первого текста для каждой n-grammы из второго текста
            distance = self.__get_distance(ngramm_target_emb, ngramm_user_emb)

            # Самые ближайшие n-граммы из второго текста
            max_indexes = distance.argmax(axis=1)

            # Самые максимальные значения ближайших n-gramm
            max_values = distance.amax(axis=1)

            pair_n_gramms = [{"curr_n_gramm": slice_list_target[i], "target_n_gramm": slice_list_user[max_indexes[i]],
                              "score": max_values[i].numpy()} for i in range(max_indexes.shape[0])]

            # [:min(3, len(pair_n_gramms))]


            # Берём 50% самых близких n-gramm
            pair_n_gramms = [n_gramm["target_n_gramm"] for n_gramm in
                             sorted(pair_n_gramms, key=lambda x: x['score'], reverse=True)]

            pair_n_gramms = list(set(pair_n_gramms))

            result.append(pair_n_gramms[:min(3, len(pair_n_gramms))])

        print("\n\nВозвращаем результат\n\n")

        return result

    def __get_distance(self, vec_1: torch.Tensor, vec_2: torch.Tensor) -> float:
        """
        Метод получения расстояния между двумя векторами

        Аргументы:
            vec_1: torch.Tensor
            vec_2: torch.Tensor

        Возвращает:
            float
        """

        # print(normalize(vec_1).reshape(1, -1).shape)
        # return torch.nn.functional.cosine_similarity(normalize(vec_1).reshape(1, -1), normalize(vec_2).reshape(1, -1))
        # return torch.nn.PairwiseDistance(p = 2, eps = 1e-10)(normalize(vec_1), normalize(vec_2))
        # return torch.nn.PairwiseDistance(p = 2, eps = 1e-10)(vec_1, vec_2)
        # return torch.nn.functional.cosine_similarity(vec_1.reshape(1, -1), vec_2.reshape(1, -1))

        # Подсчёт процента схожести
        scores = (vec_1 @ vec_2.T) * 100
        return scores
