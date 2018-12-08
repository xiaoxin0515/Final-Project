from graphics import *
from math import *
import numpy as np
import time #Sometimes using time.sleep() for better observing the result.
import random
GRID_WIDTH = 40

COLUMN = 15
ROW = 15

list1 = []  # AI with White stones
list2 = [(3,7)]  # AI with black stones.(The first move should be set up here)
list3 = [(3,7)]  # Recording all stones


list_all = []  # points of all boards
next_point = []  # best next move for AI

ratio = 2  # offensive coefficient. If it is greater than 1, means offensive playstyle. If it is less than 1, means defensive playstyle.
DEPTH = 1  # search depth, it will be faster to set up as 1 for the Monte Carlo simulation.


# Evaluation scores for different shapes of stones 
shape_score = [(50, (0, 1, 1, 0, 0)),
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


def ai():
    global cut_count   # times of prunning
    global next_point
    cut_count = 0
    global search_count   # times of searching
    search_count = 0
    negamax(True, DEPTH, -99999999, 99999999)
    #print("length of the list is"+str(len(next_point)))
    #print(next_point)
    num=int(len(next_point)/2)-1
    ans1,ans2=0,0
    if(num>2):
        num=random.randint(0,2)# Select one of three best moves to apply if there exist three better moves
        ans1=next_point[-num*2-2]
        ans2=next_point[-num*2-1]
    else:
        ans1=next_point[-2]
        ans2=next_point[-1]
    next_point=[]
    return ans1,ans2


# Game tree with alpha + beta prunning
def negamax(is_ai, depth, alpha, beta):
    # If the game is over | if it is the end of the recursion
    if depth == 0:#game_win(list1) or game_win(list2) or
        return evaluation(is_ai)

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
        list3.append(next_step) # Simulating next move

        value = -negamax(not is_ai, depth - 1, -beta, -alpha)
        if is_ai:
            list1.remove(next_step)
        else:
            list2.remove(next_step)
        list3.remove(next_step)

        if value > alpha:

            #print(str(value) + "alpha:" + str(alpha) + "beta:" + str(beta))
            #print(list3)
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
    last_pt = list3[-1]
    for item in blank_list:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))


def has_neightnor(pt):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1]+j) in list3:
                return True
    return False


# evaluation function for different shapes of stones
def evaluation(is_ai):   #return total score
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
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

    #  Calculating enemy's score
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

    total_score = my_score - enemy_score*ratio*0.1

    return total_score


# points at each position
def cal_score(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
    add_score = 0  
    # In one direction, only the largest score item is taken
    max_score_shape = (0, None)

    # If in this direction, the point already has a score shape, no double counting
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    # Searching for different shapes of stones
    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                if tmp_shap5 == (1,1,1,1,1):
                    print('www')
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_decrict, n + (0+offset) * y_derice),
                                               (m + (1+offset) * x_decrict, n + (1+offset) * y_derice),
                                               (m + (2+offset) * x_decrict, n + (2+offset) * y_derice),
                                               (m + (3+offset) * x_decrict, n + (3+offset) * y_derice),
                                               (m + (4+offset) * x_decrict, n + (4+offset) * y_derice)), (x_decrict, y_derice))

    # Calculate the intersection of two shapes
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]


def game_win(list,x,y):
    length1,length2,total=0,0,0 #judge if win horizontally
    for i in range(1,5):
        if (x-i)>=0 and (x-i,y) in list:
            length1+=1
        else:
            break
    for i in range(1,5):
        if (x+i)<=14 and (x+i,y) in list:
            length2+=1
        else:
            break
    total=length1+length2+1
    if(total>=5):
        return True

    length1,length2,total=0,0,0 #judge if win vertically
    for i in range(1,5):
        if (y-i)>=0 and (x,y-i) in list:
            length1+=1
        else:
            break
    for i in range(1,5):
        if (y+i)<=14 and (x,y+i) in list:
            length2+=1
        else:
            break
    total=length1+length2+1
    if(total>=5):
        return True

    length1,length2,total=0,0,0 #judge if win diagonally in Second and fourth quadrants
    for i in range(1,5):
        if (x-i)>=0 and (y-i)>=0 and (x-i,y-i) in list:
            length1+=1
        else:
            break
    for i in range(1,5):
        if (x+i)<=14 and (y+i)<=14 and (x+i,y+i) in list:
            length2+=1
        else:
            break
    total=length1+length2+1
    if(total>=5):
        return True

    length1,length2,total=0,0,0 #judge if win diagonally in First and Third quadrants
    for i in range(1,5):
        if (x-i)>=0 and (y+i)<=14 and (x-i,y+i) in list:
            length1+=1
        else:
            break
    for i in range(1,5):
        if (x+i)<=14 and (y-i)>=0 and (x+i,y-i) in list:
            length2+=1
        else:
            break
    total=length1+length2+1
    if(total>=5):
        return True
    
    return False


def gobangwin():
    win = GraphWin("this is a gobang game", GRID_WIDTH * COLUMN, GRID_WIDTH * ROW)
    win.setBackground("yellow")
    i1 = 0

    while i1 <= GRID_WIDTH * COLUMN:
        l = Line(Point(i1, 0), Point(i1, GRID_WIDTH * COLUMN))
        l.draw(win)
        i1 = i1 + GRID_WIDTH
    i2 = 0

    while i2 <= GRID_WIDTH * ROW:
        l = Line(Point(0, i2), Point(GRID_WIDTH * ROW, i2))
        l.draw(win)
        i2 = i2 + GRID_WIDTH
    return win


def process():
    global list3
    global list2
    global list1
    global list_all
    global next_point
    ans=0

    for i in range(COLUMN+1):
        for j in range(ROW+1):
            list_all.append((i, j))

    change = 1
    g = 0
    m = 0
    n = 0

    while g == 0:
        if change % 2 == 1:
            pos = ai()
            

            list1.append(pos)
            list3.append(pos)


            if game_win(list1,pos[0],pos[1]):
                g = 1
                ans =1
            change = change + 1
            if (change>40):
                g = 1
                ans = 0
        else:
            pos = ai()

            list2.append(pos)
            list3.append(pos)


            if game_win(list2,pos[0],pos[1]):
                g = 1
                ans = -1
            change = change + 1
            if (change>40):
                g = 1
                ans = 0

    list1 = []  # Reset all the list after one game
    list2 = [(3,7)]  
    list3 = [(3,7)]  
    list_all = []  
    next_point = []  
    return ans 

def main():
    white_win,black_win,tiegame=0,0,0
    for i in range(0,100):## simulate the game 100 times in a program
        new=process()
        if(new==1):
            white_win+=1
        elif(new==-1):
            black_win+=1
        else:
            tiegame+=1

    print("white_win is "+str(white_win)) #Print out all results in 100 games
    print("black_win is "+str(black_win))
    print("tiegame is "+str(tiegame))


main()
