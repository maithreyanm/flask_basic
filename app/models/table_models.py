'''here we are defining the tables for our project..'''

from sqla_stack.fl_sqla import sql_db
from app.models.base import BaseModel




class User(BaseModel):
    name = sql_db.Column(sql_db.String(80))
    age = sql_db.Column(sql_db.Integer())
    '''use the common query methods from base to query this table like query by name, filter
    by age'''

    @classmethod
    def by_name(cls, name, check_only=True):
        return cls.by_prop_val('name', name, check_only=check_only)

class User2(BaseModel):
    name_2 = sql_db.Column(sql_db.String(80))
    age_2 = sql_db.Column(sql_db.Integer())
    user_key = sql_db.Column(sql_db.Integer, sql_db.ForeignKey('User.pid'))

    @classmethod
    def by_user_key(cls, user_key, check_only=True):
        return cls.by_prop_val('name', user_key, check_only=check_only)


    '''a method to create sample values in db's table if needed to save as default values'''
    @classmethod
    def extract_sample_values_from_sample_data(cls):
        from app.models.sample_data import sample_datas
        for data in sample_datas:
            cls.chk_and_create(data)

    @classmethod
    def chk_and_create(cls, data):
        name_2 = data.get('name_2')
        age_2 = data.get('age_2')
        table_check = cls.by_name_and_age(name_2=name_2, age_2=age_2, check_only=True)
        if table_check is None:
            usr2 = User2()
            usr2.sf_name = data.get('name_2')
            usr2.nxg_name = data.get('age_2')
            usr2.save()

    @classmethod
    def by_name_and_age(cls, name_2, age_2, check_only=False):
        key_val_dicts = {'name_2': name_2, 'age_2': age_2}
        return cls.by_prop_values(key_val_dicts, check_only=check_only)

    ''' get the data from sample data, checking if it previously exists, then save them'''