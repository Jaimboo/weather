import os

from flask import Flask, current_app


# Adding basic info for configuration and creating a file to store them.
def init_cfg():
    cfg = {
            'SECRET_KEY' : 'dev',
            'DATABASE' : os.path.join(current_app.instance_path, "weather.sqlite"),
            'SESSION_PERMANENT' : False,
            'SESSION_TYPE' : 'filesystem'
        }
    try:
        if not os.path.exists(current_app.instance_path):
            os.makedirs(current_app.instance_path)
        with open(os.path.join(current_app.instance_path, 'config.cfg'), 'a') as f:
            for key, value in cfg.items():
                f.write(f'{key} = "{value}"\n')
    except OSError:
        pass

