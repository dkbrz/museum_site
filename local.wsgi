import sys

from museum_app.main_app import app as application

if __name__ == "__main__":
    application.run(port=5000, host='localhost', debug=True)