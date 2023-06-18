from flask import Flask, jsonify, request
import requests
import sys

app = Flask(__name__)
print(sys.path)

@app.route('/')
def home():
    return 'Flask backend is running!'

@app.route('/pull_kernel')
def pull_kernel():
    # Define the API endpoint URL and headers
    api_url = "https://www.kaggle.com/kernels/..."
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer <your_kaggle_api_key>"
    }

    # Make the API call
    response = requests.get(api_url, headers=headers)

    # Return the response as JSON
    return jsonify(response.json())
