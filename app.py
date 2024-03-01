from flask import Flask, render_template

app = Flask(__name__)
    
UPLOAD_FOLDER = 'uploads'  # 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/home_web')
def home():    
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/webapp', methods=['GET', 'POST']) 
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload'))
    return render_template('webapp.html')

@app.route('/creator')
def creator():
    return render_template('Creator.html')

if __name__ =="__main__":
    app.run(host='0.0.0.0',debug=True,port=5001)#host='0.0.0.0", port=500