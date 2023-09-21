#!/usr/bin/env python3
"""The main flask app"""


from flask import Flask, send_from_directory
from api.v1.routes import bp as api_v1_bp

app = Flask(__name__, static_folder='clips')

app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

@app.route('/clips/<path:filename>', methods=['GET'])
def serve_clip(filename):
    return send_from_directory('clips', filename)

if __name__ == '__main__':
    app.run(debug=True)
