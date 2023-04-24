from queue import Queue
from threading import Event

CameraCtrlQueue = Queue()
FrameQueue = Queue()
FrameToScoreQueue = Queue()

IsDetected = Event()