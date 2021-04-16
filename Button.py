"""
作者:
    杨贇
版权:
    GPL (C) Copyright 2021, 杨贇.
联系方式:
    smally@stu.ecnu.edu.cn
文件:
    Button.py
时间:
    2021/4/14 8:50
"""
import pygame

from Text import Text
from Settings import *


class Button(object):
    """Pygame 按钮类。

    对 Pygame 中绘制按钮时所需设置的矩形属性进行包装后得到的类。
    """

    def __init__(self, _text, _color, _enabled, _pos):
        """初始化按钮方法。

        设置按钮的各种属性。

        Args:
            _text: 按钮显示的文字
            _color: 按钮的颜色列表，需要含有可用和禁用两种颜色
            _enabled: 按钮是否可用
            _pos: 按钮左上角坐标
        """
        self.__color = _color
        self.__enabled = _enabled

        self.__rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.__rect.topleft = _pos

        self.__text = _text
        self.__text_image = Text(None, BUTTON_HEIGHT * 2 // 3,
                                 self.__text, WHITE_COLOR, self.__rect.center)

    def clicked(self, _mouse_pos):
        """判断按钮被点击方法。

        输入按钮点击的 x, y 坐标，输出按钮是否被点击。\n
        按钮必须处于可用状态才可被点击。

        Args:
            _mouse_pos: 按钮点击的坐标

        Returns:
            按钮对象是否被点击。
        """
        mouse_x, mouse_y = _mouse_pos
        return self.__enabled and self.__rect.collidepoint(mouse_x, mouse_y)

    def reverse_enabled(self):
        """反转按钮可用性方法。

        将按钮可用改为禁用，禁用改为可用。
        """
        self.__enabled = not self.__enabled

    @property
    def enabled(self):
        """可用性属性。

        Returns:
            按钮对象是否可用。
        """
        return self.__enabled

    @property
    def color(self):
        """按钮颜色属性。

        Returns:
            按钮对象当前颜色
        """
        return self.__color[0] if self.__enabled else self.__color[1]

    @property
    def rect(self):
        """按钮矩形属性。

        Returns:
            按钮矩形。
        """
        return self.__rect

    @property
    def text(self):
        """按钮上文字属性。

        Returns:
            按钮对象上文字。
        """
        return self.__text

    @text.setter
    def text(self, value):
        """设置按钮上文字方法。

        设置按钮上文字，并重新声明 Text 对象。

        Args:
            value: 新文字
        """
        self.__text = value
        self.__text_image = Text(None, BUTTON_HEIGHT * 2 // 3,
                                 self.__text, self.__color, *self.__rect.center)

    @property
    def text_element(self):
        """按钮上文字元素属性。

        Returns:
            按钮上文字元素。
        """
        return self.__text_image.text_element
