from sqlalchemy import create_engine, engine, or_, case, literal_column
from sqlalchemy.orm import scoped_session, sessionmaker, load_only
from sqlalchemy.ext.declarative import declarative_base
from config import Config


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()