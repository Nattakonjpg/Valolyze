from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = '/home/thanapat_window/codes/Valolyze/static'  # ระบุโฟลเดอร์ที่จะเก็บวิดีโอ

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/home_web')
def home():    
    return render_template("New_index.html")

@app.route('/about')
def about():
    return render_template('New_about.html')

@app.route('/webapp') 
def upload():
    return render_template('webapp_tung.html')

@app.route('/creator')
def creator():
    return render_template('Creator.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # ไม่มีการเด้งไปยังหน้า index หลังจากการอัปโหลดไฟล์
            return 'File uploaded successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
