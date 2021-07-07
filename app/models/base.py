'''this base model can be inhertied in all other models
simply the field names for other tables which would be common can be written here as a base'''

from sqlalchemy.ext import declarative as decl
# from sqla_stack.fl_sqla import sql_db
from sqla_stack.fl_sqla import sql_db
Base = decl.declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @decl.declared_attr
    def __tablename__(cls):
        return cls.__name__

    pid = sql_db.Column(sql_db.Integer(), primary_key=True, unique=True, autoincrement=True, nullable=False)
    created_on = sql_db.Column(sql_db.DateTime, nullable=False, server_default=sql_db.func.now())
    updated_on = sql_db.Column(sql_db.DateTime, nullable=False, server_default=sql_db.func.now(),
                               onupdate=sql_db.func.now())

    '''here all the commonly used crud functions are written . jutscall the class and 
    the function to save, delete or update or quuery.'''

    def save(self):
        try:
            sql_db.session.add(self)
            sql_db.session.commit()
            return self
        except Exception as e:
            sql_db.session.rollback()
            raise e

    def update(self, new_dict):
        for k, v in new_dict.items():
            setattr(self, k, v)
        sql_db.session.commit()

    def delete_me(self):
        try:
            sql_db.session.delete(self)
            sql_db.session.commit()
            return True
        except Exception as e:
            sql_db.session.rollback()
            raise e

    @classmethod
    def my_field_list(cls):
        return list(cls.__table__.columns)

    def get_attrib_names(self):
        # noinspection PyUnresolvedReferences
        column_names = [column.name for column in self.__table__.columns]
        return column_names

    def get_attrib_dict(self):
        attrib_names = self.get_attrib_names()
        attribs = {name: self.__dict__.get(name) for name in attrib_names}
        # attribs.pop('id')
        return attribs

    def to_dict(self):
        ent_dict = {
            'ent_type': self.__class__.__name__,
            'attributes': self.get_attrib_dict()
        }
        return ent_dict

    @classmethod
    def by_pid(cls, pid, check_only=False):
        entity = cls.by_prop_val('pid', pid, check_only=check_only)
        return entity

    @classmethod
    def by_xid(cls, pid, check_only=False):
        entity = cls.by_prop_val('xid', pid, check_only=check_only)
        return entity

    @classmethod
    def by_prop_val(cls, key, val, check_only=False):
        return cls.by_prop_values({key: val}, check_only=check_only)

    @classmethod
    def by_prop_values(cls, key_val_dicts, check_only=False):
        results = cls.run_query(key_val_dicts)
        num_results = None  # for PEP
        try:
            num_results = len(results)
            assert num_results == 1

            entity: cls = results[0]
            return entity
        except AssertionError:
            qstr = str(key_val_dicts)
            kind = cls.__tablename__
            if num_results == 0:
                if check_only:
                    return None
                else:
                    raise Exception(F'In sql_db Model, get_entity - query {qstr} returned NO {kind} entity')
            else:  # got more than one
                return results[0]

    @classmethod
    def list_by_query(cls, key_val_dicts):
        lbq_dict = {key: value for key, value in key_val_dicts.items() if key_val_dicts[key] is not None}
        entities = cls.run_query(lbq_dict)
        return entities

    @classmethod
    def run_query(cls, key_val_dicts):
        query = sql_db.session.query(cls)
        for key, value in key_val_dicts.items():
            attrib = getattr(cls, key)
            query = query.filter(attrib == value)
        try:
            entities = query.all()

            if entities is None:  # query always returns at least an empty list
                raise Exception
        except Exception as e:
            sql_db.session.rollback()
            raise e
        return entities

    @classmethod
    def run_query_all(cls):
        query = sql_db.session.query(cls)
        try:
            entities = query.all()

            if entities is None:  # query always returns at least an empty list
                # raise SAQueryError
                pass
        except Exception as e:
            sql_db.session.rollback()
            raise e
        return entities
