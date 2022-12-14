import os

from flask import Flask, current_app



def init_cfg():
    cfg = {
            'SECRET_KEY' : 'dev',
            'DATABASE' : os.path.join(current_app.instance_path, "weather.sqlite") 
        }
    try:
        os.makedirs(current_app.instance_path)
        with open(os.path.join(current_app.instance_path, 'config.cfg'), 'a') as f:
            for key, value in cfg.items():
                f.write(f'{key} = "{value}"\n')
    except OSError:
        pass

