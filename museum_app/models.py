from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, JSON, and_, text, ForeignKey, ForeignKeyConstraint

Base = declarative_base()

#  RAW TEXT


class AuthorRaw(Base):
    __tablename__ = "author_raw"
    id = Column("id", Integer, primary_key=True)
    text = Column("text", String, primary_key=True)


class TimeRaw(Base):
    __tablename__ = "time_raw"
    id = Column("id", Integer, primary_key=True)
    text = Column("text", String, primary_key=True)


class TechnologyRaw(Base):
    __tablename__ = "technology_raw"
    id = Column("id", Integer, primary_key=True)
    text = Column("text", String, primary_key=True)


class DescriptionRaw(Base):
    __tablename__ = "description_raw"
    id = Column("id", Integer, ForeignKey("collection.id"), primary_key=True)
    text = Column("text", String)


class ProductionRaw(Base):
    __tablename__ = "production_raw"
    id = Column("id", Integer, primary_key=True)
    text = Column("text", String, primary_key=True)


class FindRaw(Base):
    __tablename__ = "find_raw"
    id = Column("id", Integer, primary_key=True)
    text = Column("text", String, primary_key=True)

#  LINK TABLES


class WikidataProperties(Base):
    __tablename__ = "wikidata_properties"
    property_id = Column("property_id", Integer, primary_key=True)
    name_en = Column("name_en", String)
    name_ru = Column("name_ru", String)
    qid = Column("qid", String)


class WikidataEntities(Base):
    __tablename__ = "wikidata_entities"
    entity_id = Column("entity_id", Integer, primary_key=True)
    name_en = Column("name_en", String)
    name_ru = Column("name_ru", String)


class AuthorWikidata(Base):
    __tablename__ = "author_wikidata"

    author_id = Column("author_id", Integer, primary_key=True)
    property_id = Column("property_id", Integer, ForeignKey("wikidata_properties.property_id"),
                         primary_key=True)
    property = relationship("WikidataProperties")
    entity_id = Column("entity_id", Integer,
                    ForeignKey("wikidata_entities.entity_id"), primary_key=True)
    entity = relationship("WikidataEntities")
    entity_value = Column("entity_value", String, primary_key=True)


class GeoWiki(Base):
    __tablename__ = "geo_wiki"
    geo_id = Column("geo_id", Integer, primary_key=True)
    name_0 = Column("name_0", Integer)
    name_1 = Column("name_1", Integer)
    ru = Column("ru", Integer)


class LinkAuthors(Base):
    __tablename__ = "authors"

    id = Column("id", Integer, ForeignKey("collection.id"), primary_key=True)
    author_id = Column("author_id", Integer, ForeignKey("author_name.author_id"),
                       primary_key=True)


class LinkImage(Base):
    __tablename__ = "image_link"

    id = Column("id", Integer, ForeignKey("collection.id"))
    image_id = Column("image_id", Integer, primary_key=True)


class LinkTech(Base):
    __tablename__ = "technologies"

    id = Column("id", Integer, ForeignKey("collection.id"), primary_key=True)
    tech_id = Column("tech_id", Integer, ForeignKey("technology_name.tech_id"), primary_key=True)

# MAIN CLASSES


class Museums(Base):
    __tablename__ = "museums"
    museum_copuk = Column("museum_copuk", Integer, primary_key=True)
    name = Column("name", String)


class Typology(Base):
    __tablename__ = "typology"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Collection(Base):
    __tablename__ = "collection"

    # имя колонки = специальный тип (тип данных, первичный ключ)
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)

    start_year = Column("startYear", Integer)
    start_month = Column("startMonth", Integer)
    start_day = Column("startDay", Integer)
    finish_year = Column("finishYear", Integer)
    finish_month = Column("finishMonth", Integer)
    finish_day = Column("finishDay", Integer)
    time_sure = Column(Integer)

    authors = relationship("AuthorName", secondary='authors', lazy='dynamic')
    technologies = relationship("TechnologyName", secondary='technologies', lazy='dynamic')
    images = relationship("LinkImage")
    #
    author_str = Column('author_str', Integer, ForeignKey('author_raw.id'))
    author_raw = relationship('AuthorRaw', uselist=False)

    time_str = Column('time_str', Integer, ForeignKey('time_raw.id'))
    time_raw = relationship('TimeRaw', uselist=False)

    # technology_str = Column('technology_str', Integer, ForeignKey('technology_raw.id'))
    # technology_raw = relationship('TechnologyRaw', uselist=False)
    #
    # description_str = Column('id', Integer, ForeignKey('description_raw.id'))
    description_raw = relationship('DescriptionRaw', uselist=False, primaryjoin="DescriptionRaw.id==Collection.id")
    #
    production_str = Column('production_str', Integer, ForeignKey('production_raw.id'))
    production_raw = relationship('ProductionRaw', uselist=False)
    #
    # find_str = Column('find_str', Integer, ForeignKey('find_raw.id'))
    # find_raw = relationship('FindRaw', uselist=False)
    #
    geo_id = Column('geo_id', Integer, ForeignKey('geo_wiki.geo_id'))
    museum_copuk = Column(Integer, ForeignKey('museums.museum_copuk'))
    typology_id = Column('typology', Integer, ForeignKey('typology.id'))
    #
    museum = relationship("Museums", uselist=False)
    typology = relationship('Typology', uselist=False)
    geo_obj = relationship('GeoWiki')


class AuthorName(Base):
    __tablename__ = "author_name"
    author_id = Column("author_id", Integer, primary_key=True)
    name_en = Column("name_en", String)
    name_ru = Column("name_ru", String)
    qid = Column("qid", String)
    n = Column("n", Integer)
    order_name = Column("order_name", String)


class TechnologyName(Base):
    __tablename__ = "technology_name"
    tech_id = Column("tech_id", Integer, primary_key=True)
    name_en = Column("name_en", String)
    name_ru = Column("name_ru", String)
    kind = Column("kind", Integer)
    qid = Column("qid", String)


class FacesPainting(Base):
    __tablename__ = "faces_paiting"

    face_id = Column("face_id", Integer, primary_key=True)
    image_id = Column("image_id", Integer)
    obj_id = Column("obj_id", Integer, ForeignKey("collection.id"))
    collection_obj = relationship("Collection", uselist=False)
