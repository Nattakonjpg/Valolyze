from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
import shutil
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = '/home/nattakonpu/codes/Valolyze/Backend/video_data/test_videofull/agent/round'  # ระบุโฟลเดอร์ที่จะเก็บวิดีโอ
OUTPUT_FOLDER = '/home/nattakonpu/codes/Valolyze/Backend/Output/Final/'  # ระบุโฟลเดอร์ที่มีไฟล์ที่ต้องการส่งออก
STATIC_IMG_FOLDER = '/home/nattakonpu/codes/Valolyze/static/img/'  # โฟลเดอร์ที่ 2 เพื่อเก็บวิดีโอที่จะใช้แสดงในเว็บ


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['STATIC_IMG_FOLDER'] = STATIC_IMG_FOLDER


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
            file.save(os.path.join(app.config['STATIC_IMG_FOLDER'], filename))  # บันทึกไฟล์วิดีโอไว้ในโฟลเดอร์สำหรับการแสดงในเว็บด้วย

            #เรียกใช้หลัง main.py หลังอัพโหลดเสร็จ
            subprocess.Popen(["python", "/home/nattakonpu/codes/Valolyze/Backend/main.py"])
            return redirect(url_for('home'))

@app.route('/download')
def download_final_predict():
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'FinalPredict+time_Round_1.csv')
    return send_file(file_path, as_attachment=True)

@app.route('/csv_data')
def get_csv_data():
    csv_path = '/home/nattakonpu/codes/Valolyze/Backend/Output/Final/FinalPredict+time_Round_1.csv'
    return send_file(csv_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)