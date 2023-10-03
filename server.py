from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
cap = None  

def generate_frames():
    global cap
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def initialize_camera():
    global cap
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open video device")

def close_camera():
    global cap
    if cap:
        cap.release()

if __name__ == '__main__':
    try:
        initialize_camera()
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        close_camera()
