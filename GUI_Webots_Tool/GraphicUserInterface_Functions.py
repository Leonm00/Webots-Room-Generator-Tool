import Check_Input as C 
import math

def isPositiveInteger(c) :
    isPositive = False 
    if C.check_input(c) == 'int' :
        if int(c) > 0 :
            isPositive = True 
    return isPositive

def isPositiveMinMaxInteger(c, Min, Max) :
    isPositive = False 
    if C.check_input(c) == 'int' :
        if int(c) >= Min and int(c) <= Max :
            isPositive = True 
    return isPositive

def isPositiveFloat(c) :
    isPositive = False 
    if C.check_input(c) == 'int' or C.check_input(c) == 'float' :
        if float(c) > 0 :
            isPositive = True 
    return isPositive

def is01Float(c) :
    is01 = False
    if C.check_input(c) == 'int' or C.check_input(c) == 'float' :
        if float(c) >= 0 and float(c) <= 1 :
            is01 = True 
    return is01

def Next_Point(x, y, direction) :
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

def get_min_max(W_room) : 
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
    return int(min_x), int(min_y), int(max_x), int(max_y)

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