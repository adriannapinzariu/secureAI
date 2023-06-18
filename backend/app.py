from flask import Flask, send_from_directory
from routes import init_routes


def create_app():
    app = Flask(__name__, static_folder='../build') # replace 'react_app/build' with the path to your build folder
    init_routes(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)