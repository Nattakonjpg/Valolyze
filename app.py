from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home_web')
def home():    
    return render_template("index.html")


if __name__ =="__main__":
    app.run(host='0.0.0.0',debug=True,port=5001)#host='0.0.0.0", port=500