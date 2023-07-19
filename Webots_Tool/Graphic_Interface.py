# Using the tkinter library to create the graphical interface
import tkinter as tk
import math
import Graphic_Interface_Input as GI
import numpy as np 
import time

"""_The class containing methods and arguments for the graphical interface_
"""

class CreateRooms(tk.Tk) :
    def __init__(self, isDefaultUse) :
        """_The __init__ method is used to initialize the various window elements_
        """
        # Gets the number of cells 
        if isDefaultUse == True :
            config = np.loadtxt("default_configuration.txt")
            self.w = int(config[0])
            self.h = int(config[1])
        else : 
            self.w, self.h = GI.get_cells_width(), GI.get_cells_height()
        # Gets the choice of mode
        self.m = GI.get_mode()

        # Use the __init__ method of the parent class tk.Tk to create a window
        super().__init__()
        # Title and Text
        self.title("Room Creation")
        self.label = tk.Label(self, text = "Welcome - Left click to Add a Point | Right click to Remove last Point")
        # The pack() method adds the label to the window
        self.label.pack()
        
        # Define the grid size : a suitable size for canvas is 700x700 pixels
        self.grid_size = int(700 / max(self.w, self.h))
        self.width, self.height = self.w * self.grid_size, self.h * self.grid_size
        
        # Canvas
        self.canvas = tk.Canvas(self, width = self.width, height = self.height)
        self.canvas.pack()

        # To add the background grid to the canvas
        self.create_grid()
        # Empty list to store the coordinates of the points
        self.points = []
        
        if self.m == 1 :
            # Use of the bind() method to associate the add_point_1() method with the left mouse click
            self.canvas.bind("<Button-1>", self.add_point_1)
            # Use of the bind() method to associate the remove_last_1() method with the right mouse click
            self.canvas.bind("<Button-3>", self.remove_last_1)
        else :
            # Use of the bind() method to associate the add_point_2() method with the left mouse click
            self.canvas.bind("<Button-1>", self.add_point_2)
            # Use of the bind() method to associate the remove_last_2() method with the right mouse click
            self.canvas.bind("<Button-3>", self.remove_last_2)

        # To add the buttons to the canvas
        self.create_reset_button()
        self.create_finish_button()
        
    def create_grid(self) :
        """_To add grid lines on the canvas_
        """
        # Vertical lines
        for i in range(0, self.height + self.grid_size, self.grid_size) :
            self.canvas.create_line(0, i, self.width, i, fill = 'gray')
        # Horizontal lines
        for j in range(0, self.width + self.grid_size, self.grid_size) :
            self.canvas.create_line(j, 0, j, self.height, fill = 'gray')

    def add_point_1(self, event) :
        """_When the user clicks on the canvas with the left mouse click, a point is added on the canvas (with dynamic sorting for Option 1)_

        Args:
            event (_event_): _To get the coordinates of the mouse on the canvas_
        """
        x, y = event.x, event.y
        x, y = x / self.grid_size, y / self.grid_size
        
        # Take nearest point
        temp_x, temp_y = int(x), int(y)
        if abs(temp_x - x) > 0.5 :
            x = temp_x + 1
        else :
            x = temp_x
        if abs(temp_y - y) > 0.5 :
            y = temp_y + 1
        else : 
            y = temp_y

        # If it's the first point, we add just one point on the canvas
        if len(self.points) == 0 :
            self.points.append((x, y))
            print(self.points[-1])
            # A red circle with a diameter of 6 pixels
            self.canvas.create_oval(x * self.grid_size - 3, y * self.grid_size - 3, x * self.grid_size + 3, y * self.grid_size + 3, fill = "red")
        # Otherwise, we add a circle and an edge
        else :
            # If the current point is not identical to the last one
            if (x, y) != (self.points[-1][0], self.points[-1][1]) :
                self.points.append((x, y))
                print(self.points[-1])
                # The last two points are used to draw a blue line
                self.canvas.create_line(self.points[-2][0] * self.grid_size, self.points[-2][1] * self.grid_size, x * self.grid_size, y * self.grid_size, fill = "blue")
                # A red circle with a diameter of 6 pixels is added to the (x y) coordinates for easier viewing
                self.canvas.create_oval(x * self.grid_size - 3, y * self.grid_size - 3, x * self.grid_size + 3, y * self.grid_size + 3, fill = "red")

        # We sort the points list to remove any extra points that may be on an edge.
        if len(self.points) > 2 :
            temp_x, temp_y = [], []
            # We just need to analyse the last three points
            for i in range(3) : 
                temp_x.append(self.points[-1][0])
                temp_y.append(self.points[-1][1])
                self.points.pop()

            # For diagonals
            diff_x_1, diff_y_1 = abs(temp_x[2] - temp_x[1]), abs(temp_y[2] - temp_y[1])
            diff_x_2, diff_y_2 = abs(temp_x[0] - temp_x[2]), abs(temp_y[0] - temp_y[2])
            diff_x_3, diff_y_3 = abs(temp_x[0] - temp_x[1]), abs(temp_y[0] - temp_y[1])

            # The first and third points are identical
            if [temp_x[2], temp_y[2]] == [temp_x[0], temp_y[0]] :
                # We keep only the first point
                self.points.append((temp_x[2], temp_y[2]))
                self.canvas.delete("all")
                self.create_grid()
                self.add_from_points_1()
            # Same x OR same y OR in the same diagonal | We don't take the longest edge as a priority
            elif temp_x[0] == temp_x[1] == temp_x[2] or temp_y[0] == temp_y[1] == temp_y[2] or (diff_x_1 / math.gcd(diff_x_1, diff_y_1)) == (diff_x_2 / math.gcd(diff_x_2, diff_y_2)) == (diff_x_3 / math.gcd(diff_x_3, diff_y_3)) and (diff_y_1 / math.gcd(diff_x_1, diff_y_1)) == (diff_y_2 / math.gcd(diff_x_2, diff_y_2)) == (diff_y_3 / math.gcd(diff_x_3, diff_y_3)) : 
                self.points.append((temp_x[2], temp_y[2]))
                self.points.append((temp_x[0], temp_y[0]))
                self.canvas.delete("all")
                self.create_grid()
                self.add_from_points_1()
            else :
                for i in [2, 1, 0] :
                    self.points.append((temp_x[i], temp_y[i]))
                    
    def add_point_2(self, event) : 
        """_When the user clicks on the canvas with the left mouse click, a point is added on the canvas (with sorting)_

        Args:
            event (_event_): _To get the coordinates of the mouse on the canvas_
        """
        x, y = event.x, event.y
        x, y = x / self.grid_size, y / self.grid_size
        
        # Take nearest point
        temp_x, temp_y = int(x), int(y)
        if abs(temp_x - x) > 0.5 :
            x = temp_x + 1
        else :
            x = temp_x
        if abs(temp_y - y) > 0.5 :
            y = temp_y + 1
        else : 
            y = temp_y
            
        # If the points list has an even number of points, we add just one circle on the canvas for the next point
        if len(self.points) % 2 == 0 :
            self.points.append((x, y))
            print(self.points[-1])
            # A red circle with a diameter of 6 pixels
            self.canvas.create_oval(x * self.grid_size - 3, y * self.grid_size - 3, x * self.grid_size + 3, y * self.grid_size + 3, fill = "red")
        # Otherwise (odd number of points), we add a circle and an edge
        else :
            # If the current point is not identical to the last one
            if (x, y) != (self.points[-1][0], self.points[-1][1]) :
                self.points.append((x, y))
                print(self.points[-1])
                # The last two points are used to draw a blue line
                self.canvas.create_line(self.points[-2][0] * self.grid_size, self.points[-2][1] * self.grid_size, x * self.grid_size, y * self.grid_size, fill = "blue")
                # A red circle with a diameter of 6 pixels is added to the (x y) coordinates for easier viewing.
                self.canvas.create_oval(x * self.grid_size - 3, y * self.grid_size - 3, x * self.grid_size + 3, y * self.grid_size + 3, fill = "red")

        # If the points list has an even number of points, we check whether the last pair of points is already in the points list or not
        # If so, we remove the last pair added
        if len(self.points) > 3 and len(self.points) % 2 == 0 :
            nbr_pair = int(len(self.points) / 2)
            isExtra = False
            for i in range(nbr_pair - 1) :
                if (self.points[2 * i] == self.points[-2] and self.points[2 * i + 1] == self.points[-1]) or (self.points[2 * i] == self.points[-1] and self.points[2 * i + 1] == self.points[-2]) :
                    isExtra = True
            if isExtra == True :
                self.points.pop()
                self.points.pop()
    
    def add_from_points_1(self) : 
        """_Method for adding points to the canvas from the points list (Option 1)_ 
        """
        for i in range(len(self.points)) : 
            x = self.points[i][0]
            y = self.points[i][1]
            if len(self.points) > 1  and i < len(self.points) - 1 :
                self.canvas.create_line(x * self.grid_size, y * self.grid_size, self.points[i + 1][0] * self.grid_size, self.points[i + 1][1] * self.grid_size, fill = "blue")
            self.canvas.create_oval(x * self.grid_size - 3, y * self.grid_size - 3, x * self.grid_size + 3, y * self.grid_size + 3, fill = "red")

    def add_from_points_2(self) :
        """_Method for adding points to the canvas from the points list (Option 2)_ 
        """
        if len(self.points) > 1 :
            if len(self.points) % 2 == 0 :
                for i in range(0, len(self.points) - 1, 2) :
                    self.canvas.create_line(self.points[i][0] * self.grid_size, self.points[i][1] * self.grid_size, self.points[i + 1][0] * self.grid_size, self.points[i + 1][1] * self.grid_size, fill = "blue")
                    self.canvas.create_oval(self.points[i][0] * self.grid_size - 3, self.points[i][1] * self.grid_size - 3, self.points[i][0] * self.grid_size + 3, self.points[i][1] * self.grid_size + 3, fill = "red")
                    self.canvas.create_oval(self.points[i + 1][0] * self.grid_size - 3, self.points[i + 1][1] * self.grid_size - 3, self.points[i + 1][0] * self.grid_size + 3, self.points[i + 1][1] * self.grid_size + 3, fill = "red")
            else : 
                for i in range(0, len(self.points) - 2, 2) :
                    self.canvas.create_line(self.points[i][0] * self.grid_size, self.points[i][1] * self.grid_size, self.points[i + 1][0] * self.grid_size, self.points[i + 1][1] * self.grid_size, fill = "blue")
                    self.canvas.create_oval(self.points[i][0] * self.grid_size - 3, self.points[i][1] * self.grid_size - 3, self.points[i][0] * self.grid_size + 3, self.points[i][1] * self.grid_size + 3, fill = "red")
                    self.canvas.create_oval(self.points[i + 1][0] * self.grid_size - 3, self.points[i + 1][1] * self.grid_size - 3, self.points[i + 1][0] * self.grid_size + 3, self.points[i + 1][1] * self.grid_size + 3, fill = "red")
                self.canvas.create_oval(self.points[-1][0] * self.grid_size - 3, self.points[-1][1] * self.grid_size - 3, self.points[-1][0] * self.grid_size + 3, self.points[-1][1] * self.grid_size + 3, fill = "red")
        if len(self.points) == 1 : 
            self.canvas.create_oval(self.points[0][0] * self.grid_size - 3, self.points[0][1] * self.grid_size - 3, self.points[0][0] * self.grid_size + 3, self.points[0][1] * self.grid_size + 3, fill = "red")

    def create_reset_button(self) :
        """_"Reset" button allows the user to empty the points list_ 
        """
        reset_button = tk.Button(self, text = "Reset", command = self.reset)
        # To add the button to the window
        reset_button.pack()

    def create_finish_button(self) :
        """_"Finish" button which allows the user to save the current points list in a file_ 
        """
        if int(self.m) == 1 :
            finish_button = tk.Button(self, text = "Finish", command = self.finish_1)
        else :
            finish_button = tk.Button(self, text = "Finish", command = self.finish_2)
        finish_button.pack()

    def finish_1(self) :
        """_When the user clicks on the "Finish" button in mode 1_ 
        """
        isFinish = False
        if len(self.points) > 3 : 
            # We check that we have a closed figure
            if self.points[0] == self.points[-1] : 
                isFinish = True
        if isFinish == True : 
            self.destroy()
            with open("points_save_2.txt", "w") as f :
                print("Saving", end="")
                for i in range(3) :
                    time.sleep(0.25)
                    print(".", end="")
                print("")
                # To empty the other text file
            with open("points_save_1.txt", "w") as f :
                # y coordinates are in the opposite direction
                for point in self.points :
                    y = point[1]
                    gap = int(self.h) - y
                    if gap < int(int(self.h) / 2) :
                        y = gap
                    else : 
                        y = int(self.h) - y
                    f.write(str(point[0]) + " " + str(y) + "\n")
        else : 
            print("     Not a closed figure")
            print("PLEASE Reset, Remove or Add point(s)")
            
    def finish_2(self) : 
        """_When the user clicks on the "Finish" button in mode 2_ 
        """
        if len(self.points) > 0 : 
            # We check that we have an even number of points 
            if len(self.points) % 2 == 0 :
                self.destroy()
                with open("points_save_1.txt", "w") as f :
                    print("Saving", end="")
                    for i in range(3) :
                        time.sleep(0.25)
                        print(".", end="")
                    print("")
                    # To empty the other text file
                with open("points_save_2.txt", "w") as f :
                    # y coordinates are in the opposite direction
                    for point in self.points :
                        y = point[1]
                        gap = int(self.h) - y
                        if gap < int(int(self.h) / 2) :
                            y = gap
                        else : 
                            y = int(self.h) - y
                        f.write(str(point[0]) + " " + str(y) + "\n")
            else : 
                print("     Not an even number of points")
                print("PLEASE Reset, Remove or Add point(s)")
        else : 
            print("     Empty drawing")
            print("PLEASE Add points")
        
    def reset(self) :
        """_summary_ When the user clicks on the "Reset" button
        """
        self.points = []
        self.canvas.delete("all")
        self.create_grid()
        
    def remove_last_1(self, event) : 
        """_summary_ To delete the last point add in mode 1
        """
        if (len(self.points)) > 0 :
            self.points.pop(-1)
        self.canvas.delete("all")
        self.create_grid()
        self.add_from_points_1()
        
    def remove_last_2(self, event) :
        """_summary_ To delete the last point add in mode 2
        """
        if (len(self.points)) > 0 :
            self.points.pop(-1)
        self.canvas.delete("all")
        self.create_grid()
        self.add_from_points_2()


class ChooseLength(tk.Tk) :
    def __init__(self, W_room, W_type, SizeChoice, Choice, ModeChoice, min_x, min_y, max_x, max_y) :
        """_The __init__ method is used to initialize the various window elements_
        """
        self.c = Choice
        # Gets the number of cells 
        self.w = int(max_x + min_x)
        self.h = int(max_y + min_y)
        # Gets the choice of mode
        self.m = ModeChoice

        self.sizechoice = SizeChoice
        # Use the __init__ method of the parent class tk.Tk to create a window
        super().__init__()
        # Title and Text
        if self.sizechoice == 2 :
            self.title("Select a line")
        elif self.sizechoice == 3 :
            self.title("Select a vertical line")
        elif self.sizechoice == 4 :
            self.title("Select a horizontal line")
        else : 
            self.title("Select a diagonal line")
        self.label = tk.Label(self, text = "Welcome - Left click to Add a Point | Right click to Remove last Point")
        # The pack() method adds the label to the window
        self.label.pack()
        
        # Define the grid size : a suitable size for canvas is 700x700 pixels
        if self.c == 1 :
            self.grid_size = int(700 / max(self.w, self.h))
        else : 
            if max(self.w, self.h) < 350 :
                self.grid_size = int(700 / max(self.w, self.h))
            else :
                self.grid_size = 1
        self.width, self.height = self.w * self.grid_size, self.h * self.grid_size
            
        # Canvas
        self.canvas = tk.Canvas(self, width = self.width, height = self.height)
        self.canvas.pack()

        # Empty list to store the coordinates of the points
        self.points = []
        for e in W_room :
            self.points.append([e[0], e[1]])
        self.line = []
        self.type = []
        for e in W_type :
            self.type.append([e[0], e[1]])
        
        if self.c == 1 :
            for point in self.points :
                y = point[1]
                gap = self.h - y
                if gap < int(self.h / 2) :
                    y = gap
                else : 
                    y = self.h - y
                point[1] = y

            for point in self.type:
                y = point[1]
                gap = self.h - y
                if gap < int(self.h / 2) :
                    y = gap
                else : 
                    y = self.h - y
                point[1] = y

        if self.m == 1 :
            # Use of the bind() method to associate the add_point() method with the left mouse click
            self.canvas.bind("<Button-1>", self.add_point)
            # Use of the bind() method to associate the remove_last_1() method with the right mouse click
            self.canvas.bind("<Button-3>", self.remove_last_1)
            self.create_grid()
            self.add_from_points_1()
        else :
            # Use of the bind() method to associate the add_point() method with the left mouse click
            self.canvas.bind("<Button-1>", self.add_point)
            # Use of the bind() method to associate the remove_last_2() method with the right mouse click
            self.canvas.bind("<Button-3>", self.remove_last_2)
            self.create_grid()
            self.add_from_points_2()

        # To add the buttons to the canvas
        self.create_finish_button()
        
    def create_grid(self) :
        """_To add grid lines on the canvas_
        """
        # Vertical lines
        for i in range(0, self.height + self.grid_size, self.grid_size) :
            self.canvas.create_line(0, i, self.width, i, fill = 'gray')
        # Horizontal lines
        for j in range(0, self.width + self.grid_size, self.grid_size) :
            self.canvas.create_line(j, 0, j, self.height, fill = 'gray')

    def add_point(self, event) :
        """_When the user clicks on the canvas with the left mouse click, a point is added on the canvas if the point belongs to the self.type list _

        Args:
            event (_event_): _To get the coordinates of the mouse on the canvas_
        """
        x, y = event.x, event.y

        x, y = x / self.grid_size, y / self.grid_size
        
        # Take nearest point
        temp_x, temp_y = int(x), int(y)
        if abs(temp_x - x) > 0.5 :
            x = temp_x + 1
        else :
            x = temp_x
        if abs(temp_y - y) > 0.5 :
            y = temp_y + 1
        else : 
            y = temp_y

        if len(self.line) < 2 :
            if self.c == 1 : 
                if len(self.line) == 0 :
                    isOK = False
                    for i in range(len(self.type)) :
                        if self.type[i] == [x, y] and isOK == False :
                            isOK = True
                            self.line.append((x, y))
                            print(self.line[-1])
                            self.canvas.create_oval(self.line[0][0] * self.grid_size - 4, self.line[0][1] * self.grid_size - 4, self.line[0][0] * self.grid_size + 4, self.line[0][1] * self.grid_size + 4, fill = "red")
                elif len(self.line) == 1 :
                    isOK = False
                    for i in range(int(len(self.type) / 2)) :
                        H_1 = self.type[2 * i]
                        H_2 = self.type[2 * i + 1]
                        L_1 = self.line[0]

                        if [H_1[0], H_1[1]] == [L_1[0], L_1[1]] :
                            if [x, y] == [H_2[0], H_2[1]] and isOK == False :
                                isOK = True
                                self.line.append((x, y))
                                print(self.line[-1])
                                self.canvas.create_line(self.line[0][0] * self.grid_size, self.line[0][1] * self.grid_size, self.line[1][0] * self.grid_size, self.line[1][1] * self.grid_size, fill = "red")
                                self.canvas.create_oval(self.line[1][0] * self.grid_size - 4, self.line[1][1] * self.grid_size - 4, self.line[1][0] * self.grid_size + 4, self.line[1][1] * self.grid_size + 4, fill = "red")
                        elif [H_2[0], H_2[1]] == [L_1[0], L_1[1]] :
                            if [x, y] == [H_1[0], H_1[1]] and isOK == False :
                                isOK = True
                                self.line.append((x, y))
                                print(self.line[-1])
                                self.canvas.create_line(self.line[0][0] * self.grid_size, self.line[0][1] * self.grid_size, self.line[1][0] * self.grid_size, self.line[1][1] * self.grid_size, fill = "red")
                                self.canvas.create_oval(self.line[1][0] * self.grid_size - 4, self.line[1][1] * self.grid_size - 4, self.line[1][0] * self.grid_size + 4, self.line[1][1] * self.grid_size + 4, fill = "red")
            else : 
                if len(self.line) == 0 :
                    isOK = False
                    for i in range(len(self.type)) :
                        if isOK == False and math.dist(self.type[i], [x, y]) <= 5 :
                            isOK = True
                            self.line.append((self.type[i][0], self.type[i][1]))
                            print(self.line[-1])
                            self.canvas.create_oval(self.line[0][0] * self.grid_size - 4, self.line[0][1] * self.grid_size - 4, self.line[0][0] * self.grid_size + 4, self.line[0][1] * self.grid_size + 4, fill = "red")
                elif len(self.line) == 1 :
                    isOK = False
                    for i in range(int(len(self.type) / 2)) :
                        H_1 = self.type[2 * i]
                        H_2 = self.type[2 * i + 1]
                        L_1 = self.line[0]

                        if [H_1[0], H_1[1]] == [L_1[0], L_1[1]] :
                            if isOK == False and math.dist([x, y],[H_2[0], H_2[1]]) <= 5 :
                                isOK = True
                                self.line.append((H_2[0], H_2[1]))
                                print(self.line[-1])
                                self.canvas.create_line(self.line[0][0] * self.grid_size, self.line[0][1] * self.grid_size, self.line[1][0] * self.grid_size, self.line[1][1] * self.grid_size, fill = "red")
                                self.canvas.create_oval(self.line[1][0] * self.grid_size - 4, self.line[1][1] * self.grid_size - 4, self.line[1][0] * self.grid_size + 4, self.line[1][1] * self.grid_size + 4, fill = "red")
                        elif [H_2[0], H_2[1]] == [L_1[0], L_1[1]] :
                            if isOK == False and math.dist([x, y], [H_1[0], H_1[1]]) <= 5 :
                                isOK = True
                                self.line.append((H_1[0], H_1[1]))
                                print(self.line[-1])
                                self.canvas.create_line(self.line[0][0] * self.grid_size, self.line[0][1] * self.grid_size, self.line[1][0] * self.grid_size, self.line[1][1] * self.grid_size, fill = "red")
                                self.canvas.create_oval(self.line[1][0] * self.grid_size - 4, self.line[1][1] * self.grid_size - 4, self.line[1][0] * self.grid_size + 4, self.line[1][1] * self.grid_size + 4, fill = "red")
                
    def add_from_points_1(self) : 
        """_Method for adding points to the canvas from the points list (Option 1)_ 
        """
        for i in range(len(self.points)) : 
            x = self.points[i][0]
            y = self.points[i][1]
            if i < len(self.points) - 1 :
                self.canvas.create_line(x * self.grid_size, y * self.grid_size, self.points[i + 1][0] * self.grid_size, self.points[i + 1][1] * self.grid_size, fill = "green")
       
        for i in range(0, len(self.type) - 1, 2) :
            self.canvas.create_line(self.type[i][0] * self.grid_size, self.type[i][1] * self.grid_size, self.type[i + 1][0] * self.grid_size, self.type[i + 1][1] * self.grid_size, fill = "blue")
            self.canvas.create_oval(self.type[i][0] * self.grid_size - 3, self.type[i][1] * self.grid_size - 3, self.type[i][0] * self.grid_size + 3, self.type[i][1] * self.grid_size + 3, fill = "blue")
            self.canvas.create_oval(self.type[i + 1][0] * self.grid_size - 3, self.type[i + 1][1] * self.grid_size - 3, self.type[i + 1][0] * self.grid_size + 3, self.type[i + 1][1] * self.grid_size + 3, fill = "blue")

        if len(self.line) == 1 :
            self.canvas.create_oval(self.line[0][0] * self.grid_size - 4, self.line[0][1] * self.grid_size - 4, self.line[0][0] * self.grid_size + 4, self.line[0][1] * self.grid_size + 4, fill = "red")
        elif len(self.line) == 2 : 
            self.canvas.create_line(self.line[0][0] * self.grid_size, self.line[0][1] * self.grid_size, self.line[1][0] * self.grid_size, self.line[1][1] * self.grid_size, fill = "red")
            self.canvas.create_oval(self.line[0][0] * self.grid_size - 4, self.line[0][1] * self.grid_size - 4, self.line[0][0] * self.grid_size + 4, self.line[0][1] * self.grid_size + 4, fill = "red")
            self.canvas.create_oval(self.line[1][0] * self.grid_size - 4, self.line[1][1] * self.grid_size - 4, self.line[1][0] * self.grid_size + 4, self.line[1][1] * self.grid_size + 4, fill = "red")
            
    def add_from_points_2(self) :
        """_Method for adding points to the canvas from the points list (Option 2)_ 
        """
        for i in range(0, len(self.points) - 1, 2) :
            self.canvas.create_line(self.points[i][0] * self.grid_size, self.points[i][1] * self.grid_size, self.points[i + 1][0] * self.grid_size, self.points[i + 1][1] * self.grid_size, fill = "green")

        for i in range(0, len(self.type) - 1, 2) :
            self.canvas.create_line(self.type[i][0] * self.grid_size, self.type[i][1] * self.grid_size, self.type[i + 1][0] * self.grid_size, self.type[i + 1][1] * self.grid_size, fill = "blue")
            self.canvas.create_oval(self.type[i][0] * self.grid_size - 3, self.type[i][1] * self.grid_size - 3, self.type[i][0] * self.grid_size + 3, self.type[i][1] * self.grid_size + 3, fill = "blue")
            self.canvas.create_oval(self.type[i + 1][0] * self.grid_size - 3, self.type[i + 1][1] * self.grid_size - 3, self.type[i + 1][0] * self.grid_size + 3, self.type[i + 1][1] * self.grid_size + 3, fill = "blue")
        
        if len(self.line) == 1 :
            self.canvas.create_oval(self.line[0][0] * self.grid_size - 4, self.line[0][1] * self.grid_size - 4, self.line[0][0] * self.grid_size + 4, self.line[0][1] * self.grid_size + 4, fill = "red")
        elif len(self.line) == 2 : 
            self.canvas.create_line(self.line[0][0] * self.grid_size, self.line[0][1] * self.grid_size, self.line[1][0] * self.grid_size, self.line[1][1] * self.grid_size, fill = "red")
            self.canvas.create_oval(self.line[0][0] * self.grid_size - 4, self.line[0][1] * self.grid_size - 4, self.line[0][0] * self.grid_size + 4, self.line[0][1] * self.grid_size + 4, fill = "red")
            self.canvas.create_oval(self.line[1][0] * self.grid_size - 4, self.line[1][1] * self.grid_size - 4, self.line[1][0] * self.grid_size + 4, self.line[1][1] * self.grid_size + 4, fill = "red")

    def create_finish_button(self) :
        """_"Finish" button which allows the user to save the current length in a file_ 
        """
        finish_button = tk.Button(self, text = "Finish", command = self.finish)
        finish_button.pack()
            
    def finish(self) : 
        """_When the user clicks on the "Finish" button_ 
        """
        # We check that we have two points (a horizontal line)
        if len(self.line) == 2 : 
            with open("size_length.txt", "w") as f :
                f.write(str(math.dist(self.line[0], self.line[1])) + "\n")
                f.write(str(math.dist(self.line[0], self.line[1])) + "\n")
            self.destroy()
        else : 
            if self.sizechoice == 2 :
                print("     No vertical line selected")
            elif self.sizechoice == 3 :
                print("     No horizontal line selected")
            else :
                print("     No diagonal line selected")
            print("PLEASE Remove or Add point(s)")

    def remove_last_1(self, event) : 
        """_summary_ To delete the last point add in mode 1
        """
        if (len(self.line)) > 0 :
            self.line.pop(-1)
        self.canvas.delete("all")
        self.create_grid()
        self.add_from_points_1()
        
    def remove_last_2(self, event) :
        """_summary_ To delete the last point add in mode 2
        """
        if (len(self.line)) > 0 :
            self.line.pop(-1)
        self.canvas.delete("all")
        self.create_grid()
        self.add_from_points_2()
        

class DeleteLine(tk.Tk) :
    def __init__(self, W_vertical, W_horizontal, W_diagonal, Choice, min_x, min_y, max_x, max_y) :
        """_The __init__ method is used to initialize the various window elements_
        """
        self.c = Choice
        # Gets the number of cells 
        self.w = int(max_x + min_x)
        self.h = int(max_y + min_y)

        # Use the __init__ method of the parent class tk.Tk to create a window
        super().__init__()
        # Title and Text
        self.title("Select a line then click on Delete")
        self.label = tk.Label(self, text = "Welcome - Left click to Add a Point | Right click to Remove last Point")
        # The pack() method adds the label to the window
        self.label.pack()
        
        # Define the grid size : a suitable size for canvas is 700x700 pixels
        if self.c == 1 :
            self.grid_size = int(700 / max(self.w, self.h))
        else : 
            if max(self.w, self.h) < 350 :
                self.grid_size = int(700 / max(self.w, self.h))
            else :
                self.grid_size = 1
        self.width, self.height = self.w * self.grid_size, self.h * self.grid_size
            
        # Canvas
        self.canvas = tk.Canvas(self, width = self.width, height = self.height)
        self.canvas.pack()

        self.points = []
        for e in W_vertical :
            self.points.append([e[0], e[1]])
        for e in W_horizontal :
            self.points.append([e[0], e[1]])
        for e in W_diagonal :
            self.points.append([e[0], e[1]])
            
        with open("W_room.txt", "w") as f :
            for point in self.points :
                f.write(str(point[0]) + " " + str(point[1]) + "\n")
                
        # Empty list to store the coordinates of the line
        self.line = []
        self.line_index = 0
        
        if self.c == 1 :
            for point in self.points :
                y = point[1]
                gap = self.h - y
                if gap < int(self.h / 2) :
                    y = gap
                else : 
                    y = self.h - y
                point[1] = y

        # Use of the bind() method to associate the add_point() method with the left mouse click
        self.canvas.bind("<Button-1>", self.add_point)
        # Use of the bind() method to associate the remove_last() method with the right mouse click
        self.canvas.bind("<Button-3>", self.remove_last)
        self.create_grid()
        self.add_from_points()

        # To add the buttons to the canvas
        self.create_finish_button()
        self.create_delete_button()
        
    def create_grid(self) :
        """_To add grid lines on the canvas_
        """
        # Vertical lines
        for i in range(0, self.height + self.grid_size, self.grid_size) :
            self.canvas.create_line(0, i, self.width, i, fill = 'gray')
        # Horizontal lines
        for j in range(0, self.width + self.grid_size, self.grid_size) :
            self.canvas.create_line(j, 0, j, self.height, fill = 'gray')

    def add_point(self, event) :
        """_When the user clicks on the canvas with the left mouse click, a point is added on the canvas if the point belongs to a line _

        Args:
            event (_event_): _To get the coordinates of the mouse on the canvas_
        """
        x, y = event.x, event.y

        x, y = x / self.grid_size, y / self.grid_size
        
        # Take nearest point
        temp_x, temp_y = int(x), int(y)
        if abs(temp_x - x) > 0.5 :
            x = temp_x + 1
        else :
            x = temp_x
        if abs(temp_y - y) > 0.5 :
            y = temp_y + 1
        else : 
            y = temp_y

        if len(self.line) < 2 :
            if self.c == 1 : 
                if len(self.line) == 0 :
                    isOK = False
                    for i in range(len(self.points)) :
                        if self.points[i] == [x, y] and isOK == False :
                            isOK = True
                            self.line.append((x, y))
                            print(self.line[-1])
                            self.canvas.create_oval(self.line[0][0] * self.grid_size - 4, self.line[0][1] * self.grid_size - 4, self.line[0][0] * self.grid_size + 4, self.line[0][1] * self.grid_size + 4, fill = "red")
                elif len(self.line) == 1 :
                    isOK = False
                    for i in range(int(len(self.points) / 2)) :
                        H_1 = self.points[2 * i]
                        H_2 = self.points[2 * i + 1]
                        L_1 = self.line[0]

                        if [H_1[0], H_1[1]] == [L_1[0], L_1[1]] :
                            if [x, y] == [H_2[0], H_2[1]] and isOK == False :
                                isOK = True
                                self.line_index = i
                                self.line.append((x, y))
                                print(self.line[-1])
                                self.canvas.create_line(self.line[0][0] * self.grid_size, self.line[0][1] * self.grid_size, self.line[1][0] * self.grid_size, self.line[1][1] * self.grid_size, fill = "red")
                                self.canvas.create_oval(self.line[1][0] * self.grid_size - 4, self.line[1][1] * self.grid_size - 4, self.line[1][0] * self.grid_size + 4, self.line[1][1] * self.grid_size + 4, fill = "red")
                        elif [H_2[0], H_2[1]] == [L_1[0], L_1[1]] :
                            if [x, y] == [H_1[0], H_1[1]] and isOK == False :
                                isOK = True
                                self.line_index = i
                                self.line.append((x, y))
                                print(self.line[-1])
                                self.canvas.create_line(self.line[0][0] * self.grid_size, self.line[0][1] * self.grid_size, self.line[1][0] * self.grid_size, self.line[1][1] * self.grid_size, fill = "red")
                                self.canvas.create_oval(self.line[1][0] * self.grid_size - 4, self.line[1][1] * self.grid_size - 4, self.line[1][0] * self.grid_size + 4, self.line[1][1] * self.grid_size + 4, fill = "red")
            else : 
                if len(self.line) == 0 :
                    isOK = False
                    for i in range(len(self.points)) :
                        if isOK == False and math.dist(self.points[i], [x, y]) <= 5 :
                            isOK = True
                            self.line.append((self.points[i][0], self.points[i][1]))
                            print(self.line[-1])
                            self.canvas.create_oval(self.line[0][0] * self.grid_size - 4, self.line[0][1] * self.grid_size - 4, self.line[0][0] * self.grid_size + 4, self.line[0][1] * self.grid_size + 4, fill = "red")
                elif len(self.line) == 1 :
                    isOK = False
                    for i in range(int(len(self.points) / 2)) :
                        H_1 = self.points[2 * i]
                        H_2 = self.points[2 * i + 1]
                        L_1 = self.line[0]

                        if [H_1[0], H_1[1]] == [L_1[0], L_1[1]] :
                            if isOK == False and math.dist([x, y],[H_2[0], H_2[1]]) <= 5 :
                                self.line_index = i
                                isOK = True
                                self.line.append((H_2[0], H_2[1]))
                                print(self.line[-1])
                                self.canvas.create_line(self.line[0][0] * self.grid_size, self.line[0][1] * self.grid_size, self.line[1][0] * self.grid_size, self.line[1][1] * self.grid_size, fill = "red")
                                self.canvas.create_oval(self.line[1][0] * self.grid_size - 4, self.line[1][1] * self.grid_size - 4, self.line[1][0] * self.grid_size + 4, self.line[1][1] * self.grid_size + 4, fill = "red")
                        elif [H_2[0], H_2[1]] == [L_1[0], L_1[1]] :
                            if isOK == False and math.dist([x, y], [H_1[0], H_1[1]]) <= 5 :
                                self.line_index = i 
                                isOK = True
                                self.line.append((H_1[0], H_1[1]))
                                print(self.line[-1])
                                self.canvas.create_line(self.line[0][0] * self.grid_size, self.line[0][1] * self.grid_size, self.line[1][0] * self.grid_size, self.line[1][1] * self.grid_size, fill = "red")
                                self.canvas.create_oval(self.line[1][0] * self.grid_size - 4, self.line[1][1] * self.grid_size - 4, self.line[1][0] * self.grid_size + 4, self.line[1][1] * self.grid_size + 4, fill = "red")
                
    def add_from_points(self) :
        """_Method for adding points to the canvas from the points list (Option 2)_ 
        """
        for i in range(0, len(self.points) - 1, 2) :
            self.canvas.create_line(self.points[i][0] * self.grid_size, self.points[i][1] * self.grid_size, self.points[i + 1][0] * self.grid_size, self.points[i + 1][1] * self.grid_size, fill = "blue")

        if len(self.line) == 1 :
            self.canvas.create_oval(self.line[0][0] * self.grid_size - 4, self.line[0][1] * self.grid_size - 4, self.line[0][0] * self.grid_size + 4, self.line[0][1] * self.grid_size + 4, fill = "red")
        elif len(self.line) == 2 : 
            self.canvas.create_line(self.line[0][0] * self.grid_size, self.line[0][1] * self.grid_size, self.line[1][0] * self.grid_size, self.line[1][1] * self.grid_size, fill = "red")
            self.canvas.create_oval(self.line[0][0] * self.grid_size - 4, self.line[0][1] * self.grid_size - 4, self.line[0][0] * self.grid_size + 4, self.line[0][1] * self.grid_size + 4, fill = "red")
            self.canvas.create_oval(self.line[1][0] * self.grid_size - 4, self.line[1][1] * self.grid_size - 4, self.line[1][0] * self.grid_size + 4, self.line[1][1] * self.grid_size + 4, fill = "red")

    def create_finish_button(self) :
        """_"Finish" button which allows the user to save the current points list in a file_ 
        """
        finish_button = tk.Button(self, text = "Finish", command = self.finish)
        finish_button.pack()
            
    def create_delete_button(self) :
        delete_button = tk.Button(self, text = "Delete line", command = self.delete)
        delete_button.pack()
        
    def delete(self) :
        # We check that we have two points (a line)
        if len(self.line) == 2 : 
            del(self.points[2 * self.line_index + 1])
            del(self.points[2 * self.line_index])
            self.line = []
            self.canvas.delete("all")
            self.create_grid()
            self.add_from_points()
        else : 
            print("     No line selected")
            print("PLEASE Add point(s)")
            
    def finish(self) : 
        """_When the user clicks on the "Finish" button_ 
        """
        with open("W_room.txt", "w") as f :
            # y coordinates are in the opposite direction
            if self.c == 1 :
                for point in self.points :
                    y = point[1]
                    gap = int(self.h) - y
                    if gap < int(int(self.h) / 2) :
                        y = gap
                    else : 
                        y = int(self.h) - y
                    f.write(str(point[0]) + " " + str(y) + "\n")
            else : 
                for point in self.points :
                    f.write(str(point[0]) + " " + str(point[1]) + "\n")
        self.destroy()

    def remove_last(self, event) :
        """_summary_ To delete the last point add in mode 2
        """
        if (len(self.line)) > 0 :
            self.line.pop(-1)
        self.canvas.delete("all")
        self.create_grid()
        self.add_from_points()
