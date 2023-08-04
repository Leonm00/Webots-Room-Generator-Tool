import GraphicUserInterface_Functions as GF

"""_File for creating webots files_ 
""" 

def Write_Webots_File(file_name, Choice, ModeChoice, min_x, max_x, min_y, max_y, size_length, W_room, nbr_wall, wall_height, wall_thickness, wall_transparency) :
    """_Function to generate webots files_

    Args:
        file_name (_str_): _Webots file name_
        Choice (_int_): _If we use an image (2) or not_
        ModeChoice (_int_): _If a wall is between a pair of points (2) or not_
        min_x (_int_): _Minimum coordinate of x among all points_
        max_x (_int_): _Maximum coordinate of x among all points_
        min_y (_int_): _Minimum coordinate of y among all points_
        max_y (_int_): _Maximum coordinate of y among all points_
        size_length (_float_): _Total figure length_
        W_room (_list_): _List containing all the points of the walls_
        nbr_wall (_int_): _Number of walls_
        wall_height (_float_): _Height of walls_
        wall_thickness (_float_): _Thickness of walls_
        wall_transparency (_float_): _Transparency of walls_
    """
    gap_x = max_x - min_x
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
                sens, size, position_x, position_y, angle = GF.get_wall_infos(W_room[i], W_room[i + 1], min_x, max_x, min_y, max_y, size_grid)
            else : 
                sens, size, position_x, position_y, angle = GF.get_wall_infos(W_room[2 * i], W_room[2 * i + 1], min_x, max_x, min_y, max_y, size_grid)
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