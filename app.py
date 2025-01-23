from flask import Flask
from flask_cors import CORS
from api.routes import api_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    return app

app = create_app()
CORS(app)  # Enable CORS for all routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)