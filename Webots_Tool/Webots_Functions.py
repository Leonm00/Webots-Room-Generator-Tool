import numpy as np
import math
import warnings

"""_We collect the information needed for the walls_
"""

def get_infos() :
    """_In manual mode, the position of the walls and the option used are retrieved_

    Returns:
        ModeChoice (_int_): _Corresponds to the option used in manual mode_
        W_room (_list_): _Corresponds to the list containing the wall positions_
        nbr_wall (_int_): _Corresponds to the number of walls to be placed in the webots file_
    """
    # We extract the file containing the points of the figure
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        room1 = np.loadtxt("points_save_1.txt")
        room2 = np.loadtxt("points_save_2.txt")
        
    # In manual mode, depending on the option used, the file for the other option will be empty
    if len(room1) != 0 :
        ModeChoice = 1
        room_x = room1[:,0]
        room_y = room1[:,1]
        W_room = []
        for i in range(len(room1)) :
            W_room.append([room_x[i], room_y[i]])
        nbr_wall = len(W_room) - 1
    elif len(room2) != 0 : 
        ModeChoice = 2
        room_x = room2[:,0]
        room_y = room2[:,1]
        W_room = []
        for i in range(len(room2)) :
            W_room.append([room_x[i], room_y[i]])
        nbr_wall = int(len(W_room) / 2)
    else : 
        print("     ERROR : No saved figure ")
        ModeChoice = 0
        W_room = []
        nbr_wall = 0
        
    return ModeChoice, W_room, nbr_wall

def get_wall_infos(vertice_1, vertice_2, min_x, max_x, min_y, max_y, size_grid) :
    """_To find out information about the wall : direction, length, etc_

    Args:
        vertice_1 (_list_): _[x y] coordinates of the first point_
        vertice_2 (_list_): _[x y] coordinates of the second point_
        min_x (_int_): _The smallest x among all x coordinates in the W_room list_
        max_x (_int_): _The largest x among all x coordinates in the W_room list_
        min_y (_int_): _The smallest y among all y coordinates in the W_room list_
        max_y (_int_): _The largest y among all y coordinates in the W_room list_
        size_grid (_float_): _Conversion to respect size_length_

    Returns:
        sens (_str_): _Corresponds to the wall type_
        size (_float_): _Corresponds to the length of the wall_
        position_x (_float_): _Corresponds to wall position x_
        position_y (_float_): _Corresponds to wall position y_
        angle (_float_): _Corresponds to the angle of rotation of the wall_
    """
    # To find out information about the wall : direction, length, etc.
    if vertice_1[0] == vertice_2[0] :
        # Same x
        sens = 'Vertical'
        size = abs(vertice_1[1] - vertice_2[1])
        # Direction
        if vertice_2[1] > vertice_1[1] : 
            direction = 'Up'
        else : 
            direction = 'Down'
        # Position
        position_x = (vertice_1[0] - min_x) * size_grid
        if direction == 'Up' :
            position_y = (vertice_2[1] - min_y - size / 2) * size_grid
        else : 
            position_y = (vertice_2[1] - min_y + size / 2) * size_grid
        angle = 0
    elif vertice_1[1] == vertice_2[1] : 
        # Same y
        sens = 'Horizontal'
        size = abs(vertice_1[0] - vertice_2[0])
        # Direction
        if vertice_2[0] > vertice_1[0] : 
            direction = 'Right'
        else : 
            direction = 'Left'
        # Position
        position_y = (vertice_1[1] - min_y) * size_grid
        if direction == 'Right' :
            position_x = (vertice_2[0] - min_x - size / 2) * size_grid
        else :
            position_x = (vertice_2[0] - min_x + size / 2) * size_grid
        angle = 1.5708    
    else : 
        sens = 'Diagonal'
        size = math.dist(vertice_1, vertice_2)
        size_x = abs(vertice_1[0] - vertice_2[0])
        size_y = abs(vertice_1[1] - vertice_2[1])
        # Direction and position
        if vertice_2[1] > vertice_1[1] and vertice_2[0] > vertice_1[0] :
            # Up-Right
            position_x = (vertice_2[0] - min_x - size_x / 2) * size_grid
            position_y = (vertice_2[1] - min_y - size_y / 2) * size_grid
            
            angle = -1.5708 + math.atan(size_y / size_x)
        elif vertice_2[1] > vertice_1[1] and vertice_2[0] < vertice_1[0] :
            # Up-Left
            position_x = (vertice_2[0] - min_x + size_x / 2) * size_grid
            position_y = (vertice_2[1] - min_y - size_y / 2) * size_grid
            
            angle = 1.5708 - math.atan(size_y / size_x)
        elif vertice_2[1] < vertice_1[1] and vertice_2[0] > vertice_1[0] :
            # Down-Right
            position_x = (vertice_2[0] - min_x - size_x / 2) * size_grid
            position_y = (vertice_2[1] - min_y + size_y / 2) * size_grid
            
            angle = -1.5708 - math.atan(size_y / size_x)
        else : 
            # Down-Left
            position_x = (vertice_2[0] - min_x + size_x / 2) * size_grid
            position_y = (vertice_2[1] - min_y + size_y / 2) * size_grid
            
            angle = 1.5708 + math.atan(size_y / size_x)
            
    return sens, size, position_x, position_y, angle