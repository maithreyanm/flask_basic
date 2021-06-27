'''here we use this to import the credentials from yaml.. help us maintain a separate file for highly secret access'''

import root_settings as rt
from library.config_helper import ConfigHelper, CfgSrc, YAMLHelper


class Config(ConfigHelper):

    def __init__(self, config_mode=None):
        super().__init__()

        self.set_env_vars(root_path=rt.app_root(), env_name='.env') #.env file name

        # An APP_NAME env var must be set and it MUST agree with app_name_check
        self.app_name_check = 'FlaskBasicApp'

        self.config_mode_list = [
            'DEV',  # developer
            'TEST',  # testing
            'PROD'  # production
        ]
        self.DEFAULT_YAML_CONFIG = 'app_config.yaml'        #yaml config file name
        self.YAML_CONFIG = self.get_config_attrib(
            attrib_name='APP_YAML_CONFIG', option_val=self.DEFAULT_YAML_CONFIG, source=CfgSrc.ENV)
        self.yaml_config = YAMLHelper(self.YAML_CONFIG)

        self.environ_check('AppConfig/Name')

        if config_mode is None:
            self.set_config_to_environment('AppConfig/ConfigMode')
        else:
            self.set_config_mode(config_mode)

    @classmethod
    def initialize(cls, flapp, config=None):            #initializing the database

        from app.models import DataBaseConfig
        DataBaseConfig.initialize(flapp, config)


