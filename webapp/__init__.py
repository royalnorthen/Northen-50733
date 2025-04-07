import os

from flask import Flask

from .dbtools import init_app

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'research.db'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_app(app)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from .controllers.index import index_page
    from .controllers.project import project_page

    app.register_blueprint(index_page)
    app.register_blueprint(project_page)

    return app
