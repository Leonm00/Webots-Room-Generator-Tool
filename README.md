# Webots Tool - Room Generator

This tool can be used to create webot worlds consisting of a floor and walls, obtained from an image using edge detection or a graphical interface.

This tool, coded entirely in Python, saves considerable time when creating a room with many walls, for example, as Webots requires you to place each wall manually, specifying its shape, size and position.

## Key features
This tool has two main features :

- Using a graphic interface to create the different walls
- Using an image to extract contours representing walls

## Features not included 
This tool cannot be used to create walls that are not straight.

## Successfully tested version of Python
- Python 3.10
- Python 3.11

Please note that this tool does not work with versions of Python 3.8 and earlier (there is no dist() method in the math library).

## Requirements
- Programming Language : Python
- Libraries to install : if you use "pip"
```
pip install numpy
```
```
pip install opencv-python
```
- Application : Webots

## Libraries used

- [NumPy](https://pypi.org/project/numpy/) for arrays
```python
import numpy as np
```
- [math](https://docs.python.org/3/library/math.html) for mathematical functions such as gcd() or dist()
```python
import math
```
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the graphical interface
```python
import tkinter as tk
```
- [OpenCV](https://pypi.org/project/opencv-python/) for image processing
```python
import cv2
```
## Main steps

### Default Configuration
The first step is to choose whether or not to modify the default configuration. To start with, use only the first choice.
```
Welcome to this Webots Room Generator Tool. What do you want to do ?
  1 - Use the Webots Tool
  2 - Change the Default Configuration
  3 - View the Default Configuration before making a choice
Choice (int) : 1
```

### Choose the feature
The second step is to choose whether to use the graphical interface (1) or an image (2).
```
Please choose the feature you want to use for this Webots Room Generator Tool :
1 - Manual
2 - With an image (does not work well for complex plans)
Choice (int) : 
```

### Use of the Default Configuration 
```
Do you want to use the Default Configuration ?
  Press 'Y' for Yes or 'N' for No : 
```

### Initialize grid (if Default Configuration is not used) or read image
```
Keep in mind that too many cells will result in a grid with very small cells.
Number of cells on the x-axis (int between 2 and 100) :
Number of cells on the y-axis (int between 2 and 100) :
```
```
Give the image name (don't forget the file format) :
```

### Name and wall characteristics (if Default Configuration is not used)
```
Give the name for the webots file :
```
```
Define wall height (in meters). The default value is 2 :
Define wall thickness (in meters). The default value is 0.02 :
Define wall transparency (float between 0 and 1 | 1 for a transparent wall). The default value is 0 :
Define the total length of the figure (in meters), the width will be adjusted accordingly :
```

## About the first feature - Graphical Interface
```
Please choose the feature you want to use for this Webots Room Generator Tool :
  1 - Manual
  2 - With an image (does not work well for complex plans)
Choice (int) : 1
```

### Choose the option
```
Please choose the manual mode option you want to use :
  1 - Room Creation : closed figure (First Point = Last Point)
  2 - Free : each pair of points forms a wall
Mode (int) : 
```
![Graphical Interface](/screenshot/Graphical_Interface.png)

### Add points 
- Left-click to add a point
- Clicking several times in a row on the same spot does not count for more than one point
- Right-click to remove the last point added
- Click on the Reset button to reset the canvas
- Click on the Finish button to save the points. The canvas will then be reset

### Good to know : 
- Points cannot be saved for mode 1 unless the last point added is identical to the first point
- Points cannot be saved for mode 2 unless there is an even number of points
- Only one set of points can be saved at a time

### Example : 
![Room Creation](/screenshot/Room_Creation.png)

```
Give the name for the webots file : example
```

```
Do you want to delete some lines ?
  Press 'Y' for Yes or 'N' for No : N
```

```
Define wall height (in meters). The default value is 2 : 2
Define wall thickness (in meters). The default value is 0.02 : 0.02
Define wall transparency (float between 0 and 1 | 1 for a transparent wall). The default value is 0 : 0
```

```
Please choose the option you want for the size of the final figure : 
  1 - Define the total length of the figure
  2 - Define the length of a line
  3 - Define the length of a vertical line
  4 - Define the length of a horizontal line
  5 - Define the length of a diagonal line
Choice (int) : 1
```

```
Define the total length of the figure (in meters), the width will be adjusted accordingly : 20
```

#### Open the example.wbt file on Webots :
![Room Creation on Webots](/screenshot/Room_Creation_Webots.png)

## About the second feature - Image processing
```
Please choose the feature you want to use for this Webots Room Generator Tool :
  1 - Manual
  2 - With an image (does not work well for complex plans)
Choice (int) : 2
```
### Step-by-step examples

#### Use of the Default Configuration
```
Do you want to use the Default Configuration ?
  Press 'Y' for Yes or 'N' for No : N 
```

#### Image name
The image must be in the images folder.

```
Give the image name (don't forget the file format) : maze.jpg
```

![Maze](/Webots_Tool/images/maze.jpg)

```
Give the image name (don't forget the file format) : plan.jpeg
```

![Plan](/Webots_Tool/images/plan.jpeg)

#### User input - Threshold 
```
Keep in mind that values above threshold are set to 255 (white) and those below are set to 0 (black).
Threshold for the binary image (int between 0 and 255). The default value is 127 : 127
```

![Maze with value 127](/screenshot/Maze_127.png)
![Plan with value 127](/screenshot/Plan_127.png)

The threshold value can be modified to change the amount of information to be analyzed for contour detection. It is advisable to ensure that only important information is displayed.
```
Is the previous figure satisfactory (detection of all the wanted informations in black) ?
  Press 'Y' to confirm the choice or 'N' to change it : N
```
```
Threshold for the binary image (int between 0 and 255). The default value is 127 : 20
```

![Plan with value 20](/screenshot/Plan_20.png)

#### User input - Line detection
It's advisable to take the largest possible value, while still having all the information you want (all contours in green).

```
Minimum number of points (ie pixels) that can form a line (int). Lines with less than this number of points are disregarded : 10
Maximum gap between two points to be considered in the same line (int) : 10
```

![Maze with Line Detection](/screenshot/Maze_Line_Detection.png)

```
Minimum number of points (ie pixels) that can form a line (int). Lines with less than this number of points are disregarded : 10
Maximum gap between two points to be considered in the same line (int) : 5
```

![Plan with Line Detection](/screenshot/Plan_Line_Detection.png)

#### User input - Removing excess lines
```
Maximum angle of a line in relation to the vertical or horizontal to be considered as a vertical or horizontal line (int between 0 and 45) : 20
```

This step ensures that pseudo-verticals and pseudo-horizontals are verticals and horizontals respectively.

```
Initial
  Number of verticals : 34
  Number of horizontals : 31
  Number of left diagonals : 0 
  Number of right diagonals : 0
```

![Maze with Lines](/screenshot/Maze_Angle.png)

Each type of line is represented by a different color.

```
Initial
  Number of verticals : 54
  Number of horizontals : 45
  Number of left diagonals : 18
  Number of right diagonals : 14
```

![Plan with Lines](/screenshot/Plan_Angle.png)

```
Maximum gap between two lines to be considered in the same line (int) : 10
Maximum gap between two parellel lines to be considered as the same line (int) : 10
```

This is the most important step. It removes all excess lines.

```
After removing extra
  Number of verticals : 16
  Number of horizontals : 15
  Number of left diagonals : 0
  Number of right diagonals : 0
```

![Maze without Extra Lines](/screenshot/Maze_Without_Extra.png)

We fill in the gaps between the various nearby lines. It works very well with just verticals and horizontals. With diagonals, we try to keep the diagonals at the same X and Y step, but it's not perfect.

![Maze without Holes](/screenshot/Maze_Without_Hole.png)

```
After removing extra
  Number of verticals : 21
  Number of horizontals : 24
  Number of left diagonals : 7
  Number of right diagonals : 7
```

![Plan without Extra Lines](/screenshot/Plan_Without_Extra.png)

```
Do you want to remove the walls that are all alone ?
 Number of Vertical alone : 1
 Number of Horizontal alone : 2
 Number of Left Diagonal alone : 1
 Number of Right Diagonal alone : 1
  Press 'Y' for Yes or 'N' for No : Y
```

This step allows you to remove the lonely walls if you wish.

![Plan without Holes](/screenshot/Plan_Without_Hole.png)

```
Is the previous figure satisfatory (detection of all the wanted line) ?
  Press 'Y' to confirm the choice or 'N' to change it : Y
```

```
Give the name for the webots file : plan
Define wall height (in meters). The default value is 2 : 2
Define wall thickness (in meters). The default value is 0.02 : 0.02
Define wall transparency (float between 0 and 1 | 1 for a transparent wall). The default value is 0 : 0
```

```
Do you want to delete some lines ?
  Press 'Y' for Yes or 'N' for No : Y
```
To delete additional lines.

![Plan with Delete Line](/screenshot/Plan_Delete_Line.png)

Click on the two points of an existing line before clicking on the "Delete line" button to delete the line. You can delete as many lines as you want. When finished, click on the "Finish" button.

![Plan with Delete Line (2)](/screenshot/Plan_Delete_Lines.png)

![Plan with Delete Line (3)](/screenshot/Plan_Delete_More_Lines.png)

```
Please choose the option you want for the size of the final figure : 
  1 - Define the total length of the figure
  2 - Define the length of a line
  3 - Define the length of a vertical line
  4 - Define the length of a horizontal line
  5 - Define the length of a diagonal line
Choice (int) : 2
```

![Plan with Select Line](/screenshot/Plan_Select_Line.png)

```
Define the length of the selected line (in meters), the width will be adjusted accordingly : 5
  Total length of the figure : 35.0 meters
```

### Results
If additional walls remain, they can be manually removed directly from Webots.

![Maze on Webots](/screenshot/Maze_Webots.png)
![Plan on Webots](/screenshot/Plan_Webots.png)

## About the Default Configuration
```
Welcome to this Webots Room Generator Tool. What do you want to do ?
  1 - Use the Webots Tool
  2 - Change the Default Configuration
  3 - View the Default Configuration before making a choice
Choice (int) : 3
```

```
The default configuration is : 
   Manual Mode 
 Number of cells on the x-axis (int between 2 and 100) : 20
 Number of cells on the y-axis (int between 2 and 100) : 20

   Image Processing 
 Threshold for the binary image (int between 0 and 255) : 127
 Minimum number of points that can form a line (int) : 10
 Maximum gap between two points to be considered in the same line (int) : 10
 Angle for pseudo-vertical and pseudo-horizontal (int between 0 and 45) : 15
 Maximum gap between two lines to be considered in the same line (int) : 10
 Maximum gap between two parellel lines to be considered as the same line (int) : 10

   Wall Parameters
 Wall height (in meters) : 2.0
 Wall thickness (in meters) : 0.02
 Wall transparency (float between 0 and 1) : 0
```

## To Do
