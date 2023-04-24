# import lib
import signal
from threading import Thread

# import local files
from shared_queues import CameraCtrlQueue, FrameQueue, StreamConnectionQueue
from camera import main as camera_main, terminate as camera_terminate
from stream import main as stream_main, terminate as stream_terminate

camera_thread = Thread(target=camera_main)
stream_thread = Thread(target=stream_main)

# Define a signal handler function
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')

if __name__ == '__main__':
    # start the thread
    camera_thread.start()
    stream_thread.start()

    # wait for signal ctrl+c to continue
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

    # empty shared queues
    StreamConnectionQueue.queue.clear()
    CameraCtrlQueue.queue.clear()
    FrameQueue.queue.clear()

    # send signal to teardown threads
    camera_terminate()
    # camera_thread.terminate()
    camera_thread.join()
    print("camera_thread exited")
    stream_terminate()
    stream_thread.terminate()
    stream_thread.join()
    print("stream_thread exited")
