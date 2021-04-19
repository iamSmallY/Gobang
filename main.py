"""
作者:
    杨贇
版权:
    GPL (C) Copyright 2021, 杨贇.
联系方式:
    smally@stu.ecnu.edu.cn
文件:
    main.py
时间:
    2021/4/13 21:41
"""
import pygame
from Interactive import Interactive


def main():
    """五子棋游戏主入口。

    初始化并启动游戏。
    """
    pygame.init()
    game = Interactive()
    while True:
        game.play()


if __name__ == '__main__':
    main()
