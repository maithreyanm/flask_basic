import os
import dotenv
import yaml
from enum import Enum
from flask import Flask
from pathlib import Path


class ConfigErr(RuntimeError):
    pass


class YAMLError(RuntimeError):
    pass


class CfgSrc(Enum):
    ENV = 10
    YAML = 20


class YAMLHelper:

    def __init__(self, yaml_file):
        self.yaml_file = yaml_file
        self._ydict = None

    @property
    def ydict(self):

        if self._ydict is None:
            # Get root dir path
            root_dir = Path(__file__).parent.parent
            # Read the yaml file
            with open(f"{root_dir}/YAML_CONFIG/{self.yaml_file}") as file:
                self._ydict = yaml.load(file, Loader=yaml.FullLoader)

        return self._ydict

    def path_get(self, ypath: str, ydict=None, opt_value=None):
        path_dict = ydict or self.ydict

        for item in ypath.split("/"):
            value = path_dict.get(item)
            if value is None:
                if opt_value:
                    return opt_value
                raise YAMLError(F'Can not find {item} at {ypath}')
            path_dict = value

        return path_dict


class ConfigHelper:

    def __init__(self):
        self.config_mode = None
        self.config_mode_list = None

        # There MUST be a variable named APP_NAME in the environment
        # and it MUST be the same as app_name_check value
        self.app_name_check = None  # the concrete config must override
        self.APP_NAME = None  # set by environ_check()
        self.yaml_config: YAMLHelper = None  # if used config must set

    def environ_check(self, yaml_path):
        """
        Verifies the api's environment variables have been set.
        In other words, that 'source .env' has been run for the api
        """
        assert self.app_name_check is not None, "config must define app_name_check"
        if self.APP_NAME is None:
            YAML_APP_NAME = self.get_config_attrib(yaml_path, option_val=-1, source=CfgSrc.YAML)
            assert YAML_APP_NAME == self.app_name_check, F'YAML api name should be {self.app_name_check}'
            self.APP_NAME = self.app_name_check

    def set_config_to_environment(self, attrib_name=None):
        mode = self.get_config_attrib(attrib_name, source=CfgSrc.YAML)
        self.set_config_mode(mode)

    def set_config_mode(self, mode):
        assert self.APP_NAME, 'environ_check() must be called first'
        if self.config_mode == mode:
            return self.config_mode
        assert self.config_mode is None, F'Can not CHANGE config_mode. (is: {self.config_mode} requested {mode})'

        assert self.config_mode_list, 'config_mode_list is not set'
        assert mode in self.config_mode_list, \
            F'Requested config_mode:{self.config_mode} is not in the config_mode_list:{self.config_mode_list}'

        self.config_mode = mode
        return self.config_mode

    def get_config_attrib(self, attrib_name, option_val=None, source: CfgSrc = CfgSrc.YAML):

        if source == CfgSrc.YAML:
            attrib_val = self.yaml_config.path_get(attrib_name, opt_value=option_val)
        else:
            attrib_val = os.environ.get(attrib_name) or option_val

        if attrib_val is None:
            raise ConfigErr(F'In {source.name} config, attribute {attrib_name} not found.')
        return attrib_val

    @classmethod
    def set_env_vars(cls, root_path, env_name='.venv'):
        """
        This loads the environment variables from the env_name file into the current shell
        :param root_path: path to the environment file (not including the filename)
        :param env_name: name of fhe environment file
        """
        venv_path = os.path.join(root_path, env_name)
        dotenv.load_dotenv(venv_path, verbose=True)

    @classmethod
    def initialize(cls, flapp: Flask, config: 'ConfigHelper' = None):
        """
        - This method should be overridden by the concrete config class to
        initialize the api in an orderly fashion (libraries first, api sub-systems second)
        - Individual services and library also create concrete derived class from the config_helper and
        override this method to initialize their sub-system
        :param config:
        :param flapp: makes the Flask api available, as needed
        """
        pass
