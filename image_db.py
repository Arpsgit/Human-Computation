import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Float, String, Integer, Text, LargeBinary
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class img_db(Base):
    __tablename__ = "image_database"
    id = Column(Integer, primary_key = True)
    user_name = Column(Text, nullable = False)
    file_name = Column(Text, nullable = False)
    coord_x1 = Column(Float, nullable=False)
    coord_y1 = Column(Float, nullable=False)
    coord_x2 = Column(Float, nullable=False)
    coord_y2 = Column(Float, nullable=False)
    number_of_letters = Column(Integer, nullable=False)
    number_of_words = Column(Integer, nullable=False)
    font_size = Column(Integer, nullable=False)
    img = Column(LargeBinary, unique = False, nullable = False)


# engine = create_engine("sqlite:///image_db.sqlite3")
# Base.metadata.create_all(engine)
