import uuid
import yaml
from sqlalchemy import Table, create_engine, MetaData, orm, and_, Integer, Column, String, DateTime, ForeignKey, func
from pathlib import Path

root_dir = Path(__file__).parent.parent
a_yaml_file = open(f"{root_dir}/YAML_CONFIG/app_config.yaml")
parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
config_mode = parsed_yaml_file["AppConfig"]['ConfigMode']
db_host = parsed_yaml_file["Database-Connections"]['MySQL']['APP'][config_mode]['DB_HOST']
db_user = parsed_yaml_file["Database-Connections"]['MySQL']['APP'][config_mode]['DB_USER']
db_pass = parsed_yaml_file["Database-Connections"]['MySQL']['APP'][config_mode]['DB_PASS']
db_name = parsed_yaml_file["Database-Connections"]['MySQL']['APP'][config_mode]['DB_NAME']
db_url = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}'

engine = create_engine(db_url)
conn = engine.connect()
metadata = MetaData()
Session = orm.sessionmaker(bind=engine)
session = Session()

User = Table('User', metadata,
    Column('pid', Integer, primary_key=True),
    Column('created_on', DateTime, default=func.now()),
    Column('updated_on', DateTime, onupdate=func.utc_timestamp()),
    Column('name', String(50)),
    Column('age', Integer())
)

User_2 = Table('User_2', metadata,
    Column('pid', Integer, primary_key=True),
    Column('created_on',DateTime, default=func.now()),
    Column('updated_on', DateTime, onupdate=func.utc_timestamp()),
    Column('name_2', String(50)),
    Column('age_2', Integer),
    Column('user_key', Integer, ForeignKey("User.pid")),
    Column('item_id', Integer)
)

metadata.create_all(engine)

