from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

sql_db = SQLAlchemy()  # here we are initializng the sql db using sql alchemy
mg = Migrate()
