import Check_Input as C
import cv2
import numpy as np 
import OpenCV_Input as OI
import Webots_Input as WI
import Graphic_Interface_Input as GI

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

def get_Config_Choice() :
    """_Gets choice between using the Webots Tools and modifying the Default Configuration_

    Returns:
        c (_int_): _Correspond to the selected choice_
    """
    print("Welcome to this Webots Room Generator Tool. What do you want to do ? ")
    print(" 1 - Use the Webots Tool ")
    print(" 2 - Change the Default Configuration ")
    print(" 3 - View the Default Configuration before making a choice ")
    c = input("Choice (int) : ")
    isOK = False 
    isView = True
    isError = False
    while isOK == False : 
        if C.check_input(c) == 'int' :
            if int(c) == 1 or int(c) == 2 :
                isOK = True
                if int(c) == 1 and isError == True :
                    c = 4
            elif int(c) == 3 and isView == True :
                isView = False
                isError = get_default_configuration()
                
                print("What do you want to do ? ")
                print(" 1 - Use the Webots Tool ")
                print(" 2 - Change the Default Configuration ")
                c = input("Choice (int) : ")
            else :  
                if isView == True :
                    print("     Not an expected int - Please choose between 1 and 3")
                else :
                    print("     Not an expected int - Please choose between 1 and 2")
                c = input("Choice (int) : ")
        else :
            if isView == True : 
                print("     Not an int - Please choose between 1 and 3")
            else :
                print("     Not an int - Please choose between 1 and 2")
            c = input("Choice (int) : ")
    return int(c)

def get_Default_Choice() :
    """_Gets choice between using the Default Configuration or not_

    Returns:
        c (_str_): _Correspond to the selected choice_
    """
    print("Do you want to use the Default Configuration ? ")
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

def get_default_configuration() :
    """_Displays the current Default Configuration_

    Returns:
        isError (_bool_): _Finds out if there's a problem in the default configuration file_
    """
    config = np.loadtxt("default_configuration.txt")
    isError = False
    if len(config) == 11 and C.check_input(config[0]) == C.check_input(config[1]) == C.check_input(config[2]) == C.check_input(config[3]) == C.check_input(config[4]) == C.check_input(config[5]) == C.check_input(config[6]) == C.check_input(config[7]) == 'int' and (C.check_input(config[8]) == 'float' or C.check_input(config[8]) == 'int') and (C.check_input(config[9]) == 'float' or C.check_input(config[9]) == 'int') and (C.check_input(config[10]) == 'float' or C.check_input(config[10]) == 'int') :
        if int(config[0]) >= 2 and int(config[0]) <= 100 and int(config[1]) >= 2 and int(config[1]) <= 100 and int(config[2]) >= 0 and int(config[2]) <= 255 and int(config[3]) > 0 and int(config[4]) > 0 and int(config[5]) >= 0 and int(config[5]) <= 45 and int(config[6]) > 0 and int(config[7]) > 0 and float(config[8]) > 0 and float(config[9]) > 0 and float(config[10]) >= 0 and float(config[10]) <= 1 :
            print("The default configuration is : ")
            print("## Manual Mode ##")
            print(" Number of cells on the x-axis (int between 2 and 100) : ", int(config[0]))
            print(" Number of cells on the y-axis (int between 2 and 100) : ", int(config[1]))
            print("")
            print("## Image Processing ##")
            print(" Threshold for the binary image (int between 0 and 255) : ", int(config[2]))
            print(" Minimum number of points that can form a line (int) : ", int(config[3]))
            print(" Maximum gap between two points to be considered in the same line (int) : ", int(config[4]))
            print(" Angle for pseudo-vertical and pseudo-horizontal (int between 0 and 45) : ", int(config[5]))
            print(" Maximum gap between two lines to be considered in the same line (int) : ", int(config[6]))
            print(" Maximum gap between two parellel lines to be considered as the same line (int) : ", int(config[7]))
            print("")
            print("## Wall Parameters ##")
            print(" Wall height (in meters) : ", float(config[8]))
            print(" Wall thickness (in meters) : ", float(config[9]))
            print(" Wall transparency (float between 0 and 1) : ", float(config[10]))
        else : 
            print("ERROR - There is a problem with the Default Configuration text file")
            isError = True
    else :
        print("ERROR - There is a problem with the Default Configuration text file")
        isError = True
    return isError
    
def new_default_configuration() :
    """_Changes the current Default Configuration_
    """
    config = np.loadtxt("default_configuration.txt")
    with open("default_configuration.txt", "w") as f :
        f.write("# Default configuration for the Webots Tool" + "\n")
        f.write("\n")
        f.write("# Manual Mode" + "\n")
        
        if len(config) >= 1 :
            if C.check_input(config[0]) == 'int' :
                if int(config[0]) >= 2 and int(config[0]) <= 100 :
                    print("Last default value 1/11 : ", int(config[0]))
                else : 
                    print("Last default value 1/11 - Not an expected int : ", int(config[0]))
            else : 
                print("Last default value 1/11 - Not an int : ", config[0])
        else : 
            print("Last default value 1/11 : NONE")
        w = GI.get_cells_width()
        f.write(str(w) + " # Number of cells on the x-axis (int between 2 and 100)" + "\n")
        
        if len(config) >= 2 :
            if C.check_input(config[1]) == 'int' :
                if int(config[1]) >= 2 and int(config[1]) <= 100 :
                    print("Last default value 2/11 : ", int(config[1]))
                else : 
                    print("Last default value 2/11 - Not an expected int : ", int(config[1]))
            else : 
                print("Last default value 2/11 - Not an int : ", config[1])
        else : 
            print("Last default value 2/11 : NONE")
        h = GI.get_cells_height()
        f.write(str(h) + " # Number of cells on the y-axis (int between 2 and 100)" + "\n")
        
        f.write("\n")
        f.write("# Image Processing" + "\n")
        
        if len(config) >= 3 :
            if C.check_input(config[2]) == 'int' :
                if int(config[2]) >= 0 and int(config[2]) <= 255 :
                    print("Last default value 3/11 : ", int(config[2]))
                else : 
                    print("Last default value 3/11 - Not an expected int : ", int(config[2]))
            else : 
                print("Last default value 3/11 - Not an int : ", config[2])
        else : 
            print("Last default value 3/11 : NONE")
        t = OI.get_Threshold()
        f.write(str(t) + " # Threshold for the binary image (int between 0 and 255)" + "\n")

        if len(config) >= 4 :
            if C.check_input(config[3]) == 'int' :
                if int(config[3]) >= 1 :
                    print("Last default value 4/11 : ", int(config[3]))
                else : 
                    print("Last default value 4/11 - Not an expected int : ", int(config[3]))
            else : 
                print("Last default value 4/11 - Not an int : ", config[3])
        else : 
            print("Last default value 4/11 : NONE")
        l = OI.get_minLineLength()
        f.write(str(l) + " # Minimum number of points that can form a line (int)" + "\n")

        if len(config) >= 5 :
            if C.check_input(config[4]) == 'int' :
                if int(config[4]) >= 1 :
                    print("Last default value 5/11 : ", int(config[4]))
                else : 
                    print("Last default value 5/11 - Not an expected int : ", int(config[4]))
            else : 
                print("Last default value 5/11 - Not an int : ", config[4])
        else : 
            print("Last default value 5/11 : NONE")
        g = OI.get_maxLineGap()
        f.write(str(g) + " # Maximum gap between two points to be considered in the same line (int)" + "\n")

        if len(config) >= 6 :
            if C.check_input(config[5]) == 'int' :
                if int(config[5]) >= 0 and int(config[5]) <= 45 :
                    print("Last default value 6/11 : ", int(config[5]))
                else : 
                    print("Last default value 6/11 - Not an expected int : ", int(config[5]))
            else : 
                print("Last default value 6/11 - Not an int : ", config[5])
        else : 
            print("Last default value 6/11 : NONE")
        a = OI.get_angle()
        f.write(str(a) + " # Angle for pseudo-vertical and pseudo-horizontal" + "\n")
        
        if len(config) >= 7 :
            if C.check_input(config[6]) == 'int' :
                if int(config[6]) > 0 :
                    print("Last default value 7/11 : ", int(config[6]))
                else : 
                    print("Last default value 7/11 - Not an expected int : ", int(config[6]))
            else : 
                print("Last default value 7/11 - Not an int : ", config[6])
        else : 
            print("Last default value 7/11 : NONE")
        gl = OI.get_gap_length()
        f.write(str(gl) + " # Maximum gap between two lines to be considered in the same line (int)" + "\n")
        
        if len(config) >= 8 :
            if C.check_input(config[7]) == 'int' :
                if int(config[7]) > 0 :
                    print("Last default value 8/11 : ", int(config[7]))
                else : 
                    print("Last default value 8/11 - Not an expected int : ", int(config[7]))
            else : 
                print("Last default value 8/11 - Not an int : ", config[7])
        else : 
            print("Last default value 8/11 : NONE")
        g = OI.get_gap()
        f.write(str(g) + " # Maximum gap between two parellel lines to be considered as the same line (int)" + "\n")
        
        f.write("\n")
        f.write("# Wall Parameters" + "\n")
        
        if len(config) >= 9 :
            if C.check_input(config[8]) == 'int' or C.check_input(config[8]) == 'float' :
                if float(config[8]) > 0 :
                    print("Last default value 9/11 : ", float(config[8]))
                else : 
                    print("Last default value 9/11 - Not an expected float : ", float(config[8]))
            else : 
                print("Last default value 9/11 - Not a float : ", config[8])
        else : 
            print("Last default value 9/11 : NONE")
        h = WI.get_wall_height()
        f.write(str(h) + " # Wall height (in meters)" + "\n")
       
        if len(config) >= 10 :
            if C.check_input(config[9]) == 'int' or C.check_input(config[9]) == 'float' :
                if float(config[9]) > 0 :
                    print("Last default value 10/11 : ", float(config[9]))
                else : 
                    print("Last default value 10/11 - Not an expected float : ", float(config[9]))
            else : 
                print("Last default value 10/11 - Not a float : ", config[9])
        else : 
            print("Last default value 10/11 : NONE")
        t = WI.get_wall_thickness()
        f.write(str(t) + " # Wall thickness (in meters)" + "\n")
        
        if len(config) >= 11 :
            if C.check_input(config[10]) == 'int' or C.check_input(config[10]) == 'float' :
                if float(config[10]) >= 0 and float(config[10]) <= 1 :
                    print("Last default value 11/11 : ", float(config[10]))
                else : 
                    print("Last default value 11/11 - Not an expected float : ", float(config[10]))
            else : 
                print("Last default value 11/11 - Not a float : ", config[10])
        else : 
            print("Last default value 11/11 : NONE")
        tr = WI.get_wall_transparency()
        f.write(str(tr) + " # Wall transparency (float between 0 and 1)" + "\n")

def get_Delete_Choice() :
    """_Gets choice of line deletion_

    Returns:
        choice (_str_): _Correspond to the selected choice_
    """
    print("Do you want to delete some lines ? ")
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

def get_Size_Choice() :
    """_Gets choice for determining the total length of the figure_

    Returns:
        s (_int_): _Correspond to the selected choice_
    """
    print("Please choose the option you want for the size of the final figure : ")
    print(" 1 - Define the total length of the figure ")
    print(" 2 - Define the length of a line ")
    s = input("Choice (int) : ")
    isOK = False 
    while isOK == False : 
        if C.check_input(s) == 'int' :
            if int(s) == 1 or int(s) == 2 :
                isOK = True
            else :  
                print("     Not an expected int - Please choose between 1 and 2")
                s = input("Choice (int) : ")
        else :
            print("     Not an int - Please choose between 1 and 2")
            s = input("Choice (int) : ")
    return int(s)
    
def get_size_one_length() :
    """_Gets the length (in meters) of the horizontal line_

    Returns:
        l (_float_): _Corresponds to the length of the selected line_
    """
    l = input("Define the length of the selected line (in meters), the width will be adjusted accordingly : ")
    isOK = False
    while isOK == False : 
        if C.check_input(l) == 'int' or C.check_input(l) == 'float' :
            if float(l) < 0 :
                print("     Negative value - Please retry")
                l = input("Define the length of the selected line (in meters) : ")
            elif float(l) == 0 :
                print("     NULL value - Please retry")
                l = input("Define the length of the selected line (in meters) : ")
            else :
                isOK = True
        else :
            print("     Not a float - Please retry")
            l = input("Define the length of the horizontal line (in meters) : ")
    return float(l)
