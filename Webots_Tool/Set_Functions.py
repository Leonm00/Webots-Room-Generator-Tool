import Set_Input as SI
import numpy as np 
import random 
import Check_Input as C 
import Webots_File as F 
import main_Input as MI
import Basic_Line_Treatment as BT
import Vertical_Horizontal_Treatment as VH
import Diagonal_Treatment as D
import os
import cv2

def Next_Point(x, y, direction) :
    """_We return the next point_

    Args:
        x (_int_): _x coordinate of the point_
        y (_int_): _y coordinate of the point_
        direction (_str_): _next direction of the point_

    Returns:
        x (_int_): _x coordinate of the point_
        y (_int_): _y coordinate of the point_
    """
    if direction == 'Up' :
        y -= 1
    elif direction == 'Right' :
        x += 1
    elif direction == 'Down' :
        y += 1
    elif direction == 'Left' :
        x -= 1
    elif direction == 'Up-Left' :
        x -= 1
        y -= 1
    elif direction == 'Up-Right' :
        x += 1
        y -= 1
    elif direction == 'Down-Left' :
        x -= 1
        y += 1
    elif direction == 'Down-Right' :
        x += 1
        y += 1
    return x, y

def Generate_Random_Set() :
    """_Generates a random set of webots worlds_
    """
    WallChoice = SI.get_1_Or_2_Choice("About the number of walls", "A constant number of walls", 
                                    "A number of walls between a range of values")
    if WallChoice == 1 :
        Nbr_Wall = SI.get_Positive_Int_Choice("Number of walls")
    else : 
        Min_Wall, Max_Wall = SI.get_Min_Max_Wall()
        
    WhatShape = SI.get_1_2_Or_3_Choice("About the figure", "A closed figure", "An open figure", "Random")
    if WhatShape == 1 or WhatShape == 2 :
        Shape = WhatShape 
        
    isCrossing = SI.get_Yes_No_Choice("Do you allow walls that cross each other ?")
    
    isDiagonal = SI.get_Yes_No_Choice("Do you allow diagonal movements (45° angle only) ?")
    if isDiagonal == 'N' or isDiagonal == 'n' :
        All_Dir = ['Up', 'Right', 'Down', 'Left']
        # If we go up and want to change direction, we don't go down because otherwise we'll turn around
        All_Dir0 = ['Right', 'Left']
        # If we go right and want to change direction, we don't go left because otherwise we'll turn around
        All_Dir1 = ['Up', 'Down']
    else : 
        All_Dir = ['Up', 'Right', 'Down', 'Left', 'Up-Left', 'Up-Right', 'Down-Left', 'Down-Right']
        All_Dir0 = ['Right', 'Left', 'Up-Left', 'Up-Right', 'Down-Left', 'Down-Right']
        All_Dir1 = ['Up', 'Down', 'Up-Left', 'Up-Right', 'Down-Left', 'Down-Right']
        All_Dir4 = ['Up', 'Right', 'Down', 'Left', 'Up-Right', 'Down-Left']
        All_Dir5 = ['Up', 'Right', 'Down', 'Left', 'Up-Left', 'Down-Right']
        
    StartChoice = SI.get_1_Or_2_Choice("About the direction of the first wall", "Not random", "Random")
    if StartChoice == 1 : 
        if isDiagonal == 'N' or isDiagonal == 'n' :
            Start_Direction = SI.get_4_Directions()
        else :
            Start_Direction = SI.get_8_Directions()
        Start_Dir = All_Dir[Start_Direction - 1]
        
    Proba_D = SI.get_Proba_Directions()

    Grid_J, Grid_I = SI.get_Grid_Size()
    
    LengthChoice = SI.get_1_2_Or_3_Choice("About the length of the figure", "A constant length", 
                                        "A length between a range of values", "Random")
    if LengthChoice == 1 :
        Wall_Length = SI.get_Positive_Float_Choice("Define the total length of the figure (in meters)")
    elif LengthChoice == 2 :
        Min_Length , Max_Length, Step_Length = SI.get_Min_Max_Length()
    else :
        Cell_Length = SI.get_Positive_Float_Choice("Define the length of a cell (in meters)")
    
    HeightChoice = SI.get_1_Or_2_Choice("About the height of walls", "A constant height", "A height between a range of values")
    if HeightChoice == 1 :
        Wall_Height = SI.get_Positive_Float_Choice("Define wall height (in meters)")
    else : 
        Min_Height, Max_Height, Step_Height = SI.get_Min_Max_Wall_Height()
    
    ThicknessChoice = SI.get_1_Or_2_Choice("About the thickness of walls", "A constant thickness", "A thickness between a range of values")
    if ThicknessChoice == 1 :
        Wall_Thickness = SI.get_Positive_Float_Choice("Define wall thickness (in meters)")
    else : 
        Min_Thickness, Max_Thickness, Step_Thickness = SI.get_Min_Max_Wall_Thickness()
        
    TransparencyChoice = SI.get_1_Or_2_Choice("About the transparency of walls", "A constant transparency", 
                                            "A transparency between a range of values")
    if TransparencyChoice == 1 : 
        Wall_Transparency = SI.get_Constant_Wall_Transparency()
    else : 
        Min_Transparency, Max_Transparency, Step_Transparency = SI.get_Min_Max_Wall_Transparency()
        
    Nbr_World = SI.get_Positive_Int_Choice("What is the number of webots worlds to be generated satisfying all the above conditions ?")
    
    # Boolean to know when we have the number of webots world that we want
    isFinish = False
    i = 1
    while isFinish == False :
        # If the choice of the shape of the figure is random, we choose at random between closed figure and open figure
        if WhatShape == 3 :
            Shape = random.choice([1, 2])
        ind = 0
        # Boolean to know when we have a satisfactory figure to then create the associated webots world
        isNext = False
        while isNext == False :    
            # Number of the attempt to find a satisfying world
            ind += 1
            # If the number of walls is between a range of values, we choose randomly from this range of values
            if WallChoice == 2 : 
                Nbr_Wall = random.randrange(Min_Wall, Max_Wall, 1)
            # If the starting direction is random
            if StartChoice == 2 : 
                Start_Dir = random.choice(All_Dir)

            # To differentiate the walls, we increment each time we change direction
            z = 1
            # List of point pairs corresponding to walls
            W_room = []
            # Grid_I x Grid_J size matrix
            Mat = np.zeros((Grid_I, Grid_J))
            # First point of a wall
            x_1 = int((Grid_J - 1)/ 2)
            y_1 = int((Grid_I - 1)/ 2)
            Start_x = x_1 
            Start_y = y_1
            Mat[y_1][x_1] = z 
            
            Current_Dir = Start_Dir
            # Second point of a wall => modified until we change direction
            x_2, y_2 = Next_Point(x_1, y_1, Current_Dir)
            # This point exists since the grid is at least 3x3 with the first point in the middle. So no need for verification
            Mat[y_2][x_2] = z 

            # To count the number of times you pass over a wall already visited in a row
            # If >= 2, we stop the loop because it is a sign of the start of a superposed wall 
            n = 0
            isOK = False
            while isOK == False : 
                # We get a value between 0 and 100
                Prob = float(random.randint(0, 100))
                # If the value is lower than the probability for the same direction, we keep the previous direction
                if Prob <= Proba_D :
                    Next_Dir = Current_Dir 
                    # We iterate the second point
                    x_temp, y_temp = Next_Point(x_2, y_2, Next_Dir)
                    # If the second point is a point of the matrix
                    if x_temp >= 0 and x_temp < Grid_J and y_temp >= 0 and y_temp < Grid_I :
                        # We confirm the second point
                        x_2 = x_temp 
                        y_2 = y_temp
                        # If we allow the walls to intersect
                        if isCrossing == 'Y' or isCrossing == 'y' :
                            # If we want a closed figure and the next point corresponds to the starting point and we will have the number of walls we want
                            if Shape == 1 and [Start_x, Start_y] == [x_2, y_2] and int(len(W_room) / 2) == Nbr_Wall - 1 :
                                W_room.append([x_1, y_1])
                                W_room.append([x_2, y_2])
                                isOK = True
                            else :
                                # If you have passed 2 times in a row on a visited square or if the square corresponds to a point already stored
                                if n >= 2 or [x_2, y_2] in W_room : 
                                    isOK = True 
                                elif Mat[y_2][x_2] == 0 :
                                    Mat[y_2][x_2] = z 
                                    # If we go through a free square, we reset n
                                    n = 0
                                elif Mat[y_2][x_2] != 0 :
                                    n += 1
                                Current_Dir = Next_Dir
                        # If we forbid the walls to cross
                        else : 
                            if Shape == 1 and [Start_x, Start_y] == [x_2, y_2] and int(len(W_room) / 2) == Nbr_Wall - 1 :
                                W_room.append([x_1, y_1])
                                W_room.append([x_2, y_2])
                                isOK = True
                            # If we have already passed through the point in the matrix
                            elif Mat[y_2][x_2] != 0 :
                                isOK = True
                            elif Mat[y_2][x_2] == 0 :
                                Mat[y_2][x_2] = z 
                                Current_Dir = Next_Dir
                    # Otherwise, we store the wall and exit the loop then we will compare if the figure is satisfactory or not
                    else : 
                        W_room.append([x_1, y_1])
                        W_room.append([x_2, y_2])
                        isOK = True
                # Otherwise, we choose a new random direction among those remaining
                else : 
                    # We change direction, so we reset n
                    n = 0
                    # We increment z to say that we are starting a new wall
                    z += 1
                    # We add the wall in W_room 
                    W_room.append([x_1, y_1])
                    W_room.append([x_2, y_2])
                    # We iterate the first point of the new wall
                    x_1 = x_2 
                    y_1 = y_2 
                    
                    # We check if we already have the desired number of walls
                    if int(len(W_room) / 2) == Nbr_Wall : 
                        isOK = True
                    else : 
                        if Current_Dir == 'Up' :
                            Next_Dir = random.choice(All_Dir0)
                        elif Current_Dir == 'Right' :
                            Next_Dir = random.choice(All_Dir1)
                        elif Current_Dir == 'Down' :
                            Next_Dir = random.choice(All_Dir0)
                        elif Current_Dir == 'Left' :
                            Next_Dir = random.choice(All_Dir1)
                        elif Current_Dir == 'Up-Left' :
                            Next_Dir = random.choice(All_Dir4)
                        elif Current_Dir == 'Up-Right' :
                            Next_Dir = random.choice(All_Dir5)
                        elif Current_Dir == 'Down-Left' :
                            Next_Dir = random.choice(All_Dir5)
                        # Down-Right
                        else :
                            Next_Dir = random.choice(All_Dir4)
                        # We iterate the second point
                        x_temp, y_temp = Next_Point(x_1, y_1, Next_Dir)
                        # If the second point is a point of the matrix
                        if x_temp >= 0 and x_temp < Grid_J and y_temp >= 0 and y_temp < Grid_I :
                            x_2 = x_temp 
                            y_2 = y_temp
                            if isCrossing == 'Y' or isCrossing == 'y' :
                                if Shape == 1 and [Start_x, Start_y] == [x_2, y_2] and int(len(W_room) / 2) == Nbr_Wall - 1 :
                                    W_room.append([x_1, y_1])
                                    W_room.append([x_2, y_2])
                                    isOK = True
                                else :
                                    if Mat[y_2][x_2] == 0 :
                                        Mat[y_2][x_2] = z 
                                    elif Mat[y_2][x_2] != 0 :
                                        n += 1
                                    Current_Dir = Next_Dir
                            else : 
                                if Shape == 1 and [Start_x, Start_y] == [x_2, y_2] and int(len(W_room) / 2) == Nbr_Wall - 1 :
                                    W_room.append([x_1, y_1])
                                    W_room.append([x_2, y_2])
                                    isOK = True
                                elif Mat[y_2][x_2] != 0 :
                                    isOK = True
                                else : 
                                    Mat[y_2][x_2] = z 
                                    Current_Dir = Next_Dir
                        else : 
                            W_room.append([x_1, y_1])
                            W_room.append([x_2, y_2])
                            isOK = True    
            # If after 10000 attempts, we have not found a new world satisfying the conditions, we stop the loop
            if ind > 10000 : 
                isNext = True
            # We check if the generated figure satisfies all the conditions, if so isNext = True
            if int(len(W_room) / 2) == Nbr_Wall : 
                if (Shape == 1 and W_room[0] == W_room[-1]) or (Shape == 2 and W_room[0] != W_room[-1]) :
                    isNext = True

        # If we have not exceeded the 10000 attempts to find an adequate figure, it means that the figure satisfies the parameters
        if ind <= 10000 : 
            min_x, min_y, max_x, max_y = MI.get_min_max(W_room)

            if LengthChoice == 2 :
                j = 0
                T_Min_Length = Min_Length
                T_Max_Length = Max_Length
                T_Step_Length = Step_Length
                isInt = False 
                while isInt == False : 
                    if C.check_input(T_Min_Length) == 'int' and C.check_input(T_Max_Length) == 'int' and C.check_input(T_Step_Length) == 'int' :
                        isInt = True
                    else : 
                        T_Min_Length *= 10
                        T_Max_Length *= 10
                        T_Step_Length *= 10
                        j += 1
                Wall_Length = random.randrange(int(T_Min_Length) , int(T_Max_Length), int(T_Step_Length))
                for k in range(j) :
                    Wall_Length /= 10
            elif LengthChoice == 3 : 
                Wall_Length = Cell_Length * (max_x - min_x )
            
            if HeightChoice == 2 :
                j = 0
                T_Min_Height = Min_Height
                T_Max_Height = Max_Height
                T_Step_Height = Step_Height 
                isInt = False 
                while isInt == False : 
                    if C.check_input(T_Min_Height) == 'int' and C.check_input(T_Max_Height) == 'int' and C.check_input(T_Step_Height) == 'int' :
                        isInt = True
                    else : 
                        T_Min_Height *= 10
                        T_Max_Height *= 10
                        T_Step_Height *= 10
                        j += 1
                Wall_Height = random.randrange(int(T_Min_Height), int(T_Max_Height), int(T_Step_Height))
                for k in range(j) :
                    Wall_Height /= 10
                    
            if ThicknessChoice == 2 :
                j = 0
                T_Min_Thickness = Min_Thickness
                T_Max_Thickness = Max_Thickness
                T_Step_Thickness = Step_Thickness
                isInt = False 
                while isInt == False : 
                    if C.check_input(T_Min_Thickness) == 'int' and C.check_input(T_Max_Thickness) == 'int' and C.check_input(T_Step_Thickness) == 'int' :
                        isInt = True
                    else :
                        T_Min_Thickness *= 10
                        T_Max_Thickness *= 10
                        T_Step_Thickness *= 10
                        j += 1
                Wall_Thickness = random.randrange(int(T_Min_Thickness), int(T_Max_Thickness), int(T_Step_Thickness))
                for k in range(j) :
                    Wall_Thickness /= 10
                    
            if TransparencyChoice == 2 :
                j = 0
                T_Min_Transparency = Min_Transparency
                T_Max_Transparency = Max_Transparency
                T_Step_Transparency = Step_Transparency
                isInt = False 
                while isInt == False : 
                    if C.check_input(T_Min_Transparency) == 'int' and C.check_input(T_Max_Transparency) == 'int' and C.check_input(T_Step_Transparency) == 'int' :
                        isInt = True 
                    else : 
                        T_Min_Transparency *= 10
                        T_Max_Transparency *= 10
                        T_Step_Transparency *= 10
                        j += 1
                Wall_Transparency = random.randrange(int(T_Min_Transparency), int(T_Max_Transparency), int(T_Step_Transparency))
                for k in range(j) :
                    Wall_Transparency /= 10
            
            File_Name = "world" + str(i)
            F.Write_Webots_File(File_Name, 2, 2, min_x, max_x, min_y, max_y, Wall_Length, W_room, int(len(W_room) / 2), Wall_Height, Wall_Thickness, Wall_Transparency)
            
            print("World number : ", i)
            print(" Number of attempts : ", ind)
            print(" Number of walls : ", Nbr_Wall)
            if Shape == 1 : 
                print(" Shape of the figure : Closed ")
            else : 
                print(" Shape of the figure : Open ")
            if LengthChoice != 1 :
                print(" Total length : " + str(Wall_Length) + " meters")
            if HeightChoice != 1 :
                print(" Wall height : ", Wall_Height)
            if ThicknessChoice != 1 :
                print(" Wall thickness : ", Wall_Thickness)
            if TransparencyChoice != 1 :
                print(" Wall transparency : ", Wall_Transparency)
            print()
            if i == Nbr_World :
                isFinish = True
                print(" FINISH")
            else :
                # We iterate the number of generated worlds
                i += 1
        else : 
            print("World number : ", i)
            print(" Number of attempts : ", ind)
            print(" Number of walls : ", Nbr_Wall)
            if Shape == 1 : 
                print(" Shape of the figure : Closed ")
            else : 
                print(" Shape of the figure : Open ")
            print(" Generation failed - No figure found after 10 000 attempts")
            print()
            if i == Nbr_World :
                isFinish = True
                print(" FINISH")
            else :
                i += 1


def Generate_Set_With_Images() :
    """_Generate a set of webots world with a set of images_
    """
    Image_Name = []
    Not_Image = []
    files = os.listdir('set_images')
    for name in files:
        image = cv2.imread("set_images/" + name)
        if image is None :
            Not_Image.append(name)
        else :
            Image_Name.append(name)

    print(" Number of files in the folder : ", len(files))
    print("     Total images : ", len(Image_Name))
    print("     Name of image file : ", Image_Name)
    print("     Name of others file : ", Not_Image)
    
    Pixel_Length = SI.get_Positive_Float_Choice("Define the length between 2 pixels (in meters)")
    Wall_Height = SI.get_Positive_Float_Choice("Define wall height (in meters)")
    Wall_Thickness = SI.get_Positive_Float_Choice("Define wall thickness (in meters)")
    Wall_Transparency = SI.get_Constant_Wall_Transparency()
        
    for e in Image_Name : 
        print(e)
        image = cv2.imread("images/" + e)
        print("The size of the image is : " + str(len(image[0])) + " x " + str(len(image)))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
        nbr_0_127 = 0
        nbr_64_127 = 0
        nbr_0_63 = 0
        nbr_32_63 = 0
        nbr_0_31 = 0
        for elt in gray :
            for elts in elt :
                if elts <= 127 :
                    nbr_0_127 += 1
                if elts >= 0 and elts <= 63 :
                    nbr_0_63 += 1
                if elts >= 64 and elts <= 127 :
                    nbr_64_127 += 1
                if elts >= 0 and elts <= 31 :
                    nbr_0_31 += 1
                if elts >= 32 and elts <= 63 :
                    nbr_32_63 += 1

        if nbr_0_31 > nbr_32_63 :
            gray_threshold = 31
        else :
            if nbr_0_63 > nbr_64_127 :
                gray_threshold = 63
            else : 
                gray_threshold = 127
                
        print(" Threshold for binary thresholding : ", gray_threshold)
        _, binary = cv2.threshold(gray, gray_threshold, 255, cv2.THRESH_BINARY)
        
        edges = cv2.Canny(binary, 50, 150)
  
        lines = cv2.HoughLinesP(edges, rho = 1, theta = np.pi/180, threshold = 10, minLineLength = 10, maxLineGap = 10)
        
        W_room = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            W_room.append([x1, y1])
            W_room.append([x2, y2])
        
        W_vertical, W_horizontal, W_left_diagonal, W_right_diagonal, W_left_angle_diagonal, W_right_angle_diagonal = BT.line_separation(W_room, None)
      
        gap_length = 10
        # If there are at least 2 lines of a given type, we apply the extension
        if len(W_vertical) > 3 :
            W_vertical = VH.vertical_or_horizontal_extension('Vertical', W_vertical, gap_length)
        if len(W_horizontal) > 3 :
            W_horizontal = VH.vertical_or_horizontal_extension('Horizontal', W_horizontal, gap_length)
        if len(W_left_diagonal) > 3 :
            W_left_diagonal, W_left_angle_diagonal = D.left_or_right_diagonal_extension('Left_Diagonal', W_left_diagonal, W_left_angle_diagonal, gap_length)
        if len(W_right_diagonal) > 3 :
            W_right_diagonal, W_right_angle_diagonal = D.left_or_right_diagonal_extension('Right_Diagonal', W_right_diagonal, W_right_angle_diagonal, gap_length)

        gap = 10
        # If, after extension, we still have at least 2 lines, we apply the removal of extra lines
        if len(W_vertical) > 3 :
            W_vertical = VH.remove_extra_vertical_or_horizontal('Vertical', W_vertical, gap)
        if len(W_horizontal) > 3 :
            W_horizontal = VH.remove_extra_vertical_or_horizontal('Horizontal', W_horizontal, gap)
        if len(W_left_diagonal) > 3 :
            W_left_diagonal = D.remove_extra_left_or_right_diagonal('Left_Diagonal', W_left_diagonal, W_left_angle_diagonal, gap, len(image[0]), len(image))
        if len(W_right_diagonal) > 3 :
            W_right_diagonal = D.remove_extra_left_or_right_diagonal('Right_Diagonal', W_right_diagonal, W_right_angle_diagonal, gap, len(image[0]), len(image))
        
        print(" Number of verticals : ", int(len(W_vertical) / 2))
        print(" Number of horizontals : ", int(len(W_horizontal) / 2))
        print(" Number of left diagonals : ", int(len(W_left_diagonal) / 2))
        print(" Number of right diagonals : ", int(len(W_right_diagonal) / 2))
        
        W_room, W_vertical, W_horizontal, W_diagonal = BT.fill_hole(W_vertical, W_horizontal, W_left_diagonal, W_right_diagonal, gap, True)

        min_x, min_y, max_x, max_y = MI.get_min_max(W_room)

        Wall_Length = Pixel_Length * (max_x - min_x)
        
        F.Write_Webots_File(e, 2, 2, min_x, max_x, min_y, max_y, Wall_Length, W_room, int(len(W_room) / 2), Wall_Height, Wall_Thickness, Wall_Transparency)


