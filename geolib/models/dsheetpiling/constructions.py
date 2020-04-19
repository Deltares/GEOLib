from pydantic import BaseModel as DataModel


class Pile(DataModel):
    """DSheetPiling Pile.

    .. todo::
        Unify with D-Foundations Pile type.
    """


class DiaphragmWall(DataModel):
    pass


class Sheet(DataModel):
    pass
