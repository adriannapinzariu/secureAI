from flask import Flask, send_file
import subprocess

app = Flask(__name__, static_folder='../build', static_url_path='/')

@app.route('/api/run_model', methods=['GET'])
def run_model():
    # Invoke the Streamlit app using the `streamlit run` command
    subprocess.run(['streamlit', 'run', '../app.py'], cwd='.', shell=False)

    # Return the index.html file of the React app
    return send_file('../build/index.html')

if __name__ == '__main__':
    app.run()
