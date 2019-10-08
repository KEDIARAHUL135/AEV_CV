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
TYPE_OF_FILTER = 1                 # 1 for Threshold
                                    # 0 for Canny


# Black Pixel Value (For obstacle)
if TYPE_OF_FILTER == 1:
    BLACK_PIXEL_VALUE = 0               # 0 for threshold
                                          # 255 for canny

elif TYPE_OF_FILTER == 0:
    BLACK_PIXEL_VALUE = 255