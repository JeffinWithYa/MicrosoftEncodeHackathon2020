from flask import Flask, session, url_for
def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.app_context().push()
    with app.app_context():
        from . import routes  # Import routes
        return app
