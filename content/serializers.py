class ContentSerializer:
    def __init__(self, **kwargs):
        self.data = kwargs
        self.errors = {}

    dict_base: dict = {
        "title": str,
        "module": str,
        "students": int,
        "description": str,
        "is_active": bool,
    }

    def is_valid(self):
        try:
            self.check_keys()
            self.check_types()
            return True
        except KeyError:
            self.errors

    def check_keys(self):
        dict_response = list(self.dict_base.keys())
        for item in dict_response:
            if item not in self.data:
                self.errors.update({item: "missing key"})
        if self.errors:
            raise KeyError

    def check_types(self):
        for key, value in self.dict_base.items():
            if type(self.data[key]) is not value:
                self.errors.update({key: f"must be a {value.__name__}"})
        if self.errors:
            raise KeyError
