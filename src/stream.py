# import lib
import requests
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
from gevent.pywsgi import WSGIServer
import cv2

# import local files
import constants
from shared_queues import FrameQueue, StreamConnectionQueue

App = Flask(__name__)
App.config['SECRET_KEY'] = constants.SECRET_KEY
SocketIo = SocketIO(App)
Frame = None

@SocketIo.on('connect')
def handle_connect():
    StreamConnectionQueue.put(request.remote_addr)
    global user_count
    user_count += 1
    emit('user_count', {'count': user_count}, broadcast=True)

@SocketIo.on('disconnect')
def handle_disconnect():
    StreamConnectionQueue.get(request.remote_addr)
    global user_count
    user_count -= 1
    emit('user_count', {'count': user_count}, broadcast=True)

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

@App.before_request
def check_user():
    if request.endpoint == 'logout':
        # Handle user leaving the page or closing the browser window
        print('User has left the page')

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
    HttpServer = WSGIServer((constants.SERVER, constants.PORT), App)
    SocketIoServer = SocketIOServer(HttpServer, host=constants.SERVER, port=constants.PORT)
    SocketIoServer.serve_forever()

def terminate():
    requests.post(f'http://{constants.SERVER}:{constants.PORT}/shutdown')