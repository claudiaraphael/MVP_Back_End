from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importing models
from model.comment import Comment
from model.product import Product
from model.user import User

# create the database path
db_path = "database/"
# if there is no directory...
if not os.path.exists(db_path):
    # create directory
    os.makedirs(db_path)

# url to access the database in local sqlite3
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# create the engine to conect to the database
engine = create_engine(db_url,echo=False)

# instanciate a session with the database
Session = sessionmaker(bind=engine)

# create the database if it doesnt exist
if not database_exists(engine.url):
    create_database(engine.url)

