# import lib
import os
import requests
from flask import Flask, send_from_directory, render_template, Response, request
from werkzeug.serving import make_server
import cv2

# import local files
import constants
from shared_vars import FrameQueue
import firebase

App = Flask(__name__)

@App.route('/')
def index():
    FrameQueue.queue.clear()
    return render_template('index.html')

@App.route('/video_feed')
def video_feed():
    return Response(get_frame_from_queue(), mimetype='multipart/x-mixed-replace; boundary=frame')

@App.route('/videos/')
def folders():
    return render_template('file_manager.html', type = constants.TYPE_FOLDER, data = firebase.get_subfolders(f'{constants.TYPE_VIDEO}/'))

@App.route('/videos/<name>')
def videos(name):
    return render_template('file_manager.html', type = constants.TYPE_VIDEO, data = firebase.get_files(f'videos/{name}'))

def get_frame_from_queue():
    while True:
        try:
            Frame = FrameQueue.get(timeout = constants.TIMEOUT)
            Frame = cv2.imencode('.jpg', Frame)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + Frame + b'\r\n')
        except:
            pass

def main():
    global App
    # App.run(debug = True, host = constants.SERVER, port = constants.PORT)
    Server = make_server(constants.SERVER, constants.PORT, App)
    Server.serve_forever()

def terminate():
    # currently not find a way to shutdown flask app running from a thread
    FrameQueue.queue.clear()
    print(f'stream_thread: exited')
