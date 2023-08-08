import tkinter as tk
import math
import numpy as np 
import os
import cv2 
import random 
import GraphicUserInterface_Functions as TF
import Webots_File as F 
import Check_Input as C 
import Basic_Line_Treatment as BT

class GraphicInterface(tk.Tk) :
    def __init__(self):
        # Use the __init__ method of the parent class tk.Tk to create a window
        super().__init__()
        # Title
        self.title("Webots Tool - Room Generator")

        # Canvas for Graphic Treatment
        self.Canvas = tk.Canvas(self, width = 700, height = 700)
        self.Reset_Button = tk.Button(self, text = "Reset")
        self.Finish_Button = tk.Button(self, text = "Finish")
        self.Delete_Button = tk.Button(self, text = "Delete Line")
        
        # Default Configuration
        self.config = []
        
        # Canvas parameters
        self.points = []
        self.Walls = []
        self.WallsCanvas = []
        self.Grid_size = 0
        self.W = 0
        self.H = 0
        self.Width = 0
        self.Height = 0
        
        # Empty list to store the coordinates of the line to delete
        self.line = []
        self.line_index = 0
        self.dist_line = 0

        self.paddings = {'padx': 5, 'pady': 5}
        
        # Message
        self.Message = tk.Message(self, text = "")
        self.MessagePointPosition = tk.Message(self, text = "")
        
        # First main choice: choose between generating a Set of Webots World or a single Webots World.
        self.SetChoiceLabel = tk.Label(self, text = "Number of webots world to generate : ")
        self.SetChoice = tk.StringVar()
        self.SetChoiceOption = ["1+", "1"]
        self.SetChoiceMenu = tk.OptionMenu(self, self.SetChoice, *self.SetChoiceOption, command = self.Get_SetChoice)
        self.Display_SetChoice()
        
        # Second choice: Set case
        self.SetFeatureChoiceLabel = tk.Label(self, text = "Main feature to use : ")
        self.SetFeatureChoice = tk.StringVar()
        self.SetFeatureChoiceOption = ["Random", "Images"]
        self.SetFeatureChoiceMenu = tk.OptionMenu(self, self.SetFeatureChoice, *self.SetFeatureChoiceOption, command = self.Get_SetFeatureChoice)
        
        # Second choice: Single world case
        self.FeatureChoiceLabel = tk.Label(self, text = "Main feature to use : ")
        self.FeatureChoice = tk.StringVar()
        self.FeatureChoiceOption = ["Manual", "Image"]
        self.FeatureChoiceMenu = tk.OptionMenu(self, self.FeatureChoice, *self.FeatureChoiceOption, command = self.Get_FeatureChoice)

        # SET OF WEBOTS WORLD
        #### WITHOUT IMAGES ####
        self.SetWallChoiceLabel = tk.Label(self, text = "About the number of walls : ")
        self.SetWallChoice = tk.StringVar()
        self.ConstantVariableOption = ["Constant", "Variable"]
        self.SetWallChoiceMenu = tk.OptionMenu(self, self.SetWallChoice, *self.ConstantVariableOption, command = self.Get_SetWallChoice)
        
        self.SetConstantWallChoiceLabel = tk.Label(self, text = "       Number of walls (int) : ")
        self.SetConstantWallChoiceEntry = tk.Entry(self)
        self.SetConstantWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetConstantWallChoice)
        
        self.SetMinWallChoiceLabel = tk.Label(self, text = "        Minimum number of walls (int) : ")
        self.SetMinWallChoiceEntry = tk.Entry(self)
        self.SetMaxWallChoiceLabel = tk.Label(self, text = "        Maximum number of walls (int) : ")
        self.SetMaxWallChoiceEntry = tk.Entry(self)
        self.SetRangeWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetRangeWallChoice)

        self.SetFigureChoiceLabel = tk.Label(self, text = "About the shape of the figure : ")
        self.SetFigureChoice = tk.StringVar()
        self.SetFigureChoiceOption = ["Closed", "Open", "Random"]
        self.SetFigureChoiceMenu = tk.OptionMenu(self, self.SetFigureChoice, *self.SetFigureChoiceOption, command = self.Get_SetFigureChoice)
        
        self.SetWallCrossingChoiceLabel = tk.Label(self, text = "Do you allow walls crossing ? : ")
        self.SetWallCrossingChoice = tk.StringVar()
        self.YesNoOption = ["Yes", "No"]
        self.SetWallCrossingChoiceMenu = tk.OptionMenu(self, self.SetWallCrossingChoice, *self.YesNoOption, command = self.Get_SetWallCrossingChoice)

        self.SetDiagonalMovementChoiceLabel = tk.Label(self, text = "Do you allow diagonal movements (45° only) ? : ")
        self.SetDiagonalMovementChoice = tk.StringVar()
        self.SetDiagonalMovementChoiceMenu = tk.OptionMenu(self, self.SetDiagonalMovementChoice, *self.YesNoOption, command = self.Get_SetDiagonalMovementChoice)
        
        self.SetFirstDirectionChoiceLabel = tk.Label(self, text = "About the direction of the first wall : ")
        self.SetFirstDirectionChoice = tk.StringVar()
        self.SetFirstDirectionChoice1Option = ["Up", "Right", "Down", "Left", "Random"]
        self.SetFirstDirectionChoice2Option = ["Up", "Right", "Down", "Left", "Up-Left", "Up-Right", "Down-Left", "Down-Right", "Random"]
        self.SetFirstDirectionChoiceMenu = tk.OptionMenu(self, self.SetFirstDirectionChoice, *self.SetFirstDirectionChoice1Option, command = self.Get_SetFirstDirectionChoice)
        
        self.SetProbaSameDirectionChoiceLabel = tk.Label(self, text = "Probability that the next wall is in the same direction (int between 1 and 99) : ")
        self.SetProbaSameDirectionChoiceEntry = tk.Entry(self)
        self.SetProbaSameDirectionChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetProbaSameDirectionChoice)
        
        self.SetMatrixChoiceLabel = tk.Label(self, text = "The first point is in the middle of the cells ")
        self.SetMatrixJChoiceLabel = tk.Label(self, text = "        Number of cells on the x-axis (int > 2) : ")
        self.SetMatrixJChoiceEntry = tk.Entry(self)
        self.SetMatrixIChoiceLabel = tk.Label(self, text = "        Number of cells on the y-axis (int > 2) : ")
        self.SetMatrixIChoiceEntry = tk.Entry(self)
        self.SetMatrixChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetMatrixIJChoice)
        
        self.SetLengthChoiceLabel = tk.Label(self, text = "About the length of the figure : ")
        self.SetLengthChoice = tk.StringVar()
        self.SetLengthChoiceOption = ["Constant", "Variable", "Random"]
        self.SetLengthChoiceMenu = tk.OptionMenu(self, self.SetLengthChoice, *self.SetLengthChoiceOption, command = self.Get_SetLengthChoice)

        self.SetConstantLengthChoiceLabel = tk.Label(self, text = "        Total length of the figure (in meters) : ")
        self.SetConstantLengthChoiceEntry = tk.Entry(self)
        self.SetConstantLengthChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetConstantLengthChoice)
        
        self.SetMinLengthChoiceLabel = tk.Label(self, text = "        Minimum length of the figure (in meters) : ")
        self.SetMinLengthChoiceEntry = tk.Entry(self)
        self.SetMaxLengthChoiceLabel = tk.Label(self, text = "        Maximum length of the figure (in meters) : ")
        self.SetMaxLengthChoiceEntry = tk.Entry(self)
        self.SetStepLengthChoiceLabel = tk.Label(self, text = "        Variation step : ")
        self.SetStepLengthChoiceEntry= tk.Entry(self)
        self.SetRangeLengthChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetRangeLengthChoice)
        
        self.SetCellLengthChoiceLabel = tk.Label(self, text = "        Define the length of a cell (in meters) : ")
        self.SetCellLengthChoiceEntry = tk.Entry(self)
        self.SetCellLengthChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetCellLengthChoice)
        
        self.SetHeightWallChoiceLabel = tk.Label(self, text = "About the height of walls : ")
        self.SetHeightWallChoice = tk.StringVar()
        self.SetHeightWallChoiceMenu = tk.OptionMenu(self, self.SetHeightWallChoice, *self.ConstantVariableOption, command = self.Get_SetHeightWallChoice)

        self.SetConstantHeightWallChoiceLabel = tk.Label(self, text = "        Define wall height (in meters) : ")
        self.SetConstantHeightWallChoiceEntry = tk.Entry(self)
        self.SetConstantHeightWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetConstantHeightWallChoice)
        
        self.SetMinHeightWallChoiceLabel = tk.Label(self, text = "        Minimum height of the walls (in meters) : ")
        self.SetMinHeightWallChoiceEntry = tk.Entry(self)
        self.SetMaxHeightWallChoiceLabel = tk.Label(self, text = "        Maximum height of the walls (in meters) : ")
        self.SetMaxHeightWallChoiceEntry = tk.Entry(self)
        self.SetStepHeightWallChoiceLabel = tk.Label(self, text = "        Variation step : ")
        self.SetStepHeightWallChoiceEntry = tk.Entry(self)
        self.SetRangeHeightWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetRangeHeightWallChoice)
            
        self.SetThicknessWallChoiceLabel = tk.Label(self, text = "About the thickness of walls : ")
        self.SetThicknessWallChoice = tk.StringVar()
        self.SetThicknessWallChoiceMenu = tk.OptionMenu(self, self.SetThicknessWallChoice, *self.ConstantVariableOption, command = self.Get_SetThicknessWallChoice)

        self.SetConstantThicknessWallChoiceLabel = tk.Label(self, text = "        Define wall thickness (in meters) : ")
        self.SetConstantThicknessWallChoiceEntry = tk.Entry(self)
        self.SetConstantThicknessWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetConstantThicknessWallChoice)
        
        self.SetMinThicknessWallChoiceLabel = tk.Label(self, text = "        Minimum thickness of the walls (in meters) : ")
        self.SetMinThicknessWallChoiceEntry = tk.Entry(self)
        self.SetMaxThicknessWallChoiceLabel = tk.Label(self, text = "        Maximum thickness of the walls (in meters) : ")
        self.SetMaxThicknessWallChoiceEntry = tk.Entry(self)
        self.SetStepThicknessWallChoiceLabel = tk.Label(self, text = "Variation step : ")
        self.SetStepThicknessWallChoiceEntry = tk.Entry(self)
        self.SetRangeThicknessWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetRangeThicknessWallChoice)
            
        self.SetTransparencyWallChoiceLabel = tk.Label(self, text = "About the transparency of walls : ")
        self.SetTransparencyWallChoice = tk.StringVar()
        self.SetTransparencyWallChoiceMenu = tk.OptionMenu(self, self.SetTransparencyWallChoice, *self.ConstantVariableOption, command = self.Get_SetTransparencyWallChoice)

        self.SetConstantTransparencyWallChoiceLabel = tk.Label(self, text = "        Define wall transparency (float between 0 and 1) : ")
        self.SetConstantTransparencyWallChoiceEntry = tk.Entry(self)
        self.SetConstantTransparencyWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetConstantTransparencyWallChoice)
        
        self.SetMinTransparencyWallChoiceLabel = tk.Label(self, text = "        Minimum transparency of the walls (float between 0 and 1) : ")
        self.SetMinTransparencyWallChoiceEntry = tk.Entry(self)
        self.SetMaxTransparencyWallChoiceLabel = tk.Label(self, text = "        Maximum transparency of the walls (float between 0 and 1) : ")
        self.SetMaxTransparencyWallChoiceEntry = tk.Entry(self)
        self.SetStepTransparencyWallChoiceLabel = tk.Label(self, text = "        Variation step : ")
        self.SetStepTransparencyWallChoiceEntry = tk.Entry(self)
        self.SetRangeTransparencyWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetRangeTransparencyWallChoice)

        self.SetNumberWorldChoiceLabel = tk.Label(self, text = "Number of Webots World satisfying all the above conditions : ")
        self.SetNumberWorldChoiceEntry = tk.Entry(self)
        self.SetNumberWorldChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetNumberWorldChoice)

        self.SetPrefixNameChoiceLabel = tk.Label(self, text = "Prefix name for the Webots World : ")
        self.SetPrefixNameChoiceEntry = tk.Entry(self)
        self.SetPrefixNameChoiceSubmit = tk.Button(self, text = "Generate", command = self.Get_SetPrefixNameChoice)

        #### WITH IMAGES ####
        self.SetImageFolderNameChoiceLabel = tk.Label(self, text = "Choose the corresponded images folder : ")
        self.SetImageFolderNameChoice = tk.StringVar()
        # Display the available folders with at least one image
        self.SetImageFolderNameChoiceOption = []
        file = os.listdir()
        for name in file:
            try :
                files = os.listdir(name)
                isImage = False
                for names in files :
                    image = cv2.imread(str(name) + "/" + names)
                    if image is not None :
                        isImage = True
                if isImage == True :
                    self.SetImageFolderNameChoiceOption.append(name)
            except :
                a = 1
        if len(self.SetImageFolderNameChoiceOption) == 0 :
            self.SetImageFolderNameChoiceOption = ["NULL"]
        self.SetImageFolderNameChoiceMenu = tk.OptionMenu(self, self.SetImageFolderNameChoice, *self.SetImageFolderNameChoiceOption, command = self.Get_SetImageFolderNameChoice)

        self.SetPixelLengthChoiceLabel = tk.Label(self, text = "        Define the length between 2 pixels (in meters) : ")
        self.SetPixelLengthChoiceEntry = tk.Entry(self)
        self.SetPixelLengthChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetPixelLengthChoice)
        
        self.SetImageHeightWallChoiceLabel = tk.Label(self, text = "        Define wall height (in meters) : ")
        self.SetImageHeightWallChoiceEntry = tk.Entry(self)
        self.SetImageHeightWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetImageHeightWallChoice)
        
        self.SetImageThicknessWallChoiceLabel = tk.Label(self, text = "        Define wall thickness (in meters) : ")
        self.SetImageThicknessWallChoiceEntry = tk.Entry(self)
        self.SetImageThicknessWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetImageThicknessWallChoice)

        self.SetImageTransparencyWallChoiceLabel = tk.Label(self, text = "        Define wall transparency (float between 0 and 1) : ")
        self.SetImageTransparencyWallChoiceEntry = tk.Entry(self)
        self.SetImageTransparencyWallChoiceSubmit = tk.Button(self, text = "Generate", command = self.Get_SetImageTransparencyWallChoice)
        
        # SINGLE WEBOTS WORLD
        
        #### DEFAULT CONFIGURATION ####
        self.DefaultConfigurationChoiceLabel = tk.Label(self, text = "About the default configuration : ")
        self.DefaultConfigurationChoice = tk.StringVar()
        self.DefaultConfigurationChoiceOption = ["Use", "Not used", "View", "Change"]
        self.DefaultConfigurationChoiceMenu = tk.OptionMenu(self, self.DefaultConfigurationChoice, *self.DefaultConfigurationChoiceOption, command = self.Get_DefaultConfigurationChoice)

        self.NewDefaultConfigurationChoiceLabel00 = tk.Label(self, text = "### Manual Mode ###")
        self.NewDefaultConfigurationChoiceLabel01 = tk.Label(self, text = "### Image Processing ###")
        self.NewDefaultConfigurationChoiceLabel02 = tk.Label(self, text = "### Wall Parameters ###")
        self.NewDefaultConfigurationChoiceLabel1 = tk.Label(self, text = "Number of cells on the x-axis (int between 2 and 100) : ")
        self.NewDefaultConfigurationChoiceEntry1 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceLabel2 = tk.Label(self, text = "Number of cells on the y-axis (int between 2 and 100) : ")
        self.NewDefaultConfigurationChoiceEntry2 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceLabel3 = tk.Label(self, text = "Threshold for the binary image (int between 0 and 255) : ")
        self.NewDefaultConfigurationChoiceEntry3 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceLabel4 = tk.Label(self, text = "Minimum number of points that can form a line (int > 0) : ")
        self.NewDefaultConfigurationChoiceEntry4 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceLabel5 = tk.Label(self, text = "Maximum gap between two points to be considered in the same line (int > 0) : ")
        self.NewDefaultConfigurationChoiceEntry5 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceLabel6 = tk.Label(self, text = "Angle for pseudo-vertical and pseudo-horizontal (0 <= int <= 45): ")
        self.NewDefaultConfigurationChoiceEntry6 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceLabel7 = tk.Label(self, text = "Maximum gap between two lines to be considered in the same line (int > 0) : ")
        self.NewDefaultConfigurationChoiceEntry7 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceLabel8 = tk.Label(self, text = "Maximum gap between two parellel lines to be considered as the same line (int > 0) : ")
        self.NewDefaultConfigurationChoiceEntry8 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceLabel9 = tk.Label(self, text = "Wall height (in meters) : ")
        self.NewDefaultConfigurationChoiceEntry9 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceLabel10 = tk.Label(self, text = "Wall thickness (in meters) : ")
        self.NewDefaultConfigurationChoiceEntry10 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceLabel11 = tk.Label(self, text = "Wall transparency (float between 0 and 1 | 1 for a transparent wall) : ")
        self.NewDefaultConfigurationChoiceEntry11 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_NewDefaultConfigurationChoice)

        self.ViewDefaultConfigurationChoiceLabel00 = tk.Label(self, text = "### Manual Mode ###")
        self.ViewDefaultConfigurationChoiceLabel01 = tk.Label(self, text = "### Image Processing ###")
        self.ViewDefaultConfigurationChoiceLabel02 = tk.Label(self, text = "### Wall Parameters ###")
        self.ViewDefaultConfigurationChoiceLabel1 = tk.Label(self, text = "Number of cells on the x-axis (int between 2 and 100) : ")
        self.ViewDefaultConfigurationChoiceLabel2 = tk.Label(self, text = "Number of cells on the y-axis (int between 2 and 100) : ")
        self.ViewDefaultConfigurationChoiceLabel3 = tk.Label(self, text = "Threshold for the binary image (int between 0 and 255) : ")
        self.ViewDefaultConfigurationChoiceLabel4 = tk.Label(self, text = "Minimum number of points that can form a line (int > 0) : ")
        self.ViewDefaultConfigurationChoiceLabel5 = tk.Label(self, text = "Maximum gap between two points to be considered in the same line (int > 0) : ")
        self.ViewDefaultConfigurationChoiceLabel6 = tk.Label(self, text = "Angle for pseudo-vertical and pseudo-horizontal (0 <= int <= 45): ")
        self.ViewDefaultConfigurationChoiceLabel7 = tk.Label(self, text = "Maximum gap between two lines to be considered in the same line (int > 0) : ")
        self.ViewDefaultConfigurationChoiceLabel8 = tk.Label(self, text = "Maximum gap between two parellel lines to be considered as the same line (int > 0) : ")
        self.ViewDefaultConfigurationChoiceLabel9 = tk.Label(self, text = "Wall height (in meters) : ")
        self.ViewDefaultConfigurationChoiceLabel10 = tk.Label(self, text = "Wall thickness (in meters) : ")
        self.ViewDefaultConfigurationChoiceLabel11 = tk.Label(self, text = "Wall transparency (float between 0 and 1 | 1 for a transparent wall) : ")

        #### MANUAL ####
        self.GridChoiceLabel = tk.Label(self, text = "Keep in mind that too many cells will result in a grid with very small cells.")
        self.GridXChoiceLabel = tk.Label(self, text = "        Number of cells on the x-axis (int between 2 and 100) : ")
        self.GridXChoiceEntry = tk.Entry(self)
        self.GridYChoiceLabel = tk.Label(self, text = "        Number of cells on the y-axis (int between 2 and 100) : ")
        self.GridYChoiceEntry = tk.Entry(self)
        self.GridChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_GridChoice)

        self.ManualOptionChoiceLabel = tk.Label(self, text = "Option for the Manual Mode : ")
        self.ManualOptionChoice = tk.StringVar()
        self.ManualOptionChoiceOption = ["Room Creation (Closed figure)", "Free (Pair of points)"]
        self.ManualOptionChoiceOptionMenu = tk.OptionMenu(self, self.ManualOptionChoice, *self.ManualOptionChoiceOption, command = self.Get_ManualOptionChoice)
 
        self.WorldNameChoiceLabel = tk.Label(self, text = "Give the name for the webots file : ")
        self.WorldNameChoiceEntry = tk.Entry(self)
        self.WorldNameChoiceSubmit = tk.Button(self, text = "Generate", command = self.Get_WorldNameChoice)

        self.HeightWallChoiceLabel = tk.Label(self, text = "Define wall height (in meters) : ")
        self.HeightWallChoiceEntry = tk.Entry(self)
        self.HeightWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_HeightWallChoice)
        
        self.ThicknessWallChoiceLabel = tk.Label(self, text = "Define wall thickness (in meters) : ")
        self.ThicknessWallChoiceEntry = tk.Entry(self)
        self.ThicknessWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_ThicknessWallChoice)

        self.TransparencyWallChoiceLabel = tk.Label(self, text = "Define wall transparency (float between 0 and 1 | 1 for a transparent wall) : ")
        self.TransparencyWallChoiceEntry = tk.Entry(self)
        self.TransparencyWallChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_TransparencytWallChoice)

        self.DeleteLineChoiceLabel = tk.Label(self, text = "Do you want to delete some lines ?")
        self.DeleteLineChoice = tk.StringVar()
        self.DeleteLineChoiceMenu = tk.OptionMenu(self, self.DeleteLineChoice, *self.YesNoOption, command = self.Get_DeleteLineChoice)

        self.LengthFigureChoiceLabel = tk.Label(self, text = "About the size of the final figure : ")
        self.LengthFigureChoice = tk.StringVar()
        self.LengthFigureChoiceOption = ["Define the total length of the figure", "Define the length of a line"]
        self.LengthFigureChoiceMenu = tk.OptionMenu(self, self.LengthFigureChoice, *self.LengthFigureChoiceOption, command = self.Get_LengthFigureChoice)

        self.ConstantLengthFigureChoiceLabel = tk.Label(self, text = "Define the total length of the figure (in meters), the width will be adjusted accordingly : ")
        self.ConstantLengthFigureChoiceEntry = tk.Entry(self)
        self.ConstantLengthFigureChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_ConstantLengthFigureChoice)
        
        self.LineLengthChoiceLabel = tk.Label(self, text = "Define the length of the line (in meters) : ")
        self.LineLengthChoiceEntry = tk.Entry(self)
        self.LineLengthChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_LineLengthChoice)
        
        #### WITH IMAGE ####
        self.ImageFolderNameChoiceLabel = tk.Label(self, text = "Choose the corresponded images folder : ")
        self.ImageFolderNameChoice = tk.StringVar()
        self.ImageFolderNameChoiceOption = []
        file = os.listdir()
        for name in file:
            try :
                files = os.listdir(name)
                isImage = False
                for names in files :
                    image = cv2.imread(str(name) + "/" + names)
                    if image is not None :
                        isImage = True
                if isImage == True :
                    self.ImageFolderNameChoiceOption.append(name)
            except :
                a = 1
        if len(self.ImageFolderNameChoiceOption) == 0 :
            self.ImageFolderNameChoiceOption = ["NULL"]
        self.ImageFolderNameChoiceMenu = tk.OptionMenu(self, self.ImageFolderNameChoice, *self.ImageFolderNameChoiceOption, command = self.Get_ImageFolderNameChoice)

        self.ImageNameChoiceLabel = tk.Label(self, text = "Choose the image file : ")
        self.ImageNameChoice = tk.StringVar()
        self.ImageNameChoiceOption = ["NULL"]
        self.ImageNameChoiceMenu = tk.OptionMenu(self, self.ImageNameChoice, *self.ImageNameChoiceOption, command = self.Get_ImageNameChoice)
        
        self.BinaryThresholdChoiceLabel0 = tk.Label(self, text = "Keep in mind that values above threshold are set to 255 (white) and those below are set to 0 (black).")
        self.BinaryThresholdChoiceLabel = tk.Label(self, text = "Threshold for the binary image (int between 0 and 255) : ")
        self.BinaryThresholdChoiceEntry = tk.Entry(self)
        self.BinaryThresholdChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_BinaryThresholdChoice)
        
        self.LineDetectionChoiceLabel = tk.Label(self, text = "Minimum number of points (ie pixels) that can form a line (int). Lines with less than this number of points are disregarded :")
        self.LineDetectionChoiceEntry = tk.Entry(self)
        self.LineDetectionChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_LineDetectionChoice)
        
        self.GapLineDetectionChoiceLabel = tk.Label(self, text = "Maximum gap between two points to be considered in the same line (int) : ")
        self.GapLineDetectionChoiceEntry = tk.Entry(self)
        self.GapLineDetectionChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_GapLineDetectionChoice)
        
        self.AngleChoiceLabel = tk.Label(self, text = "Maximum angle of a line in relation to the vertical or horizontal to be considered as a vertical or horizontal line (int between 0 and 45) : ")
        self.AngleChoiceEntry = tk.Entry(self)
        self.AngleChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_AngleChoice)
        
        self.GapSameLineLabel = tk.Label(self, text = "Maximum gap between two lines to be considered in the same line (int) : ")
        self.GapSameLineEntry = tk.Entry(self)
        self.GapSameLineSubmit = tk.Button(self, text = "Submit", command = self.Get_GapSameLine)

        self.GapParallelLineLabel = tk.Label(self, text = "Maximum gap between two parellel lines to be considered as the same line (int) : ")
        self.GapParallelLineEntry = tk.Entry(self)
        self.GapParallelLineSubmit = tk.Button(self, text = "Submit", command = self.Get_GapParallelLine)
        
        self.mainloop()
        
    def Display_SetChoice(self) :
        self.SetChoiceLabel.grid(column = 0, row = 0, sticky = tk.W, **self.paddings)
        self.SetChoiceMenu.grid(column = 1, row = 0, sticky = tk.W, **self.paddings)
        
    # Choice between a Single Webots World or a Set of Webots World
    def Get_SetChoice(self, Choice) :
        self.Delete_AllSetWithoutImage(17)
        self.Delete_AllSetWithImage(4)
        self.Delete_AllWithoutImage(11)
        self.Delete_AllWithImage(7)
        self.Delete_FeatureChoice()
        self.Delete_SetFeatureChoice()
        # We retrieve the choice with get
        Choice = self.SetChoice.get()
        if Choice == '1+' :
            self.Display_SetFeatureChoice()
        elif Choice == '1' :
            self.Display_FeatureChoice()

    ############# SET OF WEBOTS WORLD ####################
    # Choice between using an image set or not 
    def Display_SetFeatureChoice(self) : 
        self.SetFeatureChoiceLabel.grid(column = 0, row = 1, sticky = tk.W, **self.paddings)
        
        self.SetFeatureChoice = tk.StringVar()
        self.SetFeatureChoiceMenu = tk.OptionMenu(self, self.SetFeatureChoice, *self.SetFeatureChoiceOption, command = self.Get_SetFeatureChoice)
        self.SetFeatureChoiceMenu.grid(column = 1, row = 1, sticky = tk.W, **self.paddings)
    
    def Delete_SetFeatureChoice(self) :
        self.SetFeatureChoiceLabel.grid_remove()
        self.SetFeatureChoiceMenu.grid_remove()

    def Get_SetFeatureChoice(self, Choice) :
        self.Delete_AllSetWithoutImage(17)
        self.Delete_AllSetWithImage(4)
        Choice = self.SetFeatureChoice.get()
        if Choice == 'Random' :
            self.Display_SetWallChoice()
        elif Choice == 'Images' :
            if len(self.SetImageFolderNameChoiceOption) == 1 :
                if self.SetImageFolderNameChoiceOption[0] == "NULL" :
                    self.Message = tk.Message(self, text = "No folder found")
                    self.Message.grid(column = 3, row = 1, sticky = tk.W, **self.paddings)
                else :
                    self.Display_SetImageFolderNameChoice()
            else : 
                self.Display_SetImageFolderNameChoice()
                
    # Wall Option
    def Display_SetWallChoice(self) :
        self.SetWallChoiceLabel.grid(column = 0, row = 2, sticky = tk.W, **self.paddings)
        
        self.SetWallChoice = tk.StringVar()
        self.SetWallChoiceMenu = tk.OptionMenu(self, self.SetWallChoice, *self.ConstantVariableOption, command = self.Get_SetWallChoice)
        self.SetWallChoiceMenu.grid(column = 1, row = 2, sticky = tk.W, **self.paddings)
        
    def Delete_SetWallChoice(self) :
        self.SetWallChoiceLabel.grid_remove()
        self.SetWallChoiceMenu.grid_remove()
        
    def Get_SetWallChoice(self, Choice) :
        self.Delete_AllSetWithoutImage(16)
        Choice = self.SetWallChoice.get()
        if Choice == 'Constant' :
            self.Display_SetConstantWallChoice()
        elif Choice == 'Variable' :
            self.Display_SetRangeWallChoice()
            
    # Constant number of walls (int)
    def Display_SetConstantWallChoice(self) :
        self.SetConstantWallChoiceLabel.grid(column = 0, row = 3, sticky = tk.W, **self.paddings)
        
        self.SetConstantWallChoiceEntry = tk.Entry(self)
        self.SetConstantWallChoiceEntry.grid(column = 1, row = 3, sticky = tk.W, **self.paddings)
        
        self.SetConstantWallChoiceSubmit.grid(column = 2, row = 3, sticky = tk.W, **self.paddings)
        
    def Delete_SetConstantWallChoice(self) :
        self.SetConstantWallChoiceLabel.grid_remove()
        self.SetConstantWallChoiceEntry.grid_remove()
        self.SetConstantWallChoiceSubmit.grid_remove()
        
    def Get_SetConstantWallChoice(self) :
        self.Delete_AllSetWithoutImage(15)
        Choice = self.SetConstantWallChoiceEntry.get()
        isOK = TF.isPositiveInteger(Choice)
        if isOK == True :
            self.Display_SetFigureChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive integer")
            self.Message.grid(column = 3, row = 3, sticky = tk.W, **self.paddings)
            
    # Number of walls between a value range (int)
    def Display_SetRangeWallChoice(self) :
        self.SetMinWallChoiceLabel.grid(column = 0, row = 3, sticky = tk.W, **self.paddings)
        self.SetMinWallChoiceEntry = tk.Entry(self)
        self.SetMinWallChoiceEntry.grid(column = 1, row = 3, sticky = tk.W, **self.paddings)
        
        self.SetMaxWallChoiceLabel.grid(column = 0, row = 4, sticky = tk.W, **self.paddings)
        self.SetMaxWallChoiceEntry = tk.Entry(self)
        self.SetMaxWallChoiceEntry.grid(column = 1, row = 4, sticky = tk.W, **self.paddings)
        
        self.SetRangeWallChoiceSubmit.grid(column = 2, row = 4, sticky = tk.W, **self.paddings)
        
    def Delete_SetRangeWallChoice(self) :
        self.SetMinWallChoiceLabel.grid_remove()
        self.SetMinWallChoiceEntry.grid_remove()
        self.SetMaxWallChoiceLabel.grid_remove()
        self.SetMaxWallChoiceEntry.grid_remove()
        self.SetRangeWallChoiceSubmit.grid_remove()
        
    def Get_SetRangeWallChoice(self) :
        self.Delete_AllSetWithoutImage(15)
        Choice1 = self.SetMinWallChoiceEntry.get()
        Choice2 = self.SetMaxWallChoiceEntry.get()
        isOK1 = TF.isPositiveInteger(Choice1)
        isOK2 = TF.isPositiveInteger(Choice2)
        if isOK1 == True and isOK2 == True :
            if int(Choice2) > int(Choice1) : 
                self.Display_SetFigureChoice()
            else :
                self.Message = tk.Message(self, text = "Max value must be greater than Min value")
                self.Message.grid(column = 3, row = 4, sticky = tk.W, **self.paddings)
        else :
            self.Message = tk.Message(self, text = "Not two positive integer")
            self.Message.grid(column = 3, row = 4, sticky = tk.W, **self.paddings)
    
    # Figure shape Option
    def Display_SetFigureChoice(self) :
        self.SetFigureChoiceLabel.grid(column = 0, row = 5, sticky = tk.W, **self.paddings)
        
        self.SetFigureChoice = tk.StringVar()
        self.SetFigureChoiceMenu = tk.OptionMenu(self, self.SetFigureChoice, *self.SetFigureChoiceOption, command = self.Get_SetFigureChoice)
        self.SetFigureChoiceMenu.grid(column = 1, row = 5, sticky = tk.W, **self.paddings)
        
    def Delete_SetFigureChoice(self) :
        self.SetFigureChoiceLabel.grid_remove()
        self.SetFigureChoiceMenu.grid_remove()
        
    def Get_SetFigureChoice(self, Choice) :
        self.Delete_AllSetWithoutImage(14)
        self.Display_SetWallCrossingChoice()
        
    # Wall Crossing Option
    def Display_SetWallCrossingChoice(self) :
        self.SetWallCrossingChoiceLabel.grid(column = 0, row = 6, sticky = tk.W, **self.paddings)
        
        self.SetWallCrossingChoice = tk.StringVar()
        self.SetWallCrossingChoiceMenu = tk.OptionMenu(self, self.SetWallCrossingChoice, *self.YesNoOption, command = self.Get_SetWallCrossingChoice)
        self.SetWallCrossingChoiceMenu.grid(column = 1, row = 6, sticky = tk.W, **self.paddings)

    def Delete_SetWallCrossingChoice(self) :
        self.SetWallCrossingChoiceLabel.grid_remove()
        self.SetWallCrossingChoiceMenu.grid_remove()
        
    def Get_SetWallCrossingChoice(self, Choice) :
        self.Delete_AllSetWithoutImage(13)
        self.Display_SetDiagonalMovementChoice()
        
    # Diagonal Movement Option
    def Display_SetDiagonalMovementChoice(self) :
        self.SetDiagonalMovementChoiceLabel.grid(column = 0, row = 7, sticky = tk.W, **self.paddings)
        
        self.SetDiagonalMovementChoice = tk.StringVar()
        self.SetDiagonalMovementChoiceMenu = tk.OptionMenu(self, self.SetDiagonalMovementChoice, *self.YesNoOption, command = self.Get_SetDiagonalMovementChoice)
        self.SetDiagonalMovementChoiceMenu.grid(column = 1, row = 7, sticky = tk.W, **self.paddings)
    
    def Delete_SetDiagonalMovementChoice(self) :
        self.SetDiagonalMovementChoiceLabel.grid_remove()
        self.SetDiagonalMovementChoiceMenu.grid_remove()
        
    def Get_SetDiagonalMovementChoice(self, Choice) :
        self.Delete_AllSetWithoutImage(12)
        Choice = self.SetDiagonalMovementChoice.get()
        if Choice == 'Yes' :
            self.Display_SetFirstDirection2Choice()
        elif Choice == 'No' :
            self.Display_SetFirstDirection1Choice()
        
    # Direction for the first Wall
    def Display_SetFirstDirection1Choice(self) :
        self.SetFirstDirectionChoiceLabel.grid(column = 0, row = 8, sticky = tk.W, **self.paddings)
        
        self.SetFirstDirectionChoice = tk.StringVar()
        self.SetFirstDirectionChoiceMenu = tk.OptionMenu(self, self.SetFirstDirectionChoice, *self.SetFirstDirectionChoice1Option, command = self.Get_SetFirstDirectionChoice)
        self.SetFirstDirectionChoiceMenu.grid(column = 1, row = 8, sticky = tk.W, **self.paddings)
        
    def Display_SetFirstDirection2Choice(self) :
        self.SetFirstDirectionChoiceLabel.grid(column = 0, row = 8, sticky = tk.W, **self.paddings)
        
        self.SetFirstDirectionChoice = tk.StringVar()
        self.SetFirstDirectionChoiceMenu = tk.OptionMenu(self, self.SetFirstDirectionChoice, *self.SetFirstDirectionChoice2Option, command = self.Get_SetFirstDirectionChoice)
        self.SetFirstDirectionChoiceMenu.grid(column = 1, row = 8, sticky = tk.W, **self.paddings)
        
    def Delete_SetFirstDirectionChoice(self) :
        self.SetFirstDirectionChoiceLabel.grid_remove()
        self.SetFirstDirectionChoiceMenu.grid_remove()
           
    def Get_SetFirstDirectionChoice(self, Choice) :
        self.Delete_AllSetWithoutImage(11)
        self.Display_SetProbaSameDirectionChoice()
        
    # Same direction probability (int)
    def Display_SetProbaSameDirectionChoice(self) :
        self.SetProbaSameDirectionChoiceLabel.grid(column = 0, row = 9, sticky = tk.W, **self.paddings)
        
        self.SetProbaSameDirectionChoiceEntry = tk.Entry(self)
        self.SetProbaSameDirectionChoiceEntry.grid(column = 1, row = 9, sticky = tk.W, **self.paddings)
        
        self.SetProbaSameDirectionChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetProbaSameDirectionChoice)
        self.SetProbaSameDirectionChoiceSubmit.grid(column = 2, row = 9, sticky = tk.W, **self.paddings)
        
    def Delete_SetProbaSameDirectionChoice(self) :
        self.SetProbaSameDirectionChoiceLabel.grid_remove()
        self.SetProbaSameDirectionChoiceEntry.grid_remove()
        self.SetProbaSameDirectionChoiceSubmit.grid_remove()
        
    def Get_SetProbaSameDirectionChoice(self) :
        self.Delete_AllSetWithoutImage(10)
        Choice = self.SetProbaSameDirectionChoiceEntry.get()
        isOK = TF.isPositiveInteger(Choice)
        if isOK == True :
            if int(Choice) >= 1 and int(Choice) <= 99 : 
                self.Display_SetMatrixIJChoice()
            else :
                self.Message = tk.Message(self, text = "Not an expetected integer")
                self.Message.grid(column = 3, row = 9, sticky = tk.W, **self.paddings)
        else :
            self.Message = tk.Message(self, text = "Not a positive integer")
            self.Message.grid(column = 3, row = 9, sticky = tk.W, **self.paddings)
            
    # Matrix Size (int)
    def Display_SetMatrixIJChoice(self) :
        self.SetMatrixChoiceLabel.grid(column = 0, row = 10, sticky = tk.W, **self.paddings)
        
        self.SetMatrixJChoiceLabel.grid(column = 0, row = 11, sticky = tk.W, **self.paddings)
        self.SetMatrixJChoiceEntry = tk.Entry(self)
        self.SetMatrixJChoiceEntry.grid(column = 1, row = 11, sticky = tk.W, **self.paddings)
        
        self.SetMatrixIChoiceLabel.grid(column = 0, row = 12, sticky = tk.W, **self.paddings)
        self.SetMatrixIChoiceEntry = tk.Entry(self)
        self.SetMatrixIChoiceEntry.grid(column = 1, row = 12, sticky = tk.W, **self.paddings)
        
        self.SetMatrixChoiceSubmit = tk.Button(self, text = "Submit", command = self.Get_SetMatrixIJChoice)
        self.SetMatrixChoiceSubmit.grid(column = 2, row = 12, sticky = tk.W, **self.paddings)
    
    def Delete_SetMatrixIJChoice(self) :
        self.SetMatrixChoiceLabel.grid_remove()
        self.SetMatrixJChoiceLabel.grid_remove()
        self.SetMatrixJChoiceEntry.grid_remove()
        self.SetMatrixIChoiceLabel.grid_remove()
        self.SetMatrixIChoiceEntry.grid_remove()
        self.SetMatrixChoiceSubmit.grid_remove()
        
    def Get_SetMatrixIJChoice(self) :
        self.Delete_AllSetWithoutImage(9)
        Choice1 = self.SetMatrixJChoiceEntry.get()
        Choice2 = self.SetMatrixIChoiceEntry.get()
        isOK1 = TF.isPositiveInteger(Choice1)
        isOK2 = TF.isPositiveInteger(Choice2)
        if isOK1 == True and isOK2 == True :
            if int(Choice1) > 2 and int(Choice2) > 2 : 
                self.Display_SetLengthChoice()
            else :
                self.Message = tk.Message(self, text = "Not an expected int")
                self.Message.grid(column = 3, row = 12, sticky = tk.W, **self.paddings)
        else :
            self.Message = tk.Message(self, text = "Not two positive integer")
            self.Message.grid(column = 3, row = 12, sticky = tk.W, **self.paddings)
        
    # Figure Length Option
    def Display_SetLengthChoice(self) :
        self.SetLengthChoiceLabel.grid(column = 0, row = 13, sticky = tk.W, **self.paddings)
        
        self.SetLengthChoice = tk.StringVar()
        self.SetLengthChoiceMenu = tk.OptionMenu(self, self.SetLengthChoice, *self.SetLengthChoiceOption, command = self.Get_SetLengthChoice)
        self.SetLengthChoiceMenu.grid(column = 1, row = 13, sticky = tk.W, **self.paddings)
        
    def Delete_SetLengthChoice(self) :
        self.SetLengthChoiceLabel.grid_remove()
        self.SetLengthChoiceMenu.grid_remove()

    def Get_SetLengthChoice(self, Choice) :
        self.Delete_AllSetWithoutImage(8)
        Choice = self.SetLengthChoice.get()
        if Choice == 'Constant' :
            self.Display_SetConstantLengthChoice()
        elif Choice == 'Variable' :
            self.Display_SetRangeLengthChoice()
        elif Choice == 'Random' :
            self.Display_SetCellLengthChoice()
            
    # Constant figure length (float)
    def Display_SetConstantLengthChoice(self) :
        self.SetConstantLengthChoiceLabel.grid(column = 0, row = 14, sticky = tk.W, **self.paddings)
        
        self.SetConstantLengthChoiceEntry = tk.Entry(self)
        self.SetConstantLengthChoiceEntry.grid(column = 1, row = 14, sticky = tk.W, **self.paddings)
        self.SetConstantLengthChoiceSubmit.grid(column = 2, row = 14, sticky = tk.W, **self.paddings)
        
    def Delete_SetConstantLengthChoice(self) :
        self.SetConstantLengthChoiceLabel.grid_remove()
        self.SetConstantLengthChoiceEntry.grid_remove()
        self.SetConstantLengthChoiceSubmit.grid_remove()
        
    def Get_SetConstantLengthChoice(self) :
        self.Delete_AllSetWithoutImage(7)
        Choice = self.SetConstantLengthChoiceEntry.get()
        isOK = TF.isPositiveFloat(Choice)
        if isOK == True :
            self.Display_SetHeightWallChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive float")
            self.Message.grid(column = 3, row = 14, sticky = tk.W, **self.paddings)
            
    # Figure length between value range (float)
    def Display_SetRangeLengthChoice(self) :
        self.SetMinLengthChoiceLabel.grid(column = 0, row = 14, sticky = tk.W, **self.paddings)
        self.SetMinLengthChoiceEntry = tk.Entry(self)
        self.SetMinLengthChoiceEntry.grid(column = 1, row = 14, sticky = tk.W, **self.paddings)
        
        self.SetMaxLengthChoiceLabel.grid(column = 0, row = 15, sticky = tk.W, **self.paddings)
        self.SetMaxLengthChoiceEntry = tk.Entry(self)
        self.SetMaxLengthChoiceEntry.grid(column = 1, row = 15, sticky = tk.W, **self.paddings)
        
        self.SetStepLengthChoiceLabel.grid(column = 0, row = 16, sticky = tk.W, **self.paddings)
        self.SetStepLengthChoiceEntry = tk.Entry(self)
        self.SetStepLengthChoiceEntry.grid(column = 1, row = 16, sticky = tk.W, **self.paddings)
        
        self.SetRangeLengthChoiceSubmit.grid(column = 2, row = 16, sticky = tk.W, **self.paddings)
        
    def Delete_SetRangeLengthChoice(self) :
        self.SetMinLengthChoiceLabel.grid_remove()
        self.SetMinLengthChoiceEntry.grid_remove()
        self.SetMaxLengthChoiceLabel.grid_remove()
        self.SetMaxLengthChoiceEntry.grid_remove()
        self.SetStepLengthChoiceLabel.grid_remove()
        self.SetStepLengthChoiceEntry.grid_remove()
        self.SetRangeLengthChoiceSubmit.grid_remove()
        
    def Get_SetRangeLengthChoice(self) :
        self.Delete_AllSetWithoutImage(7)
        Choice1 = self.SetMinLengthChoiceEntry.get()
        Choice2 = self.SetMaxLengthChoiceEntry.get()
        Step = self.SetStepLengthChoiceEntry.get()
        isOK1 = TF.isPositiveFloat(Choice1)
        isOK2 = TF.isPositiveFloat(Choice2)
        isOK = TF.isPositiveFloat(Step)
        if isOK1 == True and isOK2 == True and isOK == True :
            if float(Choice2) > float(Choice1) : 
                if TF.isPositiveInteger(float(float(Choice2) - float(Choice1)) / float(Step)) == True :
                    self.Display_SetHeightWallChoice()
                else : 
                    self.Message = tk.Message(self, text = "Step value must be a multiple of the difference between the two lengths")
                    self.Message.grid(column = 3, row = 16, sticky = tk.W, **self.paddings)
            else :
                self.Message = tk.Message(self, text = "Max value must be greater than Min value")
                self.Message.grid(column = 3, row = 16, sticky = tk.W, **self.paddings)
        else :
            self.Message = tk.Message(self, text = "Not all positive float")
            self.Message.grid(column = 3, row = 16, sticky = tk.W, **self.paddings)
        
    # Length for one cell
    def Display_SetCellLengthChoice(self) :
        self.SetCellLengthChoiceLabel.grid(column = 0, row = 14, sticky = tk.W, **self.paddings)
        
        self.SetCellLengthChoiceEntry = tk.Entry(self)
        self.SetCellLengthChoiceEntry.grid(column = 1, row = 14, sticky = tk.W, **self.paddings)
        self.SetCellLengthChoiceSubmit.grid(column = 2, row = 14, sticky = tk.W, **self.paddings)
        
    def Delete_SetCellLengthChoice(self) :
        self.SetCellLengthChoiceLabel.grid_remove()
        self.SetCellLengthChoiceEntry.grid_remove()
        self.SetCellLengthChoiceSubmit.grid_remove()
        
    def Get_SetCellLengthChoice(self) :
        self.Delete_AllSetWithoutImage(7)
        Choice = self.SetCellLengthChoiceEntry.get()
        isOK = TF.isPositiveFloat(Choice)
        if isOK == True :
            self.Display_SetHeightWallChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive float")
            self.Message.grid(column = 3, row = 14, sticky = tk.W, **self.paddings)
        
    # Height Wall Option
    def Display_SetHeightWallChoice(self) :
        self.SetHeightWallChoiceLabel.grid(column = 4, row = 2, sticky = tk.W, **self.paddings)
        
        self.SetHeightWallChoice = tk.StringVar()
        self.SetHeightWallChoiceMenu = tk.OptionMenu(self, self.SetHeightWallChoice, *self.ConstantVariableOption, command = self.Get_SetHeightWallChoice)
        self.SetHeightWallChoiceMenu.grid(column = 5, row = 2, sticky = tk.W, **self.paddings)
        
    def Delete_SetHeightWallChoice(self) :
        self.SetHeightWallChoiceLabel.grid_remove()
        self.SetHeightWallChoiceMenu.grid_remove()
        
    def Get_SetHeightWallChoice(self, Choice) :
        self.Delete_AllSetWithoutImage(6)
        Choice = self.SetHeightWallChoice.get()
        if Choice == 'Constant' :
            self.Display_SetConstantHeightWallChoice()
        elif Choice == 'Variable' :
            self.Display_SetRangeHeightWallChoice()
            
    # Constant Height Wall (float)
    def Display_SetConstantHeightWallChoice(self) :
        self.SetConstantHeightWallChoiceLabel.grid(column = 4, row = 3, sticky = tk.W, **self.paddings)
        
        self.SetConstantHeightWallChoiceEntry = tk.Entry(self)
        self.SetConstantHeightWallChoiceEntry.grid(column = 5, row = 3, sticky = tk.W, **self.paddings)
        self.SetConstantHeightWallChoiceSubmit.grid(column = 6, row = 3, sticky = tk.W, **self.paddings)
    
    def Delete_SetConstantHeightWallChoice(self) :
        self.SetConstantHeightWallChoiceLabel.grid_remove()
        self.SetConstantHeightWallChoiceEntry.grid_remove()
        self.SetConstantHeightWallChoiceSubmit.grid_remove()
        
    def Get_SetConstantHeightWallChoice(self) :
        self.Delete_AllSetWithoutImage(5)
        Choice = self.SetConstantHeightWallChoiceEntry.get()
        isOK = TF.isPositiveFloat(Choice)
        if isOK == True :
            self.Display_SetThicknessWallChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive float")
            self.Message.grid(column = 7, row = 3, sticky = tk.W, **self.paddings)
        
    # Height Wall between value range (float)
    def Display_SetRangeHeightWallChoice(self) :
        self.SetMinHeightWallChoiceLabel.grid(column = 4, row = 3, sticky = tk.W, **self.paddings)
        self.SetMinHeightWallChoiceEntry = tk.Entry(self)
        self.SetMinHeightWallChoiceEntry.grid(column = 5, row = 3, sticky = tk.W, **self.paddings)
        
        self.SetMaxHeightWallChoiceLabel.grid(column = 4, row = 4, sticky = tk.W, **self.paddings)
        self.SetMaxHeightWallChoiceEntry = tk.Entry(self)
        self.SetMaxHeightWallChoiceEntry.grid(column = 5, row = 4, sticky = tk.W, **self.paddings)
        
        self.SetStepHeightWallChoiceLabel.grid(column = 4, row = 5, sticky = tk.W, **self.paddings)
        self.SetStepHeightWallChoiceEntry = tk.Entry(self)
        self.SetStepHeightWallChoiceEntry.grid(column = 5, row = 5, sticky = tk.W, **self.paddings)
        
        self.SetRangeHeightWallChoiceSubmit.grid(column = 6, row = 5, sticky = tk.W, **self.paddings)
        
    def Delete_SetRangeHeightWallChoice(self) :
        self.SetMinHeightWallChoiceLabel.grid_remove()
        self.SetMinHeightWallChoiceEntry.grid_remove()
        self.SetMaxHeightWallChoiceLabel.grid_remove()
        self.SetMaxHeightWallChoiceEntry.grid_remove()
        self.SetStepHeightWallChoiceLabel.grid_remove()
        self.SetStepHeightWallChoiceEntry.grid_remove()
        self.SetRangeHeightWallChoiceSubmit.grid_remove()
        
    def Get_SetRangeHeightWallChoice(self) :
        self.Delete_AllSetWithoutImage(5)
        Choice1 = self.SetMinHeightWallChoiceEntry.get()
        Choice2 = self.SetMaxHeightWallChoiceEntry.get()
        Step = self.SetStepHeightWallChoiceEntry.get()
        isOK1 = TF.isPositiveFloat(Choice1)
        isOK2 = TF.isPositiveFloat(Choice2)
        isOK = TF.isPositiveFloat(Step)
        if isOK1 == True and isOK2 == True and isOK == True :
            if float(Choice2) > float(Choice1) : 
                if TF.isPositiveInteger(float(float(Choice2) - float(Choice1)) / float(Step)) == True :
                    self.Display_SetThicknessWallChoice()
                else : 
                    self.Message = tk.Message(self, text = "Step value must be a multiple of the difference between the two heights")
                    self.Message.grid(column = 7, row = 5, sticky = tk.W, **self.paddings)
            else :
                self.Message = tk.Message(self, text = "Max value must be greater than Min value")
                self.Message.grid(column = 7, row = 5, sticky = tk.W, **self.paddings)
        else :
            self.Message = tk.Message(self, text = "Not all positive float")
            self.Message.grid(column = 7, row = 5, sticky = tk.W, **self.paddings)
        
    # Thickness Wall Option
    def Display_SetThicknessWallChoice(self) :
        self.SetThicknessWallChoiceLabel.grid(column = 4, row = 6, sticky = tk.W, **self.paddings)
        
        self.SetThicknessWallChoice = tk.StringVar()
        self.SetThicknessWallChoiceMenu = tk.OptionMenu(self, self.SetThicknessWallChoice, *self.ConstantVariableOption, command = self.Get_SetThicknessWallChoice)
        self.SetThicknessWallChoiceMenu.grid(column = 5, row = 6, sticky = tk.W, **self.paddings)
    
    def Delete_SetThicknessWallChoice(self) :
        self.SetThicknessWallChoiceLabel.grid_remove()
        self.SetThicknessWallChoiceMenu.grid_remove()
        
    def Get_SetThicknessWallChoice(self, Choice) :
        self.Delete_AllSetWithoutImage(4)
        Choice = self.SetThicknessWallChoice.get()
        if Choice == 'Constant' :
            self.Display_SetConstantThicknessWallChoice()
        elif Choice == 'Variable' :
            self.Display_SetRangeThicknessWallChoice()
            
    # Constant Thickness Wall (float)
    def Display_SetConstantThicknessWallChoice(self) :
        self.SetConstantThicknessWallChoiceLabel.grid(column = 4, row = 7, sticky = tk.W, **self.paddings)
        
        self.SetConstantThicknessWallChoiceEntry = tk.Entry(self)
        self.SetConstantThicknessWallChoiceEntry.grid(column = 5, row = 7, sticky = tk.W, **self.paddings)
        
        self.SetConstantThicknessWallChoiceSubmit.grid(column = 6, row = 7, sticky = tk.W, **self.paddings)
    
    def Delete_SetConstantThicknessWallChoice(self) :
        self.SetConstantThicknessWallChoiceLabel.grid_remove()
        self.SetConstantThicknessWallChoiceEntry.grid_remove()
        self.SetConstantThicknessWallChoiceSubmit.grid_remove()
        
    def Get_SetConstantThicknessWallChoice(self) :
        self.Delete_AllSetWithoutImage(3)
        Choice = self.SetConstantThicknessWallChoiceEntry.get()
        isOK = TF.isPositiveFloat(Choice)
        if isOK == True :
            self.Display_SetTransparencyWallChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive float")
            self.Message.grid(column = 7, row = 7, sticky = tk.W, **self.paddings)
            
    # Thickness Wall between value range (float)
    def Display_SetRangeThicknessWallChoice(self) :
        self.SetMinThicknessWallChoiceLabel.grid(column = 4, row = 7, sticky = tk.W, **self.paddings)
        self.SetMinThicknessWallChoiceEntry = tk.Entry(self)
        self.SetMinThicknessWallChoiceEntry.grid(column = 5, row = 7, sticky = tk.W, **self.paddings)
        
        self.SetMaxThicknessWallChoiceLabel.grid(column = 4, row = 8, sticky = tk.W, **self.paddings)
        self.SetMaxThicknessWallChoiceEntry = tk.Entry(self)
        self.SetMaxThicknessWallChoiceEntry.grid(column = 5, row = 8, sticky = tk.W, **self.paddings)
        
        self.SetStepThicknessWallChoiceLabel.grid(column = 4, row = 9, sticky = tk.W, **self.paddings)
        self.SetStepThicknessWallChoiceEntry = tk.Entry(self)
        self.SetStepThicknessWallChoiceEntry.grid(column = 5, row = 9, sticky = tk.W, **self.paddings)
        
        self.SetRangeThicknessWallChoiceSubmit.grid(column = 6, row = 9, sticky = tk.W, **self.paddings)
    
    def Delete_SetRangeThicknessWallChoice(self) :
        self.SetMinThicknessWallChoiceLabel.grid_remove()
        self.SetMinThicknessWallChoiceEntry.grid_remove()
        self.SetMaxThicknessWallChoiceLabel.grid_remove()
        self.SetMaxThicknessWallChoiceEntry.grid_remove()
        self.SetStepThicknessWallChoiceLabel.grid_remove()
        self.SetStepThicknessWallChoiceEntry.grid_remove()
        self.SetRangeThicknessWallChoiceSubmit.grid_remove()
        
    def Get_SetRangeThicknessWallChoice(self) :
        self.Delete_AllSetWithoutImage(3)
        Choice1 = self.SetMinThicknessWallChoiceEntry.get()
        Choice2 = self.SetMaxThicknessWallChoiceEntry.get()
        Step = self.SetStepThicknessWallChoiceEntry.get()
        isOK1 = TF.isPositiveFloat(Choice1)
        isOK2 = TF.isPositiveFloat(Choice2)
        isOK = TF.isPositiveFloat(Step)
        if isOK1 == True and isOK2 == True and isOK == True :
            if float(Choice2) > float(Choice1) : 
                if TF.isPositiveInteger(float(float(Choice2) - float(Choice1)) / float(Step)) == True :
                    self.Display_SetTransparencyWallChoice()
                else : 
                    self.Message = tk.Message(self, text = "Step value must be a multiple of the difference between the two thickness")
                    self.Message.grid(column = 7, row = 9, sticky = tk.W, **self.paddings)
            else :
                self.Message = tk.Message(self, text = "Max value must be greater than Min value")
                self.Message.grid(column = 7, row = 9, sticky = tk.W, **self.paddings)
        else :
            self.Message = tk.Message(self, text = "Not all positive float")
            self.Message.grid(column = 7, row = 9, sticky = tk.W, **self.paddings)
        
    # Transparency Wall Option
    def Display_SetTransparencyWallChoice(self) :
        self.SetTransparencyWallChoiceLabel.grid(column = 4, row = 10, sticky = tk.W, **self.paddings)
        
        self.SetTransparencyWallChoice = tk.StringVar()
        self.SetTransparencyWallChoiceMenu = tk.OptionMenu(self, self.SetTransparencyWallChoice, *self.ConstantVariableOption, command = self.Get_SetTransparencyWallChoice)
        self.SetTransparencyWallChoiceMenu.grid(column = 5, row = 10, sticky = tk.W, **self.paddings)
        
    def Delete_SetTransparencyWallChoice(self) :
        self.SetTransparencyWallChoiceLabel.grid_remove()
        self.SetTransparencyWallChoiceMenu.grid_remove()
        
    def Get_SetTransparencyWallChoice(self, Choice) :
        self.Delete_AllSetWithoutImage(2)
        Choice = self.SetTransparencyWallChoice.get()
        if Choice == 'Constant' :
            self.Display_SetConstantTransparencyWallChoice()
        elif Choice == 'Variable' :
            self.Display_SetRangeTransparencyWallChoice()
            
    # Constant Transparency Wall (float)
    def Display_SetConstantTransparencyWallChoice(self) :
        self.SetConstantTransparencyWallChoiceLabel.grid(column = 4, row = 11, sticky = tk.W, **self.paddings)
        
        self.SetConstantTransparencyWallChoiceEntry = tk.Entry(self)
        self.SetConstantTransparencyWallChoiceEntry.grid(column = 5, row = 11, sticky = tk.W, **self.paddings)
        
        self.SetConstantTransparencyWallChoiceSubmit.grid(column = 6, row = 11, sticky = tk.W, **self.paddings)
    
    def Delete_SetConstantTransparencyWallChoice(self) :
        self.SetConstantTransparencyWallChoiceLabel.grid_remove()
        self.SetConstantTransparencyWallChoiceEntry.grid_remove()
        self.SetConstantTransparencyWallChoiceSubmit.grid_remove()
        
    def Get_SetConstantTransparencyWallChoice(self) :
        self.Delete_AllSetWithoutImage(1)
        Choice = self.SetConstantTransparencyWallChoiceEntry.get()
        isOK = TF.is01Float(Choice)
        if isOK == True :
            self.Display_SetNumberWorldChoice()
        else :
            self.Message = tk.Message(self, text = "Not an expected float")
            self.Message.grid(column = 7, row = 11, sticky = tk.W, **self.paddings)
            
    # Transparency Wall between value range (float)
    def Display_SetRangeTransparencyWallChoice(self) :
        self.SetMinTransparencyWallChoiceLabel.grid(column = 4, row = 11, sticky = tk.W, **self.paddings)
        self.SetMinTransparencyWallChoiceEntry = tk.Entry(self)
        self.SetMinTransparencyWallChoiceEntry.grid(column = 5, row = 11, sticky = tk.W, **self.paddings)
        
        self.SetMaxTransparencyWallChoiceLabel.grid(column = 4, row = 12, sticky = tk.W, **self.paddings)
        self.SetMaxTransparencyWallChoiceEntry = tk.Entry(self)
        self.SetMaxTransparencyWallChoiceEntry.grid(column = 5, row = 12, sticky = tk.W, **self.paddings)
        
        self.SetStepTransparencyWallChoiceLabel.grid(column = 4, row = 13, sticky = tk.W, **self.paddings)
        self.SetStepTransparencyWallChoiceEntry = tk.Entry(self)
        self.SetStepTransparencyWallChoiceEntry.grid(column = 5, row = 13, sticky = tk.W, **self.paddings)
        
        self.SetRangeTransparencyWallChoiceSubmit.grid(column = 6, row = 13, sticky = tk.W, **self.paddings)
        
    def Delete_SetRangeTransparencyWallChoice(self) :
        self.SetMinTransparencyWallChoiceLabel.grid_remove()
        self.SetMinTransparencyWallChoiceEntry.grid_remove()
        self.SetMaxTransparencyWallChoiceLabel.grid_remove()
        self.SetMaxTransparencyWallChoiceEntry.grid_remove()
        self.SetStepTransparencyWallChoiceLabel.grid_remove()
        self.SetStepTransparencyWallChoiceEntry.grid_remove()
        self.SetRangeTransparencyWallChoiceSubmit.grid_remove()
        
    def Get_SetRangeTransparencyWallChoice(self) :
        self.Delete_AllSetWithoutImage(1)
        Choice1 = self.SetMinTransparencyWallChoiceEntry.get()
        Choice2 = self.SetMaxTransparencyWallChoiceEntry.get()
        Step = self.SetStepTransparencyWallChoiceEntry.get()
        isOK1 = TF.is01Float(Choice1)
        isOK2 = TF.is01Float(Choice2)
        isOK = TF.is01Float(Step)
        if isOK1 == True and isOK2 == True and isOK == True :
            if float(Choice2) > float(Choice1) and float(Step) > 0 : 
                if TF.isPositiveInteger(float(float(Choice2) - float(Choice1)) / float(Step)) == True :
                    self.Display_SetNumberWorldChoice()
                else : 
                    self.Message = tk.Message(self, text = "Step value must be a multiple of the difference between the two transparency")
                    self.Message.grid(column = 7, row = 13, sticky = tk.W, **self.paddings)
            else :
                if float(Step) == 0 :
                    self.Message = tk.Message(self, text = "Step value must be positive")
                else : 
                    self.Message = tk.Message(self, text = "Max value must be greater than Min value")
                self.Message.grid(column = 7, row = 13, sticky = tk.W, **self.paddings)
        else :
            self.Message = tk.Message(self, text = "Not all float between 0 and 1")
            self.Message.grid(column = 7, row = 13, sticky = tk.W, **self.paddings)
            
    # Number of Webots World (int)
    def Display_SetNumberWorldChoice(self) :
        self.SetNumberWorldChoiceLabel.grid(column = 4, row = 14, sticky = tk.W, **self.paddings)
        
        self.SetNumberWorldChoiceEntry = tk.Entry(self)
        self.SetNumberWorldChoiceEntry.grid(column = 5, row = 14, sticky = tk.W, **self.paddings)
        
        self.SetNumberWorldChoiceSubmit.grid(column = 6, row = 14, sticky = tk.W, **self.paddings)

    def Delete_SetNumberWorldChoice(self) :
        self.SetNumberWorldChoiceLabel.grid_remove()
        self.SetNumberWorldChoiceEntry.grid_remove()
        self.SetNumberWorldChoiceSubmit.grid_remove()
        
    def Get_SetNumberWorldChoice(self) :
        self.Delete_AllSetWithoutImage(0)
        Choice = self.SetNumberWorldChoiceEntry.get()
        isOK = TF.isPositiveInteger(Choice)
        if isOK == True :
            self.Display_SetPrefixNameChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive integer")
            self.Message.grid(column = 7, row = 14, sticky = tk.W, **self.paddings)
            
    # Prefix name for the Webots World
    def Display_SetPrefixNameChoice(self) :
        self.SetPrefixNameChoiceLabel.grid(column = 4, row = 15, sticky = tk.W, **self.paddings)
        
        self.SetPrefixNameChoiceEntry = tk.Entry(self)
        self.SetPrefixNameChoiceEntry.grid(column = 5, row = 15, sticky = tk.W, **self.paddings)
        
        self.SetPrefixNameChoiceSubmit.grid(column = 6, row = 15, sticky = tk.W, **self.paddings)
        
    def Delete_SetPrefixNameChoice(self) :
        self.SetPrefixNameChoiceLabel.grid_remove()
        self.SetPrefixNameChoiceEntry.grid_remove()
        self.SetPrefixNameChoiceSubmit.grid_remove()
        
    def Get_SetPrefixNameChoice(self) :
        Choice = self.SetPrefixNameChoiceEntry.get()
        self.Message.grid_remove()
        if len(Choice) > 0 :
            self.Generate_Set_Without_Image()
        else :
            self.Message = tk.Message(self, text = "NULL String")
            self.Message.grid(column = 7, row = 15, sticky = tk.W, **self.paddings)
            
    # Generate the Set of Webots World (Without Image)
    def Generate_Set_Without_Image(self) :
        if self.SetWallChoice.get() == 'Constant' :
            WallChoice = 1
            Nbr_Wall = int(self.SetConstantWallChoiceEntry.get())
        # self.SetWallChoice.get() == 'Variable'
        else : 
            WallChoice = 2
            Min_Wall = int(self.SetMinWallChoiceEntry.get())
            Max_Wall = int(self.SetMaxWallChoiceEntry.get())
            
        if self.SetFigureChoice.get() == 'Closed' :
            WhatShape = 1
            Shape = 1
        elif self.SetFigureChoice.get() == 'Open' :
            WhatShape = 2
            Shape = 2
        # self.SetFigureChoice.get() == 'Random'
        else :
            WhatShape = 3

        if self.SetWallCrossingChoice.get() == 'Yes' :
            isCrossing = 'Y'
        # self.SetWallCrossingChoice.get() == 'No'
        else :
            isCrossing = 'N'
            
        if self.SetDiagonalMovementChoice.get() == 'Yes' :
            isDiagonal = 'Y'
        # self.SetDiagonalMovementChoice.get() == 'No'
        else :
            isDiagonal = 'N'

        if isDiagonal == 'N' :
            All_Dir = ['Up', 'Right', 'Down', 'Left']
            All_Dir0 = ['Right', 'Left']
            All_Dir1 = ['Up', 'Down']
        # isDiagonal == 'Y'
        else : 
            All_Dir = ['Up', 'Right', 'Down', 'Left', 'Up-Left', 'Up-Right', 'Down-Left', 'Down-Right']
            All_Dir0 = ['Right', 'Left', 'Up-Left', 'Up-Right', 'Down-Left', 'Down-Right']
            All_Dir1 = ['Up', 'Down', 'Up-Left', 'Up-Right', 'Down-Left', 'Down-Right']
            All_Dir4 = ['Up', 'Right', 'Down', 'Left', 'Up-Right', 'Down-Left']
            All_Dir5 = ['Up', 'Right', 'Down', 'Left', 'Up-Left', 'Down-Right']

        StartChoice = 1
        if self.SetFirstDirectionChoice.get() == 'Up' :
            Start_Direction = 1
        elif self.SetFirstDirectionChoice.get() == 'Right' :
            Start_Direction = 2
        elif self.SetFirstDirectionChoice.get() == 'Down' :
            Start_Direction = 3
        elif self.SetFirstDirectionChoice.get() == 'Left' :
            Start_Direction = 4
        elif self.SetFirstDirectionChoice.get() == 'Up-Left' :
            Start_Direction = 5
        elif self.SetFirstDirectionChoice.get() == 'Up-Right' :
            Start_Direction = 6
        elif self.SetFirstDirectionChoice.get() == 'Down-Left' :
            Start_Direction = 7
        elif self.SetFirstDirectionChoice.get() == 'Down-Right' :
            Start_Direction = 8
        # self.SetFirstDirectionChoice.get() == 'Random'
        else : 
            StartChoice = 2
            
        if StartChoice == 1 :
            Start_Dir = All_Dir[Start_Direction - 1]

        Proba_D = int(self.SetProbaSameDirectionChoiceEntry.get())

        Grid_J = int(self.SetMatrixJChoiceEntry.get())
        Grid_I = int(self.SetMatrixIChoiceEntry.get())

        if self.SetLengthChoice.get() == 'Constant' :
            LengthChoice = 1
            Wall_Length = float(self.SetConstantLengthChoiceEntry.get())
        elif self.SetLengthChoice.get() == 'Variable' :
            LengthChoice = 2
            Min_Length = float(self.SetMinLengthChoiceEntry.get())
            Max_Length = float(self.SetMaxLengthChoiceEntry.get())
            Step_Length = float(self.SetStepLengthChoiceEntry.get())
        # self.SetLengthChoice.get() == 'Random'
        else :
            LengthChoice = 3
            Cell_Length = float(self.SetCellLengthChoiceEntry.get())

        if self.SetHeightWallChoice.get() == 'Constant' :
            HeightChoice = 1
            Wall_Height = float(self.SetConstantHeightWallChoiceEntry.get())
        # self.SetHeightWallChoice.get() == 'Variable'
        else :
            HeightChoice = 2
            Min_Height = float(self.SetMinHeightWallChoiceEntry.get())
            Max_Height = float(self.SetMaxHeightWallChoiceEntry.get())
            Step_Height = float(self.SetStepHeightWallChoiceEntry.get())
            
        if self.SetThicknessWallChoice.get() == 'Constant' :
            ThicknessChoice = 1
            Wall_Thickness = float(self.SetConstantThicknessWallChoiceEntry.get())
        # self.SetThicknessWallChoice.get() == 'Variable'
        else :
            ThicknessChoice = 2
            Min_Thickness = float(self.SetMinThicknessWallChoiceEntry.get())
            Max_Thickness = float(self.SetMaxThicknessWallChoiceEntry.get())
            Step_Thickness = float(self.SetStepThicknessWallChoiceEntry.get())
            
        if self.SetTransparencyWallChoice.get() == 'Constant' :
            TransparencyChoice = 1
            Wall_Transparency = float(self.SetConstantTransparencyWallChoiceEntry.get())
        # self.SetTransparencyWallChoice.get() == 'Variable'
        else :
            TransparencyChoice = 2
            Min_Transparency = float(self.SetMinTransparencyWallChoiceEntry.get())
            Max_Transparency = float(self.SetMaxTransparencyWallChoiceEntry.get())
            Step_Transparency = float(self.SetStepTransparencyWallChoiceEntry.get())
            
        Nbr_World = int(self.SetNumberWorldChoiceEntry.get())

        Prefix_Name = self.SetPrefixNameChoiceEntry.get()
        
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
                x_2, y_2 = TF.Next_Point(x_1, y_1, Current_Dir)
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
                        x_temp, y_temp = TF.Next_Point(x_2, y_2, Next_Dir)
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
                            x_temp, y_temp = TF.Next_Point(x_1, y_1, Next_Dir)
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
                min_x, min_y, max_x, max_y = TF.get_min_max(W_room)

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
                
                File_Name = Prefix_Name + str(i)
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
                    self.Message = tk.Message(self, text = "FINISH")
                    self.Message.grid(column = 7, row = 15, sticky = tk.W, **self.paddings)
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
                    self.Message = tk.Message(self, text = "FINISH")
                    self.Message.grid(column = 7, row = 15, sticky = tk.W, **self.paddings)
                else :
                    i += 1
        #self.destroy()
        
    def Delete_AllSetWithoutImage(self, ind) :
        if ind >= 17 :
            self.Delete_SetWallChoice()
        if ind >= 16 :
            self.Delete_SetConstantWallChoice()
            self.Delete_SetRangeWallChoice()
        if ind >= 15 :
            self.Delete_SetFigureChoice()
        if ind >= 14 :
            self.Delete_SetWallCrossingChoice()
        if ind >= 13 :
            self.Delete_SetDiagonalMovementChoice()
        if ind >= 12 :
            self.Delete_SetFirstDirectionChoice()
        if ind >= 11 :
            self.Delete_SetProbaSameDirectionChoice()
        if ind >= 10 :
            self.Delete_SetMatrixIJChoice()
        if ind >= 9 :
            self.Delete_SetLengthChoice()
        if ind >= 8 :
            self.Delete_SetConstantLengthChoice()
            self.Delete_SetRangeLengthChoice()
            self.Delete_SetCellLengthChoice()
        if ind >= 7 :
            self.Delete_SetHeightWallChoice()
        if ind >= 6 :
            self.Delete_SetConstantHeightWallChoice()
            self.Delete_SetRangeHeightWallChoice()
        if ind >= 5 :
            self.Delete_SetThicknessWallChoice()
        if ind >= 4 :
            self.Delete_SetConstantThicknessWallChoice()
            self.Delete_SetRangeThicknessWallChoice()
        if ind >= 3 :
            self.Delete_SetTransparencyWallChoice()
        if ind >= 2 :
            self.Delete_SetConstantTransparencyWallChoice()
            self.Delete_SetRangeTransparencyWallChoice()
        if ind >= 1 :
            self.Delete_SetNumberWorldChoice()
        if ind >= 0 :
            self.Delete_SetPrefixNameChoice()
            self.Message.grid_remove()
        
    def Delete_AllSetWithImage(self, ind) :
        if ind >= 4 :
            self.Delete_SetImageFolderNameChoice()
        if ind >= 3 :
            self.Delete_SetPixelLengthChoice()
        if ind >= 2 :
            self.Delete_SetImageHeightWallChoice()
        if ind >= 1 :
            self.Delete_SetImageThicknessWallChoice()
        if ind >= 0 :
            self.Delete_SetImageTransparencyWallChoice()
            self.Message.grid_remove()
        
    # We choose the images folder 
    def Display_SetImageFolderNameChoice(self) :
        self.SetImageFolderNameChoiceLabel.grid(column = 0, row = 2, sticky = tk.W, **self.paddings)
        
        self.SetImageFolderNameChoice = tk.StringVar()
        self.SetImageFolderNameChoiceMenu = tk.OptionMenu(self, self.SetImageFolderNameChoice, *self.SetImageFolderNameChoiceOption, command = self.Get_SetImageFolderNameChoice)
        self.SetImageFolderNameChoiceMenu.grid(column = 1, row = 2, sticky = tk.W, **self.paddings)

    def Delete_SetImageFolderNameChoice(self) : 
        self.SetImageFolderNameChoiceLabel.grid_remove()
        self.SetImageFolderNameChoiceMenu.grid_remove()
        
    def Get_SetImageFolderNameChoice(self, Choice) :
        self.Delete_AllSetWithImage(3)
        self.Display_SetPixelLengthChoice()
        
    # Lenght for a pixel
    def Display_SetPixelLengthChoice(self) :
        self.SetPixelLengthChoiceLabel.grid(column = 0, row = 3, sticky = tk.W, **self.paddings)
        
        self.SetPixelLengthChoiceEntry = tk.Entry(self)
        self.SetPixelLengthChoiceEntry.grid(column = 1, row = 3, sticky = tk.W, **self.paddings)
        
        self.SetPixelLengthChoiceSubmit.grid(column = 2, row = 3, sticky = tk.W, **self.paddings)
    
    def Delete_SetPixelLengthChoice(self) :
        self.SetPixelLengthChoiceLabel.grid_remove()
        self.SetPixelLengthChoiceEntry.grid_remove()
        self.SetPixelLengthChoiceSubmit.grid_remove()
        
    def Get_SetPixelLengthChoice(self) :
        self.Delete_AllSetWithImage(2)
        Choice = self.SetPixelLengthChoiceEntry.get()
        isOK = TF.isPositiveFloat(Choice)
        if isOK == True :
            self.Display_SetImageHeightWallChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive float")
            self.Message.grid(column = 3, row = 3, sticky = tk.W, **self.paddings)
            
    # Height Wall Choice
    def Display_SetImageHeightWallChoice(self) :
        self.SetImageHeightWallChoiceLabel.grid(column = 0, row = 4, sticky = tk.W, **self.paddings)
        
        self.SetImageHeightWallChoiceEntry = tk.Entry(self)
        self.SetImageHeightWallChoiceEntry.grid(column = 1, row = 4, sticky = tk.W, **self.paddings)
        
        self.SetImageHeightWallChoiceSubmit.grid(column = 2, row = 4, sticky = tk.W, **self.paddings)
    
    def Delete_SetImageHeightWallChoice(self) :
        self.SetImageHeightWallChoiceLabel.grid_remove()
        self.SetImageHeightWallChoiceEntry.grid_remove()
        self.SetImageHeightWallChoiceSubmit.grid_remove()
        
    def Get_SetImageHeightWallChoice(self) :
        self.Delete_AllSetWithImage(1)
        Choice = self.SetImageHeightWallChoiceEntry.get()
        isOK = TF.isPositiveFloat(Choice)
        if isOK == True :
            self.Display_SetImageThicknessWallChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive float")
            self.Message.grid(column = 3, row = 4, sticky = tk.W, **self.paddings)
            
    # Thickness Wall Choice
    def Display_SetImageThicknessWallChoice(self) :
        self.SetImageThicknessWallChoiceLabel.grid(column = 0, row = 5, sticky = tk.W, **self.paddings)
        
        self.SetImageThicknessWallChoiceEntry = tk.Entry(self)
        self.SetImageThicknessWallChoiceEntry.grid(column = 1, row = 5, sticky = tk.W, **self.paddings)
        
        self.SetImageThicknessWallChoiceSubmit.grid(column = 2, row = 5, sticky = tk.W, **self.paddings)

    def Delete_SetImageThicknessWallChoice(self) :
        self.SetImageThicknessWallChoiceLabel.grid_remove()
        self.SetImageThicknessWallChoiceEntry.grid_remove()
        self.SetImageThicknessWallChoiceSubmit.grid_remove()
    
    def Get_SetImageThicknessWallChoice(self) :
        self.Delete_AllSetWithImage(0)
        Choice = self.SetImageThicknessWallChoiceEntry.get()
        isOK = TF.isPositiveFloat(Choice)
        if isOK == True :
            self.Display_SetImageTransparencyWallChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive float")
            self.Message.grid(column = 3, row = 5, sticky = tk.W, **self.paddings)
            
    # Transparency Wall Choice
    def Display_SetImageTransparencyWallChoice(self) :
        self.SetImageTransparencyWallChoiceLabel.grid(column = 0, row = 6, sticky = tk.W, **self.paddings)
        
        self.SetImageTransparencyWallChoiceEntry = tk.Entry(self)
        self.SetImageTransparencyWallChoiceEntry.grid(column = 1, row = 6, sticky = tk.W, **self.paddings)
        
        self.SetImageTransparencyWallChoiceSubmit.grid(column = 2, row = 6, sticky = tk.W, **self.paddings)
    
    def Delete_SetImageTransparencyWallChoice(self) :
        self.SetImageTransparencyWallChoiceLabel.grid_remove()
        self.SetImageTransparencyWallChoiceEntry.grid_remove()
        self.SetImageTransparencyWallChoiceSubmit.grid_remove()
        
    def Get_SetImageTransparencyWallChoice(self) :
        Choice = self.SetImageTransparencyWallChoiceEntry.get()
        self.Message.grid_remove()
        isOK = TF.is01Float(Choice)
        if isOK == True :
            self.Generate_Set_With_Image()
        else :
            self.Message = tk.Message(self, text = "Not a float between 0 and 1")
            self.Message.grid(column = 3, row = 6, sticky = tk.W, **self.paddings)
            
    # Generate Webots World with images
    def Generate_Set_With_Image(self) :
        Image_Name = []
        Not_Image = []
        files = os.listdir(self.SetImageFolderNameChoice.get())
        for name in files:
            image = cv2.imread(str(self.SetImageFolderNameChoice.get()) + "/" + name)
            if image is None :
                Not_Image.append(name)
            else :
                Image_Name.append(name)

        print(" Number of files in the folder : ", len(files))
        print("     Total images : ", len(Image_Name))
        print("     Name of image file : ", Image_Name)
        print("     Name of others file : ", Not_Image)
        print()
        
        Pixel_Length = float(self.SetPixelLengthChoiceEntry.get())
        Wall_Height = float(self.SetImageHeightWallChoiceEntry.get())
        Wall_Thickness = float(self.SetImageThicknessWallChoiceEntry.get())
        Wall_Transparency = float(self.SetImageTransparencyWallChoiceEntry.get())
            
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
                W_vertical = BT.vertical_or_horizontal_extension('Vertical', W_vertical, gap_length)
            if len(W_horizontal) > 3 :
                W_horizontal = BT.vertical_or_horizontal_extension('Horizontal', W_horizontal, gap_length)
            if len(W_left_diagonal) > 3 :
                W_left_diagonal, W_left_angle_diagonal = BT.left_or_right_diagonal_extension('Left_Diagonal', W_left_diagonal, W_left_angle_diagonal, gap_length)
            if len(W_right_diagonal) > 3 :
                W_right_diagonal, W_right_angle_diagonal = BT.left_or_right_diagonal_extension('Right_Diagonal', W_right_diagonal, W_right_angle_diagonal, gap_length)

            gap = 10
            # If, after extension, we still have at least 2 lines, we apply the removal of extra lines
            if len(W_vertical) > 3 :
                W_vertical = BT.remove_extra_vertical_or_horizontal('Vertical', W_vertical, gap)
            if len(W_horizontal) > 3 :
                W_horizontal = BT.remove_extra_vertical_or_horizontal('Horizontal', W_horizontal, gap)
            if len(W_left_diagonal) > 3 :
                W_left_diagonal = BT.remove_extra_left_or_right_diagonal('Left_Diagonal', W_left_diagonal, W_left_angle_diagonal, gap, len(image[0]), len(image))
            if len(W_right_diagonal) > 3 :
                W_right_diagonal = BT.remove_extra_left_or_right_diagonal('Right_Diagonal', W_right_diagonal, W_right_angle_diagonal, gap, len(image[0]), len(image))
            
            print(" Number of verticals : ", int(len(W_vertical) / 2))
            print(" Number of horizontals : ", int(len(W_horizontal) / 2))
            print(" Number of left diagonals : ", int(len(W_left_diagonal) / 2))
            print(" Number of right diagonals : ", int(len(W_right_diagonal) / 2))
            print()
            
            W_room, W_vertical, W_horizontal, W_diagonal = BT.fill_hole(W_vertical, W_horizontal, W_left_diagonal, W_right_diagonal, gap)

            min_x, min_y, max_x, max_y = TF.get_min_max(W_room)

            Wall_Length = Pixel_Length * (max_x - min_x)
            
            F.Write_Webots_File(e, 2, 2, min_x, max_x, min_y, max_y, Wall_Length, W_room, int(len(W_room) / 2), Wall_Height, Wall_Thickness, Wall_Transparency)
        #self.destroy()
        
    ############# SINGLE WEBOTS WORLD ####################
    
    # Feature Option between Manual Mode and Image Processing
    def Display_FeatureChoice(self) :
        self.FeatureChoiceLabel.grid(column = 0, row = 1, sticky = tk.W, **self.paddings)
        
        self.FeatureChoice = tk.StringVar()
        self.FeatureChoiceMenu = tk.OptionMenu(self, self.FeatureChoice, *self.FeatureChoiceOption, command = self.Get_FeatureChoice)
        self.FeatureChoiceMenu.grid(column = 1, row = 1, sticky = tk.W, **self.paddings)

    def Delete_FeatureChoice(self) :
        self.FeatureChoiceLabel.grid_remove()
        self.FeatureChoiceMenu.grid_remove()
        
    def Get_FeatureChoice(self, Choice) :
        self.Delete_AllWithoutImage(10)
        self.Delete_AllWithImage(7)
        self.Display_DefaultConfigurationChoice()

    # Default Configuration Option
    def Display_DefaultConfigurationChoice(self) :
        self.DefaultConfigurationChoiceLabel.grid(column = 0, row = 2, sticky = tk.W, **self.paddings)
        
        self.DefaultConfigurationChoice = tk.StringVar()
        self.DefaultConfigurationChoiceMenu = tk.OptionMenu(self, self.DefaultConfigurationChoice, *self.DefaultConfigurationChoiceOption, command = self.Get_DefaultConfigurationChoice)
        self.DefaultConfigurationChoiceMenu.grid(column = 1, row = 2, sticky = tk.W, **self.paddings)
        
    def Delete_DefaultConfigurationChoice(self) :
        self.DefaultConfigurationChoiceLabel.grid_remove()
        self.DefaultConfigurationChoiceMenu.grid_remove()
        
    def Get_DefaultConfigurationChoice(self, Choice) :
        self.Delete_AllWithoutImage(9)
        self.Delete_AllWithImage(7)
        Choice = self.DefaultConfigurationChoice.get()
        if Choice == 'Use' :
            self.config = np.loadtxt("default_configuration.txt")
            if len(self.config) == 11 and C.check_input(self.config[0]) == C.check_input(self.config[1]) == C.check_input(self.config[2]) == C.check_input(self.config[3]) == C.check_input(self.config[4]) == C.check_input(self.config[5]) == C.check_input(self.config[6]) == C.check_input(self.config[7]) == 'int' and (C.check_input(self.config[8]) == 'float' or C.check_input(self.config[8]) == 'int') and (C.check_input(self.config[9]) == 'float' or C.check_input(self.config[9]) == 'int') and (C.check_input(self.config[10]) == 'float' or C.check_input(self.config[10]) == 'int') :
                if int(self.config[0]) >= 2 and int(self.config[0]) <= 100 and int(self.config[1]) >= 2 and int(self.config[1]) <= 100 and int(self.config[2]) >= 0 and int(self.config[2]) <= 255 and int(self.config[3]) > 0 and int(self.config[4]) > 0 and int(self.config[5]) >= 0 and int(self.config[5]) <= 45 and int(self.config[6]) > 0 and int(self.config[7]) > 0 and float(self.config[8]) > 0 and float(self.config[9]) > 0 and float(self.config[10]) >= 0 and float(self.config[10]) <= 1 :
                    if self.FeatureChoice.get() == 'Manual' :
                        self.Display_ManualOptionChoice()
                    elif self.FeatureChoice.get() == 'Image' :
                        self.Display_ImageFolderNameChoice()
                else : 
                    if self.FeatureChoice.get() == 'Manual' :
                        self.Display_GridChoice()
                    elif self.FeatureChoice.get() == 'Image' :
                        self.Display_ImageFolderNameChoice()
                    self.DefaultConfigurationChoice = 'Not used'
            else : 
                if self.FeatureChoice.get() == 'Manual' :
                    self.Display_GridChoice()
                elif self.FeatureChoice.get() == 'Image' :
                    self.Display_ImageFolderNameChoice()
                self.DefaultConfigurationChoice = 'Not used'
        elif Choice == "Not used" :
            if self.FeatureChoice.get() == 'Manual' :
                self.Display_GridChoice()
            elif self.FeatureChoice.get() == 'Image' :
                self.Display_ImageFolderNameChoice()
        elif Choice == 'View' :
            self.Display_ViewDefaultConfigurationChoice()
        elif Choice == 'Change' :
            self.Display_NewDefaultConfigurationChoice()
            
    # If we want to change the current Default Configuration
    def Display_NewDefaultConfigurationChoice(self) :
        self.NewDefaultConfigurationChoiceLabel00.grid(column = 0, row = 3, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceLabel01.grid(column = 0, row = 6, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceLabel02.grid(column = 0, row = 13, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceLabel1.grid(column = 0, row = 4, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceEntry1 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceEntry1.grid(column = 1, row = 4, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceLabel2.grid(column = 0, row = 5, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceEntry2 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceEntry2.grid(column = 1, row = 5, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceLabel3.grid(column = 0, row = 7, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceEntry3 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceEntry3.grid(column = 1, row = 7, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceLabel4.grid(column = 0, row = 8, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceEntry4 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceEntry4.grid(column = 1, row = 8, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceLabel5.grid(column = 0, row = 9, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceEntry5 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceEntry5.grid(column = 1, row = 9, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceLabel6.grid(column = 0, row = 10, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceEntry6 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceEntry6.grid(column = 1, row = 10, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceLabel7.grid(column = 0, row = 11, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceEntry7 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceEntry7.grid(column = 1, row = 11, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceLabel8.grid(column = 0, row = 12, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceEntry8 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceEntry8.grid(column = 1, row = 12, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceLabel9.grid(column = 0, row = 14, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceEntry9 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceEntry9.grid(column = 1, row = 14, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceLabel10.grid(column = 0, row = 15, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceEntry10 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceEntry10.grid(column = 1, row = 15, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceLabel11.grid(column = 0, row = 16, sticky = tk.W, **self.paddings)
        self.NewDefaultConfigurationChoiceEntry11 = tk.Entry(self)
        self.NewDefaultConfigurationChoiceEntry11.grid(column = 1, row = 16, sticky = tk.W, **self.paddings)
        
        self.NewDefaultConfigurationChoiceSubmit.grid(column = 2, row = 16, sticky = tk.W, **self.paddings)
    
    def Delete_NewDefaultConfigurationChoice(self) :
        self.NewDefaultConfigurationChoiceLabel00.grid_remove()
        self.NewDefaultConfigurationChoiceLabel01.grid_remove()
        self.NewDefaultConfigurationChoiceLabel02.grid_remove()
        self.NewDefaultConfigurationChoiceLabel1.grid_remove()
        self.NewDefaultConfigurationChoiceEntry1.grid_remove()
        self.NewDefaultConfigurationChoiceLabel2.grid_remove()
        self.NewDefaultConfigurationChoiceEntry2.grid_remove()
        self.NewDefaultConfigurationChoiceLabel3.grid_remove()
        self.NewDefaultConfigurationChoiceEntry3.grid_remove()
        self.NewDefaultConfigurationChoiceLabel4.grid_remove()
        self.NewDefaultConfigurationChoiceEntry4.grid_remove()
        self.NewDefaultConfigurationChoiceLabel5.grid_remove()
        self.NewDefaultConfigurationChoiceEntry5.grid_remove()
        self.NewDefaultConfigurationChoiceLabel6.grid_remove()
        self.NewDefaultConfigurationChoiceEntry6.grid_remove()
        self.NewDefaultConfigurationChoiceLabel7.grid_remove()
        self.NewDefaultConfigurationChoiceEntry7.grid_remove()
        self.NewDefaultConfigurationChoiceLabel8.grid_remove()
        self.NewDefaultConfigurationChoiceEntry8.grid_remove()
        self.NewDefaultConfigurationChoiceLabel9.grid_remove()
        self.NewDefaultConfigurationChoiceEntry9.grid_remove()
        self.NewDefaultConfigurationChoiceLabel10.grid_remove()
        self.NewDefaultConfigurationChoiceEntry10.grid_remove()
        self.NewDefaultConfigurationChoiceLabel11.grid_remove()
        self.NewDefaultConfigurationChoiceEntry11.grid_remove()
        self.NewDefaultConfigurationChoiceSubmit.grid_remove()
        
    def Get_NewDefaultConfigurationChoice(self) :
        self.Delete_AllWithoutImage(8)
        self.Delete_AllWithImage(7)
        Choice1 = self.NewDefaultConfigurationChoiceEntry1.get()
        Choice2 = self.NewDefaultConfigurationChoiceEntry2.get()
        Choice3 = self.NewDefaultConfigurationChoiceEntry3.get()
        Choice4 = self.NewDefaultConfigurationChoiceEntry4.get()
        Choice5 = self.NewDefaultConfigurationChoiceEntry5.get()
        Choice6 = self.NewDefaultConfigurationChoiceEntry6.get()
        Choice7 = self.NewDefaultConfigurationChoiceEntry7.get()
        Choice8 = self.NewDefaultConfigurationChoiceEntry8.get()
        Choice9 = self.NewDefaultConfigurationChoiceEntry9.get()
        Choice10 = self.NewDefaultConfigurationChoiceEntry10.get()
        Choice11 = self.NewDefaultConfigurationChoiceEntry11.get()
        isOK1 = TF.isPositiveMinMaxInteger(Choice1, 2, 100)
        isOK2 = TF.isPositiveMinMaxInteger(Choice2, 2, 100)
        isOK3 = TF.isPositiveMinMaxInteger(Choice3, 0, 255)
        isOK4 = TF.isPositiveInteger(Choice4)
        isOK5 = TF.isPositiveInteger(Choice5)
        isOK6 = TF.isPositiveMinMaxInteger(Choice6, 0, 45)
        isOK7 = TF.isPositiveInteger(Choice7)
        isOK8 = TF.isPositiveInteger(Choice8)
        isOK9 = TF.isPositiveFloat(Choice9)
        isOK10 = TF.isPositiveFloat(Choice10)
        isOK11 = TF.is01Float(Choice11)
        if isOK1 == isOK2 == isOK3 == isOK4 == isOK5 == isOK6 == isOK7 == isOK8 == isOK9 == isOK10 == isOK11 == True :
            with open("default_configuration.txt", "w") as f :
                f.write("# Default configuration for the Webots Tool" + "\n")
                f.write("\n")
                f.write("# Manual Mode" + "\n")
                f.write(str(int(Choice1)) + " # Number of cells on the x-axis (int between 2 and 100)" + "\n")
                f.write(str(int(Choice2)) + " # Number of cells on the y-axis (int between 2 and 100)" + "\n")
                f.write("\n")
                f.write("# Image Processing" + "\n")
                f.write(str(int(Choice3)) + " # Threshold for the binary image (int between 0 and 255)" + "\n")
                f.write(str(int(Choice4)) + " # Minimum number of points that can form a line (int)" + "\n")
                f.write(str(int(Choice5)) + " # Maximum gap between two points to be considered in the same line (int)" + "\n")
                f.write(str(int(Choice6)) + " # Angle for pseudo-vertical and pseudo-horizontal" + "\n")
                f.write(str(int(Choice7)) + " # Maximum gap between two lines to be considered in the same line (int)" + "\n")
                f.write(str(int(Choice8)) + " # Maximum gap between two parellel lines to be considered as the same line (int)" + "\n")
                f.write("\n")
                f.write("# Wall Parameters" + "\n")
                f.write(str(float(Choice9)) + " # Wall height (in meters)" + "\n")
                f.write(str(float(Choice10)) + " # Wall thickness (in meters)" + "\n")
                f.write(str(float(Choice11)) + " # Wall transparency (float between 0 and 1)" + "\n")
        else : 
            self.Message = tk.Message(self, text = "Not all correct Values")
            self.Message.grid(column = 3, row = 16, sticky = tk.W, **self.paddings)

    # If we want to view the current Default Configuration
    def Display_ViewDefaultConfigurationChoice(self) :
        config = np.loadtxt("default_configuration.txt")
        if len(config) == 11 and C.check_input(config[0]) == C.check_input(config[1]) == C.check_input(config[2]) == C.check_input(config[3]) == C.check_input(config[4]) == C.check_input(config[5]) == C.check_input(config[6]) == C.check_input(config[7]) == 'int' and (C.check_input(config[8]) == 'float' or C.check_input(config[8]) == 'int') and (C.check_input(config[9]) == 'float' or C.check_input(config[9]) == 'int') and (C.check_input(config[10]) == 'float' or C.check_input(config[10]) == 'int') :
            if int(config[0]) >= 2 and int(config[0]) <= 100 and int(config[1]) >= 2 and int(config[1]) <= 100 and int(config[2]) >= 0 and int(config[2]) <= 255 and int(config[3]) > 0 and int(config[4]) > 0 and int(config[5]) >= 0 and int(config[5]) <= 45 and int(config[6]) > 0 and int(config[7]) > 0 and float(config[8]) > 0 and float(config[9]) > 0 and float(config[10]) >= 0 and float(config[10]) <= 1 :
                self.ViewDefaultConfigurationChoiceLabel00 = tk.Label(self, text = "### Manual Mode ###")
                self.ViewDefaultConfigurationChoiceLabel01 = tk.Label(self, text = "### Image Processing ###")
                self.ViewDefaultConfigurationChoiceLabel02 = tk.Label(self, text = "### Wall Parameters ###")
                self.ViewDefaultConfigurationChoiceLabel1 = tk.Label(self, text = "Number of cells on the x-axis (int between 2 and 100) : " + str(int(config[0])))
                self.ViewDefaultConfigurationChoiceLabel2 = tk.Label(self, text = "Number of cells on the y-axis (int between 2 and 100) : " + str(int(config[1])))
                self.ViewDefaultConfigurationChoiceLabel3 = tk.Label(self, text = "Threshold for the binary image (int between 0 and 255) : " + str(int(config[2])))
                self.ViewDefaultConfigurationChoiceLabel4 = tk.Label(self, text = "Minimum number of points that can form a line (int > 0) : " + str(int(config[3])))
                self.ViewDefaultConfigurationChoiceLabel5 = tk.Label(self, text = "Maximum gap between two points to be considered in the same line (int > 0) : " + str(int(config[4])))
                self.ViewDefaultConfigurationChoiceLabel6 = tk.Label(self, text = "Angle for pseudo-vertical and pseudo-horizontal (0 <= int <= 45): " + str(int(config[5])))
                self.ViewDefaultConfigurationChoiceLabel7 = tk.Label(self, text = "Maximum gap between two lines to be considered in the same line (int > 0) : " + str(int(config[6])))
                self.ViewDefaultConfigurationChoiceLabel8 = tk.Label(self, text = "Maximum gap between two parellel lines to be considered as the same line (int > 0) : " + str(int(config[7])))
                self.ViewDefaultConfigurationChoiceLabel9 = tk.Label(self, text = "Wall height (in meters) : " + str(float(config[8])))
                self.ViewDefaultConfigurationChoiceLabel10 = tk.Label(self, text = "Wall thickness (in meters) : " + str(float(config[9])))
                self.ViewDefaultConfigurationChoiceLabel11 = tk.Label(self, text = "Wall transparency (float between 0 and 1 | 1 for a transparent wall) : " + str(float(config[10])))
                
                self.ViewDefaultConfigurationChoiceLabel00.grid(column = 0, row = 3, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel01.grid(column = 0, row = 6, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel02.grid(column = 0, row = 13, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel1.grid(column = 0, row = 4, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel2.grid(column = 0, row = 5, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel3.grid(column = 0, row = 7, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel4.grid(column = 0, row = 8, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel5.grid(column = 0, row = 9, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel6.grid(column = 0, row = 10, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel7.grid(column = 0, row = 11, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel8.grid(column = 0, row = 12, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel9.grid(column = 0, row = 14, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel10.grid(column = 0, row = 15, sticky = tk.W, **self.paddings)
                self.ViewDefaultConfigurationChoiceLabel11.grid(column = 0, row = 16, sticky = tk.W, **self.paddings)
            else :
                self.Message = tk.Message(self, text = "ERROR - There is a problem with the Default Configuration text file")
                self.Message.grid(column = 2, row = 2, sticky = tk.W, **self.paddings)
        else : 
            self.Message = tk.Message(self, text = "ERROR - There is a problem with the Default Configuration text file")
            self.Message.grid(column = 2, row = 2, sticky = tk.W, **self.paddings)
            
    def Delete_ViewDefaultConfigurationChoice(self) :
        self.ViewDefaultConfigurationChoiceLabel00.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel01.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel02.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel1.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel2.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel3.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel4.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel5.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel6.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel7.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel8.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel9.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel10.grid_remove()
        self.ViewDefaultConfigurationChoiceLabel11.grid_remove()
            
    # Grid size for Manual Mode
    def Display_GridChoice(self) :
        self.GridChoiceLabel.grid(column = 0, row = 3, sticky = tk.W, **self.paddings)
        
        self.GridXChoiceLabel.grid(column = 0, row = 4, sticky = tk.W, **self.paddings)
        self.GridXChoiceEntry = tk.Entry(self)
        self.GridXChoiceEntry.grid(column = 1, row = 4, sticky = tk.W, **self.paddings)
        
        self.GridYChoiceLabel.grid(column = 0, row = 5, sticky = tk.W, **self.paddings)
        self.GridYChoiceEntry = tk.Entry(self)
        self.GridYChoiceEntry.grid(column = 1, row = 5, sticky = tk.W, **self.paddings)
        
        self.GridChoiceSubmit.grid(column = 2, row = 5, sticky = tk.W, **self.paddings)

    def Delete_GridChoice(self) :
        self.GridChoiceLabel.grid_remove()
        self.GridXChoiceLabel.grid_remove()
        self.GridXChoiceEntry.grid_remove()
        self.GridYChoiceLabel.grid_remove()
        self.GridYChoiceEntry.grid_remove()
        self.GridChoiceSubmit.grid_remove()
    
    def Get_GridChoice(self) :
        self.Delete_AllWithoutImage(7)
        Choice1 = self.GridXChoiceEntry.get()
        Choice2 = self.GridYChoiceEntry.get()
        isOK1 = TF.isPositiveMinMaxInteger(Choice1, 2, 100)
        isOK2 = TF.isPositiveMinMaxInteger(Choice2, 2, 100)
        if isOK1 == isOK2 == True : 
            self.Display_ManualOptionChoice()
        else :
            self.Message = tk.Message(self, text = "Not two int between 2 and 100")
            self.Message.grid(column = 3, row = 5, sticky = tk.W, **self.paddings)

    # Manual Mode Option
    def Display_ManualOptionChoice(self) :
        self.ManualOptionChoiceLabel.grid(column = 0, row = 6, sticky = tk.W, **self.paddings)
        
        self.ManualOptionChoice = tk.StringVar()
        self.ManualOptionChoiceOptionMenu = tk.OptionMenu(self, self.ManualOptionChoice, *self.ManualOptionChoiceOption, command = self.Get_ManualOptionChoice)
        self.ManualOptionChoiceOptionMenu.grid(column = 1, row = 6, sticky = tk.W, **self.paddings)
        
    def Delete_ManualOptionChoice(self) :
        self.ManualOptionChoiceLabel.grid_remove()
        self.ManualOptionChoiceOptionMenu.grid_remove()
        
    def Get_ManualOptionChoice(self, Choice) :
        self.Delete_AllWithoutImage(6)
        self.Display_CreationCanvas()
            
    # Canvas : Figure creation
    def Display_CreationCanvas(self) :
        isDefault = self.DefaultConfigurationChoice.get()
        Mode = self.ManualOptionChoice.get()

        self.point = []
        self.Walls = []
        self.WallsCanvas = []
        
        if isDefault == 'Use' :
            self.W = int(self.config[0])
            self.H = int(self.config[1])
        elif isDefault == 'Not used' :
            self.W = int(self.GridXChoiceEntry.get())
            self.H = int(self.GridYChoiceEntry.get())

        self.Grid_size = int(700 / max(self.W, self.H))
        self.Width = self.W * self.Grid_size 
        self.Height = self.H * self.Grid_size
        self.Canvas = tk.Canvas(self, width = self.Width, height = self.Height)
        self.Create_grid()
        self.Canvas.grid(column = 4, row = 0, sticky = tk.W, **self.paddings)
        
        if Mode == 'Room Creation (Closed figure)' :
            self.Canvas.bind("<Button-1>", self.Add_point_Room)
            self.Canvas.bind("<Button-3>", self.Remove_last_Room)
            self.Finish_Button = tk.Button(self, text = "Finish", command = self.Finish_Room)
        elif Mode == 'Free (Pair of points)' :
            self.Canvas.bind("<Button-1>", self.Add_point_Free)
            self.Canvas.bind("<Button-3>", self.Remove_last_Free)
            self.Finish_Button = tk.Button(self, text = "Finish", command = self.Finish_Free)
        self.Reset_Button = tk.Button(self, text = "Reset", command = self.Reset)
        self.Reset_Button.grid(column = 4, row = 1, sticky = tk.W, **self.paddings)
        self.Finish_Button.grid(column = 4, row = 2, sticky = tk.W, **self.paddings)
        
    def Create_grid(self) :
        for i in range(0, self.Height + self.Grid_size, self.Grid_size) :
            self.Canvas.create_line(0, i, self.Width, i, fill = 'gray')
        for j in range(0, self.Width + self.Grid_size, self.Grid_size) :
            self.Canvas.create_line(j, 0, j, self.Height, fill = 'gray')

    def Add_point_Room(self, event) :
        x, y = event.x, event.y
        x, y = x / self.Grid_size, y / self.Grid_size
        temp_x, temp_y = int(x), int(y)
        self.MessagePointPosition.grid_remove()
        if abs(temp_x - x) > 0.5 :
            x = temp_x + 1
        else :
            x = temp_x
        if abs(temp_y - y) > 0.5 :
            y = temp_y + 1
        else : 
            y = temp_y
        if len(self.points) == 0 :
            self.points.append((x, y))
            
            PointPosition = "Point coordinates : " + str(self.points[-1])
            self.MessagePointPosition = tk.Message(self, text = PointPosition)
            self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)

            self.Canvas.create_oval(x * self.Grid_size - 3, y * self.Grid_size - 3, x * self.Grid_size + 3, y * self.Grid_size + 3, fill = "red")
        else :
            if (x, y) != (self.points[-1][0], self.points[-1][1]) :
                self.points.append((x, y))
                
                PointPosition = "Point coordinates : " + str(self.points[-1])
                self.MessagePointPosition = tk.Message(self, text = PointPosition)
                self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)

                self.Canvas.create_line(self.points[-2][0] * self.Grid_size, self.points[-2][1] * self.Grid_size, x * self.Grid_size, y * self.Grid_size, fill = "blue")
                self.Canvas.create_oval(x * self.Grid_size - 3, y * self.Grid_size - 3, x * self.Grid_size + 3, y * self.Grid_size + 3, fill = "red")
        if len(self.points) > 2 :
            temp_x, temp_y = [], []
            for i in range(3) : 
                temp_x.append(self.points[-1][0])
                temp_y.append(self.points[-1][1])
                self.points.pop()
            diff_x_1, diff_y_1 = abs(temp_x[2] - temp_x[1]), abs(temp_y[2] - temp_y[1])
            diff_x_2, diff_y_2 = abs(temp_x[0] - temp_x[2]), abs(temp_y[0] - temp_y[2])
            diff_x_3, diff_y_3 = abs(temp_x[0] - temp_x[1]), abs(temp_y[0] - temp_y[1])
            if [temp_x[2], temp_y[2]] == [temp_x[0], temp_y[0]] :
                self.points.append((temp_x[2], temp_y[2]))
                self.Canvas.delete("all")
                self.Create_grid()
                self.Add_from_Room()
            elif temp_x[0] == temp_x[1] == temp_x[2] or temp_y[0] == temp_y[1] == temp_y[2] or (diff_x_1 / math.gcd(diff_x_1, diff_y_1)) == (diff_x_2 / math.gcd(diff_x_2, diff_y_2)) == (diff_x_3 / math.gcd(diff_x_3, diff_y_3)) and (diff_y_1 / math.gcd(diff_x_1, diff_y_1)) == (diff_y_2 / math.gcd(diff_x_2, diff_y_2)) == (diff_y_3 / math.gcd(diff_x_3, diff_y_3)) : 
                self.points.append((temp_x[2], temp_y[2]))
                self.points.append((temp_x[0], temp_y[0]))
                self.Canvas.delete("all")
                self.Create_grid()
                self.Add_from_Room()
            else :
                for i in [2, 1, 0] :
                    self.points.append((temp_x[i], temp_y[i]))
                    
    def Add_point_Free(self, event) : 
        x, y = event.x, event.y
        x, y = x / self.Grid_size, y / self.Grid_size
        temp_x, temp_y = int(x), int(y)
        self.MessagePointPosition.grid_remove()
        if abs(temp_x - x) > 0.5 :
            x = temp_x + 1
        else :
            x = temp_x
        if abs(temp_y - y) > 0.5 :
            y = temp_y + 1
        else : 
            y = temp_y
        if len(self.points) % 2 == 0 :
            self.points.append((x, y))

            PointPosition = "Point coordinates : " + str(self.points[-1])
            self.MessagePointPosition = tk.Message(self, text = PointPosition)
            self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
            
            self.Canvas.create_oval(x * self.Grid_size - 3, y * self.Grid_size - 3, x * self.Grid_size + 3, y * self.Grid_size + 3, fill = "red")
        else :
            if (x, y) != (self.points[-1][0], self.points[-1][1]) :
                self.points.append((x, y))
                
                PointPosition = "Point coordinates : " + str(self.points[-1])
                self.MessagePointPosition = tk.Message(self, text = PointPosition)
                self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
            
                self.Canvas.create_line(self.points[-2][0] * self.Grid_size, self.points[-2][1] * self.Grid_size, x * self.Grid_size, y * self.Grid_size, fill = "blue")
                self.Canvas.create_oval(x * self.Grid_size - 3, y * self.Grid_size - 3, x * self.Grid_size + 3, y * self.Grid_size + 3, fill = "red")
        if len(self.points) > 3 and len(self.points) % 2 == 0 :
            nbr_pair = int(len(self.points) / 2)
            isExtra = False
            for i in range(nbr_pair - 1) :
                if (self.points[2 * i] == self.points[-2] and self.points[2 * i + 1] == self.points[-1]) or (self.points[2 * i] == self.points[-1] and self.points[2 * i + 1] == self.points[-2]) :
                    isExtra = True
            if isExtra == True :
                self.points.pop()
                self.points.pop()
    
    def Add_from_Room(self) : 
        for i in range(len(self.points)) : 
            x = self.points[i][0]
            y = self.points[i][1]
            if len(self.points) > 1  and i < len(self.points) - 1 :
                self.Canvas.create_line(x * self.Grid_size, y * self.Grid_size, self.points[i + 1][0] * self.Grid_size, self.points[i + 1][1] * self.Grid_size, fill = "blue")
            self.Canvas.create_oval(x * self.Grid_size - 3, y * self.Grid_size - 3, x * self.Grid_size + 3, y * self.Grid_size + 3, fill = "red")

    def Add_from_Free(self) :
        if len(self.points) > 1 :
            if len(self.points) % 2 == 0 :
                for i in range(0, len(self.points) - 1, 2) :
                    self.Canvas.create_line(self.points[i][0] * self.Grid_size, self.points[i][1] * self.Grid_size, self.points[i + 1][0] * self.Grid_size, self.points[i + 1][1] * self.Grid_size, fill = "blue")
                    self.Canvas.create_oval(self.points[i][0] * self.Grid_size - 3, self.points[i][1] * self.Grid_size - 3, self.points[i][0] * self.Grid_size + 3, self.points[i][1] * self.Grid_size + 3, fill = "red")
                    self.Canvas.create_oval(self.points[i + 1][0] * self.Grid_size - 3, self.points[i + 1][1] * self.Grid_size - 3, self.points[i + 1][0] * self.Grid_size + 3, self.points[i + 1][1] * self.Grid_size + 3, fill = "red")
            else : 
                for i in range(0, len(self.points) - 2, 2) :
                    self.Canvas.create_line(self.points[i][0] * self.Grid_size, self.points[i][1] * self.Grid_size, self.points[i + 1][0] * self.Grid_size, self.points[i + 1][1] * self.Grid_size, fill = "blue")
                    self.Canvas.create_oval(self.points[i][0] * self.Grid_size - 3, self.points[i][1] * self.Grid_size - 3, self.points[i][0] * self.Grid_size + 3, self.points[i][1] * self.Grid_size + 3, fill = "red")
                    self.Canvas.create_oval(self.points[i + 1][0] * self.Grid_size - 3, self.points[i + 1][1] * self.Grid_size - 3, self.points[i + 1][0] * self.Grid_size + 3, self.points[i + 1][1] * self.Grid_size + 3, fill = "red")
                self.Canvas.create_oval(self.points[-1][0] * self.Grid_size - 3, self.points[-1][1] * self.Grid_size - 3, self.points[-1][0] * self.Grid_size + 3, self.points[-1][1] * self.Grid_size + 3, fill = "red")
        if len(self.points) == 1 : 
            self.Canvas.create_oval(self.points[0][0] * self.Grid_size - 3, self.points[0][1] * self.Grid_size - 3, self.points[0][0] * self.Grid_size + 3, self.points[0][1] * self.Grid_size + 3, fill = "red")

    def Finish_Room(self) :
        isFinish = False
        self.Message.grid_remove()
        self.MessagePointPosition.grid_remove()
        if len(self.points) > 3 : 
            if self.points[0] == self.points[-1] : 
                isFinish = True
        if isFinish == True : 
            # y coordinates are in the opposite direction
            for l in range(len(self.points) - 1) :
                y1 = self.points[l][1]
                gap = int(self.H) - y1
                if gap < int(int(self.H) / 2) :
                    y1 = gap
                else : 
                    y1 = int(self.H) - y1
                y2 = self.points[l + 1][1]
                gap = int(self.H) - y2
                if gap < int(int(self.H) / 2) :
                    y2 = gap
                else : 
                    y2 = int(self.H) - y2
                self.Walls.append([self.points[l][0], y1])
                self.Walls.append([self.points[l + 1][0], y2])
                self.WallsCanvas.append([self.points[l][0], self.points[l][1]])
                self.WallsCanvas.append([self.points[l + 1][0], self.points[l + 1][1]])
            self.Delete_CreationCanvas()
        else : 
            self.Message = tk.Message(self, text = "Not a closed figure")
            self.Message.grid(column = 5, row = 0, sticky = tk.W, **self.paddings)
 
    def Finish_Free(self) : 
        self.Message.grid_remove()
        self.MessagePointPosition.grid_remove()
        if len(self.points) > 0 :  
            if len(self.points) % 2 == 0 :
                # y coordinates are in the opposite direction
                for point in self.points :
                    y = point[1]
                    gap = int(self.H) - y
                    if gap < int(int(self.H) / 2) :
                        y = gap
                    else : 
                        y = int(self.H) - y
                    self.Walls.append([point[0], y])
                    self.WallsCanvas.append([point[0], point[1]])
                self.Delete_CreationCanvas()
            else : 
                self.Message = tk.Message(self, text = "Not an even number of points")
                self.Message.grid(column = 5, row = 0, sticky = tk.W, **self.paddings)
        else : 
            self.Message = tk.Message(self, text = "Empty drawing")
            self.Message.grid(column = 5, row = 0, sticky = tk.W, **self.paddings)
        
    def Reset(self) :
        self.MessagePointPosition.grid_remove()
        self.points = []
        self.Canvas.delete("all")
        self.Create_grid()
        
    def Remove_last_Room(self, event) : 
        self.MessagePointPosition.grid_remove()
        if (len(self.points)) > 0 :
            self.points.pop(-1)
        self.Canvas.delete("all")
        self.Create_grid()
        self.Add_from_Room()
        
    def Remove_last_Free(self, event) :
        self.MessagePointPosition.grid_remove()
        if (len(self.points)) > 0 :
            self.points.pop(-1)
        self.Canvas.delete("all")
        self.Create_grid()
        self.Add_from_Free()
        
    def Delete_CreationCanvas(self) : 
        self.Canvas.grid_remove()
        self.Reset_Button.grid_remove()
        self.Finish_Button.grid_remove()
        if self.DefaultConfigurationChoice.get() == 'Use' :
            self.Display_DeleteLineChoice()
        elif self.DefaultConfigurationChoice.get() == 'Not used' :
            self.Display_HeightWallChoice()
          
    # Height Wall Choice (float)
    def Display_HeightWallChoice(self) :
        self.HeightWallChoiceLabel.grid(column = 0, row = 12, sticky = tk.W, **self.paddings)
        
        self.HeightWallChoiceEntry = tk.Entry(self)
        self.HeightWallChoiceEntry.grid(column = 1, row = 12, sticky = tk.W, **self.paddings)
        
        self.HeightWallChoiceSubmit.grid(column = 2, row = 12, sticky = tk.W, **self.paddings)

    def Delete_HeightWallChoice(self) :
        self.HeightWallChoiceLabel.grid_remove()
        self.HeightWallChoiceEntry.grid_remove()
        self.HeightWallChoiceSubmit.grid_remove()
        
    def Get_HeightWallChoice(self) :
        self.Delete_AllWithoutImage(5)
        Choice = self.HeightWallChoiceEntry.get()
        isOK = TF.isPositiveFloat(Choice)
        if isOK == True :
            self.Display_ThicknessWallChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive float")
            self.Message.grid(column = 3, row = 12, sticky = tk.W, **self.paddings)
        
    # Thickness Wall Choice (float)
    def Display_ThicknessWallChoice(self) :
        self.ThicknessWallChoiceLabel.grid(column = 0, row = 13, sticky = tk.W, **self.paddings)
        
        self.ThicknessWallChoiceEntry = tk.Entry(self)
        self.ThicknessWallChoiceEntry.grid(column = 1, row = 13, sticky = tk.W, **self.paddings)
        
        self.ThicknessWallChoiceSubmit.grid(column = 2, row = 13, sticky = tk.W, **self.paddings)
    
    def Delete_ThicknessWallChoice(self) :
        self.ThicknessWallChoiceLabel.grid_remove()
        self.ThicknessWallChoiceEntry.grid_remove()
        self.ThicknessWallChoiceSubmit.grid_remove()

    def Get_ThicknessWallChoice(self) :
        self.Delete_AllWithoutImage(4)
        Choice = self.ThicknessWallChoiceEntry.get()
        isOK = TF.isPositiveFloat(Choice)
        if isOK == True :
            self.Display_TransparencyWallChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive float")
            self.Message.grid(column = 3, row = 13, sticky = tk.W, **self.paddings)
        
    # Transparency Wall Choice (float)
    def Display_TransparencyWallChoice(self) :
        self.TransparencyWallChoiceLabel.grid(column = 0, row = 14, sticky = tk.W, **self.paddings)
        
        self.TransparencyWallChoiceEntry = tk.Entry(self)
        self.TransparencyWallChoiceEntry.grid(column = 1, row = 14, sticky = tk.W, **self.paddings)
        
        self.TransparencyWallChoiceSubmit.grid(column = 2, row = 14, sticky = tk.W, **self.paddings)
        
    def Delete_TransparencyWallChoice(self) :
        self.TransparencyWallChoiceLabel.grid_remove()
        self.TransparencyWallChoiceEntry.grid_remove()
        self.TransparencyWallChoiceSubmit.grid_remove()
        
    def Get_TransparencytWallChoice(self) :
        self.Delete_AllWithoutImage(3)
        Choice = self.TransparencyWallChoiceEntry.get()
        isOK = TF.is01Float(Choice)
        if isOK == True :
            self.Display_DeleteLineChoice()
        else :
            self.Message = tk.Message(self, text = "Not an expected float")
            self.Message.grid(column = 3, row = 14, sticky = tk.W, **self.paddings)
        
    # Delete Line Option
    def Display_DeleteLineChoice(self) :
        self.DeleteLineChoiceLabel.grid(column = 0, row = 15, sticky = tk.W, **self.paddings)
        
        self.DeleteLineChoice = tk.StringVar()
        self.DeleteLineChoiceMenu = tk.OptionMenu(self, self.DeleteLineChoice, *self.YesNoOption, command = self.Get_DeleteLineChoice)
        self.DeleteLineChoiceMenu.grid(column = 1, row = 15, sticky = tk.W, **self.paddings)
        
    def Delete_DeleteLineChoice(self) :
        self.DeleteLineChoiceLabel.grid_remove()
        self.DeleteLineChoiceMenu.grid_remove()
        
    def Get_DeleteLineChoice(self, Choice) :
        self.Delete_AllWithoutImage(2)
        Choice = self.DeleteLineChoice.get()
        if Choice == 'Yes' :
            if len(self.WallsCanvas) == 0 :
                self.Message = tk.Message(self, text = "No line left")
                self.Message.grid(column = 3, row = 15, sticky = tk.W, **self.paddings)
            else : 
                self.Display_DeleteLineCanvas()
        elif Choice == 'No' :
            self.Display_LengthFigureChoice()
            
    # Canvas : Line deletion
    def Display_DeleteLineCanvas(self) :
        min_x, min_y, max_x, max_y = TF.get_min_max(self.WallsCanvas)
        
        self.line = []
        self.line_index = 0
        
        self.W = int(max_x + min_x)
        self.H = int(max_y + min_y)

        Choice = self.FeatureChoice.get()
        if Choice == 'Manual' :
            self.Grid_size = int(700 / max(self.W, self.H))
        elif Choice == 'Image' :
            if max(self.W, self.H) < 350 :
                self.Grid_size = int(700 / max(self.W, self.H))
            else :
                self.Grid_size = 1
        self.Width = self.W * self.Grid_size 
        self.Height = self.H * self.Grid_size
        self.Canvas = tk.Canvas(self, width = self.Width, height = self.Height)
        self.Create_grid()
        self.Add_from_points_DeleteLine()
        self.Canvas.grid(column = 4, row = 0, sticky = tk.W, **self.paddings)

        self.Canvas.bind("<Button-1>", self.Add_point_DeleteLine)
        self.Canvas.bind("<Button-3>", self.Remove_last_DeleteLine)
            
        self.Finish_Button = tk.Button(self, text = "Finish", command = self.Finish_DeleteLine)
        self.Delete_Button = tk.Button(self, text = "Delete Line", command = self.DeleteLine)
        
        self.Delete_Button.grid(column = 4, row = 1, sticky = tk.W, **self.paddings)
        self.Finish_Button.grid(column = 4, row = 2, sticky = tk.W, **self.paddings)
        
    def Add_point_DeleteLine(self, event) :
        x, y = event.x, event.y
        x, y = x / self.Grid_size, y / self.Grid_size
        temp_x, temp_y = int(x), int(y)
        self.MessagePointPosition.grid_remove()
        if abs(temp_x - x) > 0.5 :
            x = temp_x + 1
        else :
            x = temp_x
        if abs(temp_y - y) > 0.5 :
            y = temp_y + 1
        else : 
            y = temp_y
        if len(self.line) < 2 :
            if self.FeatureChoice.get() == 'Manual' : 
                if len(self.line) == 0 :
                    isOK = False
                    for i in range(len(self.WallsCanvas)) :
                        if self.WallsCanvas[i] == [x, y] and isOK == False :
                            isOK = True
                            self.line.append((x, y))
                            
                            PointPosition = "Point coordinates : " + str(self.line[-1])
                            self.MessagePointPosition = tk.Message(self, text = PointPosition)
                            self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)

                            self.Canvas.create_oval(self.line[0][0] * self.Grid_size - 4, self.line[0][1] * self.Grid_size - 4, self.line[0][0] * self.Grid_size + 4, self.line[0][1] * self.Grid_size + 4, fill = "red")
                elif len(self.line) == 1 :
                    isOK = False
                    for i in range(int(len(self.WallsCanvas) / 2)) :
                        H_1 = self.WallsCanvas[2 * i]
                        H_2 = self.WallsCanvas[2 * i + 1]
                        L_1 = self.line[0]

                        if [H_1[0], H_1[1]] == [L_1[0], L_1[1]] :
                            if [x, y] == [H_2[0], H_2[1]] and isOK == False :
                                isOK = True
                                self.line_index = i
                                self.line.append((x, y))
                                
                                PointPosition = "Point coordinates : " + str(self.line[-1])
                                self.MessagePointPosition = tk.Message(self, text = PointPosition)
                                self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
                            
                                self.Canvas.create_line(self.line[0][0] * self.Grid_size, self.line[0][1] * self.Grid_size, self.line[1][0] * self.Grid_size, self.line[1][1] * self.Grid_size, fill = "red")
                                self.Canvas.create_oval(self.line[1][0] * self.Grid_size - 4, self.line[1][1] * self.Grid_size - 4, self.line[1][0] * self.Grid_size + 4, self.line[1][1] * self.Grid_size + 4, fill = "red")
                        elif [H_2[0], H_2[1]] == [L_1[0], L_1[1]] :
                            if [x, y] == [H_1[0], H_1[1]] and isOK == False :
                                isOK = True
                                self.line_index = i
                                self.line.append((x, y))
                                
                                PointPosition = "Point coordinates : " + str(self.line[-1])
                                self.MessagePointPosition = tk.Message(self, text = PointPosition)
                                self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
                                
                                self.Canvas.create_line(self.line[0][0] * self.Grid_size, self.line[0][1] * self.Grid_size, self.line[1][0] * self.Grid_size, self.line[1][1] * self.Grid_size, fill = "red")
                                self.Canvas.create_oval(self.line[1][0] * self.Grid_size - 4, self.line[1][1] * self.Grid_size - 4, self.line[1][0] * self.Grid_size + 4, self.line[1][1] * self.Grid_size + 4, fill = "red")
            else : 
                if len(self.line) == 0 :
                    isOK = False
                    for i in range(len(self.WallsCanvas)) :
                        if isOK == False and math.dist(self.WallsCanvas[i], [x, y]) <= 5 :
                            isOK = True
                            self.line.append((self.WallsCanvas[i][0], self.WallsCanvas[i][1]))
                            
                            PointPosition = "Point coordinates : " + str(self.line[-1])
                            self.MessagePointPosition = tk.Message(self, text = PointPosition)
                            self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
                            
                            self.Canvas.create_oval(self.line[0][0] * self.Grid_size - 4, self.line[0][1] * self.Grid_size - 4, self.line[0][0] * self.Grid_size + 4, self.line[0][1] * self.Grid_size + 4, fill = "red")
                elif len(self.line) == 1 :
                    isOK = False
                    for i in range(int(len(self.WallsCanvas) / 2)) :
                        H_1 = self.WallsCanvas[2 * i]
                        H_2 = self.WallsCanvas[2 * i + 1]
                        L_1 = self.line[0]

                        if [H_1[0], H_1[1]] == [L_1[0], L_1[1]] :
                            if isOK == False and math.dist([x, y],[H_2[0], H_2[1]]) <= 5 :
                                self.line_index = i
                                isOK = True
                                self.line.append((H_2[0], H_2[1]))
                                
                                PointPosition = "Point coordinates : " + str(self.line[-1])
                                self.MessagePointPosition = tk.Message(self, text = PointPosition)
                                self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
                            
                                self.Canvas.create_line(self.line[0][0] * self.Grid_size, self.line[0][1] * self.Grid_size, self.line[1][0] * self.Grid_size, self.line[1][1] * self.Grid_size, fill = "red")
                                self.Canvas.create_oval(self.line[1][0] * self.Grid_size - 4, self.line[1][1] * self.Grid_size - 4, self.line[1][0] * self.Grid_size + 4, self.line[1][1] * self.Grid_size + 4, fill = "red")
                        elif [H_2[0], H_2[1]] == [L_1[0], L_1[1]] :
                            if isOK == False and math.dist([x, y], [H_1[0], H_1[1]]) <= 5 :
                                self.line_index = i 
                                isOK = True
                                self.line.append((H_1[0], H_1[1]))
                                
                                PointPosition = "Point coordinates : " + str(self.line[-1])
                                self.MessagePointPosition = tk.Message(self, text = PointPosition)
                                self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
                            
                                self.Canvas.create_line(self.line[0][0] * self.Grid_size, self.line[0][1] * self.Grid_size, self.line[1][0] * self.Grid_size, self.line[1][1] * self.Grid_size, fill = "red")
                                self.Canvas.create_oval(self.line[1][0] * self.Grid_size - 4, self.line[1][1] * self.Grid_size - 4, self.line[1][0] * self.Grid_size + 4, self.line[1][1] * self.Grid_size + 4, fill = "red")
                
    def Add_from_points_DeleteLine(self) :
        for i in range(0, len(self.WallsCanvas) - 1, 2) :
            self.Canvas.create_line(self.WallsCanvas[i][0] * self.Grid_size, self.WallsCanvas[i][1] * self.Grid_size, self.WallsCanvas[i + 1][0] * self.Grid_size, self.WallsCanvas[i + 1][1] * self.Grid_size, fill = "blue")
        if len(self.line) == 1 :
            self.Canvas.create_oval(self.line[0][0] * self.Grid_size - 4, self.line[0][1] * self.Grid_size - 4, self.line[0][0] * self.Grid_size + 4, self.line[0][1] * self.Grid_size + 4, fill = "red")
        elif len(self.line) == 2 : 
            self.Canvas.create_line(self.line[0][0] * self.Grid_size, self.line[0][1] * self.Grid_size, self.line[1][0] * self.Grid_size, self.line[1][1] * self.Grid_size, fill = "red")
            self.Canvas.create_oval(self.line[0][0] * self.Grid_size - 4, self.line[0][1] * self.Grid_size - 4, self.line[0][0] * self.Grid_size + 4, self.line[0][1] * self.Grid_size + 4, fill = "red")
            self.Canvas.create_oval(self.line[1][0] * self.Grid_size - 4, self.line[1][1] * self.Grid_size - 4, self.line[1][0] * self.Grid_size + 4, self.line[1][1] * self.Grid_size + 4, fill = "red")

    def DeleteLine(self) :
        self.Message.grid_remove()
        self.MessagePointPosition.grid_remove()
        if len(self.line) == 2 : 
            del(self.WallsCanvas[2 * self.line_index + 1])
            del(self.WallsCanvas[2 * self.line_index])
            del(self.Walls[2 * self.line_index + 1])
            del(self.Walls[2 * self.line_index])
            self.line = []
            self.Canvas.delete("all")
            self.Create_grid()
            self.Add_from_points_DeleteLine()
        else : 
            self.Message = tk.Message(self, text = "No line selected")
            self.Message.grid(column = 5, row = 0, sticky = tk.W, **self.paddings)
            
    def Finish_DeleteLine(self) : 
        self.Message.grid_remove()
        self.MessagePointPosition.grid_remove()
        self.Delete_DeleteLineCanvas()

    def Remove_last_DeleteLine(self, event) :
        self.MessagePointPosition.grid_remove()
        if (len(self.line)) > 0 :
            self.line.pop(-1)
        self.Canvas.delete("all")
        self.Create_grid()
        self.Add_from_points_DeleteLine()
        
    def Delete_DeleteLineCanvas(self) : 
        self.Canvas.grid_remove()
        self.Delete_Button.grid_remove()
        self.Finish_Button.grid_remove()
        self.Display_LengthFigureChoice()
        
    # Figure length Option
    def Display_LengthFigureChoice(self) :
        self.LengthFigureChoiceLabel.grid(column = 0, row = 16, sticky = tk.W, **self.paddings)
        
        self.LengthFigureChoice = tk.StringVar()
        self.LengthFigureChoiceMenu = tk.OptionMenu(self, self.LengthFigureChoice, *self.LengthFigureChoiceOption, command = self.Get_LengthFigureChoice)
        self.LengthFigureChoiceMenu.grid(column = 1, row = 16, sticky = tk.W, **self.paddings)
        
    def Delete_LengthFigureChoice(self) :
        self.LengthFigureChoiceLabel.grid_remove()
        self.LengthFigureChoiceMenu.grid_remove()
        
    def Get_LengthFigureChoice(self, Choice) :
        self.Delete_AllWithoutImage(1)
        Choice = self.LengthFigureChoice.get()
        if Choice == 'Define the total length of the figure' :
            self.Display_ConstantLengthFigureChoice()
        elif Choice == 'Define the length of a line' :
            if len(self.WallsCanvas) == 0 :
                self.Message = tk.Message(self, text = "No line left")
                self.Message.grid(column = 3, row = 16, sticky = tk.W, **self.paddings)
            else :
                self.Display_SelectLineCanvas()
        
    # Canvas : Select line
    def Display_SelectLineCanvas(self) :
        min_x, min_y, max_x, max_y = TF.get_min_max(self.WallsCanvas)
        
        self.line = []
        self.line_index = 0
        self.dist_line = 0
        
        self.W = int(max_x + min_x)
        self.H = int(max_y + min_y)

        Choice = self.FeatureChoice.get()
        if Choice == 'Manual' :
            self.Grid_size = int(700 / max(self.W, self.H))
        elif Choice == 'Image' :
            if max(self.W, self.H) < 350 :
                self.Grid_size = int(700 / max(self.W, self.H))
            else :
                self.Grid_size = 1
        self.Width = self.W * self.Grid_size 
        self.Height = self.H * self.Grid_size
        self.Canvas = tk.Canvas(self, width = self.Width, height = self.Height)
        self.Create_grid()
        self.Add_from_points_SelectLine()
        self.Canvas.grid(column = 4, row = 0, sticky = tk.W, **self.paddings)

        self.Canvas.bind("<Button-1>", self.Add_point_SelectLine)
        self.Canvas.bind("<Button-3>", self.Remove_last_SelectLine)
            
        self.Finish_Button = tk.Button(self, text = "Finish", command = self.Finish_SelectLine)

        self.Finish_Button.grid(column = 4, row = 1, sticky = tk.W, **self.paddings)
        
    def Add_point_SelectLine(self, event) :
        x, y = event.x, event.y
        x, y = x / self.Grid_size, y / self.Grid_size
        temp_x, temp_y = int(x), int(y)
        self.MessagePointPosition.grid_remove()
        if abs(temp_x - x) > 0.5 :
            x = temp_x + 1
        else :
            x = temp_x
        if abs(temp_y - y) > 0.5 :
            y = temp_y + 1
        else : 
            y = temp_y

        if len(self.line) < 2 :
            if self.FeatureChoice.get() == 'Manual' : 
                if len(self.line) == 0 :
                    isOK = False
                    for i in range(len(self.WallsCanvas)) :
                        if self.WallsCanvas[i] == [x, y] and isOK == False :
                            isOK = True
                            self.line.append((x, y))
                            
                            PointPosition = "Point coordinates : " + str(self.line[-1])
                            self.MessagePointPosition = tk.Message(self, text = PointPosition)
                            self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
                            
                            self.Canvas.create_oval(self.line[0][0] * self.Grid_size - 4, self.line[0][1] * self.Grid_size - 4, self.line[0][0] * self.Grid_size + 4, self.line[0][1] * self.Grid_size + 4, fill = "red")
                elif len(self.line) == 1 :
                    isOK = False
                    for i in range(int(len(self.WallsCanvas) / 2)) :
                        H_1 = self.WallsCanvas[2 * i]
                        H_2 = self.WallsCanvas[2 * i + 1]
                        L_1 = self.line[0]

                        if [H_1[0], H_1[1]] == [L_1[0], L_1[1]] :
                            if [x, y] == [H_2[0], H_2[1]] and isOK == False :
                                isOK = True
                                self.line.append((x, y))
                                
                                PointPosition = "Point coordinates : " + str(self.line[-1])
                                self.MessagePointPosition = tk.Message(self, text = PointPosition)
                                self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
                            
                                self.Canvas.create_line(self.line[0][0] * self.Grid_size, self.line[0][1] * self.Grid_size, self.line[1][0] * self.Grid_size, self.line[1][1] * self.Grid_size, fill = "red")
                                self.Canvas.create_oval(self.line[1][0] * self.Grid_size - 4, self.line[1][1] * self.Grid_size - 4, self.line[1][0] * self.Grid_size + 4, self.line[1][1] * self.Grid_size + 4, fill = "red")
                        elif [H_2[0], H_2[1]] == [L_1[0], L_1[1]] :
                            if [x, y] == [H_1[0], H_1[1]] and isOK == False :
                                isOK = True
                                self.line.append((x, y))
                                
                                PointPosition = "Point coordinates : " + str(self.line[-1])
                                self.MessagePointPosition = tk.Message(self, text = PointPosition)
                                self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
                            
                                self.Canvas.create_line(self.line[0][0] * self.Grid_size, self.line[0][1] * self.Grid_size, self.line[1][0] * self.Grid_size, self.line[1][1] * self.Grid_size, fill = "red")
                                self.Canvas.create_oval(self.line[1][0] * self.Grid_size - 4, self.line[1][1] * self.Grid_size - 4, self.line[1][0] * self.Grid_size + 4, self.line[1][1] * self.Grid_size + 4, fill = "red")
            else : 
                if len(self.line) == 0 :
                    isOK = False
                    for i in range(len(self.WallsCanvas)) :
                        if isOK == False and math.dist(self.WallsCanvas[i], [x, y]) <= 5 :
                            isOK = True
                            self.line.append((self.WallsCanvas[i][0], self.WallsCanvas[i][1]))
                            
                            PointPosition = "Point coordinates : " + str(self.line[-1])
                            self.MessagePointPosition = tk.Message(self, text = PointPosition)
                            self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
                            
                            self.Canvas.create_oval(self.line[0][0] * self.Grid_size - 4, self.line[0][1] * self.Grid_size - 4, self.line[0][0] * self.Grid_size + 4, self.line[0][1] * self.Grid_size + 4, fill = "red")
                elif len(self.line) == 1 :
                    isOK = False
                    for i in range(int(len(self.WallsCanvas) / 2)) :
                        H_1 = self.WallsCanvas[2 * i]
                        H_2 = self.WallsCanvas[2 * i + 1]
                        L_1 = self.line[0]

                        if [H_1[0], H_1[1]] == [L_1[0], L_1[1]] :
                            if isOK == False and math.dist([x, y],[H_2[0], H_2[1]]) <= 5 :
                                isOK = True
                                self.line.append((H_2[0], H_2[1]))
                                
                                PointPosition = "Point coordinates : " + str(self.line[-1])
                                self.MessagePointPosition = tk.Message(self, text = PointPosition)
                                self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
                            
                                self.Canvas.create_line(self.line[0][0] * self.Grid_size, self.line[0][1] * self.Grid_size, self.line[1][0] * self.Grid_size, self.line[1][1] * self.Grid_size, fill = "red")
                                self.Canvas.create_oval(self.line[1][0] * self.Grid_size - 4, self.line[1][1] * self.Grid_size - 4, self.line[1][0] * self.Grid_size + 4, self.line[1][1] * self.Grid_size + 4, fill = "red")
                        elif [H_2[0], H_2[1]] == [L_1[0], L_1[1]] :
                            if isOK == False and math.dist([x, y], [H_1[0], H_1[1]]) <= 5 :
                                isOK = True
                                self.line.append((H_1[0], H_1[1]))
                                
                                PointPosition = "Point coordinates : " + str(self.line[-1])
                                self.MessagePointPosition = tk.Message(self, text = PointPosition)
                                self.MessagePointPosition.grid(column = 5, row = 1, sticky = tk.W, **self.paddings)
                            
                                self.Canvas.create_line(self.line[0][0] * self.Grid_size, self.line[0][1] * self.Grid_size, self.line[1][0] * self.Grid_size, self.line[1][1] * self.Grid_size, fill = "red")
                                self.Canvas.create_oval(self.line[1][0] * self.Grid_size - 4, self.line[1][1] * self.Grid_size - 4, self.line[1][0] * self.Grid_size + 4, self.line[1][1] * self.Grid_size + 4, fill = "red")
                
    def Add_from_points_SelectLine(self) :
        for i in range(0, len(self.WallsCanvas) - 1, 2) :
            self.Canvas.create_line(self.WallsCanvas[i][0] * self.Grid_size, self.WallsCanvas[i][1] * self.Grid_size, self.WallsCanvas[i + 1][0] * self.Grid_size, self.WallsCanvas[i + 1][1] * self.Grid_size, fill = "green")
        for i in range(0, len(self.WallsCanvas) - 1, 2) :
            self.Canvas.create_line(self.WallsCanvas[i][0] * self.Grid_size, self.WallsCanvas[i][1] * self.Grid_size, self.WallsCanvas[i + 1][0] * self.Grid_size, self.WallsCanvas[i + 1][1] * self.Grid_size, fill = "blue")
            self.Canvas.create_oval(self.WallsCanvas[i][0] * self.Grid_size - 3, self.WallsCanvas[i][1] * self.Grid_size - 3, self.WallsCanvas[i][0] * self.Grid_size + 3, self.WallsCanvas[i][1] * self.Grid_size + 3, fill = "blue")
            self.Canvas.create_oval(self.WallsCanvas[i + 1][0] * self.Grid_size - 3, self.WallsCanvas[i + 1][1] * self.Grid_size - 3, self.WallsCanvas[i + 1][0] * self.Grid_size + 3, self.WallsCanvas[i + 1][1] * self.Grid_size + 3, fill = "blue")
        if len(self.line) == 1 :
            self.Canvas.create_oval(self.line[0][0] * self.Grid_size - 4, self.line[0][1] * self.Grid_size - 4, self.line[0][0] * self.Grid_size + 4, self.line[0][1] * self.Grid_size + 4, fill = "red")
        elif len(self.line) == 2 : 
            self.Canvas.create_line(self.line[0][0] * self.Grid_size, self.line[0][1] * self.Grid_size, self.line[1][0] * self.Grid_size, self.line[1][1] * self.Grid_size, fill = "red")
            self.Canvas.create_oval(self.line[0][0] * self.Grid_size - 4, self.line[0][1] * self.Grid_size - 4, self.line[0][0] * self.Grid_size + 4, self.line[0][1] * self.Grid_size + 4, fill = "red")
            self.Canvas.create_oval(self.line[1][0] * self.Grid_size - 4, self.line[1][1] * self.Grid_size - 4, self.line[1][0] * self.Grid_size + 4, self.line[1][1] * self.Grid_size + 4, fill = "red")

    def Finish_SelectLine(self) : 
        self.Message.grid_remove()
        self.MessagePointPosition.grid_remove()
        if len(self.line) == 2 : 
            self.dist_line = math.dist(self.line[0], self.line[1])
            self.Delete_SelectLineCanvas()
        else : 
            self.Message = tk.Message(self, text = "No line selected")
            self.Message.grid(column = 5, row = 0, sticky = tk.W, **self.paddings)

    def Remove_last_SelectLine(self, event) :
        self.MessagePointPosition.grid_remove()
        if (len(self.line)) > 0 :
            self.line.pop(-1)
        self.Canvas.delete("all")
        self.Create_grid()
        self.Add_from_points_SelectLine()
        
    def Delete_SelectLineCanvas(self) :
        self.Canvas.grid_remove()
        self.Finish_Button.grid_remove()

        if self.dist_line != 0 :
            self.Display_LineLengthChoice()
        else : 
            self.LengthFigureChoice = 'Define the total length of the figure'
            self.Display_ConstantLengthFigureChoice()
        
    # Constant figure length choice (float)
    def Display_ConstantLengthFigureChoice(self) :
        self.ConstantLengthFigureChoiceLabel.grid(column = 0, row = 17, sticky = tk.W, **self.paddings)
        
        self.ConstantLengthFigureChoiceEntry = tk.Entry(self)
        self.ConstantLengthFigureChoiceEntry.grid(column = 1, row = 17, sticky = tk.W, **self.paddings)
        
        self.ConstantLengthFigureChoiceSubmit.grid(column = 2, row = 17, sticky = tk.W, **self.paddings)
        
    def Delete_ConstantLengthFigureChoice(self) :
        self.ConstantLengthFigureChoiceLabel.grid_remove()
        self.ConstantLengthFigureChoiceEntry.grid_remove()
        self.ConstantLengthFigureChoiceSubmit.grid_remove()
        
    def Get_ConstantLengthFigureChoice(self) :
        self.Delete_AllWithoutImage(0)
        Choice = self.ConstantLengthFigureChoiceEntry.get()
        isOK = TF.isPositiveFloat(Choice)
        if isOK == True :
            self.Display_WorldNameChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive float")
            self.Message.grid(column = 3, row = 17, sticky = tk.W, **self.paddings)
    
    # Lenght for a line (float)
    def Display_LineLengthChoice(self) :
        self.LineLengthChoiceLabel.grid(column = 0, row = 17, sticky = tk.W, **self.paddings)
        
        self.LineLengthChoiceEntry = tk.Entry(self)
        self.LineLengthChoiceEntry.grid(column = 1, row = 17, sticky = tk.W, **self.paddings)
        
        self.LineLengthChoiceSubmit.grid(column = 2, row = 17, sticky = tk.W, **self.paddings)
        
    def Delete_LineLengthChoice(self) :
        self.LineLengthChoiceLabel.grid_remove()
        self.LineLengthChoiceEntry.grid_remove()
        self.LineLengthChoiceSubmit.grid_remove()
        
    def Get_LineLengthChoice(self) :
        self.Delete_AllWithoutImage(0)
        Choice = self.LineLengthChoiceEntry.get()
        isOK = TF.isPositiveFloat(Choice)
        if isOK == True :
            self.Display_WorldNameChoice()
        else :
            self.Message = tk.Message(self, text = "Not a positive float")
            self.Message.grid(column = 3, row = 17, sticky = tk.W, **self.paddings)
    
    # Name for the webots world (str)
    def Display_WorldNameChoice(self) :
        self.WorldNameChoiceLabel.grid(column = 0, row = 18, sticky = tk.W, **self.paddings)
        
        self.WorldNameChoiceEntry = tk.Entry(self)
        self.WorldNameChoiceEntry.grid(column = 1, row = 18, sticky = tk.W, **self.paddings)
        
        self.WorldNameChoiceSubmit.grid(column = 2, row = 18, sticky = tk.W, **self.paddings)

    def Delete_WorldNameChoice(self) :
        self.WorldNameChoiceLabel.grid_remove()
        self.WorldNameChoiceEntry.grid_remove()
        self.WorldNameChoiceSubmit.grid_remove()
        
    def Get_WorldNameChoice(self) :
        Choice = self.WorldNameChoiceEntry.get()
        self.Message.grid_remove()
        if len(Choice) > 0 :
            self.Generate_Without_Image()
        else :
            self.Message = tk.Message(self, text = "NULL String")
            self.Message.grid(column = 3, row = 18, sticky = tk.W, **self.paddings)
    
    # Generate one webots world from Manual Mode
    def Generate_Without_Image(self) :
        file_name = self.WorldNameChoiceEntry.get()

        if self.DefaultConfigurationChoice.get() == 'Use' : 
            wall_height = float(self.config[8])
            wall_thickness = float(self.config[9])
            wall_transparency = float(self.config[10])
        elif self.DefaultConfigurationChoice.get() == 'Not used' : 
            wall_height = float(self.HeightWallChoiceEntry.get())
            wall_thickness = float(self.ThicknessWallChoiceEntry.get())
            wall_transparency = float(self.TransparencyWallChoiceEntry.get())

        min_x, min_y, max_x, max_y = TF.get_min_max(self.Walls)

        gap_x = max_x - min_x

        if self.LengthFigureChoice.get() == 'Define the total length of the figure' :
            size_length = float(self.ConstantLengthFigureChoiceEntry.get())
        elif self.LengthFigureChoice.get() == 'Define the length of a line' :
            line_length = float(self.LineLengthChoiceEntry.get())
            size_length = float((line_length / float(self.dist_line)) * gap_x)
            print(" Total length of the figure : " + str(round(size_length, 2)) + " meters")
        
        if self.FeatureChoice.get() == 'Manual' :
            F.Write_Webots_File(file_name, 1, 2, min_x, max_x, min_y, max_y, size_length, self.Walls, int(len(self.Walls) / 2), wall_height, wall_thickness, wall_transparency)
        elif self.FeatureChoice.get() == 'Image' :
            F.Write_Webots_File(file_name, 2, 2, min_x, max_x, min_y, max_y, size_length, self.Walls, int(len(self.Walls) / 2), wall_height, wall_thickness, wall_transparency)
    
    # Choose the image folder
    def Display_ImageFolderNameChoice(self) :
        self.ImageFolderNameChoiceLabel.grid(column = 0, row = 3, sticky = tk.W, **self.paddings)
        
        self.ImageFolderNameChoice = tk.StringVar()
        self.ImageFolderNameChoiceMenu = tk.OptionMenu(self, self.ImageFolderNameChoice, *self.ImageFolderNameChoiceOption, command = self.Get_ImageFolderNameChoice)
        self.ImageFolderNameChoiceMenu.grid(column = 1, row = 3, sticky = tk.W, **self.paddings)
        
    def Delete_ImageFolderNameChoice(self) :
        self.ImageFolderNameChoiceLabel.grid_remove()
        self.ImageFolderNameChoiceMenu.grid_remove()
        
    def Get_ImageFolderNameChoice(self, Choice) :
        self.Delete_AllWithoutImage(6)
        self.Delete_AllWithImage(6)
        self.Display_ImageNameChoice()
        
    # Choose one image
    def Display_ImageNameChoice(self) :
        self.ImageNameChoiceLabel.grid(column = 0, row = 4, sticky = tk.W, **self.paddings)
        self.ImageNameChoice = tk.StringVar()
        self.ImageNameChoiceOption = []
        file = os.listdir(self.ImageFolderNameChoice.get())
        for name in file:
            image = cv2.imread(str(self.ImageFolderNameChoice.get()) + "/" + name)
            if image is not None :
                self.ImageNameChoiceOption.append(name)
        self.ImageNameChoiceMenu = tk.OptionMenu(self, self.ImageNameChoice, *self.ImageNameChoiceOption, command = self.Get_ImageNameChoice)
        self.ImageNameChoiceMenu.grid(column = 1, row = 4, sticky = tk.W, **self.paddings)

    def Delete_ImageNameChoice(self) :
        self.ImageNameChoiceLabel.grid_remove()
        self.ImageNameChoiceMenu.grid_remove()
        
    def Get_ImageNameChoice(self, Choice) :
        self.Delete_AllWithoutImage(6)
        self.Delete_AllWithImage(5)
        if self.DefaultConfigurationChoice.get() == 'Use' :
            self.Display_BinaryThresholdResult()
        elif self.DefaultConfigurationChoice.get() == 'Not used' :
            self.Display_BinaryThresholdChoice()
        
    # Choose the binary threshold (int)
    def Display_BinaryThresholdChoice(self) :
        self.BinaryThresholdChoiceLabel0.grid(column = 0, row = 5, sticky = tk.W, **self.paddings)
        
        self.BinaryThresholdChoiceLabel.grid(column = 0, row = 6, sticky = tk.W, **self.paddings)
        self.BinaryThresholdChoiceEntry = tk.Entry(self)
        self.BinaryThresholdChoiceEntry.grid(column = 1, row = 6, sticky = tk.W, **self.paddings)
        
        self.BinaryThresholdChoiceSubmit.grid(column = 2, row = 6, sticky = tk.W, **self.paddings)
        
    def Delete_BinaryThresholdChoice(self) :
        self.BinaryThresholdChoiceLabel0.grid_remove()
        self.BinaryThresholdChoiceLabel.grid_remove()
        self.BinaryThresholdChoiceEntry.grid_remove()
        self.BinaryThresholdChoiceSubmit.grid_remove()
        
    def Get_BinaryThresholdChoice(self) :
        self.Delete_AllWithoutImage(6)
        self.Delete_AllWithImage(4)
        Choice = self.BinaryThresholdChoiceEntry.get()
        isOK = TF.isPositiveMinMaxInteger(Choice, 0, 255)
        if isOK == True :
            self.Display_BinaryThresholdResult()
        else : 
            self.Message = tk.Message(self, text = "Not an int between 0 and 255")
            self.Message.grid(column = 3, row = 6, sticky = tk.W, **self.paddings)
    
    # Display the result with the selected binary threshold
    def Display_BinaryThresholdResult(self) :
        if self.DefaultConfigurationChoice.get() == 'Use' :
            gray_threshold = int(self.config[2])
        elif self.DefaultConfigurationChoice.get() == 'Not used' :
            gray_threshold = int(self.BinaryThresholdChoiceEntry.get())
            
        image = cv2.imread(str(self.ImageFolderNameChoice.get()) + "/" + str(self.ImageNameChoice.get()))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, gray_threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow("Close the window | Press Enter", binary)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if self.DefaultConfigurationChoice.get() == 'Use' :
            self.Display_LineDetectionResult()
        elif self.DefaultConfigurationChoice.get() == 'Not used' :
            self.Display_LineDetectionChoice()

    # Line choice for line detection (int)
    def Display_LineDetectionChoice(self) :
        self.LineDetectionChoiceLabel.grid(column = 0, row = 7, sticky = tk.W, **self.paddings)
        
        self.LineDetectionChoiceEntry = tk.Entry(self)
        self.LineDetectionChoiceEntry.grid(column = 1, row = 7, sticky = tk.W, **self.paddings)
        
        self.LineDetectionChoiceSubmit.grid(column = 2, row = 7, sticky = tk.W, **self.paddings)
        
    def Delete_LineDetectionChoice(self) :
        self.LineDetectionChoiceLabel.grid_remove()
        self.LineDetectionChoiceEntry.grid_remove()
        self.LineDetectionChoiceSubmit.grid_remove()
        
    def Get_LineDetectionChoice(self) :
        self.Delete_AllWithoutImage(6)
        self.Delete_AllWithImage(3)
        Choice = self.LineDetectionChoiceEntry.get()
        isOK = TF.isPositiveInteger(Choice)
        if isOK == True :
            self.Display_GapLineDetectionChoice()
        else : 
            self.Message = tk.Message(self, text = "Not a positive int")
            self.Message.grid(column = 3, row = 7, sticky = tk.W, **self.paddings)
            
    # Gap line for line detection (int)
    def Display_GapLineDetectionChoice(self) :
        self.GapLineDetectionChoiceLabel.grid(column = 0, row = 8, sticky = tk.W, **self.paddings)
        
        self.GapLineDetectionChoiceEntry = tk.Entry(self)
        self.GapLineDetectionChoiceEntry.grid(column = 1, row = 8, sticky = tk.W, **self.paddings)
        
        self.GapLineDetectionChoiceSubmit.grid(column = 2, row = 8, sticky = tk.W, **self.paddings)
        
    def Delete_GapLineDetectionChoice(self) :
        self.GapLineDetectionChoiceLabel.grid_remove()
        self.GapLineDetectionChoiceEntry.grid_remove()
        self.GapLineDetectionChoiceSubmit.grid_remove()
        
    def Get_GapLineDetectionChoice(self) :
        self.Delete_AllWithoutImage(6)
        self.Delete_AllWithImage(2)
        Choice = self.GapLineDetectionChoiceEntry.get()
        isOK = TF.isPositiveInteger(Choice)
        if isOK == True :
            self.Display_LineDetectionResult()
        else : 
            self.Message = tk.Message(self, text = "Not a positive int")
            self.Message.grid(column = 3, row = 8, sticky = tk.W, **self.paddings)
        
    # Display the line detection result
    def Display_LineDetectionResult(self) :
        if self.DefaultConfigurationChoice.get() == 'Use' :
            gray_threshold = int(self.config[2])
            hough_minLineLength = int(self.config[3])
            hough_maxLineGap = int(self.config[4])
        elif self.DefaultConfigurationChoice.get() == 'Not used' :
            gray_threshold = int(self.BinaryThresholdChoiceEntry.get())
            hough_minLineLength = int(self.LineDetectionChoiceEntry.get())
            hough_maxLineGap = int(self.GapLineDetectionChoiceEntry.get())
            
        image = cv2.imread(str(self.ImageFolderNameChoice.get()) + "/" + str(self.ImageNameChoice.get()))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, gray_threshold, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(binary, 50, 150)
        lines = cv2.HoughLinesP(edges, rho = 1, theta = np.pi/180, threshold = hough_minLineLength, minLineLength = hough_minLineLength, maxLineGap = hough_maxLineGap)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("Close the window | Press Enter", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if self.DefaultConfigurationChoice.get() == 'Use' :
            self.Display_AngleResult()
        elif self.DefaultConfigurationChoice.get() == 'Not used' :
            self.Display_AngleChoice()
        
    # Angle choice (int)
    def Display_AngleChoice(self) :
        self.AngleChoiceLabel.grid(column = 0, row = 9, sticky = tk.W, **self.paddings)
        
        self.AngleChoiceEntry = tk.Entry(self)
        self.AngleChoiceEntry.grid(column = 1, row = 9, sticky = tk.W, **self.paddings)
        
        self.AngleChoiceSubmit.grid(column = 2, row = 9, sticky = tk.W, **self.paddings)
        
    def Delete_AngleChoice(self) :
        self.AngleChoiceLabel.grid_remove()
        self.AngleChoiceEntry.grid_remove()
        self.AngleChoiceSubmit.grid_remove()
        
    def Get_AngleChoice(self) :
        self.Delete_AllWithoutImage(6)
        self.Delete_AllWithImage(1)
        Choice = self.GapLineDetectionChoiceEntry.get()
        isOK = TF.isPositiveMinMaxInteger(Choice, 0, 45)
        if isOK == True :
            self.Display_AngleResult()
        else : 
            self.Message = tk.Message(self, text = "Not a positive int between 0 and 45")
            self.Message.grid(column = 3, row = 9, sticky = tk.W, **self.paddings)
        
    # Display the result
    def Display_AngleResult(self) :
        if self.DefaultConfigurationChoice.get() == 'Use' :
            gray_threshold = int(self.config[2])
            hough_minLineLength = int(self.config[3])
            hough_maxLineGap = int(self.config[4])
            angle = int(self.config[5])
        elif self.DefaultConfigurationChoice.get() == 'Not used' :
            gray_threshold = int(self.BinaryThresholdChoiceEntry.get())
            hough_minLineLength = int(self.LineDetectionChoiceEntry.get())
            hough_maxLineGap = int(self.GapLineDetectionChoiceEntry.get())
            angle = int(self.GapLineDetectionChoiceEntry.get())
            
        image = cv2.imread(str(self.ImageFolderNameChoice.get()) + "/" + str(self.ImageNameChoice.get()))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, gray_threshold, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(binary, 50, 150)
        lines = cv2.HoughLinesP(edges, rho = 1, theta = np.pi/180, threshold = hough_minLineLength, minLineLength = hough_minLineLength, maxLineGap = hough_maxLineGap)
        
        W_room = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            W_room.append([x1, y1])
            W_room.append([x2, y2])
        W_vertical, W_horizontal, W_left_diagonal, W_right_diagonal, W_left_angle_diagonal, W_right_angle_diagonal = BT.line_separation(W_room, angle)
        print("Initial")
        print("The size of the image is : " + str(len(image[0])) + " x " + str(len(image)))
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
        if self.DefaultConfigurationChoice.get() == 'Use' :
            self.Display_LineTreatmentResult()
        elif self.DefaultConfigurationChoice.get() == 'Not used' :
            self.Display_GapSameLine()
            
    # Gap for line treatment (int)
    def Display_GapSameLine(self) :
        self.GapSameLineLabel.grid(column = 0, row = 10, sticky = tk.W, **self.paddings)
        
        self.GapSameLineEntry = tk.Entry(self)
        self.GapSameLineEntry.grid(column = 1, row = 10, sticky = tk.W, **self.paddings)
        
        self.GapSameLineSubmit.grid(column = 2, row = 10, sticky = tk.W, **self.paddings)

    def Delete_GapSameLine(self) :
        self.GapSameLineLabel.grid_remove()
        self.GapSameLineEntry.grid_remove()
        self.GapSameLineSubmit.grid_remove()

    def Get_GapSameLine(self) :
        self.Delete_AllWithoutImage(6)
        self.Delete_AllWithImage(0)
        Choice = self.GapSameLineEntry.get()
        isOK = TF.isPositiveInteger(Choice)
        if isOK == True :
            self.Display_GapParallelLine()
        else : 
            self.Message = tk.Message(self, text = "Not a positive int")
            self.Message.grid(column = 3, row = 10, sticky = tk.W, **self.paddings)
    
    # Gap for parallel line treatment
    def Display_GapParallelLine(self) :
        self.GapParallelLineLabel.grid(column = 0, row = 11, sticky = tk.W, **self.paddings)
        
        self.GapParallelLineEntry = tk.Entry(self)
        self.GapParallelLineEntry.grid(column = 1, row = 11, sticky = tk.W, **self.paddings)
        
        self.GapParallelLineSubmit.grid(column = 2, row = 11, sticky = tk.W, **self.paddings)
        
    def Delete_GapParallelLine(self) :
        self.GapParallelLineLabel.grid_remove()
        self.GapParallelLineEntry.grid_remove()
        self.GapParallelLineSubmit.grid_remove()
        
    def Get_GapParallelLine(self) :
        self.Delete_AllWithoutImage(6)
        Choice = self.GapParallelLineEntry.get()
        isOK = TF.isPositiveInteger(Choice)
        if isOK == True :
            self.Display_LineTreatmentResult()
        else : 
            self.Message = tk.Message(self, text = "Not a positive int")
            self.Message.grid(column = 3, row = 11, sticky = tk.W, **self.paddings)
        
    # Display the result after all the line treatment
    def Display_LineTreatmentResult(self) : 
        if self.DefaultConfigurationChoice.get() == 'Use' :
            gray_threshold = int(self.config[2])
            hough_minLineLength = int(self.config[3])
            hough_maxLineGap = int(self.config[4])
            angle = int(self.config[5])
            gap_length = int(self.config[6])
            gap = int(self.config[7])
        elif self.DefaultConfigurationChoice.get() == 'Not used' :
            gray_threshold = int(self.BinaryThresholdChoiceEntry.get())
            hough_minLineLength = int(self.LineDetectionChoiceEntry.get())
            hough_maxLineGap = int(self.GapLineDetectionChoiceEntry.get())
            angle = int(self.GapLineDetectionChoiceEntry.get())
            gap_length = int(self.GapSameLineEntry.get())
            gap = int(self.GapParallelLineEntry.get())
            
        image = cv2.imread(str(self.ImageFolderNameChoice.get()) + "/" + str(self.ImageNameChoice.get()))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, gray_threshold, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(binary, 50, 150)
        lines = cv2.HoughLinesP(edges, rho = 1, theta = np.pi/180, threshold = hough_minLineLength, minLineLength = hough_minLineLength, maxLineGap = hough_maxLineGap)
        
        W_room = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            W_room.append([x1, y1])
            W_room.append([x2, y2])
        W_vertical, W_horizontal, W_left_diagonal, W_right_diagonal, W_left_angle_diagonal, W_right_angle_diagonal = BT.line_separation(W_room, angle)
        print("After Line Treatment")
        print("The size of the image is : " + str(len(image[0])) + " x " + str(len(image)))
    
        if len(W_vertical) > 3 :
            W_vertical = BT.vertical_or_horizontal_extension('Vertical', W_vertical, gap_length)
        if len(W_horizontal) > 3 :
            W_horizontal = BT.vertical_or_horizontal_extension('Horizontal', W_horizontal, gap_length)
        if len(W_left_diagonal) > 3 :
            W_left_diagonal, W_left_angle_diagonal = BT.left_or_right_diagonal_extension('Left_Diagonal', W_left_diagonal, W_left_angle_diagonal, gap_length)
        if len(W_right_diagonal) > 3 :
            W_right_diagonal, W_right_angle_diagonal = BT.left_or_right_diagonal_extension('Right_Diagonal', W_right_diagonal, W_right_angle_diagonal, gap_length)
        if len(W_vertical) > 3 :
            W_vertical = BT.remove_extra_vertical_or_horizontal('Vertical', W_vertical, gap)
        if len(W_horizontal) > 3 :
            W_horizontal = BT.remove_extra_vertical_or_horizontal('Horizontal', W_horizontal, gap)
        if len(W_left_diagonal) > 3 :
            W_left_diagonal = BT.remove_extra_left_or_right_diagonal('Left_Diagonal', W_left_diagonal, W_left_angle_diagonal, gap, len(image[0]), len(image))
        if len(W_right_diagonal) > 3 :
            W_right_diagonal = BT.remove_extra_left_or_right_diagonal('Right_Diagonal', W_right_diagonal, W_right_angle_diagonal, gap, len(image[0]), len(image))

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
            
        cv2.imshow("Close the window | Press Enter", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        image = cv2.imread(str(self.ImageFolderNameChoice.get()) + "/" + str(self.ImageNameChoice.get()))
        self.Walls, W_vertical, W_horizontal, W_diagonal = BT.fill_hole(W_vertical, W_horizontal, W_left_diagonal, W_right_diagonal, gap)
        for e in self.Walls :
            self.WallsCanvas.append(e)
            
        for m in range(int(len(self.Walls) / 2)) :
            W_1 = self.Walls[2 * m]
            W_2 = self.Walls[2 * m + 1]
            cv2.line(image, (int(W_1[0]), int(W_1[1])), (int(W_2[0]), int(W_2[1])), (0, 255, 0), 2)
        # Display image with detected edges
        cv2.imshow("Close the window | Press Enter", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if self.DefaultConfigurationChoice.get() == 'Use' :
            self.Display_DeleteLineChoice()
        elif self.DefaultConfigurationChoice.get() == 'Not used' :
            self.Display_HeightWallChoice()
            
    def Delete_AllWithoutImage(self, ind) :
        if ind >= 11 :
            self.Delete_FeatureChoice()
        if ind >= 10 :
            self.Delete_DefaultConfigurationChoice()
        if ind >= 9 :
            self.Delete_NewDefaultConfigurationChoice()
            self.Delete_ViewDefaultConfigurationChoice()
        if ind >= 8 :
            self.Delete_GridChoice()
        if ind >= 7 :
            self.Delete_ManualOptionChoice()
        if ind >= 6 :
            self.Delete_HeightWallChoice()
            
            # Canvas parameters
            self.points = []
            self.Walls = []
            self.WallsCanvas = []
            self.Grid_size = 0
            self.W = 0
            self.H = 0
            self.Width = 0
            self.Height = 0
            # Empty list to store the coordinates of the line to delete
            self.line = []
            self.line_index = 0
            self.dist_line = 0
        if ind >= 5 :
            self.Delete_ThicknessWallChoice()
        if ind >= 4 :
            self.Delete_TransparencyWallChoice()
        if ind >= 3 : 
            self.Delete_DeleteLineChoice()
        if ind >= 2 : 
            self.Delete_LengthFigureChoice()
        if ind >= 1 :
            self.Delete_ConstantLengthFigureChoice()
            self.Delete_LineLengthChoice()
        if ind >= 0 :
            self.Delete_WorldNameChoice()
            self.Message.grid_remove()
            self.MessagePointPosition.grid_remove()
            self.Canvas.grid_remove()
            self.Reset_Button.grid_remove()
            self.Finish_Button.grid_remove()
            self.Delete_Button.grid_remove()
            
    def Delete_AllWithImage(self, ind) :
        if ind >= 7 :
            self.Delete_ImageFolderNameChoice()
        if ind >= 6 :
            self.Delete_ImageNameChoice()
            
            # Canvas parameters
            self.points = []
            self.Walls = []
            self.WallsCanvas = []
            self.Grid_size = 0
            self.W = 0
            self.H = 0
            self.Width = 0
            self.Height = 0
            # Empty list to store the coordinates of the line to delete
            self.line = []
            self.line_index = 0
            self.dist_line = 0
            
        if ind >= 5 :
            self.Delete_BinaryThresholdChoice()
        if ind >= 4 :
            self.Delete_LineDetectionChoice()
        if ind >= 3 :
            self.Delete_GapLineDetectionChoice()
        if ind >= 2 :
            self.Delete_AngleChoice()
        if ind >= 1 :
            self.Delete_GapSameLine()
        if ind >= 0 :
            self.Delete_GapParallelLine()
            self.Message.grid_remove()
            self.MessagePointPosition.grid_remove()
            self.Canvas.grid_remove()
            self.Reset_Button.grid_remove()
            self.Finish_Button.grid_remove()
            self.Delete_Button.grid_remove()
