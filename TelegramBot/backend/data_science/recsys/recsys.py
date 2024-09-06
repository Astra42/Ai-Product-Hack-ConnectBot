import torch
from sentence_transformers import SentenceTransformer
import nltk
from nltk.corpus import stopwords
from nltk import ngrams
from typing import List, Union, Optional

nltk.download('stopwords')

class TextVectorizer_v2:
    def __init__(self, model_checkpoint: str) -> None:
        
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
        print(f"Пришла форма: {form}")


        if isinstance(form, dict):
            sentences = self.__preprocess([form[key] for key in tuple(form.keys())])
            print(f"Пришла форма: {sentences}")


            with torch.no_grad():
                sentence_embeddings = self.model.encode(sentences, convert_to_tensor=True, normalize_embeddings=True).to(self.device).cpu()

            return {key: sentence_embeddings[i] for i, key in enumerate(tuple(form.keys()))}

        elif isinstance(form, list):
            sentences = self.__preprocess(form)
            with torch.no_grad():
                sentence_embeddings = self.model.encode(sentences, convert_to_tensor=True, normalize_embeddings=True).to(self.device).cpu()

            return sentence_embeddings
        
        return None
    

class RecSys:
    def __init__(self, model):
        self.model = model
    
    def get_score_by_forms(self, USERS: dict, id_current: int) -> List:
        db = USERS.copy()

        # Векторизуем целевого юзера
        current_form = self.model.vectorize([db[id_current].target])

        db.pop(id_current)
        # db = all([for key, value in ])
        db = {idx: db[idx] for idx in db.keys() if all(db[idx].make_attrs_like_dict().values())}

        print('ЖОПА\n\n\n\n')
        print(id_current)
        print(db)


        # Векторизуем остальных юзеров
        other_forms = self.model.vectorize([db[key].about_me for key in db.keys()])
        list_indexes_users = list(db.keys())

        # Получаем двумерный тензор [[..., ..., ]]
        score = self.__get_distance(current_form, other_forms)[0]

        values, indices = torch.topk(score, k=min(5, score.shape[0]))

        return [{"name": db[list_indexes_users[idx]].name, "about_me": db[list_indexes_users[idx]].about_me, "cv_path": db[list_indexes_users[idx]].cv_path} for idx in indices]

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
