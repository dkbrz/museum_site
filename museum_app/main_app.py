from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from museum_app.config import DB
from museum_app.db_queries import (
    main_search,
    get_search_params
)

PER_PAGE = 100

engine = create_engine(DB, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()


def create_app():
    """Create and configure app"""
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.secret_key = 'yyjzqy9ffY'
    return app


app = create_app()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    data = get_search_params(session)
    return render_template("search.html", data=data)


@app.route("/results")
def result():
    if request.args:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        offset = (page - 1) * PER_PAGE
        result = main_search(request, session)
        number = result.count()
        pagination = Pagination(
            page=page, per_page=PER_PAGE, total=number,
            search=False, record_name='result', css_framework='bootstrap4',
            display_msg='Результаты <b>{start} - {end}</b> из <b>{total}</b>'
        )
        # query_params = get_search_query_terms(request.args)
        result = [exhibit for exhibit in result.offset(offset).limit(PER_PAGE)]
        return render_template(
            'results.html', result=result, number=number, pagination=pagination)
    return render_template('results.html', result=[])


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
