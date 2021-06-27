from app.models.table_models import User2
from sqla_stack.fl_sqla import sql_db
from flask import Flask
from flask_cors import CORS


class AppFactory:

    @classmethod
    def create_app(cls, config=None):
        try:
            flapp = Flask(__name__)
            from library.object_broker import ob
            ob['flapp'] = flapp

            if config is None:
                from config import Config
                config = Config()

            ob['config'] = config
            flapp.config.from_object(config)
            config.initialize(flapp, config)

            from app.api.api import api_blueprint
            flapp.register_blueprint(
                api_blueprint)  # registering the api using blueprint. register here to activate the api

            sql_db.init_app(flapp)  # here we are importing the db .. we use mysql and sqlalchemy
            with flapp.app_context():
                sql_db.create_all()  # creating the tables in the db  #disable this after creating in production
                # User2.extract_sample_values_from_sample_data()
                # the above is a method to load sample values into db when server is stared. disable this if data's
                # are loaded in the future

            CORS(flapp)
            return flapp

        except Exception as e:
            raise e
