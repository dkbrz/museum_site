from flask import Flask


def create_app():
    """Create and configure app"""
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = DB
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.secret_key = 'yyjzqy9ffY'
    # db.app = app
    # db.init_app(app)
    # db.create_all()
    return app


app = create_app()


@app.route("/")
@app.route("/index")
def index():
    """Index page"""
    return "ok"


if __name__ == "__main__":
    app.run()
