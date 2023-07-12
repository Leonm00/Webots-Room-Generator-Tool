import Check_Input as C

"""_Gets all user inputs required for the graphical part of the manual mode_ 
"""

def get_cells_width() :
    """_Gets the number of cells on the x-axis_

    Returns:
        w (_int_): _Corresponds to the number of cells on the x-axis_
    """
    print("Keep in mind that too many cells will result in a grid with very small cells.")
    w = input("Number of cells on the x-axis (int between 2 and 100) : ")
    isOk = False
    while isOk == False : 
        while C.check_input(w) != 'int' :
            print("     Not an int - Please retry")
            w = input("Number of cells on the x-axis (int between 2 and 100) : ")
        if int(w) < 0 :
            print("     Negative value - Please retry")
            w = input("Number of cells on the x-axis (int between 2 and 100) : ")
        elif int(w) == 0 :
            print("     NULL value - Please retry")
            w = input("Number of cells on the x-axis (int between 2 and 100) : ")
        elif int(w) < 2 :
            print("     Value too Low - Please retry")
            w = input("Number of cells on the x-axis (int between 2 and 100) : ")
        elif int(w) > 100 :
            print("     Value too High - Please retry")
            w = input("Number of cells on the x-axis (int between 2 and 100) : ")
        else : 
            isOk = True
    return int(w)

def get_cells_height() :
    """_Gets the number of cells on the y-axis_

    Returns:
        h (_int_): _Corresponds to the number of cells on the y-axis_
    """
    print("Keep in mind that too many cells will result in a grid with very small cells.")
    h = input("Number of cells on the y-axis (int between 2 and 100) : ")
    isOk = False
    while isOk == False : 
        while C.check_input(h) != 'int' :
            print("     Not an int - Please retry")
            h = input("Number of cells on the y-axis (int between 2 and 100) : ")
        if int(h) < 0 :
            print("     Negative value - Please retry")
            h = input("Number of cells on the y-axis (int between 2 and 100) : ")
        elif int(h) == 0 :
            print("     NULL value - Please retry")
            h = input("Number of cells on the y-axis (int between 2 and 100) : ")
        elif int(h) < 2 :
            print("     Value too Low - Please retry")
            h = input("Number of cells on the y-axis (int between 2 and 100) : ")
        elif int(h) > 100 :
            print("     Value too High - Please retry")
            h = input("Number of cells on the y-axis (int between 2 and 100) : ")
        else : 
            isOk = True
    return int(h)

def get_mode() :
    """_Gets the manual mode option_

    Returns:
        m (_int_): _Corresponds to the choice for the manual mode option_
    """
    print("Please choose the manual mode option you want to use :")
    print(" 1 - Room Creation : closed figure (First Point = Last Point)")
    print(" 2 - Free : each pair of points forms a wall")
    m = input("Mode (int) : ")
    isOK = False 
    while isOK == False : 
        if C.check_input(m) == 'int' :
            if int(m) == 1 or int(m) == 2 :
                isOK = True
            else :  
                print("     Not an expected int - Please choose between 1 and 2")
                m = input("Mode (int) : ")
        else :
            print("     Not an int - Please choose between 1 and 2")
            m = input("Mode (int) : ")
    return int(m)