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

@app.route('/webapp') 
def upload():
    return render_template('webapp.html')

@app.route('/creator')
def creator():
    return render_template('Creator.html')

if __name__ =="__main__":
    app.run(host='0.0.0.0',debug=True,port=5001)#host='0.0.0.0", port=500