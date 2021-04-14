"""
作者:
    杨贇
版权:
    GPL (C) Copyright 2021, 杨贇.
联系方式:
    smally@stu.ecnu.edu.cn
文件:
    Settings.py
时间:
    2021/4/13 23:28
"""
GAME_NAME = 'Gobang'        # 游戏名称
GAME_VERSION = 'v2.0'       # 游戏版本

REC_SIZE = 50                               # 棋盘上每一格长宽
CHESS_RADIUS = REC_SIZE//2 - 2              # 棋子半径
CHESS_MAX_NUM = 15                          # 棋盘每行每列格子数量
BOARD_WIDTH = CHESS_MAX_NUM * REC_SIZE      # 棋盘长度
BOARD_HEIGHT = CHESS_MAX_NUM * REC_SIZE     # 棋盘宽度

INFO_WIDTH = 200        # 信息栏长度
BUTTON_WIDTH = 140      # 按钮长度
BUTTON_HEIGHT = 50      # 按钮宽度
BUTTON_COLOR = [(26, 173, 25), (158, 217, 157)]         # 按钮颜色
MODULE_BUTTON_COLOR = [(0, 229, 238), (83, 134, 139)]   # 按钮颜色

TITLE_WIDTH = 280       # 标题长度
TITLE_HEIGHT = 100      # 标题宽度

SCREEN_WIDTH = BOARD_WIDTH + INFO_WIDTH     # 屏幕长度
SCREEN_HEIGHT = BOARD_HEIGHT                # 屏幕宽度

TITLE_X = SCREEN_WIDTH // 2     # 标题 x 轴所在位置
TITLE_Y = SCREEN_HEIGHT // 4    # 标题 y 轴所在位置

PLAYER_ONE_COLOR = (88, 87, 86)     # 玩家 1 棋子颜色
PLAYER_TWO_COLOR = (255, 251, 240)  # 玩家 2 棋子颜色
BLACK_COLOR = (0, 0, 0)             # 黑色
WHITE_COLOR = (255, 255, 255)       # 白色
BLUE_COLOR = (0, 0, 255)            # 蓝色
PURPLE_COLOR = (255, 0, 255)        # 紫色
LIGHT_YELLOW = (247, 238, 214)      # 亮黄色
LIGHT_RED = (213, 90, 107)          # 亮红色

AI_SEARCH_DEPTH = 4         # 博弈树搜索深度
AI_LIMITED_MOVE_NUM = 10    # 博弈树搜索宽度

CHESS_TYPE_NUM = 8          # 棋形总数
