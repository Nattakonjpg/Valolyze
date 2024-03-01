from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('test_webapp.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.file['fileupload']

    file.save(f'uploads/{file.filename}')
    return redirect('')