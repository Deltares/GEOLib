from enum import IntEnum


class DrainType(IntEnum):
    STRIP = 0
    COLUMN = 1
    SANDWALL = 2


class DrainGridType(IntEnum):
    TRIANGULAR = 0
    RECTANGULAR = 1
    UNDERDETERMINED = 2


class DrainSchedule(IntEnum):
    OFF = 0
    SIMPLE_INPUT = 1
    DETAILED_INPUT = 2
