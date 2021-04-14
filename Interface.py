"""
作者:
    杨贇
版权:
    GPL (C) Copyright 2021, 杨贇.
联系方式:
    smally@stu.ecnu.edu.cn
文件:
    Interface.py
时间:
    2021/4/13 23:04
"""
from abc import abstractmethod

import pygame
import pygame.image

from Button import Button
from Constant import ButtonEnum
from Constant import PlayerEnum
from Text import Text
from Settings import *
from Utils import resource_path
from Utils import get_chess_pos


class AbstractInterface(object):
    """界面超类。"""

    @abstractmethod
    def draw(self):
        """绘制界面抽象方法

        绘制背景、按钮等界面上所存在的元素。
        """
        pass

    @abstractmethod
    def check_buttons(self, _mouse_x, _mouse_y):
        """检查按钮点击抽象方法。

        检查是否有按钮被点击。

        Args:
            _mouse_x: 鼠标点击的 x 坐标
            _mouse_y: 鼠标点击的 y 坐标

        Returns:
            有按钮被点击时，返回 ButtonEnum 中对应按钮类型，\n
            否则返回 ButtonEnum 中无按钮类型。
        """
        pass

    @abstractmethod
    def reset(self):
        """重置页面抽象方法。

        用于重置页面，将页面上元素恢复到初始状态。
        """


class FirstInterface(AbstractInterface):
    """首页类。"""

    def __init__(self, _windows):
        """初始化首页方法。

        Args:
            _windows: 由 Pygame 创建的当前游戏窗口
        """
        self.__windows = _windows

        # 加载背景图并将其缩放至适合窗口的大小。
        self.__background_img = pygame.transform.scale(
            pygame.image.load('./resource/image/background.jpg'),
            [SCREEN_WIDTH, SCREEN_HEIGHT])

        # 创建首页上标题。
        self.__title_text = Text(None, TITLE_HEIGHT, 'Gobang',
                                 WHITE_COLOR, TITLE_X, TITLE_Y)

        # 创建首页上按钮。
        self.__start_button = Button('Start', BUTTON_COLOR, True,
                                     TITLE_X - BUTTON_WIDTH // 2,
                                     TITLE_Y + TITLE_HEIGHT)
        self.__model_button = Button('PVE', MODULE_BUTTON_COLOR, True,
                                     TITLE_X - BUTTON_WIDTH // 2,
                                     TITLE_Y + TITLE_HEIGHT + 60)
        self.__exit_button = Button('Exit', BUTTON_COLOR, True,
                                    TITLE_X - BUTTON_WIDTH // 2,
                                    TITLE_Y + TITLE_HEIGHT + 120)

    def draw(self):
        """绘制首页方法。

        绘制首页的背景与按钮。
        """
        self.__draw_background()
        self.__draw_button(self.__start_button)
        self.__draw_button(self.__model_button)
        self.__draw_button(self.__exit_button)

    def check_buttons(self, _mouse_x, _mouse_y):
        """检查首页按钮点击方法。

        检查首页是否有按钮被点击。

        Args:
            _mouse_x: 鼠标点击的 x 坐标
            _mouse_y: 鼠标点击的 y 坐标

        Returns:
            有按钮被点击时，返回 ButtonEnum 中对应按钮类型，\n
            否则返回 ButtonEnum 中无按钮类型。
        """
        if self.__start_button.clicked(_mouse_x, _mouse_y):
            return ButtonEnum.START_BUTTON
        if self.__model_button.clicked(_mouse_x, _mouse_y):
            return ButtonEnum.MODULE_BUTTON
        if self.__exit_button.clicked(_mouse_x, _mouse_y):
            return ButtonEnum.EXIT_BUTTON
        return ButtonEnum.NO_BUTTON

    def reset(self):
        """重置首页方法。

        重新创建首页上的按钮。
        """
        self.__start_button = Button('Start', BUTTON_COLOR, True,
                                     TITLE_X - BUTTON_WIDTH // 2,
                                     TITLE_Y + TITLE_HEIGHT)
        self.__model_button = Button('PVE', MODULE_BUTTON_COLOR, True,
                                     TITLE_X - BUTTON_WIDTH // 2,
                                     TITLE_Y + TITLE_HEIGHT + 60)
        self.__exit_button = Button('Exit', BUTTON_COLOR, True,
                                    TITLE_X - BUTTON_WIDTH // 2,
                                    TITLE_Y + TITLE_HEIGHT + 120)

    def __draw_background(self):
        """绘制首页背景。"""
        pygame.draw.rect(self.__windows, WHITE_COLOR,
                         pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__windows.blit(self.__background_img, (0, 0))
        self.__windows.blit(*self.__title_text.text_element)

    def __draw_button(self, _button):
        """绘制首页按钮。"""
        self.__windows.fill(_button.color, _button.rect)
        self.__windows.blit(*_button.text_element)


class GameInterface(AbstractInterface):
    """游戏界面类。"""

    def __init__(self, _windows):
        """初始化游戏界面方法。

        Args:
            _windows: 由 Pygame 创建的当前游戏窗口
        """
        self.__windows = _windows

        # 加载 AI 用头像
        self.__ai_img = pygame.transform.scale(pygame.image.load(
            resource_path('./resource/image/ai.jpg')), (100, 100))

        # 创建游戏界面上按钮。
        self.__restart_button = Button('Restart', BUTTON_COLOR, False,
                                       BOARD_WIDTH + 30, 130)
        self.__give_up_button = Button('GiveUp', BUTTON_COLOR, True,
                                       BOARD_WIDTH + 30, BUTTON_HEIGHT + 160)
        self.__back_button = Button('Menu', BUTTON_COLOR, True,
                                    BOARD_WIDTH + 30, 2 * BUTTON_HEIGHT + 190)

    def draw(self, _steps=None):
        """绘制游戏界面方法。

        绘制游戏界面的棋盘、棋子与按钮。

        Args:
            _steps: 已落下的子的列表，格式为[(x 坐标，y 坐标，落子者)]，默认为空
        """
        if _steps is None:
            _steps = []
        self.__draw_background()
        self.__draw_chess(_steps)
        self.__draw_button(self.__restart_button)
        self.__draw_button(self.__give_up_button)
        self.__draw_button(self.__back_button)

    def draw_ai(self):
        """绘制 ai 头像方法。"""
        self.__windows.blit(self.__ai_img, (BOARD_WIDTH + 30, 15))

    def show_winner(self, winner):
        """显示胜者方法。

        在游戏界面右下角显示胜者。

        Args:
            winner: 胜利的玩家或 None，若无人胜利。
        """
        if winner is None:
            return
        res = 'Winner is '
        if winner == PlayerEnum.PLAYER_ONE:
            res += 'Black.'
        else:
            res += 'White.'
        text = Text(None, 30, res, BLUE_COLOR, BOARD_WIDTH + 100,
                    SCREEN_HEIGHT - 45)
        self.__windows.blit(*text.text_element)

    def check_buttons(self, _mouse_x, _mouse_y):
        """检查游戏界面按钮点击方法。

        检查游戏界面是否有按钮被点击。

        Args:
            _mouse_x: 鼠标点击的 x 坐标
            _mouse_y: 鼠标点击的 y 坐标

        Returns:
            有按钮被点击时，返回 ButtonEnum 中对应按钮类型，\n
            否则返回 ButtonEnum 中无按钮类型。
        """
        if self.__restart_button.clicked(_mouse_x, _mouse_y):
            return ButtonEnum.RESTART_BUTTON
        if self.__give_up_button.clicked(_mouse_x, _mouse_y):
            return ButtonEnum.GIVE_UP_BUTTON
        if self.__back_button.clicked(_mouse_x, _mouse_y):
            return ButtonEnum.BACK_BUTTON
        return ButtonEnum.NO_BUTTON

    def reset(self):
        """重置游戏界面方法。

        清空棋盘、棋子并重新创建游戏界面上的按钮。
        """
        self.__draw_background()
        self.__restart_button = Button('Restart', BUTTON_COLOR, False,
                                       BOARD_WIDTH + 30, 130)
        self.__give_up_button = Button('GiveUp', BUTTON_COLOR, True,
                                       BOARD_WIDTH + 30, BUTTON_HEIGHT + 160)
        self.__back_button = Button('Menu', BUTTON_COLOR, True,
                                    BOARD_WIDTH + 30, 2 * BUTTON_HEIGHT + 190)

    def enable_restart_button(self):
        """启用重新开始按钮。

        启用重新开始按钮的同时需要禁用投降按钮。
        """
        if not self.__restart_button.enabled:
            self.__restart_button.reverse_enabled()
        if self.__give_up_button.enabled:
            self.__give_up_button.reverse_enabled()

    def enable_give_up_button(self):
        """启用投降按钮。

        启用投降按钮的同时需要禁用重新开始按钮。
        """
        if not self.__give_up_button.enabled:
            self.__give_up_button.reverse_enabled()
        if self.__restart_button.enabled:
            self.__restart_button.reverse_enabled()

    @staticmethod
    def check_in_board(_x, _y):
        """检查坐标是否在棋盘内方法。

        Args:
            _x: x 坐标
            _y: y 坐标

        Returns:
            坐标是否在棋盘内。
        """
        return 0 < _x < BOARD_WIDTH and 0 < _y < BOARD_HEIGHT

    def __draw_background(self):
        """绘制游戏界面背景。"""
        # 绘制棋盘。
        pygame.draw.rect(self.__windows, LIGHT_YELLOW,
                         (0, 0, BOARD_WIDTH, BOARD_HEIGHT))
        # 绘制右侧白色背景。
        pygame.draw.rect(self.__windows, WHITE_COLOR,
                         (BOARD_WIDTH, 0, INFO_WIDTH, BOARD_HEIGHT))

        # 绘制棋盘上线。
        for y in range(CHESS_MAX_NUM):
            # 画横线。
            start_pos, end_pos = ((REC_SIZE // 2,
                                   REC_SIZE // 2 + REC_SIZE * y),
                                  (BOARD_WIDTH - REC_SIZE // 2,
                                   REC_SIZE // 2 + REC_SIZE * y))
            if y == CHESS_MAX_NUM // 2:
                width = 2
            else:
                width = 1
            pygame.draw.line(self.__windows, BLACK_COLOR, start_pos,
                             end_pos, width)
        for x in range(CHESS_MAX_NUM):
            # 画竖线。
            start_pos, end_pos = ((REC_SIZE // 2 + REC_SIZE * x,
                                   REC_SIZE // 2),
                                  (REC_SIZE // 2 + REC_SIZE * x,
                                   BOARD_HEIGHT - REC_SIZE // 2))
            if x == BOARD_HEIGHT // 2:
                width = 2
            else:
                width = 1
            pygame.draw.line(self.__windows, BLACK_COLOR, start_pos,
                             end_pos, width)

        # 绘制棋盘上方块。
        rec_size = 8
        pos = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]
        for x, y in pos:
            pygame.draw.rect(self.__windows, BLACK_COLOR,
                             (REC_SIZE // 2 + REC_SIZE * x - rec_size // 2,
                              REC_SIZE // 2 + REC_SIZE * y - rec_size // 2,
                              rec_size, rec_size))

    def __draw_chess(self, _steps):
        """绘制已落下的棋子。"""
        player_color = {
            PlayerEnum.PLAYER_ONE: PLAYER_ONE_COLOR,
            PlayerEnum.PLAYER_TWO: PLAYER_TWO_COLOR
        }
        # 绘制已落下棋子。
        for i in range(len(_steps)):
            board_x, board_y, turn = _steps[i]
            x, y = get_chess_pos(board_x, board_y)
            pos = (x + REC_SIZE // 2, y + REC_SIZE // 2)
            radius = CHESS_RADIUS
            if turn == PlayerEnum.PLAYER_ONE:
                op_turn = PlayerEnum.PLAYER_TWO
            else:
                op_turn = PlayerEnum.PLAYER_ONE
            pygame.draw.circle(self.__windows, player_color[turn],
                               pos, radius)
            text = Text(None, REC_SIZE * 2 // 3, str(i),
                        player_color[op_turn], *pos)
            self.__windows.blit(*text.text_element)
        # 圈出最后落下的棋子。
        if len(_steps) > 0:
            last_pos = _steps[-1]
            x, y = get_chess_pos(last_pos[0], last_pos[1])
            line_list = [(x, y), (x + REC_SIZE, y),
                         (x + REC_SIZE, y + REC_SIZE),
                         (x, y + REC_SIZE)]
            pygame.draw.lines(self.__windows, PURPLE_COLOR, True, line_list, 1)

    def __draw_button(self, _button):
        """绘制游戏界面按钮。"""
        self.__windows.fill(_button.color, _button.rect)
        self.__windows.blit(*_button.text_element)
