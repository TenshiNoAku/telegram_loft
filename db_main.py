from sqlalchemy import create_engine, Integer, String, \
    Column, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///uny_loft.db")


class Cities(Base):  # table Cities
    __tablename__ = "cities"
    city_id = Column(Integer, primary_key=True)
    city_title = Column(String(50), nullable=False)


class Users(Base):  # table Users
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=True)
    current_url = Column(String(500), nullable=False,
                         default="https://vuzopedia.ru/region/city/59")
    current_city = Column(String(60), nullable=True)
    ege_score = Column(Integer, default=300)
    dir_search = Column(Boolean, default=0)


class Subjects(Base):  # table Subjects
    __tablename__ = "subjects"
    subject_id = Column(Integer, primary_key=True)
    subject_name = Column(String(50), nullable=False)
    subject_code = Column(String(10), nullable=False)


class Proffesional_Directions(Base):  # table Proffesional_Directions
    __tablename__ = "directions"
    pd_id = Column(Integer, primary_key=True)
    pd_name = Column(String(50), nullable=False)
    pd_code = Column(String(50), nullable=False)


class Users_Cities(Base):  # table Users_Cities
    __tablename__ = "user_cities"
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    city = Column(String(50), ForeignKey("cities.city_id"), nullable=False)


class Users_Subjects(Base):  # table Users_Subjects
    __tablename__ = "user_subjects"
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    subject = Column(String(50), ForeignKey("subjects.subject_id"), nullable=False)


class Users_Directions(Base):  # table Users_Directions
    __tablename__ = "user_directions"
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    direction = Column(String(50), ForeignKey("directions.pd_id"), nullable=False)


class Users_Favorites(Base):  # table Users_Favorites
    __tablename__ = "user_fav"
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    fav_url = Column(String(500), nullable=False)


Base.metadata.create_all(engine)
