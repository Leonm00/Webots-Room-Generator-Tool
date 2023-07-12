import Check_Input as C
import cv2
import numpy as np

"""_Gets all user inputs required for the mode with an image as input_ 
"""

def get_GrayThreshold(gray) :
    """_The threshold value for the binary thresholding step is obtained. The user is asked for an integer between 0 and 255 (grayscale) and shown the associated result. The user is then asked whether or not to validate this value_

    Args:
        gray (_list_): _The table containing the grayscale values of the image studied_

    Returns:
        t (_int_): _The threshold value used for binary thresholding_
    """
    print("Keep in mind that values above threshold are set to 255 (white) and those below are set to 0 (black). ")
    isOK = False
    isCall = True
    while isOK == False : 
        if isCall == True :
            t = input("Threshold for the binary image (int between 0 and 255). The default value is 127 : ")
        while C.check_input(t) != 'int' :
            print("     Not an int - Please retry")
            t = input("Threshold for the binary image (int between 0 and 255) : ")
        if int(t) < 0 :
            print("     Negative value - Please retry")
            t = input("Threshold for the binary image (int between 0 and 255) : ")
            isCall = False
        elif int(t) > 255 :
            print("     Value too High - Please retry")
            t = input("Threshold for the binary image (int between 0 and 255) : ")
            isCall = False
        else : 
            isCall = True
            _, binary = cv2.threshold(gray, int(t), 255, cv2.THRESH_BINARY)
            cv2.imshow("Close the window", binary)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            print("Is the previous figure satisfactory (detection of all the wanted informations in black) ? ")
            choice = input("    Press 'Y' to confirm the choice or 'N' to change it : ")
            choiceOK = False
            while choiceOK == False :
                if C.check_input(choice) == 'str' :
                    if str(choice) == 'Y' or str(choice) == 'y' or str(choice) == 'N' or str(choice) == 'n' :
                        choiceOK = True
                        if str(choice) == 'Y' or str(choice) == 'y' :
                            isOK = True
                    else :
                        print("     Not an expected string - Please retry")
                        choice = input("    Press 'Y' to confirm the choice or 'N' to change it : ")
                else : 
                    print("     Not a string - Please retry")
                    choice = input("    Press 'Y' to confirm the choice or 'N' to change it : ")
    return int(t)

def get_HoughParameters(image_name, edges) : 
    """_The parameters for the Hough algorithm (Line detection) is obtained. The user is asked for two integers and shown the associated result. The user is then asked whether or not to validate these values_

    Args:
        image_name (_str_): _The name of the image studied_
        edges (_list_): _Image edge detection result_

    Returns:
        hough_minLineLength (_int_): _A necessary parameter for the Hough algorithm_
        hough_maxLineGap (_int_): _A necessary parameter for the Hough algorithm_
    """
    isOK = False
    while isOK == False : 
        image = cv2.imread("images/" + image_name)
        print("The size of the image is : " + str(len(image[0])) + " x " + str(len(image)))

        hough_minLineLength = get_minLineLength()
        hough_maxLineGap = get_maxLineGap()
    
        lines = cv2.HoughLinesP(edges, rho = 1, theta = np.pi/180, threshold = hough_minLineLength, minLineLength = hough_minLineLength, maxLineGap = hough_maxLineGap)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Draw green lines corresponding to detected edges
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Display image with detected edges
        cv2.imshow("Close the window", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        print("Is the previous figure satisfactory (detection of all the wanted line in green) ? ")
        choice = input("    Press 'Y' to confirm the choice or 'N' to change it : ")
        choiceOK = False
        while choiceOK == False :
            if C.check_input(choice) == 'str' :
                if str(choice) == 'Y' or str(choice) == 'y' or str(choice) == 'N' or str(choice) == 'n' :
                    choiceOK = True
                    if str(choice) == 'Y' or str(choice) == 'y' :
                        isOK = True
                else :
                    print("     Not an expected string - Please retry")
                    choice = input("    Press 'Y' to confirm the choice or 'N' to change it : ")
            else : 
                print("     Not a string - Please retry")
                choice = input("    Press 'Y' to confirm the choice or 'N' to change it : ")
                
    return int(hough_minLineLength), int(hough_maxLineGap)

def get_minLineLength() :
    """_Gets the minLineLength parameter value for the Hough algorithm_

    Returns:
        l (_int_): _The value used for the Hough algorithm_
    """
    l = input("Minimum number of points (ie pixels) that can form a line (int). Lines with less than this number of points are disregarded : ")
    isOk = False
    while isOk == False : 
        while C.check_input(l) != 'int' :
            print("     Not an int - Please retry")
            l = input("Minimum number of points that can form a line (int) : ")
        if int(l) < 0 :
            print("     Negative value - Please retry")
            l = input("Minimum number of points that can form a line (int) : ")
        if int(l) == 0 :
            print("     NULL value - Please retry")
            l = input("Minimum number of points that can form a line (int) : ")
        else : 
            isOk = True
    return int(l)

def get_maxLineGap() :
    """_Gets the maxLineGap parameter value for the Hough algorithm_

    Returns:
        g (_int_): _The value used for the Hough algorithm_
    """
    g = input("Maximum gap between two points to be considered in the same line (int) : ")
    isOk = False
    while isOk == False : 
        while C.check_input(g) != 'int' :
            print("     Not an int - Please retry")
            g = input("Maximum gap between two points to be considered in the same line (int) : ")
        if int(g) < 0 :
            print("     Negative value - Please retry")
            g = input("Maximum gap between two points to be considered in the same line (int) : ")
        if int(g) == 0 :
            print("     NULL value - Please retry")
            g = input("Maximum gap between two points to be considered in the same line (int) : ")
        else : 
            isOk = True
    return int(g)

def get_gap() :
    """_Gets the gap value for a line sorting step detected by the Hough algorithm_

    Returns:
        g (_int_): _The value used for line extension_
    """
    g = input("Maximum gap between two parallel lines to be considered as the same line (int) : ")
    isOk = False
    while isOk == False : 
        while C.check_input(g) != 'int' :
            print("     Not an int - Please retry")
            g = input("Maximum gap between two parallel lines to be considered as the same line (int) : ")
        if int(g) < 0 :
            print("     Negative value - Please retry")
            g = input("Maximum gap between two parallel lines to be considered as the same line (int) : ")
        if int(g) == 0 :
            print("     NULL value - Please retry")
            g = input("Maximum gap between two parallel lines to be considered as the same line (int) : ")
        else : 
            isOk = True
    return int(g)
    
def get_gap_length() :
    """_Gets the gap_length value for a line sorting step detected by the Hough algorithm_

    Returns:
        gl (_int_): _The value used for the step that deletes extra lines_
    """
    gl = input("Maximum gap between two lines to be considered in the same line (int) : ")
    isOk = False
    while isOk == False : 
        while C.check_input(gl) != 'int' :
            print("     Not an int - Please retry")
            gl = input("Maximum gap between two lines to be considered in the same line (int) : ")
        if int(gl) < 0 :
            print("     Negative value - Please retry")
            gl = input("Maximum gap between two lines to be considered in the same line (int) : ")
        if int(gl) == 0 :
            print("     NULL value - Please retry")
            gl = input("Maximum gap between two lines to be considered in the same line (int) : ")
        else : 
            isOk = True
    return int(gl)

def get_angle() :
    """_Gets the angle value to correct the offset detected lines by the Hough algorithm_

    Returns:
        a (_int_): _The value used to correct offset detected lines_
    """
    a = input("Maximum angle of a line in relation to the vertical or horizontal to be considered as a vertical or horizontal line (int between 0 and 45): ")
    isOk = False
    while isOk == False : 
        while C.check_input(a) != 'int' :
            print("     Not an int - Please retry")
            a = input("Maximum angle of a line in relation to the vertical or horizontal to be considered as a vertical or horizontal line (int between 0 and 45): ")
        if int(a) < 0 :
            print("     Negative value - Please retry")
            a = input("Maximum angle of a line in relation to the vertical or horizontal to be considered as a vertical or horizontal line (int between 0 and 45): ")
        if int(a) > 45 :
            print("     Value too High - Please retry")
            a = input("Maximum angle of a line in relation to the vertical or horizontal to be considered as a vertical or horizontal line (int between 0 and 45): ")
        else : 
            isOk = True
    return int(a)