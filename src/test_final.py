#!/usr/bin/env python

import cv2
import numpy as np
import sys
sys.path.append('/home/robotics/catkin_ws/devel/lib/python2.7/dist-packages')
import rospy
from tm_msgs.msg import *
from tm_msgs.srv import *
import argparse
from math import atan2, cos, sin, sqrt, pi
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import random
import itertools

class Pikaliya_Chess:
    def __init__(self):
        # self.turn = int(input("PC first: 1, User first: 0."))  # True: O, False: X
        self.turn = 1
        self.table = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.place = 0
        self.origin = 0
        self.flag = 0
        self.red_table = [0,0,0,0,0,0,0,0,0]
        self.red_check = [0,0,0,0,0,0,0,0,0]

    def update(self, place):
        i = (place - 1) // 3
        j = (place - 1) % 3
        if self.table[i][j] != 0:
            return False

        value = 1 if self.turn else -1  # 1 -> O, -1 -> X, 0 -> empty
        self.table[i][j] = value
        return True

    def get_now_turn(self):
        return 'O' if self.turn else 'X'

    def get_checkerboard(self):
        """
        format checkerboard and return
        """
        return '\n'.join(['\t'.join([{1: 'O', -1: 'X'}.get(j, ' ') for j in i]) for i in self.table])

    def check(self):
        """
        :return: True -> someone win, False -> Nobody win, None -> tie
        """
        
        for line in self.table:
            if abs(sum(line)) == 3:
                return True
        
        for i in zip(*self.table):
            if abs(sum(i)) == 3:
                return True

        if abs(sum([self.table[i][i] for i in range(3)])) == 3:
            return True
        
        if abs(sum([self.table[i][2 - i] for i in range(2, -1, -1)])) == 3:
            return True

        if 0 not in itertools.chain(*self.table):
            return None

        return False

    def switch_user(self):
        self.turn = not self.turn

    def computer_choice(self):
        check_value_list = [-2, 2, -1]
        for v in check_value_list:
            for i, line in enumerate(self.table):
                if sum(line) == v:
                    if 0 not in line:
                        continue

                    return i * 3 + line.index(0) + 1

            for i, line in enumerate(zip(*self.table)):
                if sum(line) == v:
                    if 0 not in line:
                        continue

                    return line.index(0) * 3 + i + 1

            line = [self.table[i][i] for i in range(3)]
            if sum(line) == v and 0 in line:
                i = line.index(0)
                return i * 3 + i + 1

            line = [self.table[i][2 - i] for i in range(3)]
            if sum(line) == v and 0 in line:
                i = line.index(0)
                return i * 3 + (2 - i) + 1

        counter = 0
        if self.flag == 0:
            for i in range(3):
                for j in range(3):
                    if self.table[i][j] == 1:
                        counter += 1
            if counter == 0:
                return random.choice([1, 2, 3, 4, 6, 7, 8, 9])
            else:
                return 5
            self.flag = 1

    def swap(self, x, y, a, b):
        if 3*x+y+1!=self.place:
            self.table[a][b] = self.table[x][y]
            self.table[x][y] = 0
            
    
    def move(self, dic):
        set_io(0.0)
        targetP1 = "%f , %f , 300.00 , 180.00 , 0.00 , 135" %(dic[self.origin][0], dic[self.origin][1])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)

        targetP1 = "%f , %f , 150.00 , 180.00 , 0.00 , 135" %(dic[self.origin][0], dic[self.origin][1])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)
        set_io(1.0)

        targetP1 = "%f , %f , 300.00 , 180.00 , 0.00 , 135" %(dic[self.origin][0], dic[self.origin][1])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)

        targetP1 = "%f , %f , 300.00 , 180.00 , 0.00 , 135" %(dic[self.place][0], dic[self.place][1])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)

        targetP1 = "%f , %f , 150.00 , 180.00 , 0.00 , 135" %(dic[self.place][0], dic[self.place][1])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)
        set_io(0.0)

        targetP1 = "%f , %f , 300.00 , 180.00 , 0.00 , 135" %(dic[self.place][0], dic[self.place][1])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)

        
    def blue_win(self, dic):
        for i in range(3):
            for j in range(3):
                if self.table[i][j] == -1 and 3 * i + j + 1 != self.place:
                    if i - 1 >= 0 and j - 1 >= 0 and self.table[i - 1][j - 1] == 0:
                        self.swap(i, j, i - 1, j - 1)
                        if self.check() == True:
                            self.origin = 3 * (i) + (j) + 1
                            self.place = 3 * (i-1) + (j-1) + 1
                            self.move(dic)
                            return True
                        else:
                            self.swap(i - 1, j - 1, i, j)
                    if i - 1 >= 0 and self.table[i - 1][j] == 0:
                        self.swap(i, j, i - 1, j)
                        if self.check() == True:
                            self.origin = 3 * (i) + (j) + 1
                            self.place = 3 * (i-1) + (j) + 1
                            self.move(dic)
                            return True
                        else:
                            self.swap(i - 1, j, i, j)
                    if i - 1 >= 0 and j + 1 <= 2 and self.table[i - 1][j + 1] == 0:
                        self.swap(i, j, i - 1, j + 1)
                        if self.check() == True:
                            self.origin = 3 * (i) + (j) + 1
                            self.place = 3 * (i-1) + (j+1) + 1
                            self.move(dic)
                            return True
                        else:
                            self.swap(i - 1, j + 1, i, j)
                    if j + 1 <= 2 and self.table[i][j + 1] == 0:
                        self.swap(i, j, i, j + 1)
                        if self.check() == True:
                            self.origin = 3 * (i) + (j) + 1
                            self.place = 3 * (i) + (j+1) + 1
                            self.move(dic)
                            return True
                        else:
                            self.swap(i, j + 1, i, j)
                    if i + 1 <= 2 and j + 1 <= 2 and self.table[i + 1][j + 1] == 0:
                        self.swap(i, j, i + 1, j + 1)
                        if self.check() == True:
                            self.origin = 3 * (i) + (j) + 1
                            self.place = 3 * (i+1) + (j+1) + 1
                            self.move(dic)
                            return True
                        else:
                            self.swap(i + 1, j + 1, i, j)
                    if i + 1 <= 2 and self.table[i + 1][j] == 0:
                        self.swap(i, j, i + 1, j)
                        if self.check() == True:
                            self.origin = 3 * (i) + (j) + 1
                            self.place = 3 * (i+1) + (j) + 1
                            self.move(dic)
                            return True
                        else:
                            self.swap(i + 1, j, i, j)
                    if i + 1 <= 2 and j - 1 >= 0 and self.table[i + 1][j - 1] == 0:
                        self.swap(i, j, i + 1, j - 1)
                        if self.check() == True:
                            self.origin = 3 * (i) + (j) + 1
                            self.place = 3 * (i+1) + (j-1) + 1
                            self.move(dic)
                            return True
                        else:
                            self.swap(i + 1, j - 1, i, j)
                    if j - 1 >= 0 and self.table[i][j - 1] == 0:
                        self.swap(i, j, i, j - 1)
                        if self.check() == True:
                            self.origin = 3 * (i) + (j) + 1
                            self.place = 3 * (i) + (j-1) + 1
                            self.move(dic)
                            return True
                        else:
                            self.swap(i, j - 1, i, j)
        return False
    
    def blue_block(self, dic):
        v = 2
        for i, line in enumerate(self.table):
            if sum(line) == v:
                if 0 not in line:
                    continue
                for _i in range(-1, 2, 1):
                    for _j in range(-1, 2, 1):
                        if i + _i >= 0 and i + _i <= 2 and line.index(0) + _j >= 0 and line.index(0) + _j <= 2:
                            if self.table[i + _i][line.index(0) + _j] == -1 and 3 * (i + _i) + (line.index(0) + _j) + 1 != self.place:
                                line_index0 = line.index(0) 
                                self.swap(i + _i, line_index0 + _j, i, line_index0)
                                if self.red_win() == True:
                                    self.swap(i, line_index0, i + _i, line_index0 + _j)
                                    continue
                                self.origin = 3 * (i + _i) + (line_index0 + _j) + 1
                                self.place = 3 * (i) + (line_index0) + 1
                                self.move(dic)
                                return True

        for i, line in enumerate(zip(*self.table)):
            if sum(line) == v:
                if 0 not in line:
                    continue
                for _i in range(-1, 2, 1):
                    for _j in range(-1, 2, 1):
                        if line.index(0) + _i >= 0 and line.index(0) + _i <= 2 and i + _j >= 0 and i + _j <= 2 :
                            if self.table[line.index(0) + _i][i + _j] == -1 and 3 * (line.index(0) + _i) + (i + _j) + 1 != self.place:
                                line_index0 = line.index(0) 
                                self.swap(line_index0 + _i, i + _j, line_index0, i)      
                                if self.red_win() == True:
                                    self.swap(line_index0, i, line_index0 + _i, i + _j)
                                    continue
                                self.origin = 3 * (line_index0 + _i) + (i + _j) + 1
                                self.place = 3 * (line_index0) + (i) + 1
                                self.move(dic)
                                return True          

        line = [self.table[i][i] for i in range(3)]
        if sum(line) == v and 0 in line:
            i = line.index(0)
            for _i in range(-1, 2, 1):
                    for _j in range(-1, 2, 1):
                        if i + _i >= 0 and i + _i <= 2 and i + _j >= 0 and i + _j <= 2:
                            if self.table[i + _i][i + _j] == -1 and 3 * (i + _i) + (i + _j) + 1 != self.place:
                                self.swap(i + _i, i + _j, i, i)
                                if self.red_win() == True:
                                    self.swap(i, i, i + _i, i + _j)
                                    continue
                                self.origin = 3 * (i + _i) + (i + _j) + 1
                                self.place = 3 * (i) + (i) + 1
                                self.move(dic)
                                return True

        line = [self.table[i][2 - i] for i in range(3)]
        if sum(line) == v and 0 in line:
            i = line.index(0)
            for _i in range(-1, 2, 1):
                    for _j in range(-1, 2, 1):
                        if i + _i >= 0 and i + _i <= 2 and (2 - i) + _j >= 0 and (2 - i) + _j <= 2:
                            if self.table[i + _i][(2 - i) + _j] == -1 and 3 * (i + _i) + (2 - i + _j) + 1 != self.place:
                                self.swap(i + _i, (2 - i) + _j, i, (2 - i))
                                if self.red_win() == True:
                                    self.swap(i, (2 - i), i + _i, (2 - i) + _j)
                                    continue
                                self.origin = 3 * (i + _i) + ((2 - i) + _j) + 1
                                self.place = 3 * (i) + (2-i) + 1
                                self.move(dic)
                                return True
        return False

    def red_win(self):
        check_value_list = [2]
        for v in check_value_list:
            for i, line in enumerate(self.table):
                count = 0
                if sum(line) == v and 0 in line:
                    for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if i + _i >= 0 and i + _i <= 2 and line.index(0) + _j >= 0 and line.index(0) + _j <= 2:
                                if self.table[i + _i][line.index(0) + _j] == 1:
                                    count += 1
                                if count == 3 and line.index(0) == 1:
                                    return True 
                                if count == 2 and line.index(0) != 1:
                                    return True    
            
            for i, line in enumerate(zip(*self.table)):
                count = 0
                if sum(line) == v:
                    if 0 not in line:
                        continue
                    for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if line.index(0) + _i >= 0 and line.index(0) + _i <= 2 and i + _j >= 0 and i + _j <= 2:
                                if self.table[line.index(0) + _i][i + _j] == 1:
                                    count += 1
                                if count == 3 and line.index(0) == 1:
                                    return True 
                                if count == 2 and line.index(0) != 1:
                                    return True


            line = [self.table[i][i] for i in range(3)]
            if sum(line) == v and 0 in line:
                count = 0
                i = line.index(0)
                for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if i + _i >= 0 and i + _i <= 2 and i + _j >= 0 and i + _j <= 2:
                                if self.table[i + _i][i + _j] == 1:
                                    count += 1
                                if count == 3 and i == 1:
                                    return True 
                                if count == 2 and i != 1:
                                    return True 

            line = [self.table[i][2 - i] for i in range(3)]
            if sum(line) == v and 0 in line:
                count = 0
                i = line.index(0)
                for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if i + _i >= 0 and i + _i <= 2 and (2 - i) + _j >= 0 and (2 - i) + _j <= 2:
                                if self.table[i + _i][(2 - i) + _j] == 1:
                                    count += 1
                                if count == 3 and i == 1:
                                    return True 
                                if count == 2 and i != 1:
                                    return True
        return False

    def random_pc(self, dic):
        for i in range(3):
            for j in range(3):
                if self.table[i][j] == 0:
                    for _i in range(-1, 2, 1):
                        for _j in range(-1, 2, 1):
                            if i + _i >= 0 and i + _i <= 2 and j + _j >= 0 and j + _j <= 2:
                                if self.table[i + _i][j + _j] == -1 and 3 * (i + _i) + (j + _j) + 1 != self.place:
                                    self.swap(i + _i, j + _j, i, j)
                                    if self.red_win() == True:
                                        self.swap(i, j, i + _i, j + _j)
                                    else:
                                        self.origin = 3 * (i + _i) + (j + _j) + 1
                                        self.place = 3 * (i) + (j) + 1
                                        self.move(dic)
                                        return True
        return False                        

    def upadate_table_OX(self, chess, red):
        for i in range(9):
            if self.table[i/3][i%3] != -1:
                self.table[i/3][i%3] = 0
                for j in range(3):
                    length = (chess[0, i] - red[0, j]) ** 2 + (chess[1, i] - red[1, j]) ** 2
                    if length <= 300: # update red place
                        self.table[i/3][i%3] = 1
                        self.red_table[i] = 1


    def upadate_table(self, chess, red):
        red_table_tmp = [0,0,0,0,0,0,0,0,0]
        red_check_tmp = [0,0,0,0,0,0,0,0,0]
        for i in range(9):
            if self.table[i/3][i%3] != -1:
                self.table[i/3][i%3] = 0
                for j in range(3):
                    length = (chess[0, i] - red[0, j]) ** 2 + (chess[1, i] - red[1, j]) ** 2
                    if length <= 300: # update red place
                        red_table_tmp[i] = 1
        
        for i in range(9):
            red_check_tmp[i] = red_table_tmp[i] and self.red_table[i]

        if red_check_tmp == self.red_check and red_check_tmp.count(1) != 3:
            print('\nMove same chess! Restore your move, please.')
            return False
        else:
            self.red_check = red_check_tmp
            self.red_table = red_table_tmp
            for i, item in enumerate(red_table_tmp):
                if item == 1:
                    self.table[i/3][i%3] = 1
            return True      
            
    def check_zero(self):
        counter = 0
        for i in range(3):
            for j in range(3):
                if self.table[i][j] == 0:
                    counter += 1
        
        if counter == 3:
            return True
        else:
            return False            

def cam_detection():
    camera_info = rospy.wait_for_message("/usb_cam/image_raw", Image)
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(camera_info, desired_encoding='passthrough')
    # chess
    frame_gau_blur = cv2.GaussianBlur(img, (3, 3), 0)
    hsv = cv2.cvtColor(frame_gau_blur, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([5, 40, 80])
    higher_blue = np.array([10, 250, 250])
    lower_red = np.array([95, 40,80])
    higher_red = np.array([130, 250, 250])

    blue_range = cv2.inRange(hsv, lower_blue, higher_blue)
    res_blue = cv2.bitwise_and(frame_gau_blur, frame_gau_blur, mask=blue_range)
    blue_s_gray = cv2.cvtColor(res_blue, cv2.COLOR_BGR2GRAY)
    ret_blue, binary_blue = cv2.threshold(blue_s_gray,0,255,cv2.THRESH_BINARY)

    red_range = cv2.inRange(hsv, lower_red, higher_red)
    res_red = cv2.bitwise_and(frame_gau_blur, frame_gau_blur, mask=red_range)
    red_s_gray = cv2.cvtColor(res_red, cv2.COLOR_BGR2GRAY)
    ret_red, binary_red = cv2.threshold(red_s_gray,0,255,cv2.THRESH_BINARY)

    # find all Contours
    contours, hierarchy = cv2.findContours(binary_blue.copy(), cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE )
    clone = img.copy()

    #draw all contours
    cv2.drawContours(clone, contours, -1, (0, 0, 255), 3)

    cXs = np.array([])
    cYs = np.array([])
    angles = np.array([])
    targetNum = 0

    for j in contours:
        if len(j) > 10:
            M = cv2.moments(j)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            #get Principal Component
            angles = np.append(angles, getOrientation(j,clone,cX,cY))
            cXs = np.append(cXs, cX)
            cYs = np.append(cYs, cY)
            targetNum += 1

    r_c = 0.9763
    cMat_blue = np.zeros((3, 3))
    cMat_blue[0, :] = cXs*r_c
    cMat_blue[1, :] = cYs*r_c
    cMat_blue[2, :] = np.ones((1,3))
    # print('cMat_blue', cMat_blue)
    cv2.destroyAllWindows()

    # find all Contours
    contours, hierarchy = cv2.findContours(binary_red.copy(), cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE )
    clone = img.copy()

    #draw all contours
    cv2.drawContours(clone, contours, -1, (0, 0, 255), 3)

    cXs = np.array([])
    cYs = np.array([])
    angles = np.array([])
    targetNum = 0

    for j in contours:
        if len(j) > 10:
            M = cv2.moments(j)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            #get Principal Component
            angles = np.append(angles, getOrientation(j,clone,cX,cY))
            cXs = np.append(cXs, cX)
            cYs = np.append(cYs, cY)
            targetNum += 1

    r_c = 0.9763
    cMat_red = np.zeros((3, 3))
    cMat_red[0, :] = cXs*r_c
    cMat_red[1, :] = cYs*r_c
    cMat_red[2, :] = np.ones((1,3))
    # print('cMat_red', cMat_red)
    cv2.destroyAllWindows()
    return cMat_red, cMat_blue

def main(counter, chess):
    game = Pikaliya_Chess()
    print()
    i = 0

    for g in range(5):
        targetP1 = "-100.00, 200.00 , 300.00 , 180.00 , 0.00 , 135.00"
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)

        while True:
            question = raw_input("Shall we continue? Press any key.\n")
            cMat_red, cMat_blue = cam_detection()
            game.upadate_table_OX(chess, cMat_red)
            if game.table[1][1] == 1 and g == 0:
                print('You\'re a cheater. Put at other place.\n')
            else:
                break
            
        game.switch_user()
        
        result = game.check()
        print(game.get_checkerboard() + '\n')

        if result:
            print('Player {} won!\n'.format(game.get_now_turn()))
            break

        if game.check_zero() == True:
            break

        value = game.computer_choice()
        print('Computer chose to put at:', value)

        if not game.update(value):
            print('This place can not be put\n')
            continue

        set_io(0.0)
        targetP1 = "%f , %f , 300.00 , 180.00 , 0.00 , 135" %(Rob_blue[0, i], Rob_blue[1, i])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)

        targetP1 = "%f , %f , 150.00 , 180.00 , 0.00 , 135" %(Rob_blue[0, i], Rob_blue[1, i])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)
        set_io(1.0)

        targetP1 = "%f , %f , 300.00 , 180.00 , 0.00 , 135" %(Rob_blue[0, i], Rob_blue[1, i])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)

        targetP1 = "%f , %f , 300.00 , 180.00 , 0.00 , 135" %(place2rob[value][0], place2rob[value][1])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)

        targetP1 = "%f , %f , 150.00 , 180.00 , 0.00 , 135" %(place2rob[value][0], place2rob[value][1])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)
        set_io(0.0)

        targetP1 = "%f , %f , 300.00 , 180.00 , 0.00 , 135" %(place2rob[value][0], place2rob[value][1])
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)

        i += 1

        result = game.check()
        print(game.get_checkerboard() + '\n')
        

        if result is None:
            print('Tie')
            break

        if result:
            print('Player {} won!\n'.format(game.get_now_turn()))
            break

        game.switch_user()
        print('-' * 30)

        if game.check_zero() == True:
            break

    game.turn = False

    while True:
        targetP1 = "-100.00, 200.00 , 300.00 , 180.00 , 0.00 , 135.00"
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)

        while True:
            question = raw_input("Shall we continue? Press any key.\n")
            cMat_red, cMat_blue = cam_detection()
            if game.upadate_table(chess, cMat_red):
                break

        result = game.check()
        print(game.get_checkerboard() + '\n')

        if result:
            print('Player O won!\n')
            break

        game.switch_user()

        if game.blue_win(place2rob):
            print('Player X won!\n')
            print(game.get_checkerboard() + '\n')
            break
        if game.blue_block(place2rob) == False:
            if game.random_pc(place2rob) == False:
                print('I\'m screwed!\n')
                break
                    
        print(game.get_checkerboard() + '\n')
        print('X moved from %d to %d.\n' %(game.origin, game.place))
        game.switch_user()
        print('-' * 30) 

def send_script(script):
    rospy.wait_for_service('/tm_driver/send_script')
    try:
        script_service = rospy.ServiceProxy('/tm_driver/send_script', SendScript)
        move_cmd = SendScriptRequest()
        move_cmd.script = script
        resp1 = script_service(move_cmd)
    except rospy.ServiceException as e:
        print("Send script service call failed: %s"%e)

def set_io(state):
    rospy.wait_for_service('/tm_driver/set_io')
    try:
        io_service = rospy.ServiceProxy('/tm_driver/set_io', SetIO)
        io_cmd = SetIORequest()
        io_cmd.module = 1
        io_cmd.type = 1
        io_cmd.pin = 0
        io_cmd.state = state
        resp1 = io_service(io_cmd)
    except rospy.ServiceException as e:
        print("IO service call failed: %s"%e)


def drawAxis(img, p_, q_, colour, scale):
    p = list(p_)
    q = list(q_)
    
    angle = atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
    hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
    # Here we lengthen the arrow by a factor of scale
    q[0] = p[0] - scale * hypotenuse * cos(angle)
    q[1] = p[1] - scale * hypotenuse * sin(angle)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv2.LINE_AA)
    # create the arrow hooks
    p[0] = q[0] + 9 * cos(angle + pi / 4)
    p[1] = q[1] + 9 * sin(angle + pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv2.LINE_AA)
    p[0] = q[0] + 9 * cos(angle - pi / 4)
    p[1] = q[1] + 9 * sin(angle - pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv2.LINE_AA)
            
def getOrientation(pts, img,X,Y):
    
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i,0] = pts[i,0,0]
        data_pts[i,1] = pts[i,0,1]

    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)

    #draw the center of the object
    cntr = (X,Y)
    cv2.circle(img, cntr, 5, (255, 0, 255), -1)

    p1 = (X - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], Y - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
    p2 = (X + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], Y + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
    
    drawAxis(img, cntr, p1, (0, 255, 0), 20)
    drawAxis(img, cntr, p2, (255, 255, 0), 20)
    angle = atan2(eigenvectors[0,0], eigenvectors[0,1])*180/pi # orientation in degree
    return angle


if __name__ == '__main__':
    try:

        rospy.init_node('send_scripts', anonymous=True)

        targetP1 = "-100.00, 200.00 , 200.00 , 180.00 , 0.00 , 135.00"
        script = "PTP(\"CPP\","+targetP1+",100,200,0,false)"
        send_script(script)
        
        camera_info = rospy.wait_for_message("/usb_cam/image_raw", Image)
        bridge = CvBridge()
        img = bridge.imgmsg_to_cv2(camera_info, desired_encoding='passthrough')
        
        vis=img.copy()
        h,w,l = vis.shape
        cv2.imshow('1',vis)
        cv2.waitKey(0)
        gray = cv2.cvtColor( img,cv2.COLOR_BGR2GRAY)

        corners = cv2.goodFeaturesToTrack(gray,9,0.01,10)
        corners = np.int0(corners)
        c=[]
        
        for i in corners:
            x,y = i.ravel()
            cv2.circle(vis,(x,y),3,255,-1)
            c.append([x,y])
            

        cv2.imshow('2',vis)
        cv2.waitKey(0)
        c = sorted(c, key=lambda x: x[1], reverse = True)
        c1 = sorted(c[0:3], key=lambda x: x[0], reverse = True)
        c2 = sorted(c[3:6], key=lambda x: x[0], reverse = True)
        c3 = sorted(c[6:9], key=lambda x: x[0], reverse = True)
        c=c1+c2+c3

        # chess
        frame_gau_blur = cv2.GaussianBlur(img, (3, 3), 0)
        hsv = cv2.cvtColor(frame_gau_blur, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([5, 40, 80])
        higher_blue = np.array([10, 250, 250])
        lower_red = np.array([95, 40,80])
        higher_red = np.array([130, 250, 250])

        blue_range = cv2.inRange(hsv, lower_blue, higher_blue)
        res_blue = cv2.bitwise_and(frame_gau_blur, frame_gau_blur, mask=blue_range)
        blue_s_gray = cv2.cvtColor(res_blue, cv2.COLOR_BGR2GRAY)
        ret_blue, binary_blue = cv2.threshold(blue_s_gray,0,255,cv2.THRESH_BINARY)

        red_range = cv2.inRange(hsv, lower_red, higher_red)
        res_red = cv2.bitwise_and(frame_gau_blur, frame_gau_blur, mask=red_range)
        red_s_gray = cv2.cvtColor(res_red, cv2.COLOR_BGR2GRAY)
        ret_red, binary_red = cv2.threshold(red_s_gray,0,255,cv2.THRESH_BINARY)

        # cv2.imshow('4', hsv)
        # cv2.imshow('5', binary_blue)
        # cv2.imshow('6', binary_red)
        # cv2.waitKey(100000)
        cv2.destroyAllWindows()


        # find all Contours
        contours, hierarchy = cv2.findContours(binary_blue.copy(), cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE )
        clone = img.copy()

        #draw all contours
        cv2.drawContours(clone, contours, -1, (0, 0, 255), 3)

        cXs = np.array([])
        cYs = np.array([])
        angles = np.array([])
        targetNum = 0

        for i in contours:
            if len(i) > 10:
                M = cv2.moments(i)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                #get Principal Component
                angles = np.append(angles, getOrientation(i,clone,cX,cY))
                cXs = np.append(cXs, cX)
                cYs = np.append(cYs, cY)
                targetNum += 1

        cv2.imshow('image', clone)
        cv2.waitKey(0)
        r_c = 0.9763
        cMat_blue = np.zeros((3, 3))
        cMat_blue[0, :] = cXs*r_c
        cMat_blue[1, :] = cYs*r_c
        cMat_blue[2, :] = np.ones((1,3))
        # print('cMat_blue', cMat_blue)
        cv2.destroyAllWindows()

        # find all Contours
        contours, hierarchy = cv2.findContours(binary_red.copy(), cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE )
        clone = img.copy()

        #draw all contours
        cv2.drawContours(clone, contours, -1, (0, 0, 255), 3)

        cXs = np.array([])
        cYs = np.array([])
        angles = np.array([])
        targetNum = 0

        for i in contours:
            if len(i) > 10:
                M = cv2.moments(i)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                #get Principal Component
                angles = np.append(angles, getOrientation(i,clone,cX,cY))
                cXs = np.append(cXs, cX)
                cYs = np.append(cYs, cY)
                targetNum += 1

        cMat_red = np.zeros((3, 3))
        cMat_red[0, :] = cXs*r_c
        cMat_red[1, :] = cYs*r_c
        cMat_red[2, :] = np.ones((1,3))
        # print('cMat_red', cMat_red)
        cv2.destroyAllWindows()
        
        T_cm = np.array([[-0.7038, 0.7161, 394.3814], 
              [0.7235, 0.6964, -48.0704], 
              [0, 0, 1]])

        Rob_red = np.matmul(T_cm, cMat_red)
        # print('Rob_red', Rob_red)

        Rob_blue = np.matmul(T_cm, cMat_blue)
        # print('Rob_blue', Rob_blue)

        cMat_chess = np.zeros((3,9))
        cxc = []
        cyc = []
        for i in range(9):
            cxc = np.append(cxc,c[i][0])
            cyc = np.append(cyc,c[i][1])
        cMat_chess[0, :] = cxc*r_c
        cMat_chess[1, :] = cyc*r_c
        cMat_chess[2, :] = np.ones((1,9)) 
        # print("cMat_chess",cMat_chess)    
    
        Rob_chess = np.matmul(T_cm, cMat_chess)
        # print('Rob_chess', Rob_chess)

        place2rob = {1:(Rob_chess[0,0],Rob_chess[1,0]), 2:(Rob_chess[0,1],Rob_chess[1,1]), 3:(Rob_chess[0,2],Rob_chess[1,2]),4:(Rob_chess[0,3],Rob_chess[1,3]), 5:(Rob_chess[0,4],Rob_chess[1,4]), 6:(Rob_chess[0,5],Rob_chess[1,5]), 7:(Rob_chess[0,6],Rob_chess[1,6]), 8:(Rob_chess[0,7],Rob_chess[1,7]), 9:(Rob_chess[0,8],Rob_chess[1,8])}

        counter = 0
        main(counter, cMat_chess)

        targetP1 = "-100.00, 200.00 , 200.00 , 180.00 , 0.00 , 135.00"
        script = "PTP(\"CPP\","+targetP1+",100,0,0,false)"
        send_script(script)

    except rospy.ROSInterruptException:
        pass