"""
作者:
    杨贇
版权:
    GPL (C) Copyright 2021, 杨贇.
联系方式:
    smally@stu.ecnu.edu.cn
文件:
    Text.py
时间:
    2021/4/14 8:38
"""
import pygame


class Text(object):
    """Pygame 文字类。

    对 Pygame 中绘制文字时所需设置的文字属性进行包装后得到的类。
    """

    def __init__(self, _font, _size, _text, _text_color, _pos):
        """初始化文字对象方法。

        设置文字的各种属性。

        Args:
            _font: 字体
            _size: 字号
            _text: 文字内容
            _text_color： 文字颜色
            _pos: 文字所在坐标
        """
        self.__text_font = pygame.font.SysFont(_font, _size)
        self.__text_image = self.__text_font.render(_text, True, _text_color)
        self.__text_image_rect = self.__text_image.get_rect()
        self.__text_image_rect.center = _pos

    @property
    def text_element(self):
        """文字元素属性。

        获取文字中关键属性，用以 Pygame 绘制。

        Returns:
            (文字，文字矩形)——绘图所需的两个属性。
        """
        return self.__text_image, self.__text_image_rect
