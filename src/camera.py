# import lib
import os
import cv2
from datetime import datetime, timedelta
Now = datetime.now

# import local files
import constants
from shared_vars import CameraCtrlQueue, FrameToScoreQueue, FrameQueue, IsDetected

# global vars
Camera = None
RecordPath = os.path.join(os.getcwd(), constants.RECORD_DIR)
Out = None
StopRecordTime = None

ScoringTimeGap = timedelta(seconds = constants.SEC_GAP_BETWEEN_SCORING)
RecordingTimeGap = timedelta(seconds = constants.SEC_TO_END_RECORD_WHEN_NO_DETECTION)
CurrentTime = Now()
LastScoringTime = CurrentTime

def generate_frames():
    global Camera
    Ok, Frame = Camera.read()
    if Ok:
        global CurrentTime, LastScoringTime, ScoringTimeGap, Out 
        FrameQueue.put(Frame)
        if CurrentTime > LastScoringTime + ScoringTimeGap:
            FrameToScoreQueue.put(Frame)
            LastScoringTime = CurrentTime
        if Out != None:
            Out.write(Frame)

def handle_human_detection():
    global Out, StopRecordTime, RecordingTimeGap
    if Out == None:
        global CurrentTime, RecordPath
        Filename = CurrentTime.strftime('%Y-%m-%d_%H-%M-%S')
        Filepath = f'{os.path.join(RecordPath, Filename)}.avi'
        Fourcc = cv2.VideoWriter_fourcc(*'XVID')
        Out = cv2.VideoWriter(Filepath, Fourcc, 20.0, (constants.FRAME_WIDTH, constants.FRAME_HEIGHT))
        print(f'camera_thread writing to {Filepath}')
    StopRecordTime = CurrentTime + RecordingTimeGap    

def handle_no_human_detection():
    global Out, CurrentTime
    if Out != None and CurrentTime > StopRecordTime:
        Out.release()
        Out = None
        print(f'{CurrentTime} - 1 file recorded')

def message_handler(Msg):
    global CurrentTime
    CurrentTime = Now()
    if Msg == b'$GEN_FRAME':
        generate_frames()
    elif Msg == b'$HUMAN_DETECTED':
        handle_human_detection()
    elif Msg == b'$HUMAN_UNDETECTED':
        handle_no_human_detection()

def main():
    global Camera
    Camera = cv2.VideoCapture(0)
    # Set the resolution to 1080p
    Camera.set(cv2.CAP_PROP_FRAME_WIDTH, constants.FRAME_WIDTH)
    Camera.set(cv2.CAP_PROP_FRAME_HEIGHT, constants.FRAME_HEIGHT)
    while True:
        try:
            Msg = CameraCtrlQueue.get(timeout = constants.TIMEOUT)
            if Msg == b'$EXIT':
                if Out != None:
                    Out.release()
                    Out = None
                    print(f'{CurrentTime} - video recorded')
                break
            message_handler(Msg)
        except:
            pass
        message_handler(b'$GEN_FRAME')

def terminate():
    CameraCtrlQueue.put(b'$EXIT')