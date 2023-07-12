import Check_Input as C

"""_Gets all user inputs required for the webots file_ 
"""

def get_name() :
    """_Gets the name of the webots file _

    Returns:
        n (_str_): _Correspond to the name of the webots file_
    """
    n = input ("Give the name for the webots file : ")
    isOK = False 
    while isOK == False : 
        if len(n) != 0 :
            isOK = True
        else : 
            print("     Empty name - Please retry")
            n = input ("Give the name for the webots file : ")
    return str(n)

def get_wall_height() :
    """_Gets the height of the walls_

    Returns:
        h (_float_): _Corresponds to the height of the walls_
    """
    h = input("Define wall height (in meters). The default value is 2 : ")
    isOK = False
    while isOK == False : 
        if C.check_input(h) == 'int' or C.check_input(h) == 'float' :
            if float(h) == 0 :
                print("     NULL value - Please retry")
                h = input("Define wall height (in meters) : ")
            elif float(h) > 0 :
                isOK = True
            else : 
                print("     Negative value - Please retry")
                h = input("Define wall height (in meters) : ")
        else :
            print("     Not a float - Please retry")
            h = input("Define wall height (in meters) : ")
    return float(h)
         
def get_wall_thickness() :
    """_Gets the thickness of the walls_

    Returns:
        t (_float_): _Corresponds to the thickness of the walls_
    """
    t = input("Define wall thickness (in meters). The default value is 0.02 : ")
    isOK = False
    while isOK == False : 
        if C.check_input(t) == 'int' or C.check_input(t) == 'float' :
            if float(t) == 0 :
                print("     NULL value - Please retry")
                t = input("Define wall thickness (in meters) : ")
            elif float(t) > 0 :
                isOK = True
            else : 
                print("     Negative value - Please retry")
                t = input("Define wall thickness (in meters) : ")
        else :
            print("     Not a float - Please retry")
            t = input("Define wall thickness (in meters) : ")
    return float(t)
        
def get_wall_transparency() : 
    """_Gets the transparency of the walls_

    Returns:
        tr (_float_): _Corresponds to the transparency of the walls_
    """
    tr = input("Define wall transparency (float between 0 and 1 | 1 for a transparent wall). The default value is 0 : ")
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
        
def get_total_length() : 
    """_Gets the total length (in meters) of the figure_

    Returns:
        l (_float_): _Corresponds to the total length of the figure_
    """
    l = input("Define the total length of the figure (in meters), the width will be adjusted accordingly : ")
    isOK = False
    while isOK == False : 
        if C.check_input(l) == 'int' or C.check_input(l) == 'float' :
            if float(l) < 0 :
                print("     Negative value - Please retry")
                l = input("Define the total length of the figure (in meters) : ")
            elif float(l) == 0 :
                print("     NULL value - Please retry")
                l = input("Define the total length of the figure (in meters) : ")
            else :
                isOK = True
        else :
            print("     Not a float - Please retry")
            l = input("Define the total length of the figure (in meters) : ")
    return float(l)

