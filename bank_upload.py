from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory, jsonify
import shutil
import os
import subprocess

app = Flask(__name__)

# ระบุโฟลเดอร์ที่จะเก็บวิดีโอ
UPLOAD_FOLDER = '/home/nattakonpu/codes/Valolyze/Backend/video_data/test_videofull/agent/round'
# ระบุโฟลเดอร์ที่มีไฟล์ที่ต้องการส่งออก
OUTPUT_FOLDER = '/home/nattakonpu/codes/Valolyze/Backend/Output/Final/'
# โฟลเดอร์ที่ 2 เพื่อเก็บวิดีโอที่จะใช้แสดงในเว็บ
STATIC_IMG_FOLDER = '/home/nattakonpu/codes/Valolyze/static/img/'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['STATIC_IMG_FOLDER'] = STATIC_IMG_FOLDER


# ฟังก์ชันเช็คว่าไฟล์โมเดลมีอยู่หรือไม่
def check_model_file_existence(model_file_path):
    return os.path.exists(model_file_path)


@app.route('/home_web')
def home():
    return render_template("New_index.html")


@app.route('/about')
def about():
    return render_template('New_about.html')


@app.route('/webapp')
def upload():
    return render_template('bank.html')


@app.route('/Sage.html')
def upload2():
    return render_template('Sage.html')


@app.route('/Sova.html')
def upload3():
    return render_template('Sova.html')


@app.route('/Jett.html')
def upload4():
    return render_template('Jett.html')


@app.route('/Habor.html')
def upload5():
    return render_template('Habor.html')


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
            file.save(os.path.join(app.config['STATIC_IMG_FOLDER'], filename))

            # เรียกใช้หลัง main.py หลังอัพโหลดเสร็จ
            subprocess.Popen(
                ["python", "/home/nattakonpu/codes/Valolyze/Backend/main.py"])

            subprocess.Popen(["curl", "http://localhost:5001/fetch_data"])
            return redirect(url_for('home'))


@app.route('/upload2', methods=['POST'])
def upload_file2():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # บันทึกไฟล์วิดีโอไว้ในโฟลเดอร์สำหรับการแสดงในเว็บด้วย
            file.save(os.path.join(app.config['STATIC_IMG_FOLDER'], filename))

            # เรียกใช้หลัง main.py หลังอัพโหลดเสร็จ
            subprocess.Popen(
                ["python", "/home/nattakonpu/codes/Valolyze/Backend/main2.py"])

            subprocess.Popen(["curl", "http://localhost:5001/fetch_data"])
            return redirect(url_for('home'))


@app.route('/upload3', methods=['POST'])
def upload_file3():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # บันทึกไฟล์วิดีโอไว้ในโฟลเดอร์สำหรับการแสดงในเว็บด้วย
            file.save(os.path.join(app.config['STATIC_IMG_FOLDER'], filename))

            # เรียกใช้หลัง main.py หลังอัพโหลดเสร็จ
            subprocess.Popen(
                ["python", "/home/nattakonpu/codes/Valolyze/Backend/main3.py"])

            subprocess.Popen(["curl", "http://localhost:5001/fetch_data"])
            return redirect(url_for('home'))


@app.route('/upload4', methods=['POST'])
def upload_file4():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # บันทึกไฟล์วิดีโอไว้ในโฟลเดอร์สำหรับการแสดงในเว็บด้วย
            file.save(os.path.join(app.config['STATIC_IMG_FOLDER'], filename))

            # เรียกใช้หลัง main.py หลังอัพโหลดเสร็จ
            subprocess.Popen(
                ["python", "/home/nattakonpu/codes/Valolyze/Backend/main4.py"])

            subprocess.Popen(["curl", "http://localhost:5001/fetch_data"])
            return redirect(url_for('home'))


@app.route('/upload5', methods=['POST'])
def upload_file5():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # บันทึกไฟล์วิดีโอไว้ในโฟลเดอร์สำหรับการแสดงในเว็บด้วย
            file.save(os.path.join(app.config['STATIC_IMG_FOLDER'], filename))

            # เรียกใช้หลัง main.py หลังอัพโหลดเสร็จ
            subprocess.Popen(
                ["python", "/home/nattakonpu/codes/Valolyze/Backend/main5.py"])

            subprocess.Popen(["curl", "http://localhost:5001/fetch_data"])
            return redirect(url_for('home'))


@app.route('/download')
def download_final_predict():
    file_path = os.path.join(
        app.config['OUTPUT_FOLDER'], 'FinalPredict+time_Round_1.csv')
    return send_file(file_path, as_attachment=True)


@app.route('/fetch_data')
def fetch_data():
    file_path = os.path.join(
        app.config['OUTPUT_FOLDER'], 'FinalPredict+time_Round_1.csv')
    with open(file_path, 'r') as f:
        data = f.read()
    return jsonify(data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
