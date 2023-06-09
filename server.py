from flask import Flask, make_response, render_template, request, Response
import os

app = Flask(__name__)

frame = None   # global variable to keep single JPG

@app.route('/upload', methods=['PUT'])
def upload():
    global frame
    
    # keep jpg data in global variable
    frame = request.data
    
    
    return "OK"

def gen():
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video')
def video():
    if frame:
        return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return ""

@app.route('/')
def index():
    # return ' image:<br><img src="/video">'
    
    # UPLOAD_FOLDER = "/images"
    # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'altimage.png')
    # return render_template('index.html', user_image = full_filename)
    
    
    return render_template('index.html')
    # return '<meta http-equiv="refresh" content="3"> image:<br><img src="/video">'

if __name__ == "__main__":
    app.run(debug=True, port=5000)