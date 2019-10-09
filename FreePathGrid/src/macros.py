"""
Filename    : macros.py
Created By  : Rahul Kedia
Team        : OpenCV - AEV
Institute   : IIT (ISM) Dhanbad
Created On  : 02/10/19
Description : This file contains variables which act as macros
              in the source code. Purpose of this file is to make
              the code modular and also it makes easier to change
              few parameters of the code at any time according to
              our requirements.
"""


# New Width of frame
NEW_WIDTH = 640

# Distance between lines
DISTANCE_BTW_LINES = 5

# Pixel Colour Threshold
    # How many pixels above should also be white
PIXEL_THRESH = 1

# WaitKey Value
WAITKEY_VALUE = 1


# Threshold or canny
TYPE_OF_FILTER = 7                  # 0 for Global Thresholding
                                    # 1 for Adaptive Mean Thresholding
                                    # 2 for Adaptive Gaussian Thresholding
                                    # 3 for Otsu's Thresholding
                                    # 4 for Otsu's thresholding after Gaussian filtering
                                    # 5 for Canny Edge Detection
                                    # 6 for Laplacian Gradient
                                    # 7 for Sobel Gradient

# Black Pixel Value (For obstacle)
if TYPE_OF_FILTER == 0 or TYPE_OF_FILTER == 1 or TYPE_OF_FILTER == 2 or TYPE_OF_FILTER == 3 or TYPE_OF_FILTER == 4:
    BLACK_PIXEL_VALUE = 0

elif TYPE_OF_FILTER == 5:
    BLACK_PIXEL_VALUE = 255

elif TYPE_OF_FILTER == 6 or TYPE_OF_FILTER == 7:
    BLACK_PIXEL_VALUE = 75
