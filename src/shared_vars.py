from queue import Queue
from threading import Event

CameraCtrlQueue = Queue()
FrameQueue = Queue()
FrameToScoreQueue = Queue()

HasDetection = Event()
HasDetection.clear()

def absolute_equal(Obj1, Obj2):
    return type(Obj1) == type(Obj2) and Obj1 == Obj2