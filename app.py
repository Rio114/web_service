import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
from face_rect import face_rect_out

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './outputs'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
CASCADE = 'haarcascade_frontalface_default.xml'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        try:
            img_file = request.files['img_file']  
        except:
            message = "please select an image file."
            return render_template('index.html', message=message)

        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(UPLOAD_FOLDER, filename))
            uploaded_img = os.path.join(UPLOAD_FOLDER, filename)
            img_url = os.path.join(OUTPUT_FOLDER, filename)
            trimmed_img_url = face_rect_out(uploaded_img, CASCADE, img_url)
            trimmed_list = []
            trimmed_list.extend(trimmed_img_url)
            message = "please click on your favorite image."
            if trimmed_list == []:
                message = "There is no trimmed image."
            return render_template('pickup.html', img_url=img_url, trimmed_list=trimmed_list, message=message)
        else:
            message = "its extension is not allowed."
            return render_template('index.html', message=message)

    return render_template('index.html')

@app.route('/pick', methods=['GET', 'POST'])
def pick():
    if request.method == 'POST':
        trimmed_img = request.form['trimmed_img']
        if trimmed_img:
            return render_template('index.html', img_url=trimmed_img)
    return render_template('index.html')

@app.route('/outputs/<filename>')
def uploaded_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.debug = True
    app.run()
    