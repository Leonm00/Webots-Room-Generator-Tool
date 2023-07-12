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