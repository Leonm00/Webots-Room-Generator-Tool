import math
import Check_Input as C
import OpenCV_Input as OI
import numpy as np 
import Line_Treatment_Functions as LF

"""_Basic treatment of wall lines_
"""

def line_separation(room, isDefaultUse) :
    """_We separate the various walls according to their type_

    Args:
        room (_list_): _Corresponds to the list containing the wall positions_
        isDefaultUse (_bool_): _Whether or not to use default configuration_

    Returns:
        W_vertical (_list_): _List containing vertical wall positions_
        W_horizontal (_list_): _List containing horizontal wall positions_
        W_left_diagonal (_list_): _List containing left-diagonal wall positions_
        W_right_diagonal (_list_): _List containing right-diagonal wall positions_
        W_left_angle_diagonal (_list_): _List containing left-diagonal wall angles_
        W_right_angle_diagonal (_type_): _List containing right-diagonal wall angles_
    """
    if isDefaultUse is None :
        angle = 20
    elif isDefaultUse == True : 
        config = np.loadtxt("default_configuration.txt")
        angle = int(config[5])
    else : 
        angle = OI.get_angle()
    
    if isDefaultUse is None : 
        room_x = []
        room_y = []
        for e in room :
            room_x.append(e[0])
            room_y.append(e[1])
    else : 
        room_x, room_y = room[:,0], room[:,1]

    W_vertical, W_horizontal = [], []
    W_left_diagonal, W_left_angle_diagonal = [], []
    W_right_diagonal, W_right_angle_diagonal = [], []
    # We look at all pairs of points forming a line
    for i in range(int(len(room) / 2)) :
        x_1, y_1 = room_x[2 * i], room_y[2 * i]
        x_2, y_2 = room_x[2 * i + 1], room_y[2 * i + 1]
        if [x_1, y_1] != [x_2, y_2] :
            # You can't have a pair of identical points because that would just be a pixel (i.e. a point).
            # Same x , ie vertical
            if x_1 == x_2 :
                if y_1 < y_2 :
                    W_vertical.append([x_1, y_1])
                    W_vertical.append([x_2, y_2])
                else : 
                    W_vertical.append([x_2, y_2])
                    W_vertical.append([x_1, y_1])
            # Same y , ie horizontal
            elif y_1 == y_2 :
                if x_1 < x_2 :
                    W_horizontal.append([x_1, y_1])
                    W_horizontal.append([x_2, y_2])
                else : 
                    W_horizontal.append([x_2, y_2])
                    W_horizontal.append([x_1, y_1])
            # Diagonal
            else :
                isDiagonal = True 
                # If the vertical gap is smaller than the horizontal gap
                if abs(y_1 - y_2) < abs(x_1 - x_2) :
                    # Angle < angle
                    if math.atan(abs(y_1 - y_2) / abs(x_1 - x_2)) < angle * (math.pi / 180) : 
                        # We have a horizontal line
                        y_1 = y_2 
                        if x_1 < x_2 :
                            W_horizontal.append([x_1, y_2])
                            W_horizontal.append([x_2, y_2])
                        else : 
                            W_horizontal.append([x_2, y_2])
                            W_horizontal.append([x_1, y_2])
                        isDiagonal = False 
                else :
                    if math.atan(abs(x_1 - x_2) / abs(y_1 - y_2)) < angle * (math.pi / 180) :
                        x_1 = x_2
                        if y_1 < y_2 :
                            W_vertical.append([x_2, y_1])
                            W_vertical.append([x_2, y_2])
                        else : 
                            W_vertical.append([x_2, y_2])
                            W_vertical.append([x_2, y_1])
                        isDiagonal = False
                # If the current pair is a diagonal
                if isDiagonal == True :
                    # Diagonal direction (ie left or right / or \)
                    if y_1 < y_2 :
                        # Right
                        if x_1 > x_2 :
                            W_right_diagonal.append([x_1, y_1])
                            W_right_diagonal.append([x_2, y_2])
                            W_right_angle_diagonal.append(math.atan(abs(y_1 - y_2) / abs(x_1 - x_2)))
                        # Left
                        else : 
                            W_left_diagonal.append([x_1, y_1])
                            W_left_diagonal.append([x_2, y_2])
                            W_left_angle_diagonal.append(math.atan(abs(x_1 - x_2) / abs(y_1 - y_2)))
                    else :
                        # Right
                        if x_2 > x_1 :
                            W_right_diagonal.append([x_2, y_2])
                            W_right_diagonal.append([x_1, y_1])
                            W_right_angle_diagonal.append(math.atan(abs(y_1 - y_2) / abs(x_1 - x_2)))
                        # Left
                        else : 
                            W_left_diagonal.append([x_2, y_2])
                            W_left_diagonal.append([x_1, y_1])
                            W_left_angle_diagonal.append(math.atan(abs(x_1 - x_2) / abs(y_1 - y_2)))

    return W_vertical, W_horizontal, W_left_diagonal, W_right_diagonal, W_left_angle_diagonal, W_right_angle_diagonal

def fill_hole(W_vertical, W_horizontal, W_left_diagonal, W_right_diagonal, gap, isSetUse) :
    """_Each type of line is compared with other types of line, so that any gaps between them can be bridged and linked together. We have all the possible cases between each line category and another_

    Args:
        W_vertical (_list_): _The list containing the points of the vertical lines_
        W_horizontal (_list_): _The list containing the points of the horizontal lines_
        W_left_diagonal (_list_): _The list containing the points of the left diagonal lines_
        W_right_diagonal (_list_): _The list containing the points of the right diagonal lines_
        gap (_int_): _The threshold value_

    Returns:
        W_room (_list_): _The list containing the points of all the lines_
        W_vertical (_list_): _The list containing the points of the vertical lines_
        W_horizontal (_list_): _The list containing the points of the horizontal lines_
        W_diagonal (_list_): _The list containing the points of the diagonal lines_
    """

    # Each point on a line is assigned a number between 0 (if the point has not been modified) and 1 (if it has)
    EV, EH, EL, ER = [], [], [], []
    for e in range(len(W_vertical)) :
        EV.append(0)
    for e in range(len(W_horizontal)) :
        EH.append(0)
    for e in range(len(W_left_diagonal)) :
        EL.append(0)
    for e in range(len(W_right_diagonal)) :
        ER.append(0)
    
    # Variable number of vertical lines
    Nbr_V = int(len(W_vertical) / 2)
    # We start with the vertical lines and we compare each vertical line with all the horizontal and diagonal lines
    for i in range(Nbr_V) :
        W_vertical, EV, W_horizontal, EH = LF.Fill_V_and_H(i, W_vertical, EV, W_horizontal, EH, gap)
        W_vertical, EV, Nbr_V, W_horizontal, EH, W_left_diagonal, EL = LF.Fill_VH_and_Diagonal(i, 'Vertical', W_vertical, EV, Nbr_V, W_horizontal, EH, 'Left_Diagonal', W_left_diagonal, EL, gap)
        W_vertical, EV, Nbr_V, W_horizontal, EH, W_right_diagonal, ER = LF.Fill_VH_and_Diagonal(i, 'Vertical', W_vertical, EV, Nbr_V, W_horizontal, EH, 'Right_Diagonal', W_right_diagonal, ER, gap)

    W_vertical, EV, W_horizontal, EH, W_left_diagonal, EL, W_right_diagonal, ER = LF.erase_extra_and_bug(W_vertical, EV, W_horizontal, EH, W_left_diagonal, EL, W_right_diagonal, ER)  
    
    Nbr_H = int(len(W_horizontal) / 2)
    # We continue with the horizontals, which we'll compare with the diagonals
    for i in range(Nbr_H) :
        W_vertical, EV, Nbr_H, W_horizontal, EH, W_left_diagonal, EL = LF.Fill_VH_and_Diagonal(i, 'Horizontal', W_vertical, EV, Nbr_H, W_horizontal, EH, 'Left_Diagonal', W_left_diagonal, EL, gap)    
        W_vertical, EV, Nbr_H, W_horizontal, EH, W_right_diagonal, ER = LF.Fill_VH_and_Diagonal(i, 'Horizontal', W_vertical, EV, Nbr_H, W_horizontal, EH, 'Right_Diagonal', W_right_diagonal, ER, gap)

    W_vertical, EV, W_horizontal, EH, W_left_diagonal, EL, W_right_diagonal, ER = LF.erase_extra_and_bug(W_vertical, EV, W_horizontal, EH, W_left_diagonal, EL, W_right_diagonal, ER)
 
    # We finish with the diagonals
    for i in range(int(len(W_left_diagonal) / 2)) : 
        isOK = False
        # As long as the left diagonal has been modified during a run
        while isOK == False :
            isOK = True
            
            L_1 = W_left_diagonal[2 * i]
            L_2 = W_left_diagonal[2 * i + 1]
            
            Diff_x = int(abs(L_1[0] - L_2[0]))
            Diff_y = int(abs(L_2[1] - L_1[1]))
            Pgcd = math.gcd(Diff_x, Diff_y)
            Diff_x /= Pgcd
            Diff_y /= Pgcd
            Nbr = Pgcd + 1
            Nbr_gap = gap // (int(math.dist(L_1, L_2)) / Pgcd)
            Nbr_gap = int(Nbr_gap)

            for l in range(int(len(W_right_diagonal) / 2)) : 
                if isOK == True :
                    R_1 = W_right_diagonal[2 * l]
                    R_2 = W_right_diagonal[2 * l + 1]
                    if L_1 != R_1 and L_1 != R_2 and L_2 != R_1 and L_2 != R_2 :
                        diff_x = int(abs(R_1[0] - R_2[0]))
                        diff_y = int(abs(R_2[1] - R_1[1]))
                        pgcd = math.gcd(diff_x, diff_y)
                        diff_x /= pgcd
                        diff_y /= pgcd
                        nbr = pgcd + 1
                        nbr_gap = gap // (int(math.dist(R_1, R_2)) / pgcd)
                        nbr_gap = int(nbr_gap)
                        
                        if nbr_gap != 0 and Nbr_gap != 0 :
                            Min = 10000
                            Sens = 0
                            Position_L, Position_R = [], []
                            for j in range(- Nbr_gap, Nbr + Nbr_gap) :
                                for k in range(- nbr_gap, nbr_gap) :
                                    if math.dist([L_1[0] + j * Diff_x, L_1[1] + j * Diff_y], [R_1[0] - k * diff_x, R_1[1] + k * diff_y]) < Min :
                                        Min = math.dist([L_1[0] + j * Diff_x, L_1[1] + j * Diff_y], [R_1[0] - k * diff_x, R_1[1] + k * diff_y])
                                        Position_L = [L_1[0] + j * Diff_x, L_1[1] + j * Diff_y]
                                        Position_R = [R_1[0] - k * diff_x, R_1[1] + k * diff_y]
                                        Sens = 1
                                    elif math.dist([L_1[0] + j * Diff_x, L_1[1] + j * Diff_y], [R_2[0] - k * diff_x, R_2[1] + k * diff_y]) < Min :
                                        Min = math.dist([L_1[0] + j * Diff_x, L_1[1] + j * Diff_y], [R_2[0] - k * diff_x, R_2[1] + k * diff_y])
                                        Position_L = [L_1[0] + j * Diff_x, L_1[1] + j * Diff_y]
                                        Position_R = [R_2[0] - k * diff_x, R_2[1] + k * diff_y]
                                        Sens = 2
                            if Min == 0 :
                                isOK = False
                                if math.dist(L_1, R_1) <= gap :
                                    L_1 = Position_L
                                    R_1 = Position_R
                                    W_left_diagonal[2 * i] = L_1
                                    W_right_diagonal[2 * l] = R_1
                                    EL[2 * i] = 1
                                    ER[2 * l] = 1
                                elif math.dist(L_1, R_2) <= gap :
                                    L_1 = Position_L
                                    R_2 = Position_R
                                    W_left_diagonal[2 * i] = L_1
                                    W_right_diagonal[2 * l + 1] = R_2
                                    EL[2 * i] = 1
                                    ER[2 * l + 1] = 1
                                elif math.dist(L_2, R_1) <= gap :
                                    L_2 = Position_L
                                    R_1 = Position_R
                                    W_left_diagonal[2 * i + 1] = L_2
                                    W_right_diagonal[2 * l] = R_1
                                    EL[2 * i + 1] = 1
                                    EL[2 * l] = 1
                                elif math.dist(L_2, R_2) <= gap :
                                    L_2 = Position_L
                                    R_2 = Position_R
                                    W_left_diagonal[2 * i + 1] = L_2
                                    W_right_diagonal[2 * l + 1] = R_2
                                    EL[2 * i + 1] = 1
                                    ER[2 * l + 1] = 1
                                else :
                                    if Sens == 1 :
                                        R_1 = Position_R
                                        W_right_diagonal[2 * l] = R_1
                                        ER[2 * l] = 1
                                        if EL[2 * i] == 0 :
                                            EL[2 * i] = 2
                                    elif Sens == 2 : 
                                        R_2 = Position_R
                                        W_right_diagonal[2 * l + 1] = R_2
                                        ER[2 * l + 1] = 1
                                        if EL[2 * i] == 0 :
                                            EL[2 * i] = 2
                        if isOK == True : 
                            if math.dist(L_1, R_1) <= gap :
                                isOK = False
                                if EL[2 * i] == 0 and ER[2 * l] == 0 :
                                    L_1 = [int((L_1[0] + R_1[0]) / 2), int((L_1[1] + R_1[1]) / 2)]
                                    R_1 = L_1
                                elif EL[2 * i] == 1 : 
                                    R_1 = L_1
                                elif ER[2 * l] == 1 : 
                                    L_1 = R_1
                                W_left_diagonal[2 * i] = L_1
                                W_right_diagonal[2 * l] = R_1
                                EL[2 * i] = 1
                                ER[2 * l] = 1
                            elif math.dist(L_1, R_2) <= gap :
                                isOK = False
                                if EL[2 * i] == 0 and ER[2 * l + 1] == 0 :
                                    L_1 = [int((L_1[0] + R_2[0]) / 2), int((L_1[1] + R_2[1]) / 2)]
                                    R_2 = L_1
                                elif EL[2 * i] == 1 : 
                                    R_2 = L_1
                                elif ER[2 * l + 1] == 1 : 
                                    L_1 = R_2
                                W_left_diagonal[2 * i] = L_1
                                W_right_diagonal[2 * l + 1] = R_2
                                EL[2 * i] = 1
                                ER[2 * l + 1] = 1
                            elif math.dist(L_2, R_1) <= gap :
                                isOK = False
                                if EL[2 * i + 1] == 0 and ER[2 * l] == 0 :
                                    L_2 = [int((L_2[0] + R_1[0]) / 2), int((L_2[1] + R_1[1]) / 2)]
                                    R_1 = L_2
                                elif EL[2 * i + 1] == 1 : 
                                    R_1 = L_2
                                elif ER[2 * l] == 1 : 
                                    L_2 = R_1
                                W_left_diagonal[2 * i + 1] = L_2
                                W_right_diagonal[2 * l] = R_1
                                EL[2 * i + 1] = 1
                                ER[2 * l] = 1
                            elif math.dist(L_2, R_2) <= gap :
                                isOK = False
                                if EL[2 * i + 1] == 0 and ER[2 * l + 1] == 0 :
                                    L_2 = [int((L_2[0] + R_2[0]) / 2), int((L_2[1] + R_2[1]) / 2)]
                                    R_2 = L_2
                                elif EL[2 * i + 1] == 1 : 
                                    R_2 = L_2
                                elif ER[2 * l + 1] == 1 : 
                                    L_2 = R_2
                                W_left_diagonal[2 * i + 1] = L_2
                                W_right_diagonal[2 * l + 1] = R_2
                                EL[2 * i + 1] = 1
                                ER[2 * l + 1] = 1
    W_vertical, EV, W_horizontal, EH, W_left_diagonal, EL, W_right_diagonal, ER = LF.erase_extra_and_bug(W_vertical, EV, W_horizontal, EH, W_left_diagonal, EL, W_right_diagonal, ER)

    if isSetUse == False : 
        Ind_V = []
        for i in range(int(len(EV) / 2)) :
            if EV[2 * i] == EV[2 * i + 1] == 0 :
                Ind_V.append(i)
        Ind_V.sort(reverse = True)
        Ind_H = []
        for i in range(int(len(EH) / 2)) :
            if EH[2 * i] == EH[2 * i + 1] == 0 :
                Ind_H.append(i)
        Ind_H.sort(reverse = True)
        Ind_L = []
        for i in range(int(len(EL) / 2)) :
            if EL[2 * i] == EL[2 * i + 1] == 0 :
                Ind_L.append(i)
        Ind_L.sort(reverse = True)
        Ind_R = []
        for i in range(int(len(ER) / 2)) :
            if ER[2 * i] == ER[2 * i + 1] == 0 :
                Ind_R.append(i)
        Ind_R.sort(reverse = True)
        
        print("Do you want to remove the walls that are all alone ?")
        print(" Number of Vertical alone : ", len(Ind_V))
        print(" Number of Horizontal alone : ", len(Ind_H))
        print(" Number of Left Diagonal alone : ", len(Ind_L))
        print(" Number of Right Diagonal alone : ", len(Ind_R))
        
        choice = input("    Press 'Y' for Yes or 'N' for No : ")
        choiceOK = False
        while choiceOK == False :
            if C.check_input(choice) == 'str' :
                if str(choice) == 'Y' or str(choice) == 'y' or str(choice) == 'N' or str(choice) == 'n' :
                    choiceOK = True
                else :
                    print("     Not an expected string - Please retry")
                    choice = input("    Press 'Y' for Yes or 'N' for No : ")
            else : 
                print("     Not a string - Please retry")
                choice = input("    Press 'Y' for Yes or 'N' for No : ")
                
        if choice == 'Y' or choice == 'y' :
            for e in Ind_V :
                del(W_vertical[2 * e + 1])
                del(W_vertical[2 * e])
            for e in Ind_H :
                del(W_horizontal[2 * e + 1])
                del(W_horizontal[2 * e])
            for e in Ind_L :
                del(W_left_diagonal[2 * e + 1])
                del(W_left_diagonal[2 * e])
            for e in Ind_R :
                del(W_right_diagonal[2 * e + 1])
                del(W_right_diagonal[2 * e])
            
    W_room = []
    W_diagonal = []
    for e in W_vertical :
        W_room.append([e[0], e[1]])
    for e in W_horizontal :
        W_room.append([e[0], e[1]])
    for e in W_left_diagonal :
        W_room.append([e[0], e[1]])
        W_diagonal.append([e[0], e[1]])
    for e in W_right_diagonal :
        W_room.append([e[0], e[1]])
        W_diagonal.append([e[0], e[1]])

    return W_room, W_vertical, W_horizontal, W_diagonal
