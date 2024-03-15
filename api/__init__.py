from flask import Flask
from flask_cors import CORS


def create_app() -> Flask:
    """Create and configure flask app"""

    # Create flask app.
    app = Flask(__name__)

    # Enable CORS on all routes
    CORS(app)

    _register_blueprints(app)

    return app


def _register_blueprints(app: Flask) -> None:
    """Register flask blueprints for routing endpoints"""
    from api.endpoints import covid_stats

    app.register_blueprint(covid_stats.blueprint)
