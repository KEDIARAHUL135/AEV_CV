"""
Filename    : code.py
Created By  : Rahul Kedia
Team        : OpenCV - AEV
Institute   : IIT (ISM) Dhanbad
Created On  : 30/09/19
Description : This file contains the source code of the Free Path Grid algo.
              It uses variables from the file macros.py for calculations.
"""

import FreePathGrid.src.macros
import numpy as np
import cv2

"""
Function        : CaptureVideo
Parameters      : VideoPath - string type, contains the path of input video 
                  ret - bool type, stores the status of cap.read 
                        (the image is read or not)
                  InputFrame - Mat type, Stores the input image 
                               from the video stream
Description     : Captures the video from provided path and read and 
                  initialise the algo.
Return          : NULL 
"""


def CaptureVideo(VideoPath):
    cap = cv2.VideoCapture(VideoPath)

    while cap.isOpened():
        ret, InputFrame = cap.read()

        if not ret:
            print('\nCannot Read Video\n')
            exit(1)

        InitialiseAlgo(InputFrame)

        if cv2.waitKey(FreePathGrid.src.macros.WAITKEY_VALUE) & 0xFF == ord('q'):
            break

    cap.release()


"""
Function        : InitialiseAlgo
Parameters      : Frame - Mat type, stores the input frame which is to be processed
Description     : This fuction takes in the image to be processed and calls required 
                  functions one by one and pass necessary parameters. It also displays 
                  the input and output results which can be removed when the code is finalised.
Return          : NULL
"""
def InitialiseAlgo(Frame):
    Frame = Resize(Frame)

    cv2.imshow('InputFrame', Frame)

    Frame = ApplyFilter(Frame)

    #    TestPixelValues(Frame)
    Frame = DrawLines(Frame)

    cv2.imshow('ProcessedFrame', Frame)


"""
Function        : Resize
Parameters      : Frame - Mat type, Input frame to be resized
                  (Other parameters can be ignored)
Description     : This function resize the input frame with respect to width 
                  whose new value is provided in macros.py file.
Return          : ResizedFrame - Mat type, contains resized image 
"""
def Resize(Frame):
    height, width = Frame.shape[:2]
    imgScale = FreePathGrid.src.macros.NEW_WIDTH / width
    newX, newY = Frame.shape[1] * imgScale, Frame.shape[0] * imgScale
    ResizedFrame = cv2.resize(Frame, (int(newX), int(newY)))

    return ResizedFrame


"""
Function        : ApplyFilter
Parameters      : Frame - Mat type, contains input frame to be processed
                  GrayFrame - Mat type, contains the grayscale image of the input
                  ret - Bool type, contains the status of filter on image 
                        (Success or not)
                  FilteredFrame - Mat type, contains the image after filter
Description     : This function applies thersholding on the input image.
Return          : ThresholdFrame - threshold image of the input                  
"""
def ApplyFilter(Frame):

    # Global Thresholding
    if FreePathGrid.src.macros.TYPE_OF_FILTER == 0:
        GrayFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
        ret, FilteredFrame = cv2.threshold(GrayFrame, 100, 255, cv2.THRESH_BINARY)
        if not ret:
            print('Cannot apply Filter')

    # Adaptive Mean Thresholding
    elif FreePathGrid.src.macros.TYPE_OF_FILTER == 1:
        GrayFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
        FilteredFrame = cv2.adaptiveThreshold(GrayFrame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 6)

    # Adaptive Gaussian Thresholding
    elif FreePathGrid.src.macros.TYPE_OF_FILTER == 2:
        GrayFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
        FilteredFrame = cv2.adaptiveThreshold(GrayFrame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 6)

    # Otsu's Thresholding
    elif FreePathGrid.src.macros.TYPE_OF_FILTER == 3:
        GrayFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
        ret, FilteredFrame = cv2.threshold(GrayFrame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if not ret:
            print('Cannot apply Filter')

    # Otsu's thresholding after Gaussian filtering
    elif FreePathGrid.src.macros.TYPE_OF_FILTER == 4:
        blur = cv2.GaussianBlur(Frame, (5, 5), 0)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        ret, FilteredFrame = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if not ret:
            print('Cannot apply Filter')

    # Canny Edge Detection
    elif FreePathGrid.src.macros.TYPE_OF_FILTER == 5:
        FilteredFrame = cv2.Canny(Frame, 100, 200)

    # Laplacian Gradient
    elif FreePathGrid.src.macros.TYPE_OF_FILTER == 6:
        blur = cv2.GaussianBlur(Frame, (3, 3), 0)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        dst = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)
        FilteredFrame = cv2.convertScaleAbs(dst)

    # Sobel Gradient
    elif FreePathGrid.src.macros.TYPE_OF_FILTER == 7:
        src = cv2.GaussianBlur(Frame, (3, 3), 0)
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        FilteredFrame = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    return FilteredFrame


"""
Function        : DrawLines
Parameters      : Frame - Mat type, contains input frame to be processed
                  LineLength - List type, contains the lengths of lines (in pixels)
                               drawn which shows the free path. 
Description     : This function is responsible for drawing lines for free space starting 
                  from the bottom. Lines are drawn vertical at a specified distance between 
                  them parallel to each other.
Return          : Frame - lined image
"""
def DrawLines(Frame):
    LineLength = [0] * int(FreePathGrid.src.macros.NEW_WIDTH / FreePathGrid.src.macros.DISTANCE_BTW_LINES)

    for i in range(1, (int(FreePathGrid.src.macros.NEW_WIDTH / FreePathGrid.src.macros.DISTANCE_BTW_LINES) - 1)):
        DrawSingleLine(Frame, LineLength, i)
    print(LineLength)
    return Frame


"""
Function        : DrawSingleLine
Parameters      : Frame - Mat type, contains input frame to be processed
                  LineLength - List type, contains the lengths of lines (in pixels)
                               drawn which shows the free path. 
                  i - int type, contains the line number from the left.
                  HeightOfFrame - int type, contains the height of the frame.
Description     : This function is responsible for drawing single line on the image. 
                  It calls other function to find top end of the line and then draws it
                  and saves its length in LineLength list at the respective position.
Return          : Frame - lined image
"""
def DrawSingleLine(Frame, LineLength, i):
    HeightOfFrame = Frame.shape[0]
    LineLength[i] = FindTopEnd(Frame, (i * FreePathGrid.src.macros.DISTANCE_BTW_LINES))
    cv2.line(Frame, ((i * FreePathGrid.src.macros.DISTANCE_BTW_LINES), (HeightOfFrame - 1)), \
             ((i * FreePathGrid.src.macros.DISTANCE_BTW_LINES), (HeightOfFrame - LineLength[i])),
             FreePathGrid.src.macros.BLACK_PIXEL_VALUE, 1)


"""
Function        : FindTopEnd
Parameters      : Frame - Mat type, contains input frame to be processed
                  LineXPos - int type, contains the x-axis position (column number) of 
                             the line to be drawn.
                  HeightOfFrame - int type, contains the height of the frame.
                  j - int type, used to iterate vertically on the line column. 
Description     : This function find the top end of the line. It does it by checking 
                  for change in pixel value which may show obstacle.
Return          : j/HeightOfFrame - Both values depict the total length of line to be 
                                    drawn from the bottom
"""
def FindTopEnd(Frame, LineXPos):
    HeightOfFrame = Frame.shape[0]
    # print(HeightOfFrame - src.macros.PIXEL_THRESH)
    for j in range(HeightOfFrame - FreePathGrid.src.macros.PIXEL_THRESH):
        # cv2.line(Frame, (LineXPos, (HeightOfFrame - 1)), (LineXPos, (HeightOfFrame - j)), 0, 1)
        if FreePathGrid.src.macros.TYPE_OF_FILTER == 6 or FreePathGrid.src.macros.TYPE_OF_FILTER == 7:
            if Frame[(HeightOfFrame - j - 1), LineXPos] >= FreePathGrid.src.macros.BLACK_PIXEL_VALUE:
                # print(Frame[(HeightOfFrame - j - 1), LineXPos])
                # if Frame[(HeightOfFrame - j - FreePathGrid.src.macros.PIXEL_THRESH - 1), LineXPos] ==\
                # FreePathGrid.src.macros.BLACK_PIXEL_VALUE:
                return j
        else:
            if Frame[(HeightOfFrame - j - 1), LineXPos] == FreePathGrid.src.macros.BLACK_PIXEL_VALUE:
                # print(Frame[(HeightOfFrame - j - 1), LineXPos])
                # if Frame[(HeightOfFrame - j - FreePathGrid.src.macros.PIXEL_THRESH - 1), LineXPos] ==\
                # FreePathGrid.src.macros.BLACK_PIXEL_VALUE:
                return j

    return HeightOfFrame


"""
This is a text function to be ignored and delete at the end.
"""
def TestPixelValues(Frame):
    Height, Width = Frame.shape[:2]
    print(Height)
    print(Width)
    cv2.line(Frame, (0, 0), (640, 360), 0, 5)
