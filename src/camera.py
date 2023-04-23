# import lib
import cv2

# import local files
import constants
from shared_queues import CameraCtrlQueue, FrameQueue, StreamConnectionQueue

def generate_frames(Camera):
    Ok, Frame = Camera.read()
    if Ok:
        if not StreamConnectionQueue.empty():
            FrameQueue.put(Frame)  

def message_handler(Msg, Camera):
    if Msg == 'gen_frame':
        generate_frames(Camera)

def main():
    Camera = cv2.VideoCapture(0)

    # Set the resolution to 1080p
    Camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    Camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        try:
            Msg = CameraCtrlQueue.get(timeout = constants.TIMEOUT)
            if Msg == '$EXIT':
                break
            message_handler(Msg, Camera)
        except:
            message_handler('gen_frame', Camera)

def terminate():
    CameraCtrlQueue.put('$EXIT')