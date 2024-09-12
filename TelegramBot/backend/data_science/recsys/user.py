class User:
    def __init__(self, 
            id: str,
            name: str = None,
            about_me: str = None,
            cv_path: str = None,
            target: str = None,
            hh_cv: str = None,
            github_cv: str = None,
        ):
        self.id = id
        self.name = name
        self.about_me = about_me
        self.cv_path = cv_path
        self.target = target
        self.hh_cv = hh_cv
        self.github_cv = github_cv
        
        
        # if self.name is None: 
        #     self.name = " "
        # if self.about_me is None:
        #     self.about_me = " "
        if self.cv_path is None:
            self.cv_path = " "
        # if self.target is None:
        #     self.target = " "
        # if self.hh_cv is None:
        #     self.hh_cv = {
        #         "position": "",
        #         "age": "",
        #         "gender": "",
        #         "job_search_status": "",
        #         "about": "",
        #         "jobs": [],
        #         "tags": [],
        #         "eduacation": [],
        #         "link": ""
        #     }
        
        """
        https://hh.ru/resume/46d55ec600080f27eb0039ed1f794c6a344968?query=DS&searchRid=172607926475088847a46e5d0a22c612&hhtmFrom=resume_search_result
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

        # if self.github_cv is None:
        #     self.github_cv = {
        #         "github_username": "",
        #         "github_bio": "",
        #         "github_link": "",
        #         "github_repos": [
        #         ]
        #     }
            
    # https://github.com/avalur
    # {
    #     "github_username": str,
    #     "github_bio": str,
    #     "github_link": github_url,
    #     "github_repos": [
    #         {"name": str1, "description": str1, "language": str1, "readme": str1, "link": str1},
    #         {"name": str2, "description": str2, "language": str2, "readme": str2, "link": str2},
    #         ...
    #     ]
    # }



    def make_attrs_like_dict(self):
        return vars(self)

    def __str__(self):
        return str(self.make_attrs_like_dict())

    def __repr__(self):
        return str(self.make_attrs_like_dict())



if __name__ == "__main__":
    user = User(id=0)
    print(f"{user.make_attrs_like_dict()=}")