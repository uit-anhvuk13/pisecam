# import lib
import os
import cv2
from datetime import datetime, timedelta
Now = datetime.now

# import local files
import constants
from shared_vars import CameraCtrlQueue, FrameToScoreQueue, FrameQueue, IsDetected

RecordPath = os.path.join(os.getcwd(), constants.RECORD_DIR)
Out = None
StopRecordTime = None

ScoringTimeGap = timedelta(seconds = constants.SEC_GAP_BETWEEN_SCORING)
RecordingTimeGap = timedelta(seconds = constants.SEC_TO_END_RECORD_WHEN_NO_DETECTION)
LastScoringTime = Now()

def generate_frames(Camera):
    Ok, Frame = Camera.read()
    if Ok:
        CurrentTime = Now()
        
        FrameQueue.put(Frame)
        
        global LastScoringTime
        if CurrentTime > LastScoringTime + ScoringTimeGap:
            FrameToScoreQueue.put(Frame)
            LastScoringTime = CurrentTime
        
        if IsDetected.event.is_set():
            if Out == None:
                Filename = CurrentTime.strftime('%Y-%m-%d_%H-%M-%S')
                Filepath = f'{os.path.join(RecordPath, Filename)}.avi'
                print(Filepath)
                Fourcc = cv2.VideoWriter_fourcc(*'XVID')
                Out = cv2.VideoWriter(Filepath, Fourcc, 20.0, (constants.FRAME_WIDTH, constants.FRAME_HEIGHT))
            global StopRecordTime
            StopRecordTime = CurrentTime + RecordingTimeGap    
            Out.write(Frame)      
        elif Out != None:
            if CurrentTime <= StopRecordTime:
                Out.write(Frame)
            else:
                Out.release()
                Out = None
                print('{currentTime} - 1 file recorded')

def message_handler(Msg, Camera):
    if Msg == 'gen_frame':
        generate_frames(Camera)

def main():
    Camera = cv2.VideoCapture(0)

    # Set the resolution to 1080p
    Camera.set(cv2.CAP_PROP_FRAME_WIDTH, constants.FRAME_WIDTH)
    Camera.set(cv2.CAP_PROP_FRAME_HEIGHT, constants.FRAME_HEIGHT)

    while True:
        try:
            Msg = CameraCtrlQueue.get(timeout = constants.TIMEOUT)
            if isinstance(Msg, str) and Msg == '$EXIT':
                if Out != None:
                    Out.release()
                    Out = None
                break
            message_handler(Msg, Camera)
        except:
            message_handler('gen_frame', Camera)

def terminate():
    CameraCtrlQueue.put('$EXIT')