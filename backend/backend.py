from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os
import requests
import sys

app = Flask(__name__)

# Configure the upload folder and allowed file extensions
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return "Welcome to our server !!"

@app.route('/pull-kernel', methods=['GET'])
def pull_kernel():
    # Your logic to pull kernel from GitHub

    # Call an external HTTP API (example)
    response = requests.get('https://api.github.com')

    # Return the response as JSON
    return jsonify(response.json())

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully', 200

if __name__ == '__main__':
    app.run(debug=True)
