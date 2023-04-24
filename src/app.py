# import lib
import time
import signal
from threading import Thread

# import local files
from shared_vars import CameraCtrlQueue, FrameToScoreQueue, FrameQueue
from camera import main as camera_main, terminate as camera_terminate
from detector import main as detector_main, terminate as detector_terminate
from stream import main as stream_main, terminate as stream_terminate

camera_thread = Thread(target=camera_main)
detector_thread = Thread(target=detector_main)
stream_thread = Thread(target=stream_main)

# Define a signal handler function
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')

if __name__ == '__main__':
    camera_thread.setDaemon(True)
    detector_thread.setDaemon(True)
    stream_thread.setDaemon(True)

    # ensure records dir exists
    Path = os.path.join(os.getcwd(), constants.RECORD_DIR)
    if not os.path.exists(Path):
        os.makedirs(Path)

    # start the thread
    camera_thread.start()
    detector_thread.start()
    stream_thread.start()

    # wait for signal ctrl+c to continue
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

    # empty shared queues
    CameraCtrlQueue.queue.clear()
    FrameToScoreQueue.queue.clear()
    FrameQueue.queue.clear()

    while not CameraCtrlQueue.empty() or not FrameToScoreQueue.empty() or not FrameQueue.empty():
        pass

    print('flushed all queues')

    # send signal to teardown threads
    camera_terminate()
    print('camera_thread exited')
    detector_terminate()
    print('detector_thread exited')
    # stream_terminate()
    print('stream_thread exited')
    print('app terminating...')
    time.sleep(5)
