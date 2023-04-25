#import lib
import cv2

# import local files
import constants
from shared_vars import CameraCtrlQueue, FrameToScoreQueue, absolute_equal

Timeout = constants.TIMEOUT + constants.SEC_GAP_BETWEEN_SCORING
Hog = None

def detect_human(Frame):
    global Hog
    # resize the frame and convert it to grayscale
    ResizedFrame = cv2.resize(Frame, (640, 480))
    Gray = cv2.cvtColor(ResizedFrame, cv2.COLOR_BGR2GRAY)
    # detect human using HOG
    Rects, _ = Hog.detectMultiScale(Gray, winStride = (8, 8), padding = (32, 32), scale=1.05)
    if len(Rects) > 0:
        CameraCtrlQueue.put(b'$HUMAN_DETECTED')
    else:
        CameraCtrlQueue.put(b'$HUMAN_UNDETECTED')

def main():
    global Hog, Timeout
    Hog = cv2.HOGDescriptor()
    Hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    while True:
        try:
            Msg = FrameToScoreQueue.get(timeout = Timeout)
            if absolute_equal(Msg, b'$EXIT'):
                break
            detect_human(Msg)
        except:
            pass

def terminate():
    FrameToScoreQueue.put(b'$EXIT')