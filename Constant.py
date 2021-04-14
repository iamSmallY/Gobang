"""
作者:
    杨贇
版权:
    GPL (C) Copyright 2021, 杨贇.
联系方式:
    smally@stu.ecnu.edu.cn
文件:
    Constant.py
时间:
    2021/4/14 10:02
"""
from enum import IntEnum


class ButtonEnum(IntEnum):
    """按钮枚举类。

    为每种按钮编号，无按钮编号为 -1.
    """
    NO_BUTTON = -1,
    START_BUTTON = 1,
    MODULE_BUTTON = 2,
    EXIT_BUTTON = 3,
    RESTART_BUTTON = 4,
    GIVE_UP_BUTTON = 5,
    BACK_BUTTON = 6


class PlayerEnum(IntEnum):
    """玩家枚举类。

    为每个玩家编号，分为玩家 1、玩家 2 以及无玩家。
    """
    PLAYER_ONE = 0,
    PLAYER_TWO = 1,
    NO_PLAYER = 2,


class ChessType(IntEnum):
    """棋形枚举类。

    为每种棋形编号，分为\n
    无棋形，眠二、活二、眠三、活三、冲四、活四、活五。
    """
    NONE = 0,
    SLEEP_TWO = 1,
    LIVE_TWO = 2,
    SLEEP_THREE = 3,
    LIVE_THREE = 4,
    SLEEP_FOUR = 5,
    LIVE_FOUR = 6,
    LIVE_FIVE = 7,


class ChessScore(IntEnum):
    """棋形分值枚举类。

    为每种棋形分数编号。
    """
    LIVE_FIVE = 10000,
    LIVE_FOUR = 10000,
    SLEEP_FOUR = 1000,
    LIVE_THREE = 100,
    SLEEP_THREE = 10,
    LIVE_TWO = 8,
    SLEEP_TWO = 2,
    MAX = 0x7fffffff,
    MIN = -1 * 0x7fffffff,
