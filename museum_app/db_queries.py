from museum_app.models import *


def main_search(request, session):
    # result = session.query(Collection)#.filter(Collection.id < 100).limit(10)
    result = session.query(Collection)
    return result
