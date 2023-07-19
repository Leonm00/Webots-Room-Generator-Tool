import cv2
import numpy as np
import Check_Input as C
import OpenCV_Input as OI
import Basic_Line_Treatment as BT
import Vertical_Horizontal_Treatment as VH
import Diagonal_Treatment as D

"""_We extract from the image the information needed for the walls_
"""
    
def extract_all_edges(image_name, isDefaultUse):
    """_We apply image processing algorithms to recover the lines representing the contours and store them in a file_

    Args:
        image_name (_str_): _Name of the selected image_
        isDefaultUse (_bool_): _Whether or not to use default configuration_
    """
    # Load image
    image = cv2.imread("images/" + image_name)

    if isDefaultUse == True : 
        config = np.loadtxt("default_configuration.txt")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_threshold = int(config[2])
        _, binary = cv2.threshold(gray, gray_threshold, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(binary, 50, 150)
        hough_minLineLength = int(config[3])
        hough_maxLineGap = int(config[4])
        
    else : 
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray_threshold = OI.get_GrayThreshold(gray)
        # Thresholding to obtain a binary image
        _, binary = cv2.threshold(gray, gray_threshold, 255, cv2.THRESH_BINARY)

        # Edge detection
        edges = cv2.Canny(binary, 50, 150)
        
        hough_minLineLength, hough_maxLineGap = OI.get_HoughParameters(image_name, edges)
    # Probabilistic Hough transformation to detect lines
    lines = cv2.HoughLinesP(edges, rho = 1, theta = np.pi/180, threshold = hough_minLineLength, minLineLength = hough_minLineLength, maxLineGap = hough_maxLineGap)
    
    # Browse all detected lines
    with open("points_save_3.txt", "w") as f :
        for line in lines:
            x1, y1, x2, y2 = line[0]
            f.write(str(x1) + " " + str(y1) + "\n")
            f.write(str(x2) + " " + str(y2) + "\n")
    
def get_infos(image_name, isDefaultUse) :
    """_The list containing the wall positions is retrieved after the lines have been processed to remove excess lines_

    Args:
        image_name (_str_): _Name of the selected image_
        isDefaultUse (_bool_): _Whether or not to use default configuration_

    Returns:
        2 (_int_): _Wall representation mode (each pair of points represents a wall)_
        W_room (_list_): _Corresponds to the list containing the wall positions_
        int(len(W_room) / 2) (_int_): _Number of walls_
        W_vertical (_list_): _The list containing the points of the vertical lines_
        W_horizontal (_list_): _The list containing the points of the horizontal lines_
        W_diagonal (_list_): _The list containing the points of the diagonal lines_
    """
    # We extract the file containing the points of the figure
    room = np.loadtxt("points_save_3.txt")
    
    if isDefaultUse == True :
        config = np.loadtxt("default_configuration.txt")
        gap_length = int(config[6])
        gap = int(config[7])
    isFinish = False
    while isFinish == False : 
        # Separate all lines by type: vertical, horizontal, left diagonal left, right diagonal
        # And we sort them: the first point is the one with the smallest Y for verticals and diagonals, and the smallest X for horizontals
        W_vertical, W_horizontal, W_left_diagonal, W_right_diagonal, W_left_angle_diagonal, W_right_angle_diagonal = BT.line_separation(room, isDefaultUse)

        for i in range(3) : 
            image = cv2.imread("images/" + image_name)
            if i == 0 :
                print("Initial")
            elif i == 1 : 
                print("The size of the image is : " + str(len(image[0])) + " x " + str(len(image)))
                if isDefaultUse == False :
                    gap_length = OI.get_gap_length()
                # If there are at least 2 lines of a given type, we apply the extension
                if len(W_vertical) > 3 :
                    W_vertical = VH.vertical_or_horizontal_extension('Vertical', W_vertical, gap_length)
                if len(W_horizontal) > 3 :
                    W_horizontal = VH.vertical_or_horizontal_extension('Horizontal', W_horizontal, gap_length)
                if len(W_left_diagonal) > 3 :
                    W_left_diagonal, W_left_angle_diagonal = D.left_or_right_diagonal_extension('Left_Diagonal', W_left_diagonal, W_left_angle_diagonal, gap_length)
                if len(W_right_diagonal) > 3 :
                    W_right_diagonal, W_right_angle_diagonal = D.left_or_right_diagonal_extension('Right_Diagonal', W_right_diagonal, W_right_angle_diagonal, gap_length)
                print("After extension")
            else :
                print("The size of the image is : " + str(len(image[0])) + " x " + str(len(image)))
                if isDefaultUse == False :
                    gap = OI.get_gap()
                # If, after extension, we still have at least 2 lines, we apply the removal of extra lines
                if len(W_vertical) > 3 :
                    W_vertical = VH.remove_extra_vertical_or_horizontal('Vertical', W_vertical, gap)
                if len(W_horizontal) > 3 :
                    W_horizontal = VH.remove_extra_vertical_or_horizontal('Horizontal', W_horizontal, gap)
                if len(W_left_diagonal) > 3 :
                    W_left_diagonal = D.remove_extra_left_or_right_diagonal('Left_Diagonal', W_left_diagonal, W_left_angle_diagonal, gap, len(image[0]), len(image))
                if len(W_right_diagonal) > 3 :
                    W_right_diagonal = D.remove_extra_left_or_right_diagonal('Right_Diagonal', W_right_diagonal, W_right_angle_diagonal, gap, len(image[0]), len(image))
                print("After removing extra")
                
            # We display the different lines detected and differentiate them by a different color
            print(" Number of verticals : ", int(len(W_vertical) / 2))
            for m in range(int(len(W_vertical) / 2)) :
                W_1 = W_vertical[2 * m]
                W_2 = W_vertical[2 * m + 1]
                cv2.line(image, (int(W_1[0]), int(W_1[1])), (int(W_2[0]), int(W_2[1])), (0, 255, 0), 2)
            print(" Number of horizontals : ", int(len(W_horizontal) / 2))
            for m in range(int(len(W_horizontal) / 2)) :
                W_1 = W_horizontal[2 * m]
                W_2 = W_horizontal[2 * m + 1]
                cv2.line(image, (int(W_1[0]), int(W_1[1])), (int(W_2[0]), int(W_2[1])), (255, 0, 0), 2)
            print(" Number of left diagonals : ", int(len(W_left_diagonal) / 2))
            for m in range(int(len(W_left_diagonal) / 2)) :
                W_1 = W_left_diagonal[2 * m]
                W_2 = W_left_diagonal[2 * m + 1]
                cv2.line(image, (int(W_1[0]), int(W_1[1])), (int(W_2[0]), int(W_2[1])), (0, 0, 255), 2)
            print(" Number of right diagonals : ", int(len(W_right_diagonal) / 2))
            for m in range(int(len(W_right_diagonal) / 2)) :
                W_1 = W_right_diagonal[2 * m]
                W_2 = W_right_diagonal[2 * m + 1]
                cv2.line(image, (int(W_1[0]), int(W_1[1])), (int(W_2[0]), int(W_2[1])), (255, 0, 255), 2)
            cv2.imshow("Close the window", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        image = cv2.imread("images/" + image_name)
        W_room, W_vertical, W_horizontal, W_diagonal = BT.fill_hole(W_vertical, W_horizontal, W_left_diagonal, W_right_diagonal, gap)
        for m in range(int(len(W_room) / 2)) :
            W_1 = W_room[2 * m]
            W_2 = W_room[2 * m + 1]
            cv2.line(image, (int(W_1[0]), int(W_1[1])), (int(W_2[0]), int(W_2[1])), (0, 255, 0), 2)
        # Display image with detected edges
        cv2.imshow("Close the window", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
        print("Is the previous figure satisfactory (detection of all the wanted line)? ")
        choice = input("    Press 'Y' to confirm the choice or 'N' to change it : ")
        choiceOK = False
        while choiceOK == False :
            if C.check_input(choice) == 'str' :
                if str(choice) == 'Y' or str(choice) == 'y' or str(choice) == 'N' or str(choice) == 'n' :
                    choiceOK = True
                    if str(choice) == 'Y' or str(choice) == 'y' :
                        isFinish = True
                    else :
                        isDefaultUse = False
                else :
                    print("     Not an expected string - Please retry")
                    choice = input("    Press 'Y' to confirm the choice or 'N' to change it : ")
            else : 
                print("     Not a string - Please retry")
                choice = input("    Press 'Y' to confirm the choice or 'N' to change it : ")
    
    return 2, W_room, int(len(W_room) / 2), W_vertical, W_horizontal, W_diagonal

    
    
    
    
