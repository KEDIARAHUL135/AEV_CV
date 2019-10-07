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
THRESH_OR_CANNY = 1                 # 1 for Threshold
                                    # 0 for Canny


# Black Pixel Value (For obstacle)
if THRESH_OR_CANNY == 1:
    BLACK_PIXEL_VALUE = 0               # 0 for threshold
                                          # 255 for canny

elif THRESH_OR_CANNY == 0:
    BLACK_PIXEL_VALUE = 255