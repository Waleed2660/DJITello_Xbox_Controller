from enum import Enum


class BUTTON(Enum):
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4
    RB = 5
    MID_LEFT = 6
    MID_RIGHT = 7
    LEFT_JOY_BUTTON = 8
    RIGHT_JOY_BUTTON = 9


class LEFT_JOYSTICK(Enum):
    RIGHT = 0
    LEFT = 0
    FORWARD = 1
    BACKWARD = 1


class RIGHT_JOYSTICK(Enum):
    RIGHT = 2
    LEFT = 2
    FORWARD = 3
    BACKWARD = 3


class TRIGGERS(Enum):
    LEFT = 4
    RIGHT = 5

