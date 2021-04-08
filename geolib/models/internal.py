from enum import IntEnum


class Bool(IntEnum):
    FALSE = 0
    TRUE = 1

    def __bool__(self):
        return self == Bool.TRUE
