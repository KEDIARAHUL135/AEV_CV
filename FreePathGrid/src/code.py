import FreePathGrid.src.macros
import numpy as np
import cv2


def CaptureVideo():
    cap = cv2.VideoCapture('C:/Users/HP/Videos/InputVideo.avi')

    while (cap.isOpened()):
        ret, InputFrame = cap.read()

        if not ret:
            print('\nCannot Read Video\n')
            exit(1)


        InitialiseAlgo(InputFrame)

        if cv2.waitKey(FreePathGrid.src.macros.WAITKEY_VALUE) & 0xFF == ord('q'):
            break

    cap.release()


def InitialiseAlgo(Frame):
    Frame = Resize(Frame)

    cv2.imshow('InputFrame', Frame)

    if FreePathGrid.src.macros.THRESH_OR_CANNY == 1:
        Frame = ApplyThresholding(Frame)

    elif FreePathGrid.src.macros.THRESH_OR_CANNY == 0:
        Frame = ApplyCanny(Frame)

#    TestPixelValues(Frame)
    Frame = DrawLines(Frame)

    cv2.imshow('ProcessedFrame', Frame)


def Resize(Frame):
    height, width = Frame.shape[:2]
    imgScale = FreePathGrid.src.macros.NEW_WIDTH / width
    newX, newY = Frame.shape[1] * imgScale, Frame.shape[0] * imgScale
    ResizedFrame = cv2.resize(Frame, (int(newX), int(newY)))

    return ResizedFrame


def ApplyThresholding(Frame):
    GrayFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)

    ret, ThresholdFrame = cv2.threshold(GrayFrame, 100, 255, cv2.THRESH_BINARY)
    if not ret:
        print('Cannot apply thresholding')

    return ThresholdFrame


def ApplyCanny(Frame):
    return cv2.Canny(Frame, 100, 200)


def DrawLines(Frame):
    LineLength = [0] * int(FreePathGrid.src.macros.NEW_WIDTH / FreePathGrid.src.macros.DISTANCE_BTW_LINES)

    for i in range(1, (int(FreePathGrid.src.macros.NEW_WIDTH / FreePathGrid.src.macros.DISTANCE_BTW_LINES) - 1)):
        DrawSingleLine(Frame, LineLength, i)
    print(LineLength)
    return Frame


def DrawSingleLine(Frame, LineLength, i):
    HeightOfFrame = Frame.shape[0]
    LineLength[i] = FindTopEnd(Frame, (i * FreePathGrid.src.macros.DISTANCE_BTW_LINES))
    cv2.line(Frame, ((i * FreePathGrid.src.macros.DISTANCE_BTW_LINES), (HeightOfFrame - 1)), \
             ((i * FreePathGrid.src.macros.DISTANCE_BTW_LINES), (HeightOfFrame - LineLength[i])), FreePathGrid.src.macros.BLACK_PIXEL_VALUE, 1)


def FindTopEnd(Frame, i):
    HeightOfFrame = Frame.shape[0]
    # print(HeightOfFrame - src.macros.PIXEL_THRESH)
    for j in range(HeightOfFrame - FreePathGrid.src.macros.PIXEL_THRESH):
        # cv2.line(Frame, (i, (HeightOfFrame - 1)), (i, (HeightOfFrame - j)), 0, 1)
        if Frame[(HeightOfFrame - j - 1), i] == FreePathGrid.src.macros.BLACK_PIXEL_VALUE:
            # print(Frame[(HeightOfFrame - j - 1), i])
#            if Frame[(HeightOfFrame - j - FreePathGrid.src.macros.PIXEL_THRESH - 1), i] == FreePathGrid.src.macros.BLACK_PIXEL_VALUE:
            return j
    return HeightOfFrame


def TestPixelValues(Frame):

    Height, Width = Frame.shape[:2]
    print(Height)
    print(Width)
    cv2.line(Frame, (0, 0), (640, 360), 0, 5)