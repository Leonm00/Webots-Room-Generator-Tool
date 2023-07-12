import math

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
    