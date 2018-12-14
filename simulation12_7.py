from graphics import *
from math import *
import numpy as np
import time  # Sometimes using time.sleep() for better observing the result.
import random

GRID_WIDTH = 40

COLUMN = 15
ROW = 15

list1 = []  # AI with White stones
list2 = [(7, 7), ]  # AI with black stones.(The first move should be set up here)
list3 = [(7, 7), ]  # Recording all stones

list_all = []  # points of all boards
next_point = []  # best next move for AI

ratio = 2  # offensive coefficient. If it is greater than 1, means offensive playstyle. If it is less than 1, means defensive playstyle.
DEPTH = 1  # search depth, it will be faster to set up as 1 for the Monte Carlo simulation.

# Evaluation scores for different shapes of stones
shape_score_5 = [(50, (0, 1, 1, 0, 0)),
                 (50, (0, 0, 1, 1, 0)),
                 (200, (1, 1, 0, 1, 0)),
                 (500, (0, 0, 1, 1, 1)),
                 (500, (1, 1, 1, 0, 0)),
                 (5000, (0, 1, 1, 1, 0)),
                 (5000, (0, 1, 0, 1, 1, 0)),
                 (5000, (0, 1, 1, 0, 1, 0)),
                 (5000, (1, 1, 1, 0, 1)),
                 (5000, (1, 1, 0, 1, 1)),
                 (5000, (1, 0, 1, 1, 1)),
                 (5000, (1, 1, 1, 1, 0)),
                 (5000, (0, 1, 1, 1, 1)),
                 (50000, (0, 1, 1, 1, 1, 0)),
                 (99999999, (1, 1, 1, 1, 1))]
shape_score_4 = [(200, (1, 0, 1, 0)),
                 (200, (0, 1, 0, 1)),
                 (500, (0, 0, 1, 1)),
                 (500, (1, 1, 0, 0)),
                 (5000, (0, 1, 1, 0)),
                 (5000, (0, 1, 0, 1, 0)),
                 (5000, (1, 1, 0, 1)),
                 (5000, (1, 0, 1, 1)),
                 (5000, (0, 1, 1, 1)),
                 (5000, (1, 1, 1, 0)),
                 (50000, (0, 1, 1, 1, 0)),
                 (99999999, (1, 1, 1, 1))]


def ai1(success_num):
    """
    ai1() represents the first ai player and in the following function, the parameter is_ai of this player would be set as True
    to set it apart form the second ai player. Using this function we could get the first player's next move
    :param success_num: define the rule of the game, if success_num equals 4, it means one player succeeds when he got 4 in a row;
    if success_num is 5, it represents five stones in a row means success. And this parameter would be transformed to other functions, too.
    :return: by using random number generator, we got one of the three best next move, here we will return the x-coordinate and y-coordinate
    of this best move position
    """
    global cut_count  # times of prunning
    global next_point
    cut_count = 0
    global search_count  # times of searching
    search_count = 0
    negamax(success_num, True, DEPTH, -99999999, 99999999)
    # print("length of the list is"+str(len(next_point)))
    # print(next_point)
    num = int(len(next_point) / 2) - 1
    ans1, ans2 = 0, 0
    if (num > 2):
        num = random.randint(0, 2)  # Select one of three best moves to apply if there exist three better moves
        ans1 = next_point[-num * 2 - 2]
        ans2 = next_point[-num * 2 - 1]
    else:
        ans1 = next_point[-2]
        ans2 = next_point[-1]
    next_point = []
    return ans1, ans2


def ai2(success_num):
    """
    ai2() represents the second ai player and in the following function, the parameter is_ai of this player would be set as False
    to set it apart form the first ai player. Using this function we could get the second player's next move
    :param success_num: define the rule of the game, if success_num equals 4, it means one player succeeds when he got 4 in a row;
    if success_num is 5, it represents five stones in a row means success.And this parameter would be transformed to other functions, too.
    :return: by using random number generator, we got one of the three best next move, here we will return the x-coordinate and y-coordinate
     of this best move position
    """
    global cut_count  # times of prunning
    global next_point
    cut_count = 0
    global search_count  # times of searching
    search_count = 0
    negamax(success_num, False, DEPTH, -99999999, 99999999)
    # print("length of the list is"+str(len(next_point)))
    # print(next_point)
    num = int(len(next_point) / 2) - 1
    ans1, ans2 = 0, 0
    if (num > 2):
        num = random.randint(0, 2)  # Select one of three best moves to apply if there exist three better moves
        ans1 = next_point[-num * 2 - 2]
        ans2 = next_point[-num * 2 - 1]
    else:
        ans1 = next_point[-2]
        ans2 = next_point[-1]
    next_point = []
    return ans1, ans2


# Game tree with alpha + beta prunning
def negamax(success_num, is_ai, depth, alpha, beta):
    """
    this funciton is a recursion function, it uses Min-Max search to get a list of best next move. And to make the funtion
    more efficient, it uses Alpha-Beta pruning to decrease searching times.
    :param success_num:define the rule of the game, if success_num equals 4, it means one player succeeds when he got 4 in a row;
    if success_num is 5, it represents five stones in a row means success.
    :param is_ai: to set apart 2 ai players: the first player would be set as True and the second as False
    :param depth: how many steps to see ahead of the next move. The larger this number is, the smarter the ai would be and the more
    time it would consume
    :param alpha: the maximum value to be set for pruning and would be modified during the process of pruning
    :param beta: the maximum value to be set for pruning and would be modified during the process of pruning
    :return: the return value is used in the recursion to do pruning
    """
    # If the game is over | if it is the end of the recursion
    if depth == 0:  # game_win(list1) or game_win(list2) or
        return evaluation(success_num, is_ai)

    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list)   # Ordering search order to Improve pruning efficiency
    # try out all possibilities that are around current stones
    for next_step in blank_list:

        global search_count
        search_count += 1

        # If this place has no neighbor, ignore it.
        if not has_neightnor(next_step):
            continue

        if is_ai:
            list1.append(next_step)
        else:
            list2.append(next_step)
        list3.append(next_step)  # Simulating next move

        value = -negamax(success_num, not is_ai, depth - 1, -beta, -alpha)
        if is_ai:
            list1.remove(next_step)
        else:
            list2.remove(next_step)
        list3.remove(next_step)

        if value > alpha:

            # print(str(value) + "alpha:" + str(alpha) + "beta:" + str(beta))
            # print(list3)
            if depth == DEPTH:
                next_point.append(next_step[0])
                next_point.append(next_step[1])

            # alpha + beta prunning point
            if value >= beta:
                global cut_count
                cut_count += 1
                return beta
            alpha = value

    return alpha


#  Another optimizing, the location of the neighbors from the last drop is most likely the best
def order(blank_list):
    """
    to reorder the blank list to set those positions that have neighborhood at the front of the list
    :param blank_list: a list of positions that have no stones yet
    :return: the blank_list that has been reordered according to whether it has a neighborhood
    """
    last_pt = list3[-1]
    for item in blank_list:
        for i in range(-1, 2):  # -1,0,1
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))


def has_neightnor(pt):
    """
    to check whether a position has a neighborhood, i.e., whether all the other positions closely around a given position
    has already a stone there
    :param pt: a coordinate of a given position
    :return: True for it has neighborhood and False for dosen't
    """
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1] + j) in list3:
                return True
    return False


# evaluation function for different shapes of stones
def evaluation(success_num, is_ai):  # return total score
    """
    to caculate my score and my enemy's score, then according to the ratio set at the begginning of the code which represents
    the player is more offensive or more conservative, this function caculate the final score a step could get.
    :param success_num:define the rule of the game, if success_num equals 4, it means one player succeeds when he got 4 in a row;
    if success_num is 5, it represents five stones in a row means success.
    :param is_ai: to set apart 2 ai players: the first player would be set as True and the second as False
    :return: the final score a step could get, considering both my side and my enemy's side
    """
    total_score = 0

    if is_ai:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1

    # Calculating own scores
    score_all_arr = []
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(success_num, m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(success_num, m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(success_num, m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(success_num, m, n, -1, 1, enemy_list, my_list, score_all_arr)

    #  Calculating enemy's score
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(success_num, m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(success_num, m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(success_num, m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(success_num, m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

    total_score = my_score - enemy_score * ratio * 0.1

    return total_score


# points at each position
def cal_score(success_num, m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
    """
    according to the score rule of stone shape set at the beginning as shape_score, to calculate the score of a specific given
    direction of the stone shape. To calculate this, only the maximum score would be regarded as the final score and if there is an
    intersection between 2 scored stone shapes, the score would be calculated double.
    :param success_num: define the rule of the game, if success_num equals 4, it means one player succeeds when he got 4 in a row;
    if success_num is 5, it represents five stones in a row means success. This would determine which score rule of stone shape we
    use: for success_num=4, we would use shape_score_4; for success_num=5, we would use shape_score_5;
    :param m: x-coordinate of the position we want to calcuate
    :param n: y-coordinate of the position we want to calcuate
    :param x_decrict: in x axis direction, what units we want to move
    :param y_derice: in y axis direction, what units we want to move
    :param enemy_list: a list that stores all the coordinates of enemy's stones
    :param my_list: a list that stores all the coordinates of my stones
    :param score_all_arr: a blank list to store max_score_shape which is a tuple of score, stone shape and xy direction
    :return: the score of a specific given direction of the stone shape
    """
    add_score = 0
    # In one direction, only the largest score item is taken
    max_score_shape = (0, None)

    # If in this direction, the point already has a score shape, no double counting
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    # Searching for different shapes of stones
    for offset in range(-success_num, 1):
        # offset = -2
        pos = []
        for i in range(0, success_num + 2):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        if success_num == 5:
            tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
            tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])
            shape_score = shape_score_5
        if success_num == 4:
            tmp_shap5 = (pos[0], pos[1], pos[2], pos[3])
            tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4])
            shape_score = shape_score_4
        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                # if success_num==5:
                #     if tmp_shap5 == (1,1,1,1,1):
                #         print('www')
                # if success_num==4:
                #     if tmp_shap5 == (1,1,1,1):
                #         print('www')
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0 + offset) * x_decrict, n + (0 + offset) * y_derice),
                                               (m + (1 + offset) * x_decrict, n + (1 + offset) * y_derice),
                                               (m + (2 + offset) * x_decrict, n + (2 + offset) * y_derice),
                                               (m + (3 + offset) * x_decrict, n + (3 + offset) * y_derice),
                                               (m + (4 + offset) * x_decrict, n + (4 + offset) * y_derice)),
                                       (x_decrict, y_derice))

    # Calculate the intersection of two shapes
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]


def game_win(success_num, list, x, y):
    """
    to determine after the last stone(x,y), whether this given side is win. To be more specific, firstly, we get the coordinate
    of the last stone which is (x,y), then in 4 different directions(vertical, horizontal, left diagonal and right diagonal), we set
    the stones into 2 parts according to the last stone and calculate the number of stones of these 2 parts seperately, finally,
    we add these two numbers to see whether it reaches success_num.

    >>> game_win(5,{(1,1),(2,1),(3,1),(4,1),(5,1)},5,1)
    True

    :param success_num: define the rule of the game, if success_num equals 4, it means one player succeeds when he got 4 in a row;
    if success_num is 5, it represents five stones in a row means success.
    :param list:  a list that stores all the coordinates of the stones of given side
    :param x: the x-coordinate of the last stone
    :param y: the y-coordinate of the last stone
    :return: if the given side succeeds, returns true, if not, returns false
    """
    length1, length2, total = 0, 0, 0  # judge if win horizontally
    for i in range(1, success_num):
        if (x - i) >= 0 and (x - i, y) in list:
            length1 += 1
        else:
            break
    for i in range(1, success_num):
        if (x + i) <= 14 and (x + i, y) in list:
            length2 += 1
        else:
            break
    total = length1 + length2 + 1
    if (total >= success_num):
        return True

    length1, length2, total = 0, 0, 0  # judge if win vertically
    for i in range(1, success_num):
        if (y - i) >= 0 and (x, y - i) in list:
            length1 += 1
        else:
            break
    for i in range(1, success_num):
        if (y + i) <= 14 and (x, y + i) in list:
            length2 += 1
        else:
            break
    total = length1 + length2 + 1
    if (total >= success_num):
        return True

    length1, length2, total = 0, 0, 0  # judge if win diagonally in Second and fourth quadrants
    for i in range(1, success_num):
        if (x - i) >= 0 and (y - i) >= 0 and (x - i, y - i) in list:
            length1 += 1
        else:
            break
    for i in range(1, success_num):
        if (x + i) <= 14 and (y + i) <= 14 and (x + i, y + i) in list:
            length2 += 1
        else:
            break
    total = length1 + length2 + 1
    if (total >= success_num):
        return True

    length1, length2, total = 0, 0, 0  # judge if win diagonally in First and Third quadrants
    for i in range(1, success_num):
        if (x - i) >= 0 and (y + i) <= 14 and (x - i, y + i) in list:
            length1 += 1
        else:
            break
    for i in range(1, success_num):
        if (x + i) <= 14 and (y - i) >= 0 and (x + i, y - i) in list:
            length2 += 1
        else:
            break
    total = length1 + length2 + 1
    if (total >= success_num):
        return True

    return False

def process(success_num):
    """
    one time of the whole simulation process
    :param success_num: define the rule of the game, if success_num equals 4, it means one player succeeds when he got 4 in a row;
    if success_num is 5, it represents five stones in a row means success.
    :return: ans=0 means a tie game; ans=1 means white stone wins; ans=-1 means black stone wins
    """
    global list3
    global list2
    global list1
    global list_all
    global next_point
    ans = 0

    for i in range(COLUMN + 1):
        for j in range(ROW + 1):
            list_all.append((i, j))

    change = 1 # odd change means the white turn(first ai), even change means the black turn(second ai)
    g = 0 #g=0 means the game has not end

    while g == 0:
        if change % 2 == 1:
            pos = ai1(success_num)

            list1.append(pos)
            list3.append(pos)

            if game_win(success_num, list1, pos[0], pos[1]):
                g = 1
                ans = 1
            change = change + 1
            if (change > 40):
                g = 1
                ans = 0
        else:
            pos = ai2(success_num)

            list2.append(pos)
            list3.append(pos)

            if game_win(success_num, list2, pos[0], pos[1]):
                g = 1
                ans = -1
            change = change + 1
            if (change > 40):
                g = 1
                ans = 0

    list1 = []  # Reset all the list after one game
    list2 = [(7, 7), ]
    list3 = [(7, 7), ]
    list_all = []
    next_point = []
    return ans


def main():
    white_win, black_win, tiegame = 0, 0, 0
    for i in range(0, 1):  ## simulate the game 100 times in a program
        new = process(5)  # change the parameter to 4 or 5 to change the rule of the game(five in a row or four in a row)
        if (new == 1):
            white_win += 1
        elif (new == -1):
            black_win += 1
        else:
            tiegame += 1

    print("white_win is " + str(white_win))  # Print out all results in 100 games
    print("black_win is " + str(black_win))
    print("tiegame is " + str(tiegame))


# main()
if __name__ == '__main__':
     main()