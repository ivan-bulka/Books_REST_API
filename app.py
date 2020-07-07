from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import autenticate, identity
from resources.user import UserRegister
from resources.books import Book, BooksList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Ivan'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, autenticate, identity)

api.add_resource(Book, '/book/<string:name>')
api.add_resource(BooksList, '/books')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug = True)