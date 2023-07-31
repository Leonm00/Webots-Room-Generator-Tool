import Graphic_Interface as G
import Webots_Input as WI
import Webots_Functions as WF
import main_Input as MI
import OpenCV_Functions as OF
import numpy as np 
import Check_Input as C 
import Webots_File as F 
import Set_Input as SI 
import Set_Functions as SF 

"""_Main file for creating webots files_ 
""" 

MainChoice = MI.get_isSet_Choice()

if MainChoice == 1 :
    SetChoice = SI.get_1_Or_2_Choice("Please choose the feature you want to use for this Set of Webots Room Generator Tool", 
                                "Without a set of images", "With a set of images (does not work well for complex images)")
    if SetChoice == 1 :
        # It is possible to have identical figures
        SF.Generate_Random_Set()
    else : 
        SF.Generate_Set_With_Images()
        
else :
    # You have the choice of using the tool directly or first modifying the default configuration
    ConfigChoice = MI.get_Config_Choice()
    if ConfigChoice == 2 : 
        MI.new_default_configuration()
        
    # You can choose to use the graphical interface or image processing.
    Choice = MI.get_Choice()
        
    # You can choose to use the default configuration or not
    DefaultChoice = MI.get_Default_Choice()
    isDefaultUse = False
    if DefaultChoice == 'Y' or DefaultChoice == 'y' :
        config = np.loadtxt("default_configuration.txt")
        if len(config) == 11 and C.check_input(config[0]) == C.check_input(config[1]) == C.check_input(config[2]) == C.check_input(config[3]) == C.check_input(config[4]) == C.check_input(config[5]) == C.check_input(config[6]) == C.check_input(config[7]) == 'int' and (C.check_input(config[8]) == 'float' or C.check_input(config[8]) == 'int') and (C.check_input(config[9]) == 'float' or C.check_input(config[9]) == 'int') and (C.check_input(config[10]) == 'float' or C.check_input(config[10]) == 'int') :
            if int(config[0]) >= 2 and int(config[0]) <= 100 and int(config[1]) >= 2 and int(config[1]) <= 100 and int(config[2]) >= 0 and int(config[2]) <= 255 and int(config[3]) > 0 and int(config[4]) > 0 and int(config[5]) >= 0 and int(config[5]) <= 45 and int(config[6]) > 0 and int(config[7]) > 0 and float(config[8]) > 0 and float(config[9]) > 0 and float(config[10]) >= 0 and float(config[10]) <= 1 :
                isDefaultUse = True
            else : 
                print("ERROR - There is a problem with the Default Configuration text file")
        else :
            print("ERROR - There is a problem with the Default Configuration text file")

    if Choice == 1 :
        creator = G.CreateRooms(isDefaultUse)
        creator.mainloop()
    else :
        image_name = MI.get_name()
        OF.extract_all_edges(image_name, isDefaultUse)

    if Choice == 1 :
        ModeChoice, W_room, nbr_wall, W_vertical, W_horizontal, W_diagonal = WF.get_infos()
    else :
        ModeChoice, W_room, nbr_wall, W_vertical, W_horizontal, W_diagonal = OF.get_infos(image_name, isDefaultUse)
        
    file_name = WI.get_name()

    if isDefaultUse == True : 
        wall_height = float(config[8])
        wall_thickness = float(config[9])
        wall_transparency = float(config[10])
    else : 
        wall_height = WI.get_wall_height()
        wall_thickness = WI.get_wall_thickness()
        wall_transparency = WI.get_wall_transparency()

    min_x, min_y, max_x, max_y = MI.get_min_max(W_room)

    # You can choose to delete lines
    DeleteChoice = MI.get_Delete_Choice()
    if DeleteChoice == 'Y' or DeleteChoice == 'y' :
        creator = G.DeleteLine(W_vertical, W_horizontal, W_diagonal, Choice, min_x, min_y, max_x, max_y)
        creator.mainloop()
        
        ModeChoice = 2
        room = np.loadtxt("W_room.txt")
        room_x = room[:,0]
        room_y = room[:,1]
        W_room = []
        for i in range(len(room)) :
            W_room.append([room_x[i], room_y[i]])
        nbr_wall = int(len(W_room) / 2)
        W_vertical = []
        W_horizontal = []
        W_diagonal = []
        for i in range(int(len(room) / 2)) :
            if room_x[2 * i] == room_x[2 * i + 1] :
                W_vertical.append([room_x[2 * i], room_y[2 *i]])
                W_vertical.append([room_x[2 * i + 1], room_y[2 * i + 1]])
            elif room_y[2 * i] == room_y[2 * i + 1] :
                W_horizontal.append([room_x[2 * i], room_y[2 *i]])
                W_horizontal.append([room_x[2 * i + 1], room_y[2 * i + 1]])
            else : 
                W_diagonal.append([room_x[2 * i], room_y[2 *i]])
                W_diagonal.append([room_x[2 * i + 1], room_y[2 * i + 1]])
        
        min_x, min_y, max_x, max_y = MI.get_min_max(W_room)
        
    gap_x = max_x - min_x

    # There are several options for determining the total length of the figure
    SizeChoice = MI.get_Size_Choice()
    if SizeChoice == 1 :
        size_length = WI.get_total_length()
    else : 
        if (SizeChoice == 2 and len(W_room) == 0) :
            print(" There is no line available")
            size_length = WI.get_total_length()
        else :
            with open("size_length.txt", "w") as f :
                if SizeChoice == 2 : 
                    print(" Please select a line from those available")
            if SizeChoice == 2 : 
                creator = G.ChooseLength(W_room, W_room, SizeChoice, Choice, ModeChoice, min_x, min_y, max_x, max_y)
                creator.mainloop()

            length = np.loadtxt("size_length.txt")
            if len(length) == 2 :
                if C.check_input(length[0]) == 'int' or C.check_input(length[0]) == 'float':
                    if float(length[0]) != 0 :
                        size_one_length = MI.get_size_one_length()
                        size_length = float((size_one_length / float(length[0])) * gap_x)
                        print(" Total length of the figure : " + str(round(size_length, 2)) + " meters")
                    else : 
                        print(" There's a problem with the choice of line")
                        size_length = WI.get_total_length()
                else : 
                    print(" There's a problem with the choice of line")
                    size_length = WI.get_total_length()
            else :
                print(" There's a problem with the choice of line")
                size_length = WI.get_total_length()

    F.Write_Webots_File(file_name, Choice, ModeChoice, min_x, max_x, min_y, max_y, size_length, W_room, nbr_wall, wall_height, wall_thickness, wall_transparency)
