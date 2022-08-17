from config import get_env_config
from app import create_app
import os

application = create_app(get_env_config())


@application.route("/gunicorn_hello/version", methods=['GET'])
def version():
    from app.utils.setLogger import logger
    logger.info("/version happen******************************************************************************")
    return {'code': 200, 'version': application.config.get('APP_VERSION')}, 200


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=application.config['APP_PORT'], use_reloader=False)
