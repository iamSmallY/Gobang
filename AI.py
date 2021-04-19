"""
作者:
    杨贇
版权:
    GPL (C) Copyright 2021, 杨贇.
联系方式:
    smally@stu.ecnu.edu.cn
文件:
    AI.py
时间:
    2021/4/14 23:47
"""
from Constant import ChessType
from Constant import ChessScore
from Constant import PlayerEnum
from Settings import *
from Utils import random_score


class AI:
    """AI 类。"""

    def __init__(self, _player):
        """AI 对象初始化函数。

        Args:
            _player: (真实玩家编号，AI 玩家编号)
        """
        # 搜索时所需要遍历的米字方向。
        self.__search_direction = [(0, 1), (1, 0), (1, -1), (1, 1)]

        # 棋盘上当前可选落子点。
        self.__can_move = [[0] * CHESS_MAX_NUM for _ in range(CHESS_MAX_NUM)]
        self.__radius = 1  # 可选落子点半径。

        # 初始化玩家和 AI 编号。
        people_player, ai_player = _player
        self.__people_player = people_player
        self.__ai_player = ai_player

    def game_over(self, _board, _pos, _player):
        """判断游戏是否结束方法。
        
        根据当前所落子判断游戏是否结束。

        Args:
            _board: 棋盘数组
            _pos: 当前落子的坐标
            _player: (当前玩家编号, 对手玩家编号)
            
        Returns:
            游戏是否结束。
        """
        count = [0] * CHESS_TYPE_NUM
        for offset in self.__search_direction:
            self.__get_one_chess_shape(_board, _pos, _player,
                                       offset, count)
        return count[ChessType.LIVE_FIVE] > 0

    def make_decision(self, _board, _pos):
        """AI 落子方法。

        根据玩家落子位置，决定本次落子位置。

        Args:
            _board: 棋盘数组
            _pos: 玩家落子的坐标

        Returns:
            (x, y)——决定落子的坐标。
        """
        self.__update_can_move(_board, _pos, True)  # 更新可选落子点。

        # 搜索最佳落子点。
        player = self.__ai_player, self.__people_player
        _, best_move = self.__min_max_search(_board, player, ChessScore.MIN,
                                             ChessScore.MAX, 0)

        self.__update_can_move(_board, best_move, True)  # 更新可选落子点。

        return best_move

    def __min_max_search(self, _board, _player, _alpha, _beta, _depth):
        """获取最佳落子点方法。

        搜索主体为极小极大搜索，所涉及到的剪枝算法有：\n
        1). α,β-剪枝；\n
        2). 启发式搜索。

        Args:
            _board: 棋盘数组
            _player: (己方玩家编号, 敌方玩家编号)
            _alpha: 剪枝算法所用 α 值
            _beta: 剪枝算法所用 β 值
            _depth: 当前搜索深度

        Returns:
            (score, (x, y))——当前最大分值，该分值的 x，y 坐标。
        """
        score = self.__evaluate_board(_board, _player)
        if _depth >= AI_SEARCH_DEPTH or abs(score) >= ChessScore.LIVE_FIVE:
            return score, None

        # 枚举每一个未落子的候选点进行遍历搜索。
        can_moves = self.__get_can_move(_board, _player)

        best_move = None
        mine, opponent = _player
        for _, pos in can_moves:
            x, y = pos
            _board[x][y] = mine
            self.__update_can_move(_board, pos, True)

            score, _ = self.__min_max_search(_board, _player[::-1], -_beta,
                                             -_alpha, _depth + 1)
            score *= -1
            _board[x][y] = PlayerEnum.NO_PLAYER
            self.__update_can_move(_board, pos, False)

            if score > _alpha:
                _alpha = score
                best_move = x, y
                if _alpha >= _beta:
                    break

        return _alpha, best_move

    def __get_can_move(self, _board, _player):
        """获取可落子点。

        获取可落子点与该点的分值，仅返回分值较高的数个点。

        Args:
            _board: 棋盘数组
            _player: (己方玩家编号，敌方玩家编号)

        Returns:
            可落子点数组。
        """
        fives = []
        m_fours, o_fours = [], []
        m_sfours, o_sfours = [], []
        can_moves = []
        for x in range(CHESS_MAX_NUM):
            for y in range(CHESS_MAX_NUM):
                m_s, o_s = self.__evaluate_point(_board, (x, y), _player)
                if self.__can_move[x][y] > 0:
                    if max(m_s, o_s) >= ChessScore.LIVE_FIVE:
                        fives.append((max(m_s, o_s), (x, y)))
                    elif m_s >= ChessScore.LIVE_FOUR:
                        m_fours.append((m_s, (x, y)))
                    elif o_s >= ChessScore.LIVE_FOUR:
                        o_fours.append((o_s, (x, y)))
                    elif m_s >= ChessScore.SLEEP_FOUR:
                        m_sfours.append((m_s, (x, y)))
                    elif o_s >= ChessScore.SLEEP_FOUR:
                        o_sfours.append((o_s, (x, y)))
                    else:
                        can_moves.append((max(m_s, o_s), (x, y)))

        if len(fives) > 0:
            return fives
        if len(m_fours) > 0:
            return m_fours
        if len(o_fours) > 0:
            return o_fours + m_sfours

        can_moves.sort(reverse=True)
        return can_moves[:AI_LIMITED_MOVE_NUM]

    def __evaluate_board(self, _board, _player):
        """计算当前棋局分值方法。

        Args:
            _player: (己方玩家编号, 敌方玩家编号)

        Returns:
            随机化后的棋局分值。
        """
        mine, opponent = _player
        visited = [[[False] * CHESS_MAX_NUM
                    for _ in range(CHESS_MAX_NUM)]
                   for _ in range(len(self.__search_direction))]
        count = [[0] * CHESS_TYPE_NUM for _ in range(2)]

        for x in range(CHESS_MAX_NUM):
            for y in range(CHESS_MAX_NUM):
                if _board[x][y] == PlayerEnum.NO_PLAYER: continue
                pos = x, y
                for i in range(len(self.__search_direction)):
                    if visited[i][x][y]: continue
                    offset = self.__search_direction[i]
                    if _board[x][y] == mine:
                        self.__get_one_chess_shape(
                            _board, pos, _player, offset, count[mine],
                            visited[i])
                    elif _board[x][y] == opponent:
                        self.__get_one_chess_shape(
                            _board, pos, _player[::-1], offset, count[opponent],
                            visited[i])
        m_s, o_s = self.__get_board_score([count[mine], count[opponent]])
        return random_score(m_s - o_s)

    def __evaluate_point(self, _board, _pos, _player):
        """计算 _pos 处分值。

        Args:
            _board: 棋局数组
            _pos: 待评分坐标
            _player: (己方玩家编号，敌方玩家编号)

        Returns:
            (己方分数，敌方分数).
        """
        count = [[0] * CHESS_TYPE_NUM for _ in range(2)]
        # 获取该点在两种情况下的棋形。
        mine, opponent = _player
        for offset in self.__search_direction:
            self.__get_one_chess_shape(_board, _pos, _player, offset,
                                       count[mine])
            self.__get_one_chess_shape(_board, _pos, _player[::-1], offset,
                                       count[opponent])
        m_score = self.__get_point_score(count[mine])
        o_score = self.__get_point_score(count[opponent])
        return m_score, o_score

    def __update_can_move(self, _board, _pos, _add):
        """更新可选落子点。

        根据当前所下位置更新可选落子点。

        Args:
            _board: 棋盘数组
            _pos: 中间点
            _add: 为 True 时是落子，否则为取回了一子
        """
        x, y = _pos
        start_x = max(0, x - self.__radius)
        start_y = max(0, y - self.__radius)
        end_x = min(CHESS_MAX_NUM - 1, x + self.__radius)
        end_y = min(CHESS_MAX_NUM - 1, y + self.__radius)

        self.__can_move[x][y] = 0
        for i in range(start_x, end_x + 1):
            for j in range(start_y, end_y + 1):
                if _add and (i != x or j != y):
                    # 添加子时，该子周围未落子点计数都加一。
                    if _board[i][j] == PlayerEnum.NO_PLAYER:
                        self.__can_move[i][j] += 1
                elif i != x or j != y:
                    # 取回子时，该子周围未落子点减一，并计算该子周围有多少个已落子点。
                    if _board[i][j] == PlayerEnum.NO_PLAYER:
                        self.__can_move[i][j] -= 1
                    else:
                        self.__can_move[x][y] += 1

    @staticmethod
    def __get__chess_list(_board, _pos, _offset, _player):
        """获取一行棋子方法。

        根据偏移方向将棋盘上棋子的落子者放置在一维列表中。\n
        如果超出边界，则算对方所落的子。

        Args:
            _board: 棋盘数组
            _pos: 该行中间位置的坐标
            _offset: 偏移方向
            _player: (己方玩家编号, 敌方玩家编号)

        Returns:
            一行棋子的落子者的列表。
        """
        x, y = _pos
        _, opponent = _player
        start_x = x + (-5 * _offset[0])
        start_y = y + (-5 * _offset[1])
        res = []
        for i in range(9):
            start_x += _offset[0]
            start_y += _offset[1]
            if (not 0 <= start_x < CHESS_MAX_NUM or
                    not 0 <= start_y < CHESS_MAX_NUM):
                res.append(opponent)
            else:
                res.append(_board[start_x][start_y])
        return res

    @staticmethod
    def __get_one_chess_shape(_board, _pos, _player, _offset, _count,
                              _visited=None):
        """获取一行棋子中的棋形。

        根据 _pos 处在 _offset 方向上获取的一行棋子落子者列表，\n
        判断其中所含有的棋形。

        Args:
            _board: 棋盘数组
            _pos: 中心点坐标
            _player: (己方玩家编号, 对手玩家编号)
            _offset: 偏移方向
            _count: 棋形数量数组
            _visited: 记录已统计过棋形的棋子列表

        Returns:
            各种棋形数量的列表。
        """
        def set_visited(_left, _right, _pos, _offset, _visited):
            """更新 visited 数组函数。"""
            if _visited is None: return
            x, y = _pos
            offset_x, offset_y = _offset
            start_x = x + (-5 + _left) * offset_x
            start_y = y + (-5 + _left) * offset_y
            for i in range(_left, _right + 1):
                start_x += offset_x
                start_y += offset_y
                _visited[start_x][start_y] = True

        mine, opponent = _player
        chess_list = AI.__get__chess_list(_board, _pos, _offset, _player)

        # 统计己方有多少已连起来的棋子。
        left_index, right_index = 4, 4
        while right_index < 8:
            if chess_list[right_index + 1] != mine:
                break
            right_index += 1
        while left_index > 0:
            if chess_list[left_index - 1] != mine:
                break
            left_index -= 1

        # 统计两端有多少空格。
        left_range, right_range = left_index, right_index
        while right_range < 8:
            if chess_list[right_range + 1] == opponent:
                break
            right_range += 1
        while left_range > 0:
            if chess_list[left_range - 1] == opponent:
                break
            left_range -= 1

        chess_range = right_range - left_range + 1  # 连续的己方棋子 + 空白格数。
        if chess_range < 5:
            # 己方棋子 + 空白格数不到 5 格，则无法形成活五棋形。
            set_visited(left_range, right_range, _pos, _offset, _visited)
            return

        set_visited(left_index, right_index, _pos, _offset, _visited)

        mine_range = right_index - left_index + 1  # 连续的己方棋子数。
        if mine_range >= 5:
            # 活五棋形。
            _count[ChessType.LIVE_FIVE] += 1

        if mine_range == 4:
            # 考虑冲四和活四棋形。
            left_empty = right_empty = False
            if chess_list[left_index - 1] == PlayerEnum.NO_PLAYER:
                left_empty = True
            if chess_list[right_index + 1] == PlayerEnum.NO_PLAYER:
                right_empty = True
            if left_empty and right_empty:
                # 活四。
                _count[ChessType.LIVE_FOUR] += 1
            elif left_empty or right_empty:
                # 冲四。
                _count[ChessType.SLEEP_FOUR] += 1

        if mine_range == 3:
            # 考虑眠三、活三和冲四棋形。
            left_empty = right_empty = False
            left_four = right_four = False
            if chess_list[left_index - 1] == PlayerEnum.NO_PLAYER:
                if chess_list[left_index - 2] == mine:
                    set_visited(left_index - 2, left_index - 1, _pos, _offset,
                                _visited)
                    # 左侧有缺口的冲四棋形。
                    _count[ChessType.SLEEP_FOUR] += 1
                    left_four = True
                left_empty = True

            if chess_list[right_index + 1] == PlayerEnum.NO_PLAYER:
                if chess_list[right_index + 2] == mine:
                    set_visited(right_index + 1, right_index + 2, _pos, _offset,
                                _visited)
                    # 右侧有缺口的冲四棋形。
                    _count[ChessType.SLEEP_FOUR] += 1
                    right_four = True
                right_empty = True

            if left_four or right_four:
                pass
            elif left_empty and right_empty:
                if chess_range > 5:
                    # 活三棋形。
                    _count[ChessType.LIVE_THREE] += 1
                else:
                    # 眠三棋形。
                    _count[ChessType.SLEEP_THREE] += 1
            elif left_empty or right_empty:
                # 眠三棋形。
                _count[ChessType.SLEEP_THREE] += 1

            if mine_range == 2:
                # 考虑冲四、眠三、活三、眠二和活二棋形。
                left_empty = right_empty = False
                left_three = right_three = False
                if chess_list[left_index - 1] == PlayerEnum.NO_PLAYER:
                    if chess_list[left_index - 2] == mine:
                        set_visited(left_index - 2, left_index - 1, _pos,
                                    _offset, _visited)
                        if chess_list[left_index - 3] == PlayerEnum.NO_PLAYER:
                            if (chess_list[right_index + 1] ==
                                    PlayerEnum.NO_PLAYER):
                                # 活三棋形。
                                _count[ChessType.LIVE_THREE] += 1
                            else:
                                # 眠三棋形。
                                _count[ChessType.SLEEP_THREE] += 1
                            left_three = True
                        elif chess_list[left_index - 3] == opponent:
                            if (chess_list[right_index + 1] ==
                                    PlayerEnum.NO_PLAYER):
                                # 眠三棋形。
                                _count[ChessType.SLEEP_THREE] += 1
                                left_three = True

                    left_empty = True

                if chess_list[right_index + 1] == PlayerEnum.NO_PLAYER:
                    if chess_list[right_index + 2] == mine:
                        if chess_list[right_index + 3] == mine:
                            set_visited(right_index + 1, right_index + 2, _pos,
                                        _offset, _visited)
                            # 冲四棋形。
                            _count[ChessType.SLEEP_FOUR] += 1
                            right_three = True
                        elif (chess_list[right_index + 3] ==
                              PlayerEnum.NO_PLAYER):
                            if left_empty:
                                # 活三棋形。
                                _count[ChessType.LIVE_THREE] += 1
                            else:
                                # 眠三棋形。
                                _count[ChessType.SLEEP_THREE] += 1
                            right_three = True
                        elif left_empty:
                            # 眠三棋形。
                            _count[ChessType.SLEEP_THREE] += 1
                            right_three = True

                    right_empty = True

                if left_three or right_three:
                    pass
                elif left_empty and right_empty:
                    # 活二棋形。
                    _count[ChessType.LIVE_TWO] += 1
                elif left_empty or right_empty:
                    # 眠二棋形。
                    _count[ChessType.SLEEP_TWO] += 1

            if mine_range == 1:
                # 考虑眠二和活二棋形。
                left_empty = False
                if chess_list[left_index - 1] == PlayerEnum.NO_PLAYER:
                    if chess_list[left_index - 2] == mine:
                        if chess_list[left_index - 3] == PlayerEnum.NO_PLAYER:
                            if chess_list[right_index + 1] == opponent:
                                # 眠二棋形。
                                _count[ChessType.SLEEP_TWO] += 1
                    left_empty = True

                if chess_list[right_index + 1] == PlayerEnum.NO_PLAYER:
                    if chess_list[right_index + 2] == mine:
                        if chess_list[right_index + 3] == PlayerEnum.NO_PLAYER:
                            if left_empty:
                                # 活二棋形。
                                _count[ChessType.LIVE_TWO] += 1
                            else:
                                # 眠二棋形。
                                _count[ChessType.SLEEP_TWO] += 1
                    elif chess_list[right_index + 2] == PlayerEnum.NO_PLAYER:
                        if (chess_list[right_index + 3] == mine and
                                chess_list[right_index + 4] ==
                                PlayerEnum.NO_PLAYER):
                            # 活二棋形。
                            _count[ChessType.LIVE_TWO] += 1
        return _count

    @staticmethod
    def __get_point_score(_count):
        """根据棋形获取某点的分值。

        根据 __get_chess_shape 函数中获得的各个棋形数量，\n
        获取某点的分值。

        Args:
            _count: 各棋形数量

        Returns:
            该点分值。
        """
        score = 0
        if _count[ChessType.LIVE_FIVE] > 0:
            return ChessScore.LIVE_FIVE

        if _count[ChessType.LIVE_FOUR] > 0:
            return ChessScore.LIVE_FOUR

        if _count[ChessType.SLEEP_FOUR] > 1:
            score += _count[ChessType.SLEEP_FOUR] * ChessScore.SLEEP_FOUR
        elif (_count[ChessType.SLEEP_FOUR] > 0 and
              _count[ChessType.LIVE_THREE] > 0):
            score += _count[ChessType.SLEEP_FOUR] * ChessScore.SLEEP_FOUR
        elif _count[ChessType.SLEEP_FOUR] > 0:
            score += ChessScore.LIVE_THREE

        if _count[ChessType.LIVE_THREE] > 1:
            score += 5 * ChessScore.LIVE_THREE
        elif _count[ChessType.LIVE_THREE] > 0:
            score += ChessScore.LIVE_THREE

        if _count[ChessType.SLEEP_THREE] > 0:
            score += (_count[ChessType.SLEEP_THREE] *
                      ChessScore.SLEEP_THREE)
        if _count[ChessType.LIVE_TWO] > 0:
            score += _count[ChessType.LIVE_TWO] * ChessScore.LIVE_TWO
        if _count[ChessType.SLEEP_TWO] > 0:
            score += _count[ChessType.SLEEP_TWO] * ChessScore.SLEEP_TWO

        return score

    @staticmethod
    def __get_board_score(_player_count):
        """获取全局棋形评分。

        Args:
            _player_count: (己方棋形数量, 对方棋形数量)

        Returns:
            (我方评分，对方评分)。
        """
        mine_count, opponent_count = _player_count
        m_score, o_score = 0, 0
        # 有活五时，直接返回活五分值。
        if mine_count[ChessType.LIVE_FIVE] > 0:
            return ChessScore.LIVE_FIVE, 0
        if opponent_count[ChessType.LIVE_FIVE] > 0:
            return 0, ChessScore.LIVE_FIVE

        # 有两个冲四时，可以视作一个活四。
        if mine_count[ChessType.SLEEP_FOUR] >= 2:
            mine_count[ChessType.LIVE_FOUR] += 1
        if opponent_count[ChessType.SLEEP_FOUR] >= 2:
            opponent_count[ChessType.LIVE_FOUR] += 1

        # 优先考虑己方活四和冲四。
        if mine_count[ChessType.LIVE_FOUR] > 0:
            return 9050, 0
        if mine_count[ChessType.SLEEP_FOUR] > 0:
            return 9040, 0

        # 其次考虑防守敌方活四。
        if opponent_count[ChessType.LIVE_FOUR] > 0:
            return 0, 9030
        # 如果敌方有冲四又有活三，需要防守。
        if (opponent_count[ChessType.SLEEP_FOUR] > 0 and
                opponent_count[ChessType.LIVE_THREE] > 0):
            return 0, 9020

        # 己方有活三、敌方无冲四时，可以返回活三分值。
        if (mine_count[ChessType.LIVE_THREE] > 0 and
                opponent_count[ChessType.SLEEP_FOUR] == 0):
            return 9010, 0

        # 敌方有活三，己方无眠三、活三时，需要防守活三。
        if (opponent_count[ChessType.LIVE_THREE] > 1 and
                mine_count[ChessType.LIVE_THREE] == 0 and
                mine_count[ChessType.SLEEP_THREE] == 0):
            return 0, 9000

        # 以下是对非优先棋形的计分。
        if opponent_count[ChessType.SLEEP_FOUR] > 0:
            m_score += 40

        if mine_count[ChessType.LIVE_THREE] > 1:
            m_score += 5000
        elif mine_count[ChessType.LIVE_THREE] == 1:
            m_score += 100

        if opponent_count[ChessType.LIVE_THREE] > 1:
            o_score += 2000
        elif opponent_count[ChessType.LIVE_THREE] == 1:
            o_score += 400

        m_score += mine_count[ChessType.SLEEP_THREE] * 10
        o_score += opponent_count[ChessType.SLEEP_THREE] * 10

        m_score += mine_count[ChessType.LIVE_TWO] * 6
        o_score += opponent_count[ChessType.SLEEP_TWO] * 6

        m_score += mine_count[ChessType.SLEEP_TWO] * 2
        o_score += opponent_count[ChessType.SLEEP_TWO] * 2

        return m_score, o_score


if __name__ == '__main__':
    def test(i, a):
        if i == 3: return
        print(a)
        test(i + 1, a[::-1])
        test(i + 1, a[::-1])

    test(0, (1, 2))
    pass
