#import lib
import cv2

# import local files
import constants
from shared_vars import FrameToScoreQueue, IsDetected

Timeout = constants.TIMEOUT + constants.SEC_GAP_BETWEEN_SCORING

def detect_human(Frame, Hog):
    # resize the frame and convert it to grayscale
    ResizedFrame = cv2.resize(Frame, (640, 480))
    Gray = cv2.cvtColor(ResizedFrame, cv2.COLOR_BGR2GRAY)

    # detect human using HOG
    Rects, _ = Hog.detectMultiScale(Gray, winStride = (8, 8), padding = (32, 32), scale=1.05)

    if len(Rects) > 0:
        IsDetected.event.set()
    else:
        IsDetected.event.clear()

def main():
    Hog = cv2.HOGDescriptor()
    Hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    while True:
        try:
            Msg = FrameToScoreQueue.get(timeout = Timeout)
            if isinstance(Msg, str) and Msg == '$EXIT':
                break
            detect_human(Msg, Hog)
        except:
            pass

def terminate():
    FrameToScoreQueue.put('$EXIT')