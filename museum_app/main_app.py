from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from museum_app.config import DB
from museum_app.db_queries import (
    main_search,
    get_search_params,
    get_museums,
    get_museum_map
)
from museum_app.face_search import get_image_results

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
limiter = Limiter(app, key_func=get_remote_address)


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


@app.route("/image_search")
def image_search():
    return render_template("image_search.html")


@app.route("/image_results", methods=["POST"])
@limiter.limit("50/hour")
def image_results():
    if request.method == "POST":
        if request.form.get("painting"):
            image_type = "живописи"
            which = "painting"
        else:
            image_type = "фотографиям"
            which = "photo"
        n_candidates = request.form.get("n_results", type=int, default=50)
        input_file = request.files["file"]
        results = get_image_results(input_file, session, n=n_candidates, which=which)
    else:
        results = []
        image_type = "..."
    return render_template("image_results.html", result=results, image_type=image_type)


@app.errorhandler(429)
def error429(error):
    error = str(error).split(":")[-1].strip()
    return render_template("error/429.html", error=error)


@app.route("/museums")
def museums():
    museum_list = get_museums(session)
    return render_template("museums.html", data=museum_list)


@app.route("/museum/<int:museum_copuk>")
def museum_one(museum_copuk):
    museum_map, museum = get_museum_map(session, museum_copuk)
    return render_template("museum.html", museum_map=museum_map, museum=museum)


if __name__ == "__main__":
    app.run()
