from flask import Flask
from flask import url_for, redirect
from waitress import serve


from api.db_handler import db_api


def create_app():
    """Creates a new Flask application and initialize application."""

    app = Flask(__name__, static_url_path='',
                static_folder='../dist',
                template_folder='../dist')

    @app.route('/')
    def home():
        return redirect(url_for('static', filename='index.html'))

    app.url_map.strict_slashes = False
    app.register_blueprint(db_api, url_prefix='/api/db')

    return app


def run():
    serve(create_app(), host='0.0.0.0', port=8808)
