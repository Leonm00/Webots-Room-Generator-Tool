import math

"""_Functions for Basic treatment of wall lines_
"""

def Fill_V_and_H(i, W_vertical, EV, W_horizontal, EH, gap) :
    """_Compare a vertical line with all the horizontal lines and fill in the gaps if they are close together_

    Args:
        i (_int_): _Index of the vertical to be compared_
        W_vertical (_list_): _List containing vertical wall positions_
        EV (_list_): _To find out whether or not a point on a vertical has already been modified_
        W_horizontal (_list_): _List containing horizontal wall positions_
        EH (_list_): _To find out whether or not a point on a horizontal has already been modified_
        gap (_int_): _The threshold value_

    Returns:
        W_vertical (_list_): _List containing vertical wall positions_
        EV (_list_): _To find out whether or not a point on a vertical has already been modified_
        W_horizontal (_list_): _List containing horizontal wall positions_
        EH (_list_): _To find out whether or not a point on a horizontal has already been modified_
    """
    V_1 = W_vertical[2 * i]
    V_2 = W_vertical[2 * i + 1]
    EV_1 = EV[2 * i]
    EV_2 = EV[2 * i + 1]
    Extra_H = []
    for j in range(int(len(W_horizontal) / 2)) : 
        H_1 = W_horizontal[2 * j]
        H_2 = W_horizontal[2 * j + 1]
        EH_1 = EH[2 * j]
        EH_2 = EH[2 * j + 1]
        # If there's already a connection between the vertical and the horizontal
        if V_1 == H_1 :
            EV_1 = 1
            EH_1 = 1
        elif V_1 == H_2 :
            EV_1 = 1
            EH_2 = 1
        elif V_2 == H_1 :
            EV_2 = 1
            EH_1 = 1
        elif V_2 == H_2 :
            EV_2 = 1
            EH_2 = 1
        else :
            # We look to see if there are two points close together
            if math.dist(V_1, H_1) <= gap and math.dist(V_1, H_1) < math.dist(V_1, H_2) :
                V_1[1] = H_1[1]
                H_1[0] = V_1[0]
                EV_1 = 1
                EH_1 = 1
            elif math.dist(V_1, H_2) <= gap :
                V_1[1] = H_2[1]
                H_2[0] = V_1[0]
                EV_1 = 1
                EH_2 = 1
            elif math.dist(V_2, H_1) <= gap and math.dist(V_2, H_1) < math.dist(V_2, H_2) :
                V_2[1] = H_1[1]
                H_1[0] = V_2[0]
                EV_2 = 1
                EH_1 = 1
            elif math.dist(V_2, H_2) <= gap :
                V_2[1] = H_2[1]
                H_2[0] = V_2[0]
                EV_2 = 1
                EH_2 = 1
            # If not, we'll see if we can lengthen or narrow the vertical wall to fit the horizontal line, or vice versa
            else :
                # If the horizontal is above or below the vertical
                if H_1[0] < V_1[0] and H_2[0] > V_1[0] :
                    # Up and close
                    if H_1[1] != V_1[1] and abs(H_1[1] - V_1[1]) <= gap :
                        V_1[1] = H_1[1]
                        EV_1 = 1
                        # To ensure that the horizontal is not considered as an isolated wall
                        if EH_1 == 0 :
                            EH_1 = 2
                    # Down and close
                    elif H_1[1] != V_2[1] and abs(H_1[1] - V_2[1]) <= gap :
                        V_2[1] = H_1[1]
                        EV_2 = 1
                        if EH_1 == 0 :
                            EH_1 = 2
                # If the horizontal is to the left or right of the vertical
                if V_1[1] < H_1[1] and V_2[1] > H_1[1] :
                    # Right and close
                    if V_1[0] != H_1[0] and abs(V_1[0] - H_1[0]) <= gap :
                        H_1[0] = V_1[0]
                        EH_1 = 1
                        if EV_1 == 0 :
                            EV_1 = 2
                    # Left and close
                    elif V_1[0] != H_2[0] and abs(V_1[0] - H_2[0]) <= gap :
                        H_2[0] = V_1[0]
                        EH_2 = 1
                        if EV_1 == 0 :
                            EV_1 = 2
                # If the two lines cross
                if H_1[0] < V_1[0] and H_2[0] > V_1[0] and V_1[1] < H_1[1] and V_2[1] > H_1[1] :
                    EV_1 = 2
                    EH_1 = 2
        W_horizontal[2 * j] = H_1
        W_horizontal[2 * j + 1] = H_2
        EH[2 * j] = EH_1
        EH[2 * j + 1] = EH_2
        if H_1 == H_2 :
            Extra_H.append(j)
    if len(Extra_H) != 0 :
        Extra_H.sort(reverse = True)
        for e in Extra_H :
            del(W_horizontal[2 * e + 1])
            del(W_horizontal[2 * e])
            del(EH[2 * e + 1])
            del(EH[2 * e])
    W_vertical[2 * i] = V_1
    W_vertical[2 * i + 1] = V_2
    EV[2 * i] = EV_1
    EV[2 * i + 1] = EV_2
            
    return W_vertical, EV, W_horizontal, EH

def Fill_VH_and_Diagonal(i, VH_Choice, W_vertical, EV, Nbr_VH, W_horizontal, EH, Diagonal_Choice, W_diagonal, ELR, gap) : 
    """_Compare a vertical line or a horizontal line with diagonals and fill in the gaps if they are close together_

    Args:
        i (_int_): _Index of the vertical or horizontal to be compared_
        VH_Choice (_str_): _To find out whether the line to be compared is vertical or horizontal_
        W_vertical (_list_): _List containing vertical wall positions_
        EV (_list_): _To find out whether or not a point on a vertical has already been modified_
        Nbr_VH (_int_): _Number of vertical or horizontal lines according to choice_
        W_horizontal (_list_): _List containing horizontal wall positions_
        EH (_list_): _To find out whether or not a point on a horizontal has already been modified_
        Diagonal_Choice (_str_): _Choosing the type of diagonal to compare_
        W_diagonal (_list_): _List containing diagonal wall positions_
        ELR (_list_): _To find out whether or not a point on a diagonal has already been modified_
        gap (_int_): _The threshold value_

    Returns:
        W_vertical (_list_): _List containing vertical wall positions_
        EV (_list_): _To find out whether or not a point on a vertical has already been modified_
        Nbr_VH (_int_): _Number of vertical or horizontal lines according to choice_
        W_horizontal (_list_): _List containing horizontal wall positions_
        EH (_list_): _To find out whether or not a point on a horizontal has already been modified_
        W_diagonal (_list_): _List containing diagonal wall positions_
        ELR (_list_): _To find out whether or not a point on a diagonal has already been modified_
    """
    if VH_Choice == 'Vertical' :
        VH_1 = W_vertical[2 * i]
        VH_2 = W_vertical[2 * i + 1]
        EVH_1 = EV[2 * i]
        EVH_2 = EV[2 * i + 1]
    else :
        VH_1 = W_horizontal[2 * i]
        VH_2 = W_horizontal[2 * i + 1]
        EVH_1 = EH[2 * i]
        EVH_2 = EH[2 * i + 1]

    Extra_LR = []
    Add_V = []
    Add_H = []
    for k in range(int(len(W_diagonal) / 2)) : 
        LR_1 = W_diagonal[2 * k]
        LR_2 = W_diagonal[2 * k + 1]
        ELR_1 = ELR[2 * k]
        ELR_2 = ELR[2 * k + 1]
        # If there's already a connection between the vertical and the left diagonal
        if VH_1 == LR_1 :
            EVH_1 = 1
            ELR_1 = 1
        elif VH_1 == LR_2 :
            EVH_1 = 1
            ELR_2 = 1
        elif VH_2 == LR_1 :
            EVH_2 = 1
            ELR_1 = 1
        elif VH_2 == LR_2 :
            EVH_2 = 1
            ELR_2 = 1
        else :
            # Gets the X and Y step of the current left diagonal
            diff_x = int(abs(LR_1[0] - LR_2[0]))
            diff_y = int(abs(LR_2[1] - LR_1[1]))
            pgcd = math.gcd(diff_x, diff_y)
            diff_x /= pgcd
            diff_y /= pgcd
    
            # We look to see if there are two points close together
            if math.dist(VH_1, LR_1) <= gap :
                # If the near vertical point has already been modified
                if EVH_1 == 1 :
                    LR_1 = VH_1
                    ELR_1 = 1
                # Else, both diagonal and vertical can be lengthened/shortened
                else : 
                    if VH_Choice == 'Vertical' :
                        # Same x between the two nearby points. We just lengthen the vertical
                        if LR_1[0] == VH_1[0] :
                            VH_1[1] = LR_1[1]
                        # Otherwise, extend the diagonal to the correct y position and then extend the vertical to the same point.
                        else : 
                            y = int(abs(LR_1[0] - VH_1[0]) / (diff_x / diff_y))
                            if Diagonal_Choice == 'Left_Diagonal' :
                                if LR_1[0] < VH_1[0] :
                                    VH_1[1] = LR_1[1] + y
                                elif LR_1[0] > VH_1[0] :
                                    VH_1[1] = LR_1[1] - y
                            # Right_Diagonal
                            else : 
                                if LR_1[0] < VH_1[0] :
                                    VH_1[1] = LR_1[1] - y
                                elif LR_1[0] > VH_1[0] :
                                    VH_1[1] = LR_1[1] + y
                            LR_1 = VH_1 
                    # Horizontal
                    else : 
                        if LR_1[1] == VH_1[1] :
                            VH_1[0] = LR_1[0]
                        else : 
                            x = int(abs(LR_1[1] - VH_1[1]) / (diff_y / diff_x))
                            if Diagonal_Choice == 'Left_Diagonal' :
                                if LR_1[1] < VH_1[1] :
                                    VH_1[0] = LR_1[0] + x
                                elif LR_1[1] > VH_1[1] :
                                    VH_1[0] = LR_1[0] - x
                            # Right_Diagonal
                            else :
                                if LR_1[1] < VH_1[1] :
                                    VH_1[0] = LR_1[0] - x
                                elif LR_1[1] > VH_1[1] :
                                    VH_1[0] = LR_1[0] + x
                            LR_1 = VH_1
                    EVH_1 = 1
                    ELR_1 = 1  
            elif math.dist(VH_1, LR_2) <= gap :
                if EVH_1 == 1 :
                    LR_2 = VH_1
                    ELR_2 = 1
                else : 
                    if VH_Choice == 'Vertical' :
                        if LR_2[0] == VH_1[0] :
                            VH_1[1] = LR_2[1]
                        else : 
                            y = int(abs(LR_2[0] - VH_1[0]) / (diff_x / diff_y))
                            if Diagonal_Choice == 'Left_Diagonal' :
                                if LR_2[0] < VH_1[0] :
                                    VH_1[1] = LR_2[1] + y
                                elif LR_2[0] > VH_1[0] :
                                    VH_1[1] = LR_2[1] - y
                            else : 
                                if LR_2[0] < VH_1[0] :
                                    VH_1[1] = LR_2[1] - y
                                elif LR_2[0] > VH_1[0] :
                                    VH_1[1] = LR_2[1] + y
                            LR_2 = VH_1
                    else : 
                        if LR_2[1] == VH_1[1] :
                            VH_1[0] = LR_2[0]
                        else : 
                            x = int(abs(LR_2[1] - VH_1[1]) / (diff_y / diff_x))
                            if Diagonal_Choice == 'Left_Diagonal' :
                                if LR_2[1] < VH_1[1] :
                                    VH_1[0] = LR_2[0] + x
                                elif LR_2[1] > VH_1[1] :
                                    VH_1[0] = LR_2[0] - x
                            else :
                                if LR_2[1] < VH_1[1] :
                                    VH_1[0] = LR_2[0] - x
                                elif LR_2[1] > VH_1[1] :
                                    VH_1[0] = LR_2[0] + x
                            LR_2 = VH_1
                    EVH_1 = 1
                    ELR_2 = 1
            elif math.dist(VH_2, LR_1) <= gap :
                if EVH_2 == 1 :
                    LR_1 = VH_2
                    ELR_1 = 1
                else : 
                    if VH_Choice == 'Vertical' :
                        if LR_1[0] == VH_2[0] :
                            VH_2[1] = LR_1[1]
                        else : 
                            y = int(abs(LR_1[0] - VH_2[0]) / (diff_x / diff_y))
                            if Diagonal_Choice == 'Left_Diagonal' :
                                if LR_1[0] < VH_2[0] :
                                    VH_2[1] = LR_1[1] + y
                                elif LR_1[0] > VH_2[0] :
                                    VH_2[1] = LR_1[1] - y
                            else : 
                                if LR_1[0] < VH_2[0] :
                                    VH_2[1] = LR_1[1] - y
                                elif LR_1[0] > VH_2[0] :
                                    VH_2[1] = LR_1[1] + y
                            LR_1 = VH_2
                    else : 
                        if LR_1[1] == VH_2[1] :
                            VH_2[0] = LR_1[0]
                        else : 
                            x = int(abs(LR_1[1] - VH_2[1]) / (diff_y / diff_x))
                            if Diagonal_Choice == 'Left_Diagonal' :
                                if LR_1[1] < VH_2[1] :
                                    VH_2[0] = LR_1[0] + x
                                elif LR_1[1] > VH_2[1] :
                                    VH_2[0] = LR_1[0] - x
                            else :
                                if LR_1[1] < VH_2[1] :
                                    VH_2[0] = LR_1[0] - x
                                elif LR_1[1] > VH_2[1] :
                                    VH_2[0] = LR_1[0] + x
                            LR_1 = VH_2
                    EVH_2 = 1
                    ELR_1 = 1
            elif math.dist(VH_2, LR_2) <= gap :
                if EVH_2 == 1 :
                    LR_2 = VH_2
                    ELR_2 = 1
                else : 
                    if VH_Choice == 'Vertical' :
                        if LR_2[0] == VH_2[0] :
                            VH_2[1] = LR_2[1]
                        else : 
                            y = int(abs(LR_2[0] - VH_2[0]) / (diff_x / diff_y))
                            if Diagonal_Choice == 'Left_Diagonal' :
                                if LR_2[0] < VH_2[0] :
                                    VH_2[1] = LR_2[1] + y
                                elif LR_2[0] > VH_2[0] :
                                    VH_2[1] = LR_2[1] - y
                            else : 
                                if LR_2[0] < VH_2[0] :
                                    VH_2[1] = LR_2[1] - y
                                elif LR_2[0] > VH_2[0] :
                                    VH_2[1] = LR_2[1] + y
                            LR_2 = VH_2
                    else :
                        if LR_2[1] == VH_2[1] :
                            VH_2[0] = LR_2[0]
                        else : 
                            x = int(abs(LR_2[1] - VH_2[1]) / (diff_y / diff_x))
                            if Diagonal_Choice == 'Left_Diagonal' :
                                if LR_2[1] < VH_2[1] :
                                    VH_2[0] = LR_2[0] + x
                                elif LR_2[1] > VH_2[1] :
                                    VH_2[0] = LR_2[0] - x
                            else :
                                if LR_2[1] < VH_2[1] :
                                    VH_2[0] = LR_2[0] - x
                                elif LR_2[1] > VH_2[1] :
                                    VH_2[0] = LR_2[0] + x
                            LR_2 = VH_2
                    EVH_2 = 1
                    ELR_2 = 1
            # If there's no close point, we see if we can lengthen or narrow the vertical wall or the left diagonal wall so that they touch
            else :
                if VH_Choice == 'Vertical' :
                    if Diagonal_Choice == 'Left_Diagonal' :
                        # Diagonal to the left of vertical and close 
                        if LR_1[0] < VH_1[0] and abs(LR_2[0] - VH_1[0]) <= gap and LR_2[1] > VH_1[1] and LR_2[1] < VH_2[1] :
                            y = int(abs(LR_2[0] - VH_1[0]) / (diff_x / diff_y))         
                            if LR_2[0] < VH_1[0] :
                                LR_2[0] = VH_1[0]
                                LR_2[1] += y
                            elif LR_2[0] > VH_1[0] :
                                LR_2[0] = VH_1[0]
                                LR_2[1] -= y
                            ELR_2 = 1
                            if EVH_1 == 0 :
                                EVH_1 = 2
                        # Diagonal to the right of vertical and close
                        elif LR_2[0] > VH_1[0] and abs(LR_1[0] - VH_1[0]) <= gap and LR_1[1] > VH_1[1] and LR_1[1] < VH_2[1] :
                            y = int(abs(LR_1[0] - VH_1[0]) / (diff_x / diff_y))         
                            if LR_1[0] < VH_1[0] :
                                LR_1[0] = VH_1[0]
                                LR_1[1] += y
                            elif LR_1[0] > VH_1[0] :
                                LR_1[0] = VH_1[0]
                                LR_1[1] -= y
                            ELR_1 = 1
                            if EVH_1 == 0 :
                                EVH_1 = 2
                        # Diagonal at the top of the vertical or at the bottom
                        elif LR_1[0] < VH_1[0] and LR_2[0] > VH_1[0] :
                            y = int(abs(LR_1[0] - VH_1[0]) / (diff_x / diff_y)) 
                            # Top and close
                            if abs(LR_1[1] + y - VH_1[1]) <= gap :
                                VH_1[1] = LR_1[1] + y
                                EVH_1 = 1
                                if ELR_1 == 0 :
                                    ELR_1 = 2
                            # Bottom and close
                            elif abs(LR_1[1] + y - VH_2[1]) <= gap :
                                VH_2[1] = LR_1[1] + y
                                EVH_2 = 1
                                if ELR_1 == 0 :
                                    ELR_1 = 2
                    # Right_Diagonal
                    else : 
                        # Diagonal to the left of vertical and close
                        if LR_2[0] < VH_1[0] and abs(LR_1[0] - VH_1[0]) <= gap and LR_1[1] > VH_1[1] and LR_1[1] < VH_2[1] :
                            y = int(abs(LR_1[0] - VH_1[0]) / (diff_x / diff_y))         
                            if LR_1[0] < VH_1[0] :
                                LR_1[0] = VH_1[0]
                                LR_1[1] -= y
                            elif LR_1[0] > VH_1[0] :
                                LR_1[0] = VH_1[0]
                                LR_1[1] += y
                            ELR_1 = 1
                            if EVH_1 == 0 :
                                EVH_1 = 2
                        # Diagonal to the right of vertical and close 
                        elif LR_1[0] > VH_1[0] and abs(LR_2[0] - VH_1[0]) <= gap and LR_2[1] > VH_1[1] and LR_2[1] < VH_2[1] :
                            y = int(abs(LR_2[0] - VH_1[0]) / (diff_x / diff_y))         
                            if LR_2[0] < VH_1[0] :
                                LR_2[0] = VH_1[0]
                                LR_2[1] -= y
                            elif LR_2[0] > VH_1[0] :
                                LR_2[0] = VH_1[0]
                                LR_2[1] += y
                            ELR_2 = 1
                            if EVH_1 == 0 :
                                EVH_1 = 2
                        # Diagonal at the top of the vertical or at the bottom
                        elif LR_2[0] < VH_1[0] and LR_1[0] > VH_1[0] :
                            y = int(abs(LR_1[0] - VH_1[0]) / (diff_x / diff_y)) 
                            # Top and close
                            if abs(LR_1[1] + y - VH_1[1]) <= gap :
                                VH_1[1] = LR_1[1] + y
                                EVH_1 = 1
                                if ELR_1 == 0 :
                                    ELR_1 = 2
                            # Bottom and close
                            elif abs(LR_1[1] + y - VH_2[1]) <= gap :
                                VH_2[1] = LR_1[1] + y
                                EVH_2 = 1
                                if ELR_1 == 0 :
                                    ELR_1 = 2
                # Horizontal
                else :
                    if Diagonal_Choice == 'Left_Diagonal' :
                        # Diagonal at the top of the horizontal and close 
                        if LR_1[1] < VH_1[1] and abs(LR_2[1] - VH_1[1]) <= gap and LR_2[0] > VH_1[0] and LR_2[0] < VH_2[0] :
                            x = int(abs(LR_2[1] - VH_1[1]) / (diff_y / diff_x))         
                            if LR_2[1] < VH_1[1] :
                                LR_2[1] = VH_1[1]
                                LR_2[0] += x
                            elif LR_2[1] > VH_1[1] :
                                LR_2[1] = VH_1[1]
                                LR_2[0] -= x
                            ELR_2 = 1
                            if EVH_1 == 0 :
                                EVH_1 = 2
                        # Diagonal at the bottom of the horizontal and close
                        elif LR_2[1] > VH_1[1] and abs(LR_1[1] - VH_1[1]) <= gap and LR_1[0] > VH_1[0] and LR_1[0] < VH_2[0] :
                            x = int(abs(LR_1[1] - VH_1[1]) / (diff_y / diff_x))         
                            if LR_1[1] < VH_1[1] :
                                LR_1[1] = VH_1[1]
                                LR_1[0] += x
                            elif LR_1[1] > VH_1[1] :
                                LR_1[1] = VH_1[1]
                                LR_1[0] -= x
                            ELR_1 = 1
                            if EVH_1 == 0 :
                                EVH_1 = 2
                        # Diagonal to the left or right of horizontal
                        elif LR_1[1] < VH_1[1] and LR_2[1] > VH_1[1] :
                            x = int(abs(LR_1[1] - VH_1[1]) / (diff_y / diff_x)) 
                            # Left and close
                            if abs(LR_1[0] + x - VH_1[0]) <= gap :
                                VH_1[0] = LR_1[0] + x
                                EVH_1 = 1
                                if ELR_1 == 0 :
                                    ELR_1 = 2
                            # Right and close
                            elif abs(LR_1[0] + x - VH_2[0]) <= gap :
                                VH_2[0] = LR_1[0] + x
                                EVH_2 = 1
                                if ELR_1 == 0 :
                                    ELR_1 = 2
                    # Right_Diagonal
                    else :
                        if LR_1[1] < VH_1[1] and abs(LR_2[1] - VH_1[1]) <= gap and LR_2[0] > VH_1[0] and LR_2[0] < VH_2[0] :
                            x = int(abs(LR_2[1] - VH_1[1]) / (diff_y / diff_x))         
                            if LR_2[1] < VH_1[1] :
                                LR_2[1] = VH_1[1]
                                LR_2[0] -= x
                            elif LR_2[1] > VH_1[1] :
                                LR_2[1] = VH_1[1]
                                LR_2[0] += x
                            ELR_2 = 1
                            if EVH_1 == 0 :
                                EVH_1 = 2
                        elif LR_2[1] > VH_1[1] and abs(LR_1[1] - VH_1[1]) <= gap and LR_1[0] > VH_1[0] and LR_1[0] < VH_2[0] :
                            x = int(abs(LR_1[1] - VH_1[1]) / (diff_y / diff_x))         
                            if LR_1[1] < VH_1[1] :
                                LR_1[1] = VH_1[1]
                                LR_1[0] -= x
                            elif LR_1[1] > VH_1[1] :
                                LR_1[1] = VH_1[1]
                                LR_1[0] += x
                            ELR_1 = 1
                            if EVH_1 == 0 :
                                EVH_1 = 2
                        elif LR_1[1] < VH_1[1] and LR_2[1] > VH_1[1] :
                            x = int(abs(LR_1[1] - VH_1[1]) / (diff_y / diff_x)) 
                            if abs(LR_1[0] + x - VH_1[0]) <= gap :
                                VH_1[0] = LR_1[0] + x
                                EVH_1 = 1
                                if ELR_1 == 0 :
                                    ELR_1 = 2
                            elif abs(LR_1[0] + x - VH_2[0]) <= gap :
                                VH_2[0] = LR_1[0] + x
                                EVH_2 = 1
                                if ELR_1 == 0 :
                                    ELR_1 = 2
                        
        W_diagonal[2 * k] = LR_1
        W_diagonal[2 * k + 1] = LR_2
        ELR[2 * k] = ELR_1
        ELR[2 * k + 1] = ELR_2
        if LR_1 == LR_2 :
            Extra_LR.append(k)
        elif LR_1[0] == LR_2[0] :
            Add_V.append(k)
        elif LR_1[1] == LR_2[1] : 
            Add_H.append(k)
            
    Extra_Add = []
    for z in Extra_LR :
        Extra_Add.append(z)
    for z in Add_V :
        Extra_Add.append(z)
    for z in Add_H : 
        Extra_Add.append(z)
    if len(Extra_Add) != 0 :
        Extra_Add.sort(reverse = True)
        for e in Extra_Add :
            if e in Extra_LR :
                del(W_diagonal[2 * e + 1])
                del(W_diagonal[2 * e])
                del(ELR[2 * e + 1])
                del(ELR[2 * e])
            elif e in Add_V :
                W_vertical.append(W_diagonal[2 * e])
                W_vertical.append(W_diagonal[2 * e + 1])
                EV.append(1)
                EV.append(1)
                del(W_diagonal[2 * e + 1])
                del(W_diagonal[2 * e])
                del(ELR[2 * e + 1])
                del(ELR[2 * e])
                if VH_Choice == 'Vertical' :
                    Nbr_VH += 1
            elif e in Add_H :
                if Diagonal_Choice == 'Left_Diagonal' :
                    W_horizontal.append(W_diagonal[2 * e])
                    W_horizontal.append(W_diagonal[2 * e + 1])
                else : 
                    W_horizontal.append(W_diagonal[2 * e + 1])
                    W_horizontal.append(W_diagonal[2 * e])
                EH.append(1)
                EH.append(1)
                del(W_diagonal[2 * e + 1])
                del(W_diagonal[2 * e])
                del(ELR[2 * e + 1])
                del(ELR[2 * e])
                if VH_Choice == 'Horizontal' : 
                    Nbr_VH += 1
                
    if VH_Choice == 'Vertical' :
        W_vertical[2 * i] = VH_1
        W_vertical[2 * i + 1] = VH_2
        EV[2 * i] = EVH_1
        EV[2 * i + 1] = EVH_2
    else :
        W_horizontal[2 * i] = VH_1
        W_horizontal[2 * i + 1] = VH_2
        EH[2 * i] = EVH_1
        EH[2 * i + 1] = EVH_2
    
    return W_vertical, EV, Nbr_VH, W_horizontal, EH, W_diagonal, ELR
  
def erase_extra_and_bug(W_vertical, EV, W_horizontal, EH, W_left_diagonal, EL, W_right_diagonal, ER) :
    """_To delete all problematic lines_

    Args:
        W_vertical (_list_): _List containing vertical wall positions_
        EV (_list_): _To find out whether or not a point on a vertical has already been modified_
        W_horizontal (_list_): _List containing horizontal wall positions_
        EH (_list_): _To find out whether or not a point on a horizontal has already been modified_
        W_left_diagonal (_list_): _List containing left diagonal wall positions_
        EL (_list_): _To find out whether or not a point on a left diagonal has already been modified_
        W_right_diagonal (_list_): _List containing right diagonal wall positions_
        ER (_list_): _To find out whether or not a point on a right diagonal has already been modified_

    Returns:
        W_vertical (_list_): _List containing vertical wall positions_
        EV (_list_): _To find out whether or not a point on a vertical has already been modified_
        W_horizontal (_list_): _List containing horizontal wall positions_
        EH (_list_): _To find out whether or not a point on a horizontal has already been modified_
        W_left_diagonal (_list_): _List containing left diagonal wall positions_
        EL (_list_): _To find out whether or not a point on a left diagonal has already been modified_
        W_right_diagonal (_list_): _List containing right diagonal wall positions_
        ER (_list_): _To find out whether or not a point on a right diagonal has already been modified_
    """
    Extra_V = []
    for i in range(int(len(W_vertical) / 2)) : 
        V_1 = W_vertical[2 * i]
        V_2 = W_vertical[2 * i + 1]
        if V_1 == V_2 or V_1[0] != V_2[0] :
            Extra_V.append(i)
    if len(Extra_V) != 0 :
        Extra_V.sort(reverse = True)
        for e in Extra_V :
            del(W_vertical[2 * e + 1])
            del(W_vertical[2 * e])
            del(EV[2 * e + 1])
            del(EV[2 * e])
    
    Extra_H = []
    for i in range(int(len(W_horizontal) / 2)) :
        H_1 = W_horizontal[2 * i]
        H_2 = W_horizontal[2 * i + 1]
        if H_1 == H_2 or H_1[1] != H_2[1] : 
            Extra_H.append(i)
    if len(Extra_H) != 0 :
        Extra_H.sort(reverse = True)
        for e in Extra_H :
            del(W_horizontal[2 * e + 1])
            del(W_horizontal[2 * e])
            del(EH[2 * e + 1])
            del(EH[2 * e])    
                
    Extra_L = []
    for i in range(int(len(W_left_diagonal) / 2)) :
        L_1 = W_left_diagonal[2 * i]
        L_2 = W_left_diagonal[2 * i + 1]
        if L_1[0] == L_2[0] or L_1[1] == L_2[1] : 
            Extra_L.append(i)
    if len(Extra_L) != 0 :
        Extra_L.sort(reverse = True)
        for e in Extra_L :
            del(W_left_diagonal[2 * e + 1])
            del(W_left_diagonal[2 * e])
            del(EL[2 * e + 1])
            del(EL[2 * e]) 
            
    Extra_R = []
    for i in range(int(len(W_right_diagonal) / 2)) :
        R_1 = W_right_diagonal[2 * i]
        R_2 = W_right_diagonal[2 * i + 1]
        if R_1[0] == R_2[0] or R_1[1] == R_2[1] : 
            Extra_R.append(i)
    if len(Extra_R) != 0 :
        Extra_R.sort(reverse = True)
        for e in Extra_R :
            del(W_right_diagonal[2 * e + 1])
            del(W_right_diagonal[2 * e])
            del(ER[2 * e + 1])
            del(ER[2 * e])   
    
    return W_vertical, EV, W_horizontal, EH, W_left_diagonal, EL, W_right_diagonal, ER
