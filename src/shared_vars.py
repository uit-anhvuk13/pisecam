from queue import Queue

CameraCtrlQueue = Queue()
FrameQueue = Queue()
FrameToScoreQueue = Queue()

def absolute_equal(Obj1, Obj2):
    return type(Obj1) == type(Obj2) and Obj1 == Obj2