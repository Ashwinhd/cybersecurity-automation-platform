import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import Blueprints
from routes.scan_routes import scan_bp
from routes.ai_routes import ai_bp
from routes.alert_routes import alert_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable Cross-Origin Resource Sharing

    # Configuration
    app.config['DEBUG'] = os.getenv('DEBUG', 'True') == 'True'
    app.config['PORT'] = int(os.getenv('PORT', 5000))

    # Register Blueprints
    app.register_blueprint(scan_bp, url_prefix='/api/scans')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(alert_bp, url_prefix='/api/alerts')

    @app.route('/')
    def index():
        return jsonify({
            "message": "Cybersecurity Automation Platform (CAP) API is running",
            "status": "healthy"
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])
