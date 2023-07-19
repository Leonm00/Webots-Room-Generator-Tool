import Graphic_Interface as G
import Webots_Input as WI
import Webots_Functions as WF
import main_Input as MI
import OpenCV_Functions as OF
import numpy as np 
import Check_Input as C 

"""_Main file for creating webots files_ 
""" 

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
            if C.check_input(length[0]) == 'int' :
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
            
# If you are in manual mode option 2 and have only one vertical wall, the wall_thickness parameter conflicts with the size_length parameter
if gap_x != 0 :
    size_grid = size_length / gap_x
else :
    size_grid = wall_thickness
gap_y = max_y - min_y 

with open("webots/" + file_name + ".wbt", "w") as f :
    f.write("#VRML_SIM R2023a utf8" + "\n")
    f.write("\n")
    
    # Proto
    f.write("EXTERNPROTO \"https://raw.githubusercontent.com/cyberbotics/webots/R2023a/projects/objects/backgrounds/protos/TexturedBackground.proto\"" + "\n")
    f.write("EXTERNPROTO \"https://raw.githubusercontent.com/cyberbotics/webots/R2023a/projects/objects/backgrounds/protos/TexturedBackgroundLight.proto\"" + "\n")
 
    f.write("WorldInfo {" + "\n")
    f.write("  basicTimeStep 16" + "\n")
    f.write("  contactProperties [" + "\n")
    f.write("    ContactProperties {" + "\n")
    f.write("      material2 \"caster\"" + "\n")
    f.write("      coulombFriction [" + "\n")
    f.write("        0.01" + "\n")
    f.write("      ]" + "\n")
    f.write("      softERP 0.1" + "\n")
    f.write("      softCFM 0.0002" + "\n")
    f.write("    }" + "\n")
    f.write("  ]" + "\n")
    f.write("}" + "\n")
    
    f.write("Viewpoint {" + "\n")
    # Top view
    f.write("  orientation -0.577 0.577 0.577 2.09" + "\n")
    # Centered view
    if Choice == 1 :
        f.write("  position " + str((gap_x * size_grid) / 2) + " " + str((gap_y * size_grid) / 2) + " " + str(size_length * 2) + "\n")
    else :
        f.write("  position " + str((gap_x * size_grid) / 2) + " " + str(-((gap_y * size_grid) / 2)) + " " + str(size_length * 2) + "\n")
    f.write("}" + "\n")
    
    f.write("TexturedBackground {" + "\n")
    f.write("}" + "\n")
    
    f.write("TexturedBackgroundLight {" + "\n")
    f.write("}" + "\n")

    # WALLS
    f.write("Solid {" + "\n")
    f.write("  translation 0 0 " + str(wall_height / 2) + "\n")
    # If we take an image, its walls are reversed by 180°.
    if Choice == 2 :
        f.write("  rotation 1 0 0 3.14159" + "\n")
    f.write("  children [" + "\n")
    
    # For each wall
    for i in range(nbr_wall) : 
        if ModeChoice == 1 : 
            sens, size, position_x, position_y, angle = WF.get_wall_infos(W_room[i], W_room[i + 1], min_x, max_x, min_y, max_y, size_grid)
        else : 
            sens, size, position_x, position_y, angle = WF.get_wall_infos(W_room[2 * i], W_room[2 * i + 1], min_x, max_x, min_y, max_y, size_grid)
     
        f.write("    Solid {" + "\n")
        f.write("      translation " + str(position_x) + " " + str(position_y) + " 0" + "\n")
        
        if sens == 'Horizontal' or sens == 'Vertical' or sens == 'Diagonal' : 
            f.write("      rotation 0 0 1 " + str(angle) + "\n")
        else : 
            print("     ERROR - Rotation")
            f.write("      rotation 0 0 1 0" + "\n")
            
        f.write("      children [" + "\n")
        f.write("        DEF WALL Shape {" + "\n")
        
        # DEF for the first one
        if i == 0 : 
            f.write("          appearance DEF Wall_app PBRAppearance {" + "\n")
            f.write("            baseColorMap ImageTexture {" + "\n")
            f.write("              url [" + "\n")
            f.write("                \"https://lynchp13.github.io/old1/WhitePaintedWall.jpg\"" + "\n")
            f.write("              ]" + "\n")
            f.write("            }" + "\n")
            f.write("            transparency " + str(wall_transparency) + " " + "\n")
            f.write("            roughness 1" + "\n")
            f.write("            metalness 0" + "\n")
            f.write("          }" + "\n")
        else : 
            f.write("          appearance USE Wall_app" + "\n")
            
        f.write("          geometry Box {" + "\n")
        f.write("            size " + str(wall_thickness) + " "+ str(float(size * size_grid)) +" " + str(wall_height) + "\n")
        f.write("          }" + "\n")
        f.write("        }" + "\n")
        f.write("      ]" + "\n")
        f.write("      name \"" + "W_" + str(i) + "\"" + "\n")
        f.write("      boundingObject USE WALL" + "\n")
        f.write("    }" + "\n")
        
    f.write("  ]" + "\n")
    f.write("  name \"Walls\"" + "\n")
    f.write("  boundingObject USE WALL" + "\n")
    f.write("}" + "\n")

    # FLOOR
    f.write("Solid {" + "\n")
    if Choice == 1 :
        f.write("  translation " + str((gap_x * size_grid) / 2) + " " + str((gap_y * size_grid) / 2) + " -0.1" + "\n")
    # In the case of the image mode, since the walls have been rotated, the floor must be shifted.
    else : 
        f.write("  translation " + str((gap_x * size_grid) / 2) + " " + str(-((gap_y * size_grid) / 2)) + " -0.1" + "\n")
    f.write("  children [" + "\n")
    f.write("    Shape {" + "\n")
    f.write("      appearance PBRAppearance {" + "\n")
    f.write("        baseColorMap ImageTexture {" + "\n")
    f.write("          url [" + "\n")
    f.write("            \"https://lynchp13.github.io/old1/WoodenFloor.jpeg\"" + "\n")
    f.write("          ]" + "\n")
    f.write("        }" + "\n")
    f.write("        roughness 1" + "\n")
    f.write("        metalness 0" + "\n")
    f.write("      }" + "\n")
    f.write("      geometry DEF Floor Box {" + "\n")
    if gap_x != 0 :
        f.write("        size " + str(gap_x * size_grid) + " " + str(gap_y * size_grid)  + " 0.2" + "\n")
    else :
        f.write("        size " + str(wall_thickness) + " " + str(gap_y * size_grid)  + " 0.2" + "\n")
    f.write("      }" + "\n")
    f.write("    }" + "\n")
    f.write("  ]" + "\n")
    f.write("  name \"Floor\"" + "\n")
    f.write("  boundingObject USE Floor" + "\n")
    f.write("}" + "\n")
