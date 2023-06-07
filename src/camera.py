# import lib
import os
import time
import cv2
from datetime import datetime, timedelta
Now = datetime.now

# import local files
import constants
from shared_vars import CameraCtrlQueue, FrameToScoreQueue, FrameQueue, HasDetection
import firebase

# global vars
Camera = None
RecordPath = os.path.join(os.getcwd(), constants.RECORD_DIR)
Out = None
StopRecordTime = None
Filepath = None

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
        global CurrentTime, RecordPath, Filepath
        Filename = CurrentTime.strftime('%Y-%m-%d_%H-%M-%S')
        Filepath = f'{os.path.join(RecordPath, Filename)}.webm' # sử dụng webm vì webm có thể play trên html
        Fourcc = cv2.VideoWriter_fourcc(*'VP90')
        Out = cv2.VideoWriter(Filepath, Fourcc, 20.0, (constants.FRAME_WIDTH, constants.FRAME_HEIGHT))
        print(f'camera_thread: writing to {Filepath}')

    print("Detect")
    StopRecordTime = CurrentTime + RecordingTimeGap    

def handle_no_human_detection():
    global Out, CurrentTime, Filepath
    if Out != None and CurrentTime > StopRecordTime:
        Out.release()
        Out = None
        print(f'camera_thread: {CurrentTime} video recorded')

        # convert mp4 v1 -> mpv v2 -> do broswer chỉ có thể  play file mp4 v2
        # Filepath_mp4v2 = Filepath.split('.mp4')[0] + '_mp4v2.mp4'
        # os.system("ffmpeg -i {0} -c copy -map 0 -brand mp42 {1}".format(Filepath, Filepath_mp4v2))
        # firebase.push_file(Filepath_mp4v2, constants.TYPE_VIDEOS)
        # os.system("rm {0}".format(Filepath_mp4v2))
        firebase.push_file(Filepath, constants.TYPE_VIDEOS)
        
    
    print("Not detect")

def message_handler(Msg):
    global CurrentTime
    CurrentTime = Now()
    IsDetected = HasDetection.is_set()
    if IsDetected:
        handle_human_detection()
    else:
        handle_no_human_detection()
    
    if Msg == b'$GEN_FRAME':
        generate_frames()

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
                global Out
                if Out != None:
                    Out.release()
                    Out = None
                    print(f'camera_thread: {CurrentTime} video recorded')
                print(f'camera_thread: exited')
                return
            message_handler(Msg)
        except:
            pass
        message_handler(b'$GEN_FRAME')

def terminate():
    CameraCtrlQueue.queue.clear()
    CameraCtrlQueue.put(b'$EXIT')
    time.sleep(0.5)
