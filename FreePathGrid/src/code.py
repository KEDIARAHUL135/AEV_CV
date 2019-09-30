import numpy as np
import cv2

def CaptureVideo():
    cap = cv2.VideoCapture('C:/Users/kedia/Downloads/InputVideo.mp4')

    while (cap.isOpened()):
        ret, InputFrame = cap.read()

        if not ret:
            print('\nCannot Read Video\n')
            exit(1)

        InitialiseAlgo(InputFrame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


def InitialiseAlgo(Frame):

    Frame = Resize(Frame)

    Frame = ApplyThresholding(Frame)

    cv2.imshow('frame', Frame)


def Resize(Frame):
    NewWidth = 640
    height, width, depth = Frame.shape
    imgScale = NewWidth / width
    newX, newY = Frame.shape[1] * imgScale, Frame.shape[0] * imgScale
    ResizedFrame = cv2.resize(Frame, (int(newX), int(newY)))

    return ResizedFrame


def ApplyThresholding(Frame):
    GrayFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)

    ret, ThresholdFrame = cv2.threshold(GrayFrame,75,255,cv2.THRESH_BINARY)
    if not ret:
        print('Cannot apply thresholding')

    return ThresholdFrame

