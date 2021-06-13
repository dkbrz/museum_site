import json
import os
from museum_app.models import *

geo = json.load(open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/geo.json")
))

geo_museum = json.load(open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/geo_museum.json")
))


def _years(args, result, session):
    if args.get("min_year") or args.get("max_year"):
        min_year = args.get("min_year", type=int, default=None)
        max_year = args.get("max_year", type=int, default=None)
        print(min_year, max_year)
        if min_year:
            result = result.filter(Collection.start_year >= min_year)
        if max_year:
            result = result.filter(Collection.finish_year <= max_year)
    return result


def _typology(args, result, session):
    typology = args.get("typology")
    if typology != "-" and typology is not None:
        typology = int(typology)
        result = result.filter(Collection.typology_id == typology)
    return result


def _authors(args, result, session):
    author = args.get("author")
    if author:
        author = session.query(AuthorName).filter_by(order_name=author).one()
        result = result.join(LinkAuthors).filter(LinkAuthors.author_id == author.author_id)
    return result


def _geo(args, result, session):
    name_0 = args.get("country")
    name_1 = args.get("region")
    if not name_0 and not name_1:
        return result
    if name_0:
        geo = session.query(GeoWiki).filter_by(name_0=name_0)
    if name_1:
        geo = geo.filter_by(name_1=name_1)
    geo_ids = {i.geo_id for i in geo.all()}
    # print(geo_ids)
    result = result.filter(Collection.geo_id.in_(geo_ids))
    return result


def _geo_museum(args, result, session):
    region = args.get("region_now")
    district = args.get("district_now")
    museum = args.get("museum_now")
    if not region and not district and not museum:
        return result
    if region:
        geo = session.query(Museums).filter_by(nl_name_1=region)
    if district:
        geo = geo.filter_by(nl_name_2=district)
    if museum:
        geo = geo.filter_by(name=museum)
    ids = {i.museum_copuk for i in geo.all()}
    result = result.filter(Collection.museum_copuk.in_(ids))
    return result


def _techniques(args, result, session):
    # tecnhiques = {i for i in args.getlist("techniques") if i != ""}
    tecnhiques = args.get("techniques", type=int)
    # print(tecnhiques)
    if not tecnhiques:
        return result
    result = result.join(LinkTech).filter(LinkTech.tech_id == tecnhiques)
    return result


def main_search(request, session):
    # result = session.query(Collection)#.filter(Collection.id < 100).limit(10)
    args = request.args
    result = session.query(Collection)

    for func in [_geo, _geo_museum, _authors, _typology, _years, _techniques]:
        print(func)
        try:
            result = func(args, result, session)
        except:
            pass
    result = result.limit(100000)
    return result


def get_search_params(session):
    typology = session.query(Typology).all()
    authors = session.query(
        AuthorName
    ).filter(AuthorName.n >= 500).with_entities(
        AuthorName.author_id, AuthorName.order_name
    ).all()
    techniques = session.query(
        TechnologyName
    ).order_by(TechnologyName.name_ru).all()
    return {
        "typology": typology,
        "authors": authors,
        "geo_obj": geo.keys(),
        "geo_museum": geo_museum.keys(),
        "techniques": techniques
    }
