"""
作者:
    杨贇
版权:
    GPL (C) Copyright 2021, 杨贇.
联系方式:
    smally@stu.ecnu.edu.cn
文件:
    Utils.py
时间:
    2021/4/14 8:20
"""
import os
import sys
from random import randint

from Settings import *


def resource_path(path):
    """获取资源路径。

    对于由 Python 文件直接运行的窗口，资源路径应为当前文件夹路径 + 资源的相对路径。\n
    而对于从打包后的 exe 文件所运行的窗口，资源会被存放到 windows 临时文件夹下，
    所以资源路径为临时文件夹路径 + 资源相对路径。

    Args:
        path: 资源文件所在相对路径。

    Returns:
        拼接后的资源文件绝对路径。
    """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, path)


def get_chess_pos(_board_pos):
    """获取棋子坐标。

    输入棋子在棋盘上的坐标，输出棋子在游戏中的真实坐标。

    Args:
        _board_pos: 棋盘上坐标

    Returns:
        (真实 x 坐标， 真实 y 坐标).
    """
    board_x, board_y = _board_pos
    return board_x * REC_SIZE, board_y * REC_SIZE


def get_board_pos(_pos):
    """获取棋子在棋盘上坐标。

    输入棋子真实坐标，输出棋子在棋盘上坐标。

    Args:
        _pos: 真实坐标

    Returns:
        (棋盘上 x 坐标，棋盘上 y 坐标).
    """
    x, y = _pos
    return x // REC_SIZE, y // REC_SIZE


def board_to_str(_board):
    """获取棋盘的 str 形式。

    Args:
        _board: 棋盘数组

    Returns:
        棋盘的字符串形式。
    """
    return "".join(["".join([str(i.value) for i in j]) for j in _board])


def random_score(score):
    """使得分值进行上下 1% 的浮动。

    Args:
        score: 分值

    Returns:
        随机浮动的分值。
    """
    rand = randint(0, 200)
    # 产生 -10% - 10% 之间的随机数
    rand = (rand - 100) / 1000
    return int(score + rand * score)
