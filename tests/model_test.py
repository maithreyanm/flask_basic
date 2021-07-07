import unittest
from flask_svc import app
from datetime import datetime


class UserTests(unittest.TestCase):
    app.app_context().push()

    def test_user(self):
        from app.models.table_models import User
        usr = User()
        usr.created_on = datetime.now()
        usr.updated_on = datetime.now()
        usr.name = 'Mathew Perrera'
        usr.age = 25
        usr.save()

    def test_by_name_and_age(self):
        from app.models.table_models import User
        usr = User()
        result = usr.by_name('Mathew Perrera')
        print(result.name)
