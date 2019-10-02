import src.macros
import numpy as np
import cv2


def CaptureVideo():
    cap = cv2.VideoCapture('C:/Users/kedia/Downloads/InputVideo2.mp4')

    while (cap.isOpened()):
        ret, InputFrame = cap.read()

        if not ret:
            print('\nCannot Read Video\n')
            exit(1)

        InitialiseAlgo(InputFrame)

        if cv2.waitKey(src.macros.WAITKEY_VALUE) & 0xFF == ord('q'):
            break

    cap.release()


def InitialiseAlgo(Frame):
    Frame = Resize(Frame)

    Frame = ApplyThresholding(Frame)

#    TestPixelValues(Frame)
    Frame = DrawLines(Frame)

    cv2.imshow('Frame', Frame)


def Resize(Frame):
    height, width = Frame.shape[:2]
    imgScale = src.macros.NEW_WIDTH / width
    newX, newY = Frame.shape[1] * imgScale, Frame.shape[0] * imgScale
    ResizedFrame = cv2.resize(Frame, (int(newX), int(newY)))

    return ResizedFrame


def ApplyThresholding(Frame):
    GrayFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)

    ret, ThresholdFrame = cv2.threshold(GrayFrame, 100, 255, cv2.THRESH_BINARY)
    if not ret:
        print('Cannot apply thresholding')

    return ThresholdFrame


def DrawLines(Frame):
    LineLength = [0] * int(src.macros.NEW_WIDTH / src.macros.DISTANCE_BTW_LINES)

    for i in range(1, (int(src.macros.NEW_WIDTH / src.macros.DISTANCE_BTW_LINES) - 1)):
        DrawSingleLine(Frame, LineLength, i)
    print(LineLength)
    return Frame


def DrawSingleLine(Frame, LineLength, i):
    HeightOfFrame = Frame.shape[0]
    LineLength[i] = HeightOfFrame - FindTopEnd(Frame, (i * src.macros.DISTANCE_BTW_LINES))
    cv2.line(Frame, ((i * src.macros.DISTANCE_BTW_LINES), (HeightOfFrame - 1)), \
             ((i * src.macros.DISTANCE_BTW_LINES), LineLength[i]), 0, 1)


def FindTopEnd(Frame, i):
    HeightOfFrame = Frame.shape[0]
    # print(HeightOfFrame - src.macros.PIXEL_THRESH)
    for j in range(HeightOfFrame - src.macros.PIXEL_THRESH):
        # cv2.line(Frame, (i, (HeightOfFrame - 1)), (i, (HeightOfFrame - j)), 0, 1)
        if Frame[(HeightOfFrame - j - 1), i] == 0:
            # print(Frame[(HeightOfFrame - j - 1), i])
            if Frame[(HeightOfFrame - j - src.macros.PIXEL_THRESH - 1), i] == 0:
                return j
    return HeightOfFrame


def TestPixelValues(Frame):

    Height, Width = Frame.shape[:2]
    print(Height)
    print(Width)
    cv2.line(Frame, (0, 0), (640, 360), 0, 5)