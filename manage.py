from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app.models.table_models import User, User_2
from flask_svc import app
from sqla_stack.fl_sqla import sql_db
from config import Config

config = Config()

migrate = Migrate(app, sql_db)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=sql_db, user=User, user_2=User_2)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()


# python manage.py db init
# python manage.py db upgrade
# python manage.py db migrate
