import Check_Input as C

"""_Gets all user inputs required for the Set Functions file_ 
"""

def get_1_Or_2_Choice(Explanation, Choice1, Choice2) :
    """_We choose a choice among 2 choices offered_

    Args:
        Explanation (_str_): _Explanation for the choice_
        Choice1 (_str_): _First choice_
        Choice2 (_str_): _Second choice_

    Returns:
        c (_int_): _Correspond to the selected choice_
    """
    print(str(Explanation) + " : ")
    print(" 1 - " + str(Choice1) + " ")
    print(" 2 - " + str(Choice2) + " ")
    c = input("Choice (int) : ")
    isOK = False 
    while isOK == False : 
        if C.check_input(c) == 'int' :
            if int(c) == 1 or int(c) == 2 :
                isOK = True
            else :  
                print("     Not an expected int - Please choose between 1 and 2")
                c = input("Choice (int) : ")
        else :
            print("     Not an int - Please choose between 1 and 2")
            c = input("Choice (int) : ")
    return int(c)


def get_Positive_Int_Choice(Explanation) :
    """_To choose a strictly positive integer_

    Args:
        Explanation (_str_): _Explanation for the choice_

    Returns:
        c (_int_): _Correspond to the selected int value_
    """
    c = input(str(Explanation) + " : ")
    isOk = False
    while isOk == False : 
        while C.check_input(c) != 'int' :
            print("     Not an int - Please retry")
            c = input(str(Explanation) + " : ")
        if int(c) < 0 :
            print("     Negative value - Please retry")
            c = input(str(Explanation) + " : ")
        elif int(c) == 0 :
            print("     NULL value - Please retry")
            c = input(str(Explanation) + " : ")
        else : 
            isOk = True
    return int(c)


def get_Min_Max_Wall() :
    """_We choose the range of value for the number of walls_

    Returns:
        w_min (_int_): _Minimum number of walls_
        w_max (_int_): _Maximum number of walls_
        
    """
    w_min = get_Positive_Int_Choice("Minimum number of walls")
    
    w_max = input("Maximum number of walls : ")
    isOk = False
    while isOk == False : 
        while C.check_input(w_max) != 'int' :
            print("     Not an int - Please retry")
            w_max = input("Maximum number of walls : ")
        if int(w_max) < int(w_min) :
            print("     Value Less than the minimum number of walls - Please retry")
            w_max = input("Maximum number of walls : ")
        elif int(w_max) == int(w_min) :
            print("     Value Identical to the minimum number of walls - Please retry")
            w_max = input("Maximum number of walls : ")
        else : 
            isOk = True
    return int(w_min), int(w_max)


def get_1_2_Or_3_Choice(Explanation, Choice1, Choice2, Choice3) :
    """_We choose a choice among 3 choices offered_

    Args:
        Explanation (_str_): _Explanation for the choice_
        Choice1 (_str_): _First choice_
        Choice2 (_str_): _Second choice_
        Choice3 (_str_): _Third choice_

    Returns:
        c (_int_): _Correspond to the selected choice_
    """
    print(str(Explanation) + " : ")
    print(" 1 - " + str(Choice1) + " ")
    print(" 2 - " + str(Choice2) + " ")
    print(" 3 - " + str(Choice3) + " ")
    c = input("Choice (int) : ")
    isOK = False 
    while isOK == False : 
        if C.check_input(c) == 'int' :
            if int(c) >= 1 and int(c) <= 3 :
                isOK = True
            else :  
                print("     Not an expected int - Please choose between 1 and 3")
                c = input("Choice (int) : ")
        else :
            print("     Not an int - Please choose between 1 and 3")
            c = input("Choice (int) : ")
    return int(c)


def get_Yes_No_Choice(Explanation) :
    """_We choose between Yes or No_

    Args:
        Explanation (_str_): _Explanation for the choice_
    Returns:
        choice (_str_): _Correspond to the selected choice_
    """
    print(str(Explanation) + " ")
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
    return choice


def get_Positive_Float_Choice(Explanation) : 
    """_To choose a strictly positive float_

    Args:
        Explanation (_str_): _Explanation for the choice_

    Returns:
        c (_float_): _Correspond to the selected float value_
    """
    c = input(str(Explanation) + " : ")
    isOK = False
    while isOK == False : 
        if C.check_input(c) == 'int' or C.check_input(c) == 'float' :
            if float(c) < 0 :
                print("     Negative value - Please retry")
                c = input(str(Explanation) + " : ")
            elif float(c) == 0 :
                print("     NULL value - Please retry")
                c = input(str(Explanation) + " : ")
            else :
                isOK = True
        else :
            print("     Not a float - Please retry")
            c = input(str(Explanation) + " : ")
    return float(c)


def get_Grid_Size() :
    """_We get the size x y of the grid_

    Returns:
        w (_int_): _Number of cells on the x-axis_
        h (_int_): _Number of cells on the y-axis_
    """
    print("Keep in mind that too few cells will result in few different worlds.")
    w = input("Number of cells on the x-axis : ")
    isOk = False
    while isOk == False : 
        while C.check_input(w) != 'int' :
            print("     Not an int - Please retry")
            w = input("Number of cells on the x-axis : ")
        if int(w) < 0 :
            print("     Negative value - Please retry")
            w = input("Number of cells on the x-axis : ")
        elif int(w) == 0 :
            print("     NULL value - Please retry")
            w = input("Number of cells on the x-axis : ")
        elif int(w) < 3 :
            print("     Value too Low - Please retry")
            w = input("Number of cells on the x-axis : ")
        else : 
            isOk = True
    h = input("Number of cells on the y-axis : ")
    isOk = False
    while isOk == False : 
        while C.check_input(h) != 'int' :
            print("     Not an int - Please retry")
            h = input("Number of cells on the y-axis : ")
        if int(h) < 0 :
            print("     Negative value - Please retry")
            h = input("Number of cells on the y-axis : ")
        elif int(h) == 0 :
            print("     NULL value - Please retry")
            h = input("Number of cells on the y-axis : ")
        elif int(h) < 3 :
            print("     Value too Low - Please retry")
            h = input("Number of cells on the y-axis : ")
        else : 
            isOk = True
    return int(w), int(h)


def get_Min_Max_Length() :
    """_We choose the range of value for the total length of the figure_

    Returns:
        l_min (_float_): _Minimum length_
        l_max (_float_): _Maximum length_
        l_step (_float_): _Variation step between the value range_
    """
    l_min = get_Positive_Float_Choice("Minimum length (in meters)")

    l_max = input("Maximum length (in meters) : ")
    isOK = False
    while isOK == False : 
        if C.check_input(l_max) == 'int' or C.check_input(l_max) == 'float' :
            if float(l_max) < float(l_min) :
                print("     Value Less than the minimum length - Please retry")
                l_max = input("Maximum length (in meters) : ")
            elif float(l_max) == float(l_min) :
                print("     Value Identical than the minimum length - Please retry")
                l_max = input("Maximum length (in meters) : ")
            else : 
                isOK = True
        else :
            print("     Not a float - Please retry")
            l_max = input("Maximum length (in meters) : ")
    l_step = input("Step variation for the length (in meters) : ")
    isOK = False
    while isOK == False : 
        if C.check_input(l_step) == 'int' or C.check_input(l_step) == 'float' :
            if float(l_step) < 0 :
                print("     Negative value - Please retry")
                l_step = input("Step variation for the length (in meters) : ")
            elif float(l_step) == 0 : 
                print("     NULL value - Please retry")
                l_step = input("Step variation for the length (in meters) : ")
            else : 
                if C.check_input(float(float(l_max) - float(l_min)) / float(l_step)) == 'int' : 
                    isOK = True
                else : 
                    print("     The value is not a multiple of the difference between the two lengths - Please retry")
                    l_step = input("Step variation for the length (in meters) : ")
        else :
            print("     Not a float - Please retry")
            l_step = input("Step variation for the length (in meters) : ")
    return float(l_min), float(l_max), float(l_step)


def get_Min_Max_Wall_Height() :
    """_We choose the range of value for the height of the walls_

    Returns:
        h_min (_float_): _Minimum height_
        h_max (_float_): _Maximum height_
        h_step (_float_): _Variation step between the value range_
    """
    h_min = get_Positive_Float_Choice("Minimum height (in meters)")

    h_max = input("Maximum height (in meters) : ")
    isOK = False
    while isOK == False : 
        if C.check_input(h_max) == 'int' or C.check_input(h_max) == 'float' :
            if float(h_max) < float(h_min) :
                print("     Value Less than the minimum height - Please retry")
                h_max = input("Maximum height (in meters) : ")
            elif float(h_max) == float(h_min) :
                print("     Value Identical than the minimum height - Please retry")
                h_max = input("Maximum height (in meters) : ")
            else : 
                isOK = True
        else :
            print("     Not a float - Please retry")
            h_max = input("Maximum height (in meters) : ")
    h_step = input("Step variation for the height (in meters) : ")
    isOK = False
    while isOK == False : 
        if C.check_input(h_step) == 'int' or C.check_input(h_step) == 'float' :
            if float(h_step) < 0 :
                print("     Negative value - Please retry")
                h_step = input("Step variation for the height (in meters) : ")
            elif float(h_step) == 0 : 
                print("     NULL value - Please retry")
                h_step = input("Step variation for the height (in meters) : ")
            else : 
                if C.check_input(float(float(h_max) - float(h_min)) / float(h_step)) == 'int' : 
                    isOK = True
                else : 
                    print("     The value is not a multiple of the difference between the two heights - Please retry")
                    h_step = input("Step variation for the height (in meters) : ")
        else :
            print("     Not a float - Please retry")
            h_step = input("Step variation for the height (in meters) : ")
    return float(h_min), float(h_max), float(h_step)


def get_Min_Max_Wall_Thickness() :
    """_We choose the range of value for the thickness of the walls_

    Returns:
        t_min (_float_): _Minimum thickness_
        t_max (_float_): _Maximum thickness_
        t_step (_float_): _Variation step between the value range_
    """
    t_min = get_Positive_Float_Choice("Minimum thickness (in meters)")

    t_max = input("Maximum thickness (in meters) : ")
    isOK = False
    while isOK == False : 
        if C.check_input(t_max) == 'int' or C.check_input(t_max) == 'float' :
            if float(t_max) < float(t_min) :
                print("     Value Less than the minimum thickness - Please retry")
                t_max = input("Maximum thickness (in meters) : ")
            elif float(t_max) == float(t_min) :
                print("     Value Identical than the minimum thickness - Please retry")
                t_max = input("Maximum thickness (in meters) : ")
            else : 
                isOK = True
        else :
            print("     Not a float - Please retry")
            t_max = input("Maximum thickness (in meters) : ")
    t_step = input("Step variation for the thickness (in meters) : ")
    isOK = False
    while isOK == False : 
        if C.check_input(t_step) == 'int' or C.check_input(t_step) == 'float' :
            if float(t_step) < 0 :
                print("     Negative value - Please retry")
                t_step = input("Step variation for the thickness (in meters) : ")
            elif float(t_step) == 0 : 
                print("     NULL value - Please retry")
                t_step = input("Step variation for the thickness (in meters) : ")
            else : 
                if C.check_input(float(float(t_max) - float(t_min)) / float(t_step)) == 'int' : 
                    isOK = True
                else : 
                    print("     The value is not a multiple of the difference between the two thickness - Please retry")
                    t_step = input("Step variation for the thickness (in meters) : ")
        else :
            print("     Not a float - Please retry")
            t_step = input("Step variation for the thickness (in meters) : ")
    return float(t_min), float(t_max), float(t_step)


def get_Constant_Wall_Transparency() : 
    """_Gets the transparency of the walls_

    Returns:
        tr (_float_): _Corresponds to the transparency of the walls_
    """
    tr = input("Define wall transparency (float between 0 and 1 | 1 for a transparent wall) : ")
    isOK = False 
    while isOK == False : 
        if C.check_input(tr) == 'int' or C.check_input(tr) == 'float' :
            if float(tr) < 0 : 
                print("     Negative value - Please retry")
                tr = input("Define wall transparency (float between 0 and 1 | 1 for a transparent wall) : ")
            elif float(tr) >= 0 and float(tr) <= 1 :
                isOK = True
            else :  
                print("     Value too High - Please retry")
                tr = input("Define wall transparency (float between 0 and 1 | 1 for a transparent wall) : ")
        else :
            print("     Not a float - Please retry")
            tr = input("Define wall transparency (float between 0 and 1 | 1 for a transparent wall) : ")
    return float(tr)


def get_Min_Max_Wall_Transparency() :
    """_We choose the range of value for the transparency of the walls_

    Returns:
        tr_min (_float_): _Minimum transparency_
        tr_max (_float_): _Maximum transparency_
        tr_step (_float_): _Variation step between the value range_
    """
    tr_min = input("Minimum transparency (float between 0 and 1) : ")
    isOK = False
    while isOK == False : 
        if C.check_input(tr_min) == 'int' or C.check_input(tr_min) == 'float' :
            if float(tr_min) < 0 : 
                print("     Negative value - Please retry")
                tr_min = input("Minimum transparency (float between 0 and 1) : ")
            elif float(tr_min) >= 0 and float(tr_min) < 1 :
                isOK = True
            else :  
                print("     Value too High - Please retry")
                tr_min = input("Minimum transparency (float between 0 and 1) : ")
        else :
            print("     Not a float - Please retry")
            tr_min = input("Minimum transparency (float between 0 and 1) : ")
    tr_max = input("Maximum transparency (float between 0 and 1) : ")
    isOK = False
    while isOK == False : 
        if C.check_input(tr_max) == 'int' or C.check_input(tr_max) == 'float' :
            if float(tr_max) < float(tr_min) :
                print("     Value Less than the minimum transarency - Please retry")
                tr_max = input("Maximum transparency (float between 0 and 1) : ")
            elif float(tr_max) == float(tr_min) :
                print("     Value Identical than the minimum transparency - Please retry")
                tr_max = input("Maximum transparency (float between 0 and 1) : ")
            elif float(tr_max) > 1 :
                print("     Value too High - Please retry")
                tr_max = input("Maximum transparency (float between 0 and 1) : ")
            else : 
                isOK = True
        else :
            print("     Not a float - Please retry")
            tr_max = input("Maximum transparency (float between 0 and 1) : ")
    tr_step = input("Step variation for the transparency (float between 0 and 1) : ")
    isOK = False
    while isOK == False : 
        if C.check_input(tr_step) == 'int' or C.check_input(tr_step) == 'float' :
            if float(tr_step) < 0 :
                print("     Negative value - Please retry")
                tr_step = input("Step variation for the transparency (float between 0 and 1) : ")
            elif float(tr_step) == 0 : 
                print("     NULL value - Please retry")
                tr_step = input("Step variation for the transparency (float between 0 and 1) : ")
            else : 
                if C.check_input(float(float(tr_max) - float(tr_min)) / float(tr_step)) == 'int' : 
                    isOK = True
                else : 
                    print("     The value is not a multiple of the difference between the two transparencies - Please retry")
                    tr_step = input("Step variation for the transparency (float between 0 and 1) : ")
        else :
            print("     Not a float - Please retry")
            tr_step = input("Step variation for the transparency (float between 0 and 1) : ")
    return float(tr_min), float(tr_max), float(tr_step)


def get_4_Directions() :
    """_We choose the direction of the first wall_

    Returns:
        c (_int_): _Correspond to the selected choice_
    """
    print("Choose the direction of the first wall : ")
    print(" 1 - Up ")
    print(" 2 - Right ")
    print(" 3 - Down ")
    print(" 4 - Left ")
    c = input("Choice (int) : ")
    isOK = False 
    while isOK == False : 
        if C.check_input(c) == 'int' :
            if int(c) >= 1 and int(c) <= 4 :
                isOK = True
            else :  
                print("     Not an expected int - Please choose between 1 and 4")
                c = input("Choice (int) : ")
        else :
            print("     Not an int - Please choose between 1 and 4")
            c = input("Choice (int) : ")
    return int(c)
    
    
def get_8_Directions() :
    """_We choose the direction of the first wall_

    Returns:
        c (_int_): _Correspond to the selected choice_
    """
    print("Choose the direction of the first wall : ")
    print(" 1 - Up ")
    print(" 2 - Right ")
    print(" 3 - Down ")
    print(" 4 - Left ")
    print(" 5 - Up-Left ")
    print(" 6 - Up-Right ")
    print(" 7 - Down-Left ")
    print(" 8 - Down-Right ")
    c = input("Choice (int) : ")
    isOK = False 
    while isOK == False : 
        if C.check_input(c) == 'int' :
            if int(c) >= 1 and int(c) <= 8 :
                isOK = True
            else :  
                print("     Not an expected int - Please choose between 1 and 8")
                c = input("Choice (int) : ")
        else :
            print("     Not an int - Please choose between 1 and 8")
            c = input("Choice (int) : ")
    return int(c)


def get_Proba_Directions() :
    """_We choose the probability that the next wall will be in the same direction that the last wall_

    Returns:
        c (_int_): _Correspond to the selected probability_
    """
    print("Knowing that the last wall is in a certain direction, what's the probability that the next wall will also be in that direction ?")
    p = input("Probabiliy (int between 1 and 99) : ")
    isOK = False 
    while isOK == False : 
        if C.check_input(p) == 'int' :
            if int(p) > 0 and int(p) < 100:
                isOK = True
            else :
                print("     Not an expected int - Please retry")
                p = input("Probabiliy (int between 1 and 99) : ")
        else : 
            print("     Not an int - Please retry")
            p = input("Probabiliy (int between 1 and 99) : ")
    return float(p)
 