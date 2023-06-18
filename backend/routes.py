from flask import send_from_directory, request, jsonify
from PIL import Image
import base64
import io

def init_routes(app):
    @app.route('/')
    def serve():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def static_proxy(path):
        return app.send_static_file(path)
    
    @app.route('/api/analyze', methods=['POST'])
    def analyze():
        data = request.get_json()  # Get the data sent in the request
        image_data = data.get('image')

        # The base64 string usually has a prefix 'data:image/jpeg;base64,'. You need to remove this.
        prefix = 'data:image/jpeg;base64,'
        if image_data.startswith(prefix):
            image_data = image_data[len(prefix):]
        
        # Convert base64 image data to PIL Image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        image.save('/usr/src/app/data/image_flask.jpg')


        print("image_data: ",type(image_data))
        print("image_data: ",type(image_data))


        # Call your Python API here with the image_data
        # For now, let's just return some mock data
        response_data = {
            'percentage': 90,
            'hotelName': 'Grandiose Hotel',
            'location': 'San Francisco',
        }

        return jsonify(response_data)