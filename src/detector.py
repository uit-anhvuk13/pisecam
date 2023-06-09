#import lib
import cv2
import time

# import local files
import constants
from shared_vars import FrameToScoreQueue, HasDetection, absolute_equal

Timeout = constants.TIMEOUT + constants.SEC_GAP_BETWEEN_SCORING
Hog = None
IsPrevFrameHumanDetected = False

def detect_human(Frame):
    global Hog
    # resize the frame and convert it to grayscale
    ResizedFrame = cv2.resize(Frame, (640, 480))
    Gray = cv2.cvtColor(ResizedFrame, cv2.COLOR_BGR2GRAY)
    # detect human using HOG
    Rects, _ = Hog.detectMultiScale(Gray, winStride = (8, 8), padding = (32, 32), scale=1.05)
    global IsPrevFrameHumanDetected
    if len(Rects) > 0:
        if not IsPrevFrameHumanDetected:
            HasDetection.set()
            IsPrevFrameHumanDetected = True
    else:
        if IsPrevFrameHumanDetected:
            HasDetection.clear()
            IsPrevFrameHumanDetected = False

def main():
    global Hog, Timeout
    Hog = cv2.HOGDescriptor()
    Hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    while True:
        try:
            Msg = FrameToScoreQueue.get(timeout = Timeout)
            if absolute_equal(Msg, b'$EXIT'):
                print(f'detector_thread: exited')
                return

            detect_human(Msg)
        except:
            pass

def terminate():
    FrameToScoreQueue.queue.clear()
    FrameToScoreQueue.put(b'$EXIT')
    time.sleep(0.5)