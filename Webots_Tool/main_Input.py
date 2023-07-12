import Check_Input as C
import cv2

"""_Gets all user inputs required for the main file_ 
"""

def get_Choice() :
    """_Gets choice of Webots Room Generator Tool mode_

    Returns:
        c (_int_): _Correspond to the choice mode_
    """
    print("Please choose the feature you want to use for this Webots Room Generator Tool : ")
    print(" 1 - Manual ")
    print(" 2 - With an image (does not work well for complex plans) ")
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

def get_name() :
    """_Gets the image file name_

    Returns:
        n (_str_): _Corresponds to the name of the selected image_
    """
    n = input ("Give the image name (don't forget the file format) : ")
    isOK = False 
    while isOK == False : 
        if len(n) != 0 :
            try : 
                with open("images/" + n): isOK = True
            except IOError:
                print("     Image file name does not exist - Please retry")
                n = input ("Give the image name (don't forget the file format) : ")
        else : 
            print("     Empty name - Please retry")
            n = input ("Give the image name (don't forget the file format) : ")
    return str(n)

def get_min_max(W_room) : 
    """_Gets minimum and maximum (x y) coordinates_

    Args:
        W_room (_list_): _List containing all points corresponding to the walls_

    Returns:
        min_x (_int_): _The smallest x among all x coordinates in the W_room list_
        max_x (_int_): _The largest x among all x coordinates in the W_room list_
        min_y (_int_): _The smallest y among all y coordinates in the W_room list_
        max_y (_int_): _The largest y among all y coordinates in the W_room list_
    """
    min_x = 10000
    min_y = 10000
    max_x = 0
    max_y = 0
    for e in W_room : 
        if e[0] < min_x :
            min_x = e[0]
        if e[0] > max_x : 
            max_x = e[0]
        if e[1] < min_y :
            min_y = e[1]
        if e[1] > max_y :
            max_y = e[1]
    return min_x, min_y, max_x, max_y