from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory, jsonify
import shutil
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = '/home/thanapat_window/codes/Valolyze/Backend/video_data/test_videofull/agent/round'  # ระบุโฟลเดอร์ที่จะเก็บวิดีโอ
OUTPUT_FOLDER = '/home/thanapat_window/codes/Valolyze/Backend/Output/Final/'  # ระบุโฟลเดอร์ที่มีไฟล์ที่ต้องการส่งออก
STATIC_IMG_FOLDER = '/home/thanapat_window/codes/Valolyze/static/img/'  # โฟลเดอร์ที่ 2 เพื่อเก็บวิดีโอที่จะใช้แสดงในเว็บ


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['STATIC_IMG_FOLDER'] = STATIC_IMG_FOLDER


@app.route('/home_web')
def home():    
    return render_template("New_index.html")

@app.route('/Test')
def Test():    
    return render_template("123456Testttt.html")
@app.route('/Test')
def Test():    
    return render_template("123456Testttt.html")

@app.route('/clear-files', methods=['POST'])
def clear_files():
    if request.method == 'POST':
        # รับเส้นทางโฟลเดอร์ที่ต้องการเคลียร์ไฟล์
        directory_path = request.json.get('directory')

        # ตรวจสอบว่าเป็นเส้นทางที่ถูกต้องและมีอยู่จริงหรือไม่
        if directory_path and os.path.exists(directory_path):
            # เคลียร์ไฟล์ในโฟลเดอร์
            files = os.listdir(directory_path)
            for file in files:
                file_path = os.path.join(directory_path, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
            return jsonify(message="Files cleared successfully.")
        else:
            return jsonify(message="Invalid directory path.")


@app.route('/about')
def about():
    return render_template('New_about.html')

@app.route('/webapp') 
def upload():
    return render_template('bank.html')

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
            subprocess.Popen(["python", "/home/thanapat_window/codes/Valolyze/Backend/main_tung.py"])

            subprocess.Popen(["curl", "http://localhost:5001/fetch_data"])
            return redirect(url_for('home'))

@app.route('/download')
def download_final_predict():
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'FinalPredict+time_Round_1.csv')
    return send_file(file_path, as_attachment=True)

@app.route('/fetch_data')
def fetch_data():
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'FinalPredict+time_Round_1.csv')
    with open(file_path, 'r') as f:
        data = f.read()
    return jsonify(data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)