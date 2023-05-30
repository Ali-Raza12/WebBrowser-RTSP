from app import app
from flask import Response, render_template, request, redirect
import cv2


URL = None


def generate_frames():
    cap = cv2.VideoCapture(str(URL))
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/get_url", methods = ['POST'])
def get_url():
    global URL
    URL = request.form['rtsp_url']
    return redirect('/')


@app.route("/get_stream")
def get_stream():
    return video_feed()
