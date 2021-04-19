"""
作者:
    杨贇
版权:
    GPL (C) Copyright 2021, 杨贇.
联系方式:
    smally@stu.ecnu.edu.cn
文件:
    Interactive.py
时间:
    2021/4/14 15:28
"""
import pygame

from AI import AI
from Constant import ButtonEnum
from Constant import PlayerEnum
from Interface import FirstInterface
from Interface import GameInterface
from Settings import *
from Utils import get_board_pos
from Utils import resource_path


class Interactive(object):
    """游戏交互类。

    用于完成游戏中的人机交互。
    """

    def __init__(self):
        """游戏交互初始化方法。"""
        # 初始化游戏窗口和时钟。
        self.__windows, self.__clock = Interactive.__init_windows()

        # 初始化游戏界面。
        self.__first_interface = FirstInterface(self.__windows)
        self.__game_interface = GameInterface(self.__windows)
        self.__in_first_interface = True

        # 初始化游戏相关数据。
        self.__board = [[PlayerEnum.NO_PLAYER] * BOARD_WIDTH
                        for _ in range(BOARD_HEIGHT)]
        self.__player = PlayerEnum.PLAYER_ONE, PlayerEnum.PLAYER_TWO
        self.__winner = None        # 游戏中胜者。
        self.__steps = []        # 落子记录。

        # 初始化 AI 相关数据
        self.__use_AI = True  # 默认为人机对战。
        self.__ai = AI(self.__player)

    def play(self):
        """进行游戏方法。

        处理游戏中的各种交互事件：\n
        1. 关闭界面事件。\n
        2. 界面跳转事件。\n
        3. 落子事件。\n
        4. 投降与重新开始事件。
        """
        self.__handle_event()       # 处理 Pygame 中的事件。

        self.__draw_window()

        now, _ = self.__player
        if self.__winner is None and now == PlayerEnum.PLAYER_TWO:
            people_pos = self.__steps[-1][0]
            self.__make_one_step(
                self.__ai.make_decision(self.__board, people_pos))

    def __make_one_step(self, _board_pos):
        """进行一步落子方法。

        先进行一步落子，再判断是否获胜，最后翻转当前落子者。

        Args:
            _board_pos: 落子坐标。
        """
        board_x, board_y = _board_pos
        now, _ = self.__player
        self.__board[board_x][board_y] = now
        self.__steps.append(((board_x, board_y), now))
        if self.__ai.game_over(self.__board, _board_pos, self.__player):
            self.__winner = now
        self.__player = self.__player[::-1]

    def __click(self, _mouse_pos):
        """处理点击事件方法。

        根据所在界面，判断点击位置并处理。

        Args:
            _mouse_pos: 鼠标点击的坐标
        """
        now, nxt = self.__player
        if self.__in_first_interface:
            status = self.__first_interface.check_buttons(_mouse_pos)
            if status == ButtonEnum.START_BUTTON:
                self.__game_interface.reset()
                self.__in_first_interface = False
            elif status == ButtonEnum.EXIT_BUTTON:
                exit(0)
        else:
            status = self.__game_interface.check_buttons(_mouse_pos)
            if status == ButtonEnum.RESTART_BUTTON:
                # 重新开始游戏，先清空游戏数据，并使得投降按钮可用。
                self.__reset_game_data()
                self.__game_interface.enable_give_up_button()
            elif status == ButtonEnum.GIVE_UP_BUTTON:
                # 投降，设定胜者，并使得重新开始按钮可用。
                if self.__use_AI and now == PlayerEnum.PLAYER_TWO:
                    # 不能替 AI 投降。
                    return
                self.__winner = nxt
                self.__game_interface.enable_restart_button()
            elif status == ButtonEnum.BACK_BUTTON:
                self.__first_interface.reset()      # 清空页面。
                self.__reset_game_data()        # 清空游戏数据。
                self.__in_first_interface = True
            else:
                # 棋盘内落子事件。
                if self.__use_AI and now == PlayerEnum.PLAYER_TWO:
                    # 如果是 AI 的回合，则不可落子。
                    return
                if self.__winner is not None:
                    # 如果游戏结束，则不可落子。
                    return
                elif self.__game_interface.check_in_board(_mouse_pos):
                    board_x, board_y = get_board_pos(_mouse_pos)
                    if self.__board[board_x][board_y] == PlayerEnum.NO_PLAYER:
                        self.__make_one_step((board_x, board_y))

    def __draw_window(self):
        """渲染窗口方法。"""
        if self.__in_first_interface:
            self.__first_interface.draw()
        else:
            self.__game_interface.draw(self.__steps)

            # 如果是人机对战，且比赛未结束，则画出 AI 头像。
            if self.__use_AI and self.__winner is None:
                self.__game_interface.draw_ai()

            # 如果有胜者，则标出胜者，否则说明在游戏中，进行游戏中判断。
            if self.__winner is not None:
                self.__game_interface.show_winner(self.__winner)

            # 修改鼠标样式。
            self.__change_mouse_show()

        pygame.display.update()

    def __handle_event(self):
        """处理 Pygame 事件方法。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 退出事件。
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标点击事件。
                self.__click(pygame.mouse.get_pos())

    def __change_mouse_show(self):
        """更改鼠标样式方法。

        在非 AI 模式，或 AI 模式但非后手落子时，更改鼠标样式，便于判断位置。\n
        当鼠标位于棋盘内且该处无棋子时，将鼠标变为一个亮红色的圆圈。
        """
        now, _ = self.__player
        if self.__in_first_interface or self.__winner is not None:
            # 在非游戏中时，不修改鼠标样式
            pygame.mouse.set_visible(True)
            return
        if self.__use_AI and now == PlayerEnum.PLAYER_TWO:
            # 在 AI 落子时，不修改鼠标样式
            pygame.mouse.set_visible(True)
            return
        if self.__game_interface.check_in_board(pygame.mouse.get_pos()):
            board_x, board_y = get_board_pos(pygame.mouse.get_pos())
            if self.__board[board_x][board_y] == PlayerEnum.NO_PLAYER:
                pygame.mouse.set_visible(False)
                pygame.draw.circle(self.__windows, LIGHT_RED,
                                   pygame.mouse.get_pos(), CHESS_RADIUS)
            else:
                pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(True)

    def __reset_game_data(self):
        """重置游戏数据方法。

        清空棋盘，并设置目前玩家为玩家 1，胜者为空。
        """
        self.__board = [[PlayerEnum.NO_PLAYER] * BOARD_WIDTH
                        for _ in range(BOARD_HEIGHT)]
        self.__player = PlayerEnum.PLAYER_ONE, PlayerEnum.PLAYER_TWO
        self.__winner = None
        self.__steps = []
        self.__ai = AI(self.__player)

    @staticmethod
    def __init_windows():
        """初始化游戏窗口方法。

        初始化游戏窗口，设定窗口大小、标题、图标以及游戏帧率。

        Returns:
            (windows, clock)——游戏窗口和游戏时钟。
        """
        # 初始化窗口、标题和图标。
        windows = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("{} {}".format(GAME_NAME, GAME_VERSION))
        pygame.display.set_icon(
            pygame.image.load(resource_path('./resource/image/head.ico')))

        # 初始化时钟、设定帧率为 60 帧/秒。
        clock = pygame.time.Clock()
        clock.tick(60)
        return windows, clock
