from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('test_webapp.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.file['file']

    file.save(f'uploads/{file.filename}')

    return redirect('/')

if __name__ =="__main__":
    app.run(host='0.0.0.0',debug=True,port=5001)#host='0.0.0.0", port=500