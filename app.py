from flask import Flask, render_template, request

app = Flask(__name__)
    
UPLOAD_FOLDER = 'uploads'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/home_web')
def home():    
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/creator')
def creator():
    return render_template('Creator.html')

@app.route('/webapp') 
def upload():
    return render_template('webapp.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        # ถ้าไม่มีไฟล์ในคำขอ
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        # ถ้าไม่ได้เลือกไฟล์
        return 'No selected file'

    # ทำอะไรกับไฟล์ที่ถูกอัปโหลด เช่น บันทึกลงในโฟลเดอร์
    file.save('uploads/' + file.filename)

    return 'File uploaded successfully'

if __name__ =="__main__":
    app.run(host='0.0.0.0',debug=True,port=5001)#host='0.0.0.0", port=500