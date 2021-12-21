from app import Base
from app.models import Table, Column, Integer, ForeignKey, VARCHAR

user_category = Table('user_category', Base.metadata,
                      Column('user_id', ForeignKey('user.id'), primary_key=True),
                      Column('category_id', ForeignKey('category.id'), primary_key=True))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR, nullable=False)
    last_name = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, nullable=False, unique=True)
    password = Column(VARCHAR, nullable=False)
    country = Column(VARCHAR, nullable=False)
    username = Column(VARCHAR, nullable=False, unique=True)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)