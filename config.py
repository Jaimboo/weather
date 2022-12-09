import os

from flask import Flask, current_app



def init_cfg():
    cfg = {
            'SECRET_KEY' : 'prova2',
            'DATABASE' : os.path.join(current_app.instance_path, "weather.sqlite") 
        }
    with open(os.path.join(current_app.instance_path, 'config.cfg'), 'a') as f:
        for key, value in cfg.items():
            f.write(f'{key} = "{value}"\n')
