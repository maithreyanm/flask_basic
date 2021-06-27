'''getting the db cocnfigurations from yaml via config.py. written in init can be used anywhere in models'''

from config import Config

config = Config()  # config class to config object


class DataBaseConfig:
    DEBUG = False
    config = None
    config_mode = None

    # db_configuration
    db_user = None
    db_pwd = None
    db_name = None
    db_host = None
    db_url = None

    @classmethod  # initialzing the db using the sql alchemy uri
    def initialize(cls, flapp, config=None):
        cls.config = config
        cls.config_mode = cls.config.config_mode

        cls.db_config()

        flapp.config['SQLALCHEMY_DATABASE_URI'] = cls.db_url

        flapp.config['SQLALCHEMY_BINDS'] = {
            "sql_db": cls.db_url,
        }

        flapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @classmethod
    def db_config(cls):
        ydict = cls.config.yaml_config.path_get('Database-Connections/MySQL/APP')

        cls.db_host = config.yaml_config.path_get(f'{cls.config_mode}/DB_HOST', ydict)
        cls.db_user = config.yaml_config.path_get(f'{cls.config_mode}/DB_USER', ydict)
        cls.db_pwd = config.yaml_config.path_get(f'{cls.config_mode}/DB_PASS', ydict)
        cls.db_name = config.yaml_config.path_get(f'{cls.config_mode}/DB_NAME', ydict)
        cls.db_url = f"mysql+mysqlconnector://{cls.db_user}:{cls.db_pwd}@" \
                     f"{cls.db_host}/{cls.db_name}"
