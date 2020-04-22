from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.core import core_bp
    app.register_blueprint(core_bp)

    return app
