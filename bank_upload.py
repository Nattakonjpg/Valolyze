from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = '/home/nattakonpu/codes/Valolyze/Backend/video_data/test_videofull/agent/round'  # ระบุโฟลเดอร์ที่จะเก็บวิดีโอ
OUTPUT_FOLDER = '/home/nattakonpu/codes/Valolyze/Backend/Output/Final/'  # ระบุโฟลเดอร์ที่มีไฟล์ที่ต้องการส่งออก


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/home_web')
def home():    
    return render_template("New_index.html")

@app.route('/about')
def about():
    return render_template('New_about.html')

@app.route('/webapp') 
def upload():
    return render_template('bank.html')

@app.route('/creator')
def creator():
    return render_template('creator.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #เรียกใช้หลัง main.py หลังอัพโหลดเสร็จ
            subprocess.Popen(["python", "/home/nattakonpu/codes/Valolyze/Backend/main.py"])
            return redirect(url_for('home'))

@app.route('/download')
def download_final_predict():
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'FinalPredict+time_Round_1.csv')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)