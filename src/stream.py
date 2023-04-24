# import lib
import requests
from flask import Flask, render_template, Response, request
from wsgiref.simple_server import make_server
import cv2

# import local files
import constants
from shared_queues import FrameQueue, StreamConnectionQueue

App = Flask(__name__)
Frame = None

@App.route('/')
def index():
    return render_template('index.html')

@App.route('/video_feed')
def video_feed():
    # client connected to stream
    StreamConnectionQueue.put(None)
    def stream_handler():
        try:
            get_frame_from_queue()
        # client disconnected
        except (IOError, WebSocketError):
            StreamConnectionQueue.get()
    return Response(stream_handler(), mimetype='multipart/x-mixed-replace; boundary=frame')

@App.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running with the Werkzeug server')
    shutdown_func()
    return 'Server is shutting down'

def get_frame_from_queue():
    while True:
        try:
            Frame = FrameQueue.get(timeout = constants.TIMEOUT)
            Frame = cv2.imencode('.jpg', Frame)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + Frame + b'\r\n')
        except:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + Frame + b'\r\n')

def main():
    Server = make_server(constants.SERVER, constants.PORT, App)
    Server.serve_forever()

def terminate():
    requests.post(f'http://{constants.SERVER}:{constants.PORT}/shutdown')