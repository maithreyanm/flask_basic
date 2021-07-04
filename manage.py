from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from flask_svc import app
from sqla_stack.fl_sqla import sql_db
from config import Config

config = Config()

migrate = Migrate(app, sql_db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()