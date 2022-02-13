from app import Base, engine
from app.models import Table, Column, Integer, ForeignKey, VARCHAR
from sqlalchemy import BigInteger, Date
from sqlalchemy.orm import relationship


user_category = Table('user_category', Base.metadata,
                      Column('user_id', ForeignKey('user.id'), primary_key=True),
                      Column('category_id', ForeignKey('category.id'), primary_key=True))


user_satellite = Table('user_satellite', Base.metadata,
                       Column('user_id', ForeignKey('user.id')),
                       Column('satellite_id', ForeignKey('satellites.norad_id')))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR, nullable=False)
    last_name = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, nullable=False, unique=True)
    password = Column(VARCHAR, nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'))
    username = Column(VARCHAR, nullable=False, unique=True)

    categories = relationship("Category", secondary=user_category)
    satellite = relationship("Satellites", secondary=user_satellite)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False)


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)
    latitude = Column(VARCHAR, nullable=False)
    longitude = Column(VARCHAR, nullable=False)
    admin_name = Column(VARCHAR, nullable=False)


class Satellites(Base):
    __tablename__ = 'satellites'
    norad_id = Column(BigInteger, primary_key=True)
    satname = Column(VARCHAR, nullable=False)
    inclination = Column(VARCHAR, nullable=False)
    ascending_node_longitude = Column(VARCHAR, nullable=False)
    eccentricity = Column(VARCHAR, nullable=False)
    pericenter_argument = Column(VARCHAR, nullable=False)
    average_anomaly = Column(VARCHAR, nullable=False)
    call_frequency = Column(VARCHAR, nullable=False)


class Stars(Base):
    __tablename__ = 'stars'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(VARCHAR)
    right_ascension = Column(VARCHAR)
    declination = Column(VARCHAR)
    flux_visible_light = Column(VARCHAR)
    parallax = Column(VARCHAR)
    spectral_type = Column(VARCHAR)


class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    mass = Column(VARCHAR)
    density = Column(VARCHAR)
    mean_temperature = Column(VARCHAR)
    radius = Column(VARCHAR)
    visual_mag = Column(VARCHAR)


class PlanetCoordinates(Base):
    __tablename__ = 'planet_coordinates'
    id = Column(Integer, primary_key=True)
    planet_id = Column(Integer, ForeignKey('planet.id'))
    date = Column(Date)
    dec = Column(VARCHAR)
    ra = Column(VARCHAR)

    planet = relationship(Planet, backref='planet_coordinates', lazy=False)


class KeyModel(Base):
    __tablename__ = 'key'
    id = Column(Integer, primary_key=True)
    code = Column(VARCHAR)
    key_role = Column(VARCHAR)


# models for views
StarsFluxV = Table('stars_flux_v', Base.metadata, autoload_with=engine)
StarsParallax = Table('stars_parallax', Base.metadata, autoload_with=engine)
