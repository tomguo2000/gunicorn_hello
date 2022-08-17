from flask import Flask
import os
# from redis import Redis
import _thread

def create_app(config_filename: str) -> Flask:

    app = Flask(__name__)

    # setup application environment
    app.config.from_object(config_filename)
    app.url_map.strict_slashes = False

    # upload some useful config into os.env
    os.environ['NACOS_SERVER_URI'] = app.config['NACOS_SERVER_URI']

    # init logger
    from app.utils.setLogger import init_logger, logger
    init_logger(LOG_basename=app.config.get('LOGFILE_NAME')+'.log', Log_level=app.config.get('LOG_LEVEL'))

    return app
