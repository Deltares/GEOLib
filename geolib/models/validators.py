class BaseValidator:
    def __init__(self, ds):
        self.ds = ds

    @property
    def is_valid(self) -> bool:
        return all(
            [
                getattr(self, func)()
                for func in dir(self)
                if (func.startswith("is_valid_"))
            ]
        )
