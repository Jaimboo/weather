import os

from flask import Flask

from .config import init_cfg

from livereload import Server

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)

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
server = Server(app.wsgi_app)
server.serve(liveport=35729, host='0.0.0.0', port=5500)