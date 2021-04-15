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
        # 任何对 __board 的操作都需要先行转置。
        self.__board = [[PlayerEnum.NO_PLAYER] * BOARD_WIDTH
                        for _ in range(BOARD_HEIGHT)]
        self.__now = PlayerEnum.PLAYER_ONE     # 默认玩家 1 先手。
        self.__next = PlayerEnum.PLAYER_TWO    # 玩家 2 为后手。
        self.__winner = None        # 游戏中胜者。
        self.__steps = []        # 落子记录。

        # 初始化 AI 相关数据
        self.__use_AI = True  # 默认为人机对战。

    def play(self):
        """进行游戏方法。

        处理游戏中的各种交互事件：\n
        1. 关闭界面事件。\n
        2. 界面跳转事件。\n
        3. 落子事件。\n
        4. 投降与重新开始事件。
        """
        self.__handle_event()       # 处理 Pygame 中的事件。

        # 渲染页面。
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
            else:
                # TODO(SmallY) 游戏中判断。
                #   判断是否游戏结束。
                #   判断是否轮到 AI 落子。
                pass

            # 修改鼠标样式。
            self.__change_mouse_show()

        pygame.display.update()

    def __click(self, _mouse_x, _mouse_y):
        """处理点击事件方法。

        根据所在界面，判断点击位置并处理。

        Args:
            _mouse_x: 鼠标点击的 x 坐标
            _mouse_y: 鼠标点击的 y 坐标
        """
        if self.__in_first_interface:
            status = self.__first_interface.check_buttons(_mouse_x, _mouse_y)
            if status == ButtonEnum.START_BUTTON:
                self.__game_interface.reset()
                self.__in_first_interface = False
            elif status == ButtonEnum.EXIT_BUTTON:
                exit(0)
        else:
            status = self.__game_interface.check_buttons(_mouse_x, _mouse_y)
            if status == ButtonEnum.RESTART_BUTTON:
                # 重新开始游戏，先清空游戏数据，并使得投降按钮可用。
                self.__reset_game_data()
                self.__game_interface.enable_give_up_button()
            elif status == ButtonEnum.GIVE_UP_BUTTON:
                # 投降，设定胜者，并使得重新开始按钮可用。
                if self.__use_AI and self.__now == PlayerEnum.PLAYER_TWO:
                    # 不能替 AI 投降。
                    return
                self.__winner = self.__next
                self.__game_interface.enable_restart_button()
            elif status == ButtonEnum.BACK_BUTTON:
                self.__first_interface.reset()      # 清空页面。
                self.__reset_game_data()        # 清空游戏数据。
                self.__in_first_interface = True
            else:
                # 棋盘内落子事件。
                if self.__use_AI and self.__now == PlayerEnum.PLAYER_TWO:
                    # 如果是 AI 的回合，则不可落子。
                    return
                elif self.__game_interface.check_in_board(_mouse_x, _mouse_y):
                    board_x, board_y = get_board_pos(_mouse_x, _mouse_y)
                    if self.__board[board_y][board_x] == 0:
                        self.__board[board_y][board_x] = self.__now
                        self.__steps.append((board_x, board_y, self.__now))
                        self.__now, self.__next = self.__next, self.__now

    def __handle_event(self):
        """处理 Pygame 事件方法。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 退出事件。
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标点击事件。
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.__click(mouse_x, mouse_y)

    def __change_mouse_show(self):
        """更改鼠标样式方法。

        在非 AI 模式，或 AI 模式但非后手落子时，更改鼠标样式，便于判断位置。\n
        当鼠标位于棋盘内且该处无棋子时，将鼠标变为一个亮红色的圆圈。
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.__in_first_interface or self.__winner is not None:
            # 在非游戏中时，不修改鼠标样式
            pygame.mouse.set_visible(True)
            return
        if self.__use_AI and self.__now == PlayerEnum.PLAYER_TWO:
            # 在 AI 落子时，不修改鼠标样式
            pygame.mouse.set_visible(True)
            return
        if self.__game_interface.check_in_board(mouse_x, mouse_y):
            board_x, board_y = get_board_pos(mouse_x, mouse_y)
            if self.__board[board_y][board_x] == 0:
                pygame.mouse.set_visible(False)
                pygame.draw.circle(self.__windows, LIGHT_RED,
                                   (mouse_x, mouse_y), CHESS_RADIUS)
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
        self.__now = PlayerEnum.PLAYER_ONE
        self.__next = PlayerEnum.PLAYER_TWO
        self.__winner = None
        self.__steps = []

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


if __name__ == '__main__':
    pygame.init()
    game = Interactive()
    while True:
        game.play()
