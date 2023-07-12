import math
import Check_Input as C
import OpenCV_Input as OI

"""_Basic treatment of wall lines_
"""

def line_separation(room) :
    """_We separate the various walls according to their type_

    Args:
        room (_list_): _Corresponds to the list containing the wall positions_

    Returns:
        W_vertical (_list_): _List containing vertical wall positions_
        W_horizontal (_list_): _List containing horizontal wall positions_
        W_left_diagonal (_list_): _List containing left-diagonal wall positions_
        W_right_diagonal (_list_): _List containing right-diagonal wall positions_
        W_left_angle_diagonal (_list_): _List containing left-diagonal wall angles_
        W_right_angle_diagonal (_type_): _List containing right-diagonal wall angles_
    """
    angle = OI.get_angle()
    
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
                            W_horizontal.append([x_1, y_1])
                            W_horizontal.append([x_2, y_2])
                        else : 
                            W_horizontal.append([x_2, y_2])
                            W_horizontal.append([x_1, y_1])
                        isDiagonal = False 
                else :
                    if math.atan(abs(x_1 - x_2) / abs(y_1 - y_2)) < angle * (math.pi / 180) :
                        x_1 = x_2
                        if y_1 < y_2 :
                            W_vertical.append([x_1, y_1])
                            W_vertical.append([x_2, y_2])
                        else : 
                            W_vertical.append([x_2, y_2])
                            W_vertical.append([x_1, y_1])
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

def fill_hole(W_vertical, W_horizontal, W_left_diagonal, W_right_diagonal, gap) :
    """_Each type of line is compared with other types of line, so that any gaps between them can be bridged and linked together. We have all the possible cases between each line category and another_

    Args:
        W_vertical (_list_): _The list containing the points of the vertical lines_
        W_horizontal (_list_): _The list containing the points of the horizontal lines_
        W_left_diagonal (_list_): _The list containing the points of the left diagonal lines_
        W_right_diagonal (_list_): _The list containing the points of the right diagonal lines_
        gap (_int_): _The threshold value_

    Returns:
        W_room (_list_): _The list containing the points of all the lines_
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
        
    # If, after processing all the verticals, there are pairs of identical points, we store the corresponding index and then remove them.
    Extra_V = []
    # We start with the vertical lines and we compare each vertical line with all the horizontal and diagonal lines
    for i in range(int(len(W_vertical) / 2)) :
        V_1, V_2 = W_vertical[2 * i], W_vertical[2 * i + 1]
        Extra_H, Extra_L, Extra_R = [], [], []
        for j in range(int(len(W_horizontal) / 2)) : 
            H_1, H_2 = W_horizontal[2 * j], W_horizontal[2 * j + 1]
            # If there's already a connection between the vertical and the horizontal
            if V_1 == H_1 :
                EV[2 * i] = EH[2 * j] = 1
            elif V_1 == H_2 :
                EV[2 * i] = EH[2 * j + 1] = 1
            elif V_2 == H_1 :
                EV[2 * i + 1] = EH[2 * j] = 1
            elif V_2 == H_2 :
                EV[2 * i + 1] = EH[2 * j + 1] = 1
            else :
                # We look to see if there are two points close together
                if math.dist(V_1, H_1) <= gap and math.dist(V_1, H_1) < math.dist(V_1, H_2) :
                    V_1[1] = H_1[1]
                    W_vertical[2 * i] = W_horizontal[2 * j] = V_1
                    EV[2 * i] = EH[2 * j] = 1
                elif math.dist(V_1, H_2) <= gap :
                    V_1[1] = H_2[1]
                    W_vertical[2 * i] = W_horizontal[2 * j + 1] = V_1
                    EV[2 * i] = EH[2 * j + 1] = 1
                elif math.dist(V_2, H_1) <= gap and math.dist(V_2, H_1) < math.dist(V_2, H_2) :
                    V_2[1] = H_1[1]
                    W_vertical[2 * i + 1] = W_horizontal[2 * j] = V_2
                    EV[2 * i + 1] = EH[2 * j] = 1
                elif math.dist(V_2, H_2) <= gap :
                    V_2[1] = H_2[1]
                    W_vertical[2 * i + 1] = W_horizontal[2 * j + 1] = V_2
                    EV[2 * i + 1] = EH[2 * j + 1] = 1
                # If not, we'll see if we can lengthen or narrow the vertical wall to fit the horizontal line, or vice versa
                else :
                    # If the horizontal is above or below the vertical
                    if H_1[0] < V_1[0] and H_2[0] > V_1[0] :
                        # Up and close
                        if H_1[1] != V_1[1] and abs(H_1[1] - V_1[1]) <= gap :
                            V_1[1] = H_1[1]
                            W_vertical[2 * i] = V_1
                            EV[2 * i] = 1
                            # To ensure that the horizontal is not considered as an isolated wall
                            if EH[2 * j] == 0 :
                                EH[2 * j] = 2
                        # Down and close
                        elif H_1[1] != V_2[1] and abs(H_1[1] - V_2[1]) <= gap :
                            V_2[1] = H_1[1]
                            W_vertical[2 * i + 1] = V_2
                            EV[2 * i + 1] = 1
                            if EH[2 * j] == 0 :
                                EH[2 * j] = 2
                    # If the horizontal is to the left or right of the vertical
                    if V_1[1] < H_1[1] and V_2[1] > H_1[1] :
                        # Right and close
                        if V_1[0] != H_1[0] and abs(V_1[0] - H_1[0]) <= gap :
                            H_1[0] = V_1[0]
                            W_horizontal[2 * j] = H_1
                            EH[2 * j] = 1
                            if EV[2 * i] == 0 :
                                EV[2 * i] = 2
                        # Left and close
                        elif V_1[0] != H_2[0] and abs(V_1[0] - H_2[0]) <= gap :
                            H_2[0] = V_1[0]
                            W_horizontal[2 * j + 1] = H_2
                            EH[2 * j + 1] = 1
                            if EV[2 * i] == 0 :
                                EV[2 * i] = 2
            if H_1 == H_2 :
                Extra_H.append(j)
        if len(Extra_H) != 0 :
            Extra_H.sort(reverse = True)
            for e in Extra_H :
                del(W_horizontal[2 * e + 1])
                del(W_horizontal[2 * e])
                del(EH[2 * e + 1])
                del(EH[2 * e])
                
        for k in range(int(len(W_left_diagonal) / 2)) : 
            L_1, L_2 = W_left_diagonal[2 * k], W_left_diagonal[2 * k + 1]
            # If there's already a connection between the vertical and the left diagonal
            if V_1 == L_1 :
                EV[2 * i] = EL[2 * k] = 1
            elif V_1 == L_2 :
                EV[2 * i] = EL[2 * k + 1] = 1
            elif V_2 == L_1 :
                EV[2 * i + 1] = EL[2 * k] = 1
            elif V_2 == L_2 :
                EV[2 * i + 1] = EL[2 * k + 1] = 1
            else :
                # Gets the X and Y step of the current left diagonal
                diff_x = int(abs(L_1[0] - L_2[0]))
                diff_y = int(abs(L_2[1] - L_1[1]))
                pgcd = math.gcd(diff_x, diff_y)
                diff_x /= pgcd
                diff_y /= pgcd
                # We look to see if there are two points close together
                if math.dist(V_1, L_1) <= gap :
                    # If the near vertical point has already been modified
                    if EV[2 * i] == 1 :
                        L_1 = V_1
                        W_left_diagonal[2 * k] = L_1
                        EL[2 * k] = 1
                    # Else, both diagonal and vertical can be lengthened/shortened
                    else : 
                        # Same x between the two nearby points. We just lengthen the vertical
                        if L_1[0] == V_1[0] :
                            V_1[1] = L_1[1]
                        # Otherwise, extend the diagonal to the correct y position and then extend the vertical to the same point.
                        else : 
                            y = int(abs(L_1[0] - V_1[0]) / (diff_x / diff_y))
                            if L_1[0] < V_1[0] :
                                V_1[1] = L_1[1] + y
                            elif L_1[0] > V_1[0] :
                                V_1[1] = L_1[1] - y
                            L_1 = V_1
                            W_left_diagonal[2 * k] = L_1
                        W_vertical[2 * i] = V_1
                        EV[2 * i] = EL[2 * k] = 1
                elif math.dist(V_1, L_2) <= gap :
                    if EV[2 * i] == 1 :
                        L_2 = V_1
                        W_left_diagonal[2 * k + 1] = L_2
                        EL[2 * k + 1] = 1
                    else : 
                        if L_2[0] == V_1[0] :
                            V_1[1] = L_2[1]
                        else : 
                            y = int(abs(L_2[0] - V_1[0]) / (diff_x / diff_y))
                            if L_2[0] < V_1[0] :
                                V_1[1] = L_2[1] + y
                            elif L_2[0] > V_1[0] :
                                V_1[1] = L_2[1] - y
                            L_2 = V_1
                            W_left_diagonal[2 * k + 1] = L_2
                        W_vertical[2 * i] = V_1
                        EV[2 * i] = EL[2 * k + 1] = 1
                elif math.dist(V_2, L_1) <= gap :
                    if EV[2 * i + 1] == 1 :
                        L_1 = V_2
                        W_left_diagonal[2 * k] = L_1
                        EL[2 * k] = 1
                    else : 
                        if L_1[0] == V_2[0] :
                            V_2[1] = L_1[1]
                        else : 
                            y = int(abs(L_1[0] - V_2[0]) / (diff_x / diff_y))
                            if L_1[0] < V_2[0] :
                                V_2[1] = L_1[1] + y
                            elif L_1[0] > V_2[0] :
                                V_2[1] = L_1[1] - y
                            L_1 = V_2
                            W_left_diagonal[2 * k] = L_1
                        W_vertical[2 * i + 1] = V_2
                        EV[2 * i + 1] = EL[2 * k] = 1
                elif math.dist(V_2, L_2) <= gap :
                    if EV[2 * i + 1] == 1 :
                        L_2 = V_2
                        W_left_diagonal[2 * k + 1] = L_2
                        EL[2 * k + 1] = 1
                    else : 
                        if L_2[0] == V_2[0] :
                            V_2[1] = L_2[1]
                        else : 
                            y = int(abs(L_2[0] - V_2[0]) / (diff_x / diff_y))
                            if L_2[0] < V_2[0] :
                                V_2[1] = L_2[1] + y
                            elif L_2[0] > V_2[0] :
                                V_2[1] = L_2[1] - y
                            L_2 = V_2
                            W_left_diagonal[2 * k + 1] = L_2
                        W_vertical[2 * i + 1] = V_2
                        EV[2 * i + 1] = EL[2 * k + 1] = 1
                # If there's no close point, we see if we can lengthen or narrow the vertical wall or the left diagonal wall so that they touch
                else :
                    # Diagonal to the left of vertical and close 
                    if L_1[0] < V_1[0] and abs(L_2[0] - V_1[0]) <= gap and L_2[1] > V_1[1] and L_2[1] < V_2[1] :
                        y = int(abs(L_2[0] - V_1[0]) / (diff_x / diff_y))         
                        if L_2[0] < V_1[0] :
                            L_2[0] = V_1[0]
                            L_2[1] += y
                        elif L_2[0] > V_1[0] :
                            L_2[0] = V_1[0]
                            L_2[1] -= y
                        W_left_diagonal[2 * k + 1] = L_2
                        EL[2 * k + 1] = 1
                        if EV[2 * i] == 0 :
                            EV[2 * i] = 2
                    # Diagonal to the right of vertical and close
                    elif L_2[0] > V_1[0] and abs(L_1[0] - V_1[0]) <= gap and L_1[1] > V_1[1] and L_1[1] < V_2[1] :
                        y = int(abs(L_1[0] - V_1[0]) / (diff_x / diff_y))         
                        if L_1[0] < V_1[0] :
                            L_1[0] = V_1[0]
                            L_1[1] += y
                        elif L_1[0] > V_1[0] :
                            L_1[0] = V_1[0]
                            L_1[1] -= y
                        W_left_diagonal[2 * k] = L_1
                        EL[2 * k] = 1
                        if EV[2 * i] == 0 :
                            EV[2 * i] = 2
                    # Diagonal at the top of the vertical or at the bottom
                    elif L_1[0] < V_1[0] and L_2[0] > V_1[0] :
                        y = int(abs(L_1[0] - V_1[0]) / (diff_x / diff_y)) 
                        # Top and close
                        if abs(L_1[1] + y - V_1[1]) <= gap :
                            V_1[1] = L_1[1] + y
                            W_vertical[2 * i] = V_1
                            EV[2 * i] = 1
                            if EL[2 * k] == 0 :
                                EL[2 * k] = 2
                        # Bottom and close
                        elif abs(L_1[1] + y - V_2[1]) <= gap :
                            V_2[1] = L_1[1] + y
                            W_vertical[2 * i + 1] = V_2
                            EV[2 * i + 1] = 1
                            if EL[2 * k] == 0 :
                                EL[2 * k] = 2
            if L_1 == L_2 :
                Extra_L.append(k)
        if len(Extra_L) != 0 :
            Extra_L.sort(reverse = True)
            for e in Extra_L :
                del(W_left_diagonal[2 * e + 1])
                del(W_left_diagonal[2 * e])
                del(EL[2 * e + 1])
                del(EL[2 * e])
                
        for l in range(int(len(W_right_diagonal) / 2)) : 
            R_1, R_2 = W_right_diagonal[2 * l], W_right_diagonal[2 * l + 1]
            if V_1 == R_1 :
                EV[2 * i] = ER[2 * l] = 1
            elif V_1 == R_2 :
                EV[2 * i] = ER[2 * l + 1] = 1
            elif V_2 == R_1 :
                EV[2 * i + 1] = ER[2 * l] = 1
            elif V_2 == R_2 :
                EV[2 * i + 1] = ER[2 * l + 1] = 1
            else :
                # Gets the X and Y step of the current right diagonal
                diff_x = int(abs(R_1[0] - R_2[0]))
                diff_y = int(abs(R_2[1] - R_1[1]))
                pgcd = math.gcd(diff_x, diff_y)
                diff_x /= pgcd
                diff_y /= pgcd
                if math.dist(V_1, R_1) <= gap :
                    if EV[2 * i] == 1 :
                        R_1 = V_1
                        W_right_diagonal[2 * l] = R_1
                        ER[2 * l] = 1
                    else : 
                        if R_1[0] == V_1[0] :
                            V_1[1] = R_1[1]
                        else : 
                            y = int(abs(R_1[0] - V_1[0]) / (diff_x / diff_y))
                            if R_1[0] < V_1[0] :
                                V_1[1] = R_1[1] - y
                            elif R_1[0] > V_1[0] :
                                V_1[1] = L_1[1] + y
                            R_1 = V_1
                            W_right_diagonal[2 * l] = R_1
                        W_vertical[2 * i] = V_1
                        EV[2 * i] = ER[2 * l] = 1
                elif math.dist(V_1, R_2) <= gap :
                    if EV[2 * i] == 1 :
                        R_2 = V_1
                        W_right_diagonal[2 * l + 1] = R_2
                        ER[2 * l + 1] = 1
                    else : 
                        if R_2[0] == V_1[0] :
                            V_1[1] = R_2[1]
                        else : 
                            y = int(abs(R_2[0] - V_1[0]) / (diff_x / diff_y))
                            if R_2[0] < V_1[0] :
                                V_1[1] = R_2[1] - y
                            elif R_2[0] > V_1[0] :
                                V_1[1] = R_2[1] + y
                            R_2 = V_1
                            W_right_diagonal[2 * l + 1] = R_2
                        W_vertical[2 * i] = V_1
                        EV[2 * i] = ER[2 * l + 1] = 1
                elif math.dist(V_2, R_1) <= gap :
                    if EV[2 * i + 1] == 1 :
                        R_1 = V_2
                        W_right_diagonal[2 * l] = R_1
                        ER[2 * l] = 1
                    else : 
                        if R_1[0] == V_2[0] :
                            V_2[1] = R_1[1]
                        else : 
                            y = int(abs(R_1[0] - V_2[0]) / (diff_x / diff_y))
                            if R_1[0] < V_2[0] :
                                V_2[1] = R_1[1] - y
                            elif R_1[0] > V_2[0] :
                                V_2[1] = R_1[1] + y
                            R_1 = V_2
                            W_right_diagonal[2 * l] = R_1
                        W_vertical[2 * i + 1] = V_2
                        EV[2 * i + 1] = ER[2 * l] = 1
                elif math.dist(V_2, R_2) <= gap :
                    if EV[2 * i + 1] == 1 :
                        R_2 = V_2
                        W_right_diagonal[2 * l + 1] = R_2
                        ER[2 * l + 1] = 1
                    else : 
                        if R_2[0] == V_2[0] :
                            V_2[1] = R_2[1]
                        else : 
                            y = int(abs(R_2[0] - V_2[0]) / (diff_x / diff_y))
                            if R_2[0] < V_2[0] :
                                V_2[1] = R_2[1] - y
                            elif R_2[0] > V_2[0] :
                                V_2[1] = R_2[1] + y
                            R_2 = V_2
                            W_right_diagonal[2 * l + 1] = R_2
                        W_vertical[2 * i + 1] = V_2
                        EV[2 * i + 1] = ER[2 * l + 1] = 1
                else :
                    # Diagonal to the left of vertical and close 
                    if R_2[0] < V_1[0] and abs(R_1[0] - V_1[0]) <= gap and R_1[1] > V_1[1] and R_1[1] < V_2[1] :
                        y = int(abs(R_1[0] - V_1[0]) / (diff_x / diff_y))         
                        if R_1[0] < V_1[0] :
                            R_1[0] = V_1[0]
                            R_1[1] -= y
                        elif R_1[0] > V_1[0] :
                            R_1[0] = V_1[0]
                            R_1[1] += y
                        W_right_diagonal[2 * l] = R_1
                        ER[2 * l] = 1
                        if EV[2 * i] == 0 :
                            EV[2 * i] = 2
                    # Diagonal to the right of vertical and close 
                    elif R_1[0] > V_1[0] and abs(R_2[0] - V_1[0]) <= gap and R_2[1] > V_1[1] and R_2[1] < V_2[1] :
                        y = int(abs(R_2[0] - V_1[0]) / (diff_x / diff_y))         
                        if R_2[0] < V_1[0] :
                            R_2[0] = V_1[0]
                            R_2[1] -= y
                        elif R_2[0] > V_1[0] :
                            R_2[0] = V_1[0]
                            R_2[1] += y
                        W_right_diagonal[2 * l + 1] = R_2
                        ER[2 * l + 1] = 1
                        if EV[2 * i] == 0 :
                            EV[2 * i] = 2
                    # Diagonal at the top of the vertical or at the bottom
                    elif R_2[0] < V_1[0] and R_1[0] > V_1[0] :
                        y = int(abs(R_1[0] - V_1[0]) / (diff_x / diff_y)) 
                        # Top and close
                        if abs(R_1[1] + y - V_1[1]) <= gap :
                            V_1[1] = R_1[1] + y
                            W_vertical[2 * i] = V_1
                            EV[2 * i] = 1
                            if ER[2 * l] == 0 :
                                ER[2 * l] = 2
                        # Bottom and close
                        elif abs(R_1[1] + y - V_2[1]) <= gap :
                            V_2[1] = R_1[1] + y
                            W_vertical[2 * i + 1] = V_2
                            EV[2 * i + 1] = 1
                            if ER[2 * l] == 0 :
                                ER[2 * l] = 2
                        
            if R_1 == R_2 :
                Extra_R.append(l)
        if len(Extra_R) != 0 :
            Extra_R.sort(reverse = True)
            for e in Extra_R :
                del(W_right_diagonal[2 * e + 1])
                del(W_right_diagonal[2 * e])
                del(ER[2 * e + 1])
                del(ER[2 * e])
        
        if V_1 == V_2 :
            Extra_V.append(i)
    if len(Extra_V) != 0 :
        Extra_V.sort(reverse = True)
        for e in Extra_V :
            del(W_vertical[2 * e + 1])
            del(W_vertical[2 * e])
            del(EV[2 * e + 1])
            del(EV[2 * e])
    
    # We continue with the horizontals, which we'll compare with the diagonals
    Extra_H = []
    for i in range(int(len(W_horizontal) / 2)) :
        H_1, H_2 = W_horizontal[2 * i], W_horizontal[2 * i + 1]  
        Extra_L, Extra_R = [], []      
        for k in range(int(len(W_left_diagonal) / 2)) : 
            L_1, L_2 = W_left_diagonal[2 * k], W_left_diagonal[2 * k + 1]
            if H_1 == L_1 :
                EH[2 * i] = EL[2 * k] = 1
            elif H_1 == L_2 :
                EH[2 * i] = EL[2 * k + 1] = 1
            elif H_2 == L_1 :
                EH[2 * i + 1] = EL[2 * k] = 1
            elif H_2 == L_2 :
                EH[2 * i + 1] = EL[2 * k + 1] = 1
            else :
                # Gets the X and Y step of the current left diagonal
                diff_x = int(abs(L_1[0] - L_2[0]))
                diff_y = int(abs(L_2[1] - L_1[1]))
                pgcd = math.gcd(diff_x, diff_y)
                diff_x /= pgcd
                diff_y /= pgcd
                if math.dist(H_1, L_1) <= gap :
                    if EH[2 * i] == 1 :
                        L_1 = H_1
                        W_left_diagonal[2 * k] = L_1
                        EL[2 * k] = 1
                    else : 
                        if L_1[1] == H_1[1] :
                            H_1[0] = L_1[0]
                        else : 
                            x = int(abs(L_1[1] - H_1[1]) / (diff_y / diff_x))
                            if L_1[1] < H_1[1] :
                                H_1[0] = L_1[0] + x
                            elif L_1[1] > H_1[1] :
                                H_1[0] = L_1[0] - x
                            L_1 = H_1
                            W_left_diagonal[2 * k] = L_1
                        W_horizontal[2 * i] = H_1
                        EH[2 * i] = EL[2 * k] = 1
                elif math.dist(H_1, L_2) <= gap :
                    if EH[2 * i] == 1 :
                        L_2 = H_1
                        W_left_diagonal[2 * k + 1] = L_2
                        EL[2 * k + 1] = 1
                    else : 
                        if L_2[1] == H_1[1] :
                            H_1[0] = L_2[0]
                        else : 
                            x = int(abs(L_2[1] - H_1[1]) / (diff_y / diff_x))
                            if L_2[1] < H_1[1] :
                                H_1[0] = L_2[0] + x
                            elif L_2[1] > H_1[1] :
                                H_1[0] = L_2[0] - x
                            L_2 = H_1
                            W_left_diagonal[2 * k + 1] = L_2
                        W_horizontal[2 * i] = H_1
                        EH[2 * i] = EL[2 * k + 1] = 1
                elif math.dist(H_2, L_1) <= gap :
                    if EH[2 * i + 1] == 1 :
                        L_1 = H_2
                        W_left_diagonal[2 * k] = L_1
                        EL[2 * k] = 1
                    else : 
                        if L_1[1] == H_2[1] :
                            H_2[0] = L_1[0]
                        else : 
                            x = int(abs(L_1[1] - H_2[1]) / (diff_y / diff_x))
                            if L_1[1] < H_2[1] :
                                H_2[0] = L_1[0] + x
                            elif L_1[1] > H_2[1] :
                                H_2[0] = L_1[0] - x
                            L_1 = H_2
                            W_left_diagonal[2 * k] = L_1
                        W_horizontal[2 * i + 1] = H_2
                        EH[2 * i + 1] = EL[2 * k] = 1
                elif math.dist(H_2, L_2) <= gap :
                    if EH[2 * i + 1] == 1 :
                        L_2 = H_2
                        W_left_diagonal[2 * k + 1] = L_2
                        EL[2 * k + 1] = 1
                    else : 
                        if L_2[1] == H_2[1] :
                            H_2[0] = L_2[0]
                        else : 
                            x = int(abs(L_2[1] - H_2[1]) / (diff_y / diff_x))
                            if L_2[1] < H_2[1] :
                                H_2[0] = L_2[0] + x
                            elif L_2[1] > H_2[1] :
                                H_2[0] = L_2[0] - x
                            L_2 = H_2
                            W_left_diagonal[2 * k + 1] = L_2
                        W_horizontal[2 * i + 1] = H_2
                        EH[2 * i + 1] = EL[2 * k + 1] = 1
                else :
                    # Diagonal at the top of the horizontal and close 
                    if L_1[1] < H_1[1] and abs(L_2[1] - H_1[1]) <= gap and L_2[0] > H_1[0] and L_2[0] < H_2[0] :
                        x = int(abs(L_2[1] - H_1[1]) / (diff_y / diff_x))         
                        if L_2[1] < H_1[1] :
                            L_2[1] = H_1[1]
                            L_2[0] += x
                        elif L_2[1] > H_1[1] :
                            L_2[1] = H_1[1]
                            L_2[0] -= x
                        W_left_diagonal[2 * k + 1] = L_2
                        EL[2 * k + 1] = 1
                        if EH[2 * i] == 0 :
                            EH[2 * i] = 2
                    # Diagonal at the bottom of the horizontal and close
                    elif L_2[1] > H_1[1] and abs(L_1[1] - H_1[1]) <= gap and L_1[0] > H_1[0] and L_1[0] < H_2[0] :
                        x = int(abs(L_1[1] - H_1[1]) / (diff_y / diff_x))         
                        if L_1[1] < H_1[1] :
                            L_1[1] = H_1[1]
                            L_1[0] += x
                        elif L_1[1] > H_1[1] :
                            L_1[1] = H_1[1]
                            L_1[0] -= x
                        W_left_diagonal[2 * k] = L_1
                        EL[2 * k] = 1
                        if EH[2 * i] == 0 :
                            EH[2 * i] = 2
                    # Diagonal to the left or right of horizontal
                    elif L_1[1] < H_1[1] and L_2[1] > H_1[1] :
                        x = int(abs(L_1[1] - H_1[1]) / (diff_y / diff_x)) 
                        # Left and close
                        if abs(L_1[0] + x - H_1[0]) <= gap :
                            H_1[0] = L_1[0] + x
                            W_horizontal[2 * i] = H_1
                            EH[2 * i] = 1
                            if EL[2 * k] == 0 :
                                EL[2 * k] = 2
                        # Right and close
                        elif abs(L_1[0] + x - H_2[0]) <= gap :
                            H_2[0] = L_1[0] + x
                            W_horizontal[2 * i + 1] = H_2
                            EH[2 * i + 1] = 1
                            if EL[2 * k] == 0 :
                                EL[2 * k] = 2
            if L_1 == L_2 :
                Extra_L.append(k)
        if len(Extra_L) != 0 :
            Extra_L.sort(reverse = True)
            for e in Extra_L :
                del(W_left_diagonal[2 * e + 1])
                del(W_left_diagonal[2 * e])
                del(EL[2 * e + 1])
                del(EL[2 * e])
                            
        for l in range(int(len(W_right_diagonal) / 2)) : 
            R_1, R_2 = W_right_diagonal[2 * l], W_right_diagonal[2 * l + 1]
            if H_1 == R_1 :
                EH[2 * i] = ER[2 * l] = 1
            elif H_1 == R_2 :
                EH[2 * i] = ER[2 * l + 1] = 1
            elif H_2 == R_1 :
                EH[2 * i + 1] = ER[2 * l] = 1
            elif H_2 == R_2 :
                EH[2 * i + 1] = ER[2 * l + 1] = 1
            else :
                # Gets the X and Y step of the current right diagonal
                diff_x = int(abs(R_1[0] - R_2[0]))
                diff_y = int(abs(R_2[1] - R_1[1]))
                pgcd = math.gcd(diff_x, diff_y)
                diff_x /= pgcd
                diff_y /= pgcd
                if math.dist(H_1, R_1) <= gap :
                    if EH[2 * i] == 1 :
                        R_1 = H_1
                        W_right_diagonal[2 * l] = R_1
                        ER[2 * l] = 1
                    else : 
                        if R_1[1] == H_1[1] :
                            H_1[0] = R_1[0]
                        else : 
                            x = int(abs(R_1[1] - H_1[1]) / (diff_y / diff_x))
                            if R_1[1] < H_1[1] :
                                H_1[0] = R_1[0] - x
                            elif R_1[1] > H_1[1] :
                                H_1[0] = R_1[0] + x
                            R_1 = H_1
                            W_right_diagonal[2 * l] = R_1
                        W_horizontal[2 * i] = H_1
                        EH[2 * i] = ER[2 * l] = 1
                elif math.dist(H_1, R_2) <= gap :
                    if EH[2 * i] == 1 :
                        R_2 = H_1
                        W_right_diagonal[2 * l + 1] = R_2
                        ER[2 * l + 1] = 1
                    else : 
                        if R_2[1] == H_1[1] :
                            H_1[0] = R_2[0]
                        else : 
                            x = int(abs(R_2[1] - H_1[1]) / (diff_y / diff_x))
                            if R_2[1] < H_1[1] :
                                H_1[0] = R_2[0] - x
                            elif R_2[1] > H_1[1] :
                                H_1[0] = R_2[0] + x
                            R_2 = H_1
                            W_right_diagonal[2 * l + 1] = R_2
                        W_horizontal[2 * i] = H_1
                        EH[2 * i] = ER[2 * l + 1] = 1
                elif math.dist(H_2, R_1) <= gap :
                    if EH[2 * i + 1] == 1 :
                        R_1 = H_2
                        W_right_diagonal[2 * l] = R_1
                        ER[2 * l] = 1
                    else : 
                        if R_1[1] == H_2[1] :
                            H_2[0] = R_1[0]
                        else : 
                            x = int(abs(R_1[1] - H_2[1]) / (diff_y / diff_x))
                            if R_1[1] < H_2[1] :
                                H_2[0] = R_1[0] - x
                            elif R_1[1] > H_2[1] :
                                H_2[0] = R_1[0] + x
                            R_1 = H_2
                            W_right_diagonal[2 * l] = R_1
                        W_horizontal[2 * i + 1] = H_2
                        EH[2 * i + 1] = ER[2 * l] = 1
                elif math.dist(H_2, R_2) <= gap :
                    if EH[2 * i + 1] == 1 :
                        R_2 = H_2
                        W_right_diagonal[2 * l + 1] = R_2
                        ER[2 * l + 1] = 1
                    else : 
                        if R_2[1] == H_2[1] :
                            H_2[0] = R_2[0]
                        else : 
                            x = int(abs(R_2[1] - H_2[1]) / (diff_y / diff_x))
                            if R_2[1] < H_2[1] :
                                H_2[0] = R_2[0] - x
                            elif R_2[1] > H_2[1] :
                                H_2[0] = R_2[0] + x
                            R_2 = H_2
                            W_right_diagonal[2 * l + 1] = R_2
                        W_horizontal[2 * i + 1] = H_2
                        EH[2 * i + 1] = ER[2 * l + 1] = 1
                else :
                    if R_1[1] < H_1[1] and abs(R_2[1] - H_1[1]) <= gap and R_2[0] > H_1[0] and R_2[0] < H_2[0] :
                        x = int(abs(R_2[1] - H_1[1]) / (diff_y / diff_x))         
                        if R_2[1] < H_1[1] :
                            R_2[1] = H_1[1]
                            R_2[0] -= x
                        elif R_2[1] > H_1[1] :
                            R_2[1] = H_1[1]
                            R_2[0] += x
                        W_right_diagonal[2 * l + 1] = R_2
                        ER[2 * l + 1] = 1
                        if EH[2 * i] == 0 :
                            EH[2 * i] = 2
                    elif R_2[1] > H_1[1] and abs(R_1[1] - H_1[1]) <= gap and R_1[0] > H_1[0] and R_1[0] < H_2[0] :
                        x = int(abs(R_1[1] - H_1[1]) / (diff_y / diff_x))         
                        if R_1[1] < H_1[1] :
                            R_1[1] = H_1[1]
                            R_1[0] -= x
                        elif R_1[1] > H_1[1] :
                            R_1[1] = H_1[1]
                            R_1[0] += x
                        W_right_diagonal[2 * l] = R_1
                        ER[2 * l] = 1
                        if EH[2 * i] == 0 :
                            EH[2 * i] = 2
                    elif R_1[1] < H_1[1] and R_2[1] > H_1[1] :
                        x = int(abs(R_1[1] - H_1[1]) / (diff_y / diff_x)) 
                        if abs(R_1[0] + x - H_1[0]) <= gap :
                            H_1[0] = R_1[0] + x
                            W_horizontal[2 * i] = H_1
                            EH[2 * i] = 1
                            if ER[2 * l] == 0 :
                                ER[2 * l] = 2
                        elif abs(R_1[0] + x - H_2[0]) <= gap :
                            H_2[0] = R_1[0] + x
                            W_horizontal[2 * i + 1] = H_2
                            EH[2 * i + 1] = 1
                            if ER[2 * l] == 0 :
                                ER[2 * l] = 2
            if R_1 == R_2 :
                Extra_R.append(l)
        if len(Extra_R) != 0 :
            Extra_R.sort(reverse = True)
            for e in Extra_R :
                del(W_right_diagonal[2 * e + 1])
                del(W_right_diagonal[2 * e])
                del(ER[2 * e + 1])
                del(ER[2 * e])
        
        if H_1 == H_2 :
            Extra_H.append(i)
    if len(Extra_H) != 0 :
        Extra_H.sort(reverse = True)
        for e in Extra_H :
            del(W_horizontal[2 * e + 1])
            del(W_horizontal[2 * e])
            del(EH[2 * e + 1])
            del(EH[2 * e])
            
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

    Ind_V, Ind_H, Ind_L, Ind_R = [], [], [], []
    for i in range(int(len(EV) / 2)) :
        if EV[2 * i] == EV[2 * i + 1] == 0 :
            Ind_V.append(i)
    Ind_V.sort(reverse = True)
    for i in range(int(len(EH) / 2)) :
        if EH[2 * i] == EH[2 * i + 1] == 0 :
            Ind_H.append(i)
    Ind_H.sort(reverse = True)
    for i in range(int(len(EL) / 2)) :
        if EL[2 * i] == EL[2 * i + 1] == 0 :
            Ind_L.append(i)
    Ind_L.sort(reverse = True)
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
    for e in W_vertical :
        W_room.append([e[0], e[1]])
    for e in W_horizontal :
        W_room.append([e[0], e[1]])
    for e in W_left_diagonal :
        W_room.append([e[0], e[1]])
    for e in W_right_diagonal :
        W_room.append([e[0], e[1]])
        
    return W_room