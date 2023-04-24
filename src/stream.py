# import lib
import os
import requests
from flask import Flask, send_from_directory, render_template, Response, request
from werkzeug.serving import make_server
import cv2

# import local files
import constants
from shared_vars import FrameQueue

App = Flask(__name__)

@App.route('/')
def index():
    return render_template('index.html')

@App.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(App.root_path, 'templates'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@App.route('/video_feed')
def video_feed():
    return Response(get_frame_from_queue(), mimetype='multipart/x-mixed-replace; boundary=frame')

@App.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running with the Werkzeug server')
    shutdown_func()
    return 'Server is shutting down'

def get_frame_from_queue():
    StreamFrame = b'0'
    while True:
        try:
            StreamFrame = FrameQueue.get(timeout = constants.TIMEOUT)
            StreamFrame = cv2.imencode('.jpg', StreamFrame)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + StreamFrame + b'\r\n')
        except:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + StreamFrame + b'\r\n')

def main():
    # App.run(debug = True, host = constants.SERVER, port = constants.PORT)
    Server = make_server(constants.SERVER, constants.PORT, App)
    Server.serve_forever()

def terminate():
    requests.post(f'http://{constants.SERVER}:{constants.PORT}/shutdown')
