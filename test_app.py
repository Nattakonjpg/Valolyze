from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_Directory'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = ['.mp4', '.avi']

@app.route('/')
def index():
    return render_template('test_webapp.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    extension = os.path.splitext(file.filename)[1]

    if file and extension.lower() in app.config['ALLOWED_EXTENSIONS']:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_Directory'], filename))
        return redirect('/')
    else:
        return 'File is not a Video'

if __name__ =="__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)
