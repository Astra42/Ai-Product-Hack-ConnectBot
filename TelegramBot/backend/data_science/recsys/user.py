

class User:
    def __init__(self, 
            id: str,
            name: str = None,
            about_me: str = None,
            cv_path: str = None,
            target: str = None,
            hh_cv: str = None,
        ):
        self.id = id
        self.name = name
        self.about_me = about_me
        self.cv_path = cv_path
        self.target = target
        self.hh_cv = hh_cv
        """
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

    def make_attrs_like_dict(self):
        return vars(self)

    def __str__(self):
        return str(self.make_attrs_like_dict())

    def __repr__(self):
        return str(self.make_attrs_like_dict())



if __name__ == "__main__":
    user = User(id=0)
    print(f"{user.make_attrs_like_dict()=}")
