import os

from flask import Flask

from .config import init_cfg

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)

    # On start the application creates some path if they do not exists yet and setup a basic configuration file.
    # User have to manually update the cfg file to insert an API_KEY
    if not os.path.exists(os.path.join(app.instance_path, 'config.cfg')):
        with app.app_context():
            init_cfg()

    app.config.from_pyfile('config.cfg')
   
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    
    else:
        app.config.from_mapping(test_config)
 
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import api
    app.register_blueprint(api.bp)

    return app

app = create_app()
