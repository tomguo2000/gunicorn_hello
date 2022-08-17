import logging
import os
from dotenv import load_dotenv
from datetime import timedelta


class BaseConfig(object):
    """Base configuration."""

    # 确认 .env 文件的内容已经加载到环境变量
    dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path, override=True)


    DEBUG = False
    TESTING = False

    # ******************************************************************************
    # APP name and port
    APP_NAME = 'gunicorn_hello'
    APP_PORT = 7788
    APP_VERSION = "0.0.1"
    # ******************************************************************************

    # Logfile name
    LOGFILE_NAME = APP_NAME
    LOG_LEVEL = logging.INFO

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 3600

    # Nacos register
    NACOS_REGISTER = False
    NACOS_HEARTBEAT_INTERVAL = 10   # 秒

    # Example:
    # MySQL: mysql+pymysql://{db_user}:{db_password}@{db_endpoint}/{db_name}
    # SQLite: sqlite:///local_data.db
    DB_TYPE = os.getenv("DB_TYPE")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_ENDPOINT = os.getenv("DB_ENDPOINT")
    DB_NAME = os.getenv("DB_NAME")

    UNVERIFIED_USER_THRESHOLD = 2592000  # 30 days

    # Flask JWT settings
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(weeks=4)

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", None)
    if not SECRET_KEY:
        raise ValueError('You need to export SECRET_KEY set for Flask application')
    #
    # SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True

    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    @staticmethod
    def build_db_uri(
        db_type_arg=DB_TYPE,
        db_user_arg=DB_USERNAME,
        db_password_arg=DB_PASSWORD,
        db_endpoint_arg=DB_ENDPOINT,
        db_name_arg=DB_NAME,
    ):
        """Build remote database uri using specific environment variables."""

        return "{db_type}://{db_user}:{db_password}@{db_endpoint}/{db_name}".format(
            db_type=db_type_arg,
            db_user=db_user_arg,
            db_password=db_password_arg,
            db_endpoint=db_endpoint_arg,
            db_name=db_name_arg,
        )


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = BaseConfig.build_db_uri()
    MOCK_EMAIL = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = BaseConfig.build_db_uri()

    # register this APP to Nacos
    NACOS_REGISTER = True
    NACOS_SERVER_URI = "http://27.0.167.76:8848"

    # redis
    REDIS_HOST = '27.0.167.77'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None
    REDIS_DB = 1

    # Kafka
    KAFKASERVER = ['27.0.167.77:9092']
    KAFKA_CONSUMER = True
    KAFKA_CONSUMER_TOPIC = "DEV_INTERNAL_INFORM_TEST"
    KAFKA_ZOOKEEPER = '27.0.167.77:2181'


class LocalConfig(BaseConfig):
    """Local configuration."""

    DEBUG = True

    # Using a local sqlite database
    SQLALCHEMY_DATABASE_URI = "sqlite:///local_data.db"

    # register this APP to Nacos
    NACOS_REGISTER = False
    NACOS_SERVER_URI = "http://27.0.167.76:8848"

    # redis
    REDIS_HOST = '27.0.167.77'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None
    REDIS_DB = 11

    # Kafka
    KAFKASERVER = ['27.0.167.77:9092']
    KAFKA_CONSUMER = True
    KAFKA_CONSUMER_TOPIC = "DEV_INTERNAL_INFORM_TEST"
    KAFKA_ZOOKEEPER = '27.0.167.77:2181'


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    MOCK_EMAIL = True

    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = "sqlite://"


def get_env_config() -> str:

    flask_config_name = os.getenv("FLASK_ENVIRONMENT_CONFIG", "dev")

    if flask_config_name not in ["prod", "test", "dev", "local"]:
        raise ValueError(
            "The environment config value has to be within these values: prod, dev, test, local."
        )
    return CONFIGURATION_MAPPER[flask_config_name]


CONFIGURATION_MAPPER = {
    "dev": "config.DevelopmentConfig",
    "prod": "config.ProductionConfig",
    "local": "config.LocalConfig",
    "test": "config.TestingConfig",
}
