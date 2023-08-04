import math
import Line_Treatment_Functions as LF

"""_Basic treatment of wall lines_
"""

def line_separation(room, Angle) :
    """_We separate the various walls according to their type_

    Args:
        room (_list_): _Corresponds to the list containing the wall positions_
        Angle (_int_): _The value for the angle parameter_

    Returns:
        W_vertical (_list_): _List containing vertical wall positions_
        W_horizontal (_list_): _List containing horizontal wall positions_
        W_left_diagonal (_list_): _List containing left-diagonal wall positions_
        W_right_diagonal (_list_): _List containing right-diagonal wall positions_
        W_left_angle_diagonal (_list_): _List containing left-diagonal wall angles_
        W_right_angle_diagonal (_type_): _List containing right-diagonal wall angles_
    """
    if Angle is None :
        angle = 20
        room_x = []
        room_y = []
        for e in room :
            room_x.append(e[0])
            room_y.append(e[1])
    else :
        angle = Angle
        
    room_x = []
    room_y = []
    for e in room :
        room_x.append(e[0])
        room_y.append(e[1])

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


"""_Treatment of diagonal lines (Y coordinate increase from top to bottom)_
"""

def left_or_right_diagonal_extension(type, W_type, W_angle_type, gap_length) :
    """_For diagonal lines, we lengthen the lines that are separated by a distance less than gap_length and that are on the same infinite line_

    Args:
        type (_str_): _The type of lines studied_
        W_type (_list_): _The list containing the points of the lines studied_
        W_angle_type (_list_): _The list containing the angles of the lines studied_
        gap_length (_int_): _The threshold value for line extension_

    Returns:
        W_type (_list_): _The list containing the points of the lines studied after treatment_
        W_angle_type (_list_): _The list containing the angles of the lines studied after treatment_
    """
    isFinish = False
    i = 0
    Max = int(len(W_type) / 2)

    # Data is not processed if type does not match
    if type != 'Left_Diagonal' and type != 'Right_Diagonal' :
        isFinish = True 
        
    while isFinish == False :
        Next = False
        W_1 = W_type[2 * i]
        W_2 = W_type[2 * i + 1]
        
        while Next == False :
            Next = True
            isExtension = False 
            # Gets the X and Y step of the current line
            diff_x = int(abs(W_1[0] - W_2[0]))
            diff_y = int(abs(W_2[1] - W_1[1]))
            pgcd = math.gcd(diff_x, diff_y)
            diff_x /= pgcd
            diff_y /= pgcd
            nbr = pgcd + 1
            nbr_gap = gap_length // (int(math.dist(W_1, W_2)) / pgcd)
            nbr_gap = int(nbr_gap)

            for j in range(i + 1, Max) :
                if isExtension == False :
                    # Same angle
                    if W_angle_type[i] == W_angle_type[j] :
                        C_1 = W_type[2 * j]
                        C_2 = W_type[2 * j + 1]
                        if type == 'Left_Diagonal' :
                            for k in range(- nbr_gap, nbr + nbr_gap) :
                                if [W_1[0] + k * diff_x, W_1[1] + k * diff_y] == C_1 or [W_1[0] + k * diff_x, W_1[1] + k * diff_y] == C_2 :
                                    Next = False
                                    isExtension = True
                            if isExtension == True :
                                # We lengthen the current line
                                if C_2[1] > W_2[1] :
                                    W_2 = C_2
                                elif C_1[1] < W_1[1] :
                                    W_1 = C_1
                                Max -= 1
                                del(W_type[2 * j + 1])
                                del(W_type[2 * j])
                                del(W_angle_type[j])  
                        elif type == 'Right_Diagonal' :
                            for k in range(- nbr_gap, nbr + nbr_gap) :
                                if [W_1[0] - k * diff_x, W_1[1] + k * diff_y] == C_1 or [W_1[0] - k * diff_x, W_1[1] + k * diff_y] == C_2 :
                                    Next = False
                                    isExtension = True
                            if isExtension == True :
                                if C_2[1] > W_2[1] :
                                    W_2 = C_2
                                elif C_1[1] < W_1[1] :
                                    W_1 = C_1
                                Max -= 1
                                del(W_type[2 * j + 1])
                                del(W_type[2 * j])
                                del(W_angle_type[j])
        W_type[2 * i] = W_1
        W_type[2 * i + 1] = W_2
        if i == Max - 1 :
            isFinish = True
        else : 
            i += 1
            
    return W_type, W_angle_type

def remove_extra_left_or_right_diagonal(type, W_type, W_angle_type, gap, size_x, size_y) :
    """_For diagonal lines, between parallel lines whose distance does not exceed the gap value, only one line is kept_

    Args:
        type (_str_): _The type of lines studied_
        W_type (_list_): _The list containing the points of the lines studied_
        W_angle_type (_list_): _The list containing the angles of the lines studied_
        gap (_int_): _The threshold value for removing extra lines_
        size_x (_int_): _X-axis image size_
        size_y (_int_): _Y-axis image size_

    Returns:
        W_type (_list_): _The list containing the points of the lines studied after treatment_
    """
    isFinish = False
    i = 0
    Max = int(len(W_type) / 2)

    # Data is not processed if type does not match
    if type != 'Left_Diagonal' and type != 'Right_Diagonal' :
        isFinish = True 
        
    while isFinish == False :
        Next = False
        W_1 = W_type[2 * i]
        W_2 = W_type[2 * i + 1]
        # We store the index of the pairs to be deleted
        Ind = []
        # We retrieve the coordinates of the current line
        Y_min = W_1[1]
        Y_max = W_2[1]
        # Gets the X and Y step of the current line
        diff_x = int(abs(W_1[0] - W_2[0]))
        diff_y = int(abs(W_2[1] - W_1[1]))
        pgcd = math.gcd(diff_x, diff_y)
        diff_x /= pgcd
        diff_y /= pgcd
        nbr = pgcd + 1
        
        while Next == False :
            Next = True
            for j in range(i + 1, Max) :
                if j not in Ind :
                    # If the difference in angle between the two lines does not exceed 5°
                    if abs(W_angle_type[i] - W_angle_type[j]) <= 5 * (math.pi / 180) :
                        C_1 = W_type[2 * j]
                        C_2 = W_type[2 * j + 1]

                        Diff_x = int(abs(C_1[0] - C_2[0]))
                        Diff_y = int(abs(C_2[1] - C_1[1]))
                        Pgcd = math.gcd(Diff_x, Diff_y)
                        Diff_x /= Pgcd
                        Diff_y /= Pgcd
                        Nbr = Pgcd + 1

                        isExtra = False
                        if type == 'Left_Diagonal' :
                            for k in range(nbr) :
                                if isExtra == False :
                                    for l in range(Nbr) :
                                        if math.dist([W_1[0] + k * diff_x, W_1[1] + k * diff_y], [C_1[0] + l * Diff_x, C_1[1] + l * Diff_y]) <= gap or math.dist([W_1[0] + k * diff_x, W_1[1] + k * diff_y], [C_1[0] + l * Diff_x, C_1[1] + l * Diff_y]) <= gap :
                                            Next = False
                                            isExtra = True
                            # If an extra line is found, we look among the two lines with a small X Y step,
                            # keep the small one and lengthen it until reaching the Y_min and Y_max coordinates
                            if isExtra == True : 
                                if Diff_y < diff_y :
                                    diff_x = Diff_x
                                    diff_y = Diff_y
                                    nbr = Nbr
                                    W_1 = C_1
                                    W_2 = C_2
                                Ind.append(j)
                                if abs(C_1[1] - Y_min) > diff_y :
                                    if C_1[1] < Y_min :
                                        Y_min = C_1[1]  
                                    Temp_1 = W_1
                                    cpt = 0
                                    Stop = False
                                    while abs(Y_min - Temp_1[1]) > diff_y and Stop == False :
                                        if (Temp_1[0] - diff_x) >= 0 and (Temp_1[1] - diff_y) >= 0 :
                                            Temp_1[0] -= diff_x
                                            Temp_1[1] -= diff_y
                                            cpt += 1
                                        else : 
                                            Stop = True
                                    W_1 = Temp_1
                                    nbr += cpt
                                if abs(C_2[1] - Y_max) > diff_y :
                                    if C_2[1] > Y_max :
                                        Y_max = C_2[1]
                                    Temp_2 = W_2
                                    cpt = 0 
                                    Stop = False 
                                    while abs(Y_max - Temp_2[1]) > diff_y and Stop == False :
                                        if (Temp_2[0] + diff_x) <= size_x and (Temp_2[1] + diff_y) <= size_y :
                                            Temp_2[0] += diff_x
                                            Temp_2[1] += diff_y
                                            cpt += 1
                                        else : 
                                            Stop = True     
                                    W_2 = Temp_2
                                    nbr += cpt
                        elif type == 'Right_Diagonal' :
                            for k in range(nbr) :
                                if isExtra == False :
                                    for l in range(Nbr) :
                                        if math.dist([W_1[0] - k * diff_x, W_1[1] + k * diff_y], [C_1[0] - l * Diff_x, C_1[1] + l * Diff_y]) <= gap or math.dist([W_1[0] - k * diff_x, W_1[1] + k * diff_y], [C_1[0] - l * Diff_x, C_1[1] + l * Diff_y]) <= gap :
                                            Next = False
                                            isExtra = True
                            if isExtra == True : 
                                if Diff_y < diff_y :
                                    diff_x = Diff_x
                                    diff_y = Diff_y
                                    nbr = Nbr
                                    W_1 = C_1
                                    W_2 = C_2
                                Ind.append(j)
                                if abs(C_1[1] - Y_min) > diff_y :
                                    if C_1[1] < Y_min :
                                        Y_min = C_1[1]  
                                    Temp_1 = W_1
                                    cpt = 0
                                    Stop = False
                                    while abs(Y_min - Temp_1[1]) > diff_y and Stop == False :
                                        if (Temp_1[0] + diff_x) <= size_x and (Temp_1[1] - diff_y) >= 0 :
                                            Temp_1[0] += diff_x
                                            Temp_1[1] -= diff_y
                                            cpt += 1
                                        else : 
                                            Stop = True
                                    W_1 = Temp_1
                                    nbr += cpt
                                if abs(C_2[1] - Y_max) > diff_y :
                                    if C_2[1] > Y_max :
                                        Y_max = C_2[1]
                                    Temp_2 = W_2
                                    cpt = 0 
                                    Stop = False
                                    while abs(Y_max - Temp_2[1]) > diff_y and Stop == False :
                                        if (Temp_2[0] - diff_x) >= 0 and (Temp_2[1] + diff_y) <= size_y :
                                            Temp_2[0] -= diff_x
                                            Temp_2[1] += diff_y
                                            cpt += 1
                                        else : 
                                            Stop = True
                                    W_2 = Temp_2
                                    nbr += cpt
        Ind.sort(reverse = True)
        if len(Ind) > 0 :
            for e in Ind :
                del(W_type[2 * e + 1])
                del(W_type[2 * e])
                del(W_angle_type[e])
                Max -= 1
            W_type[2 * i] = W_1
            W_type[2 * i + 1] = W_2
        if i == Max - 1 :
            isFinish = True
        else : 
            i += 1

    return W_type


"""_Treatment of vertical and horizontal lines_
"""

def vertical_or_horizontal_extension(type, W_type, gap_length) :
    """_For vertical and horizontal lines, we lengthen the lines that are located on the same x or y coordinates (depending on the type) and are separated by a distance less than gap_length_

    Args:
        type (_str_): _The type of lines studied_
        W_type (_list_): _The list containing the points of the lines studied_
        gap_length (_int_): _The threshold value for line extension_

    Returns:
        W_type (_list_): _The list containing the points of the lines studied after treatment_
    """
    isFinish = False
    i = 0
    Max = int(len(W_type) / 2)
    
    # Data is not processed if type does not match
    if type != 'Vertical' and type != 'Horizontal' :
        isFinish = True 
        
    while isFinish == False :
        Next = False
        W_1 = W_type[2 * i]
        W_2 = W_type[2 * i + 1]
        # For each pair of points, we see if it can be lengthened
        # If so, we use the extended pair and look again at the remaining pairs to see if the pair can still be extended
        # If this is no longer the case, we move on to the next pair
        while Next == False :
            Next = True
            isExtension = False 
            # For each pair of points following the current point
            for j in range(i + 1, Max) :
                if isExtension == False :
                    C_1 = W_type[2 * j]
                    C_2 = W_type[2 * j + 1]
                    if type == 'Vertical' :
                        # If these two pairs of points have the same x coordinate
                        if C_1[0] == W_1[0] :
                            # If the gap between these two lines is less than gap_length
                            if abs(C_1[1] - W_2[1]) <= gap_length or abs(C_2[1] - W_1[1]) <= gap_length :
                                # We lengthen the current line
                                if abs(C_1[1] - W_2[1]) <= gap_length :
                                    W_2[1] = C_2[1]
                                elif abs(C_2[1] - W_1[1]) <= gap_length :
                                    W_1[1] = C_1[1]
                                # And we remove the useless pair
                                Max -= 1
                                del(W_type[2 * j + 1])
                                del(W_type[2 * j])
                                Next = False
                                isExtension = True
                    elif type == 'Horizontal' :
                        # If these two pairs of points have the same y coordinate
                        if C_1[1] == W_1[1] :
                            if abs(C_1[0] - W_2[0]) <= gap_length or abs(C_2[0] - W_1[0]) <= gap_length :
                                if abs(C_1[0] - W_2[0]) <= gap_length :
                                    W_2[0] = C_2[0]
                                elif abs(C_2[0] - W_1[0]) <= gap_length :
                                    W_1[0] = C_1[0]
                                Max -= 1
                                del(W_type[2 * j + 1])
                                del(W_type[2 * j])
                                Next = False
                                isExtension = True 
        W_type[2 * i] = W_1
        W_type[2 * i + 1] = W_2
        # We stop if we've analyzed the last pair of points
        if i == Max - 1 :
            isFinish = True
        else : 
            i += 1

    return W_type

def remove_extra_vertical_or_horizontal(type, W_type, gap) :
    """_For vertical and horizontal lines, between parallel lines whose distance does not exceed the gap value, only one line is kept_

    Args:
        type (_str_): _The type of lines studied_
        W_type (_list_): _The list containing the points of the lines studied_
        gap (_int_): _The threshold value for removing extra lines_

    Returns:
        W_type (_list_): _The list containing the points of the lines studied after treatment_
    """
    isFinish = False
    i = 0
    Max = int(len(W_type) / 2)
    
    # Data is not processed if type does not match
    if type != 'Vertical' and type != 'Horizontal' :
        isFinish = True 
        
    while isFinish == False :
        W_1 = W_type[2 * i]
        W_2 = W_type[2 * i + 1]
        # We retrieve the coordinates of the current pair
        if type == 'Vertical' :
            X_min = X_max = W_1[0]
            Y_min = W_1[1]
            Y_max = W_2[1]
        elif type == 'Horizontal' :
            Y_min = Y_max = W_1[1]
            X_min = W_1[0]
            X_max = W_2[0]
        # We store the index of the pairs to be deleted
        Ind = []
        Next = False
        while Next == False : 
            Next = True
            if type == 'Vertical' :
                # For each pair of points following the current point
                for j in range(i + 1, Max) :
                    if j not in Ind :
                        C_1 = W_type[2 * j]
                        C_2 = W_type[2 * j + 1]
                        # If the line is at a distance less than gap from the current pair of points and those stored in the Ind list
                        if abs(C_1[0] - X_min) <= gap or abs(C_1[0] - X_max) <= gap or (C_1[0] > X_min and C_1[0] < X_max) :
                            # We'll see if we can also extend the line
                            if (C_1[1] < W_1[1] and C_2[1] > W_2[1]) or (abs(C_1[1] - W_2[1]) <= gap) or (abs(C_2[1] - W_1[1]) <= gap) or (C_1[1] >= Y_min and C_1[1] <= Y_max) or (C_2[1] >= Y_min and C_2[1] <= Y_max) :
                                Ind.append(j)
                                Next = False
                                if C_1[0] < X_min :
                                    X_min = C_1[0]
                                elif C_1[0] > X_max :
                                    X_max = C_1[0]
                                if C_1[1] < Y_min :
                                    Y_min = C_1[1]
                                if C_2[1] > Y_max :
                                    Y_max = C_2[1]
            elif type == 'Horizontal' :
                for j in range(i + 1, Max) :
                    if j not in Ind :
                        C_1 = W_type[2 * j]
                        C_2 = W_type[2 * j + 1]
                        if abs(C_1[1] - Y_min) <= gap or abs(C_1[1] - Y_max) <= gap or (C_1[1] > Y_min and C_1[1] < Y_max) :
                            if (C_1[0] < W_1[0] and C_2[0] > W_2[0]) or (abs(C_1[0] - W_2[0]) <= gap) or (abs(C_2[0] - W_1[0]) <= gap) or (C_1[0] >= X_min and C_1[0] <= X_max) or (C_2[0] >= X_min and C_2[0] <= X_max) :
                                Ind.append(j)
                                Next = False
                                if C_1[1] < Y_min :
                                    Y_min = C_1[1]
                                elif C_1[1] > Y_max :
                                    Y_max = C_1[1]
                                if C_1[0] < X_min :
                                    X_min = C_1[0]
                                if C_2[0] > X_max :
                                    X_max = C_2[0]
        # The indices are sorted in descending order
        Ind.sort(reverse = True)
        for e in Ind :
            del(W_type[2 * e + 1])
            del(W_type[2 * e])
            Max -= 1
        # We take the center of the lines
        if type == 'Vertical' :
            W_1[0] = W_2[0] = int((X_min + X_max) / 2)  
            W_1[1] = Y_min
            W_2[1] = Y_max       
        elif type == 'Horizontal' :
            W_1[1] = W_2[1] = int((Y_min + Y_max) / 2)  
            W_1[0] = X_min
            W_2[0] = X_max  
                 
        W_type[2 * i] = W_1
        W_type[2 * i + 1] = W_2
        if i == Max - 1 :
            isFinish = True
        else : 
            i += 1
    
    return W_type


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

