from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import *


sql_db = SQLAlchemy()  # here we are initializng the sql db using sql alchemy
mg = Migrate()

from sqlalchemy import MetaData, create_engine
from sqlalchemy_utils import database_exists, create_database

meta = MetaData