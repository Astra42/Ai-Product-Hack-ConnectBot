class User:
    def __init__(self, id: str, name: str = None, about_me: str = None, cv_path: str = None, target: str = None):
        self.id = id
        self.name = name
        self.about_me = about_me
        self.cv_path = cv_path
        self.target = target

    def make_attrs_like_dict(self):
        return vars(self)

    def __str__(self):
        return str(self.make_attrs_like_dict())

    def __repr__(self):
        return str(self.make_attrs_like_dict())
