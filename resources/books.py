import sqlite3
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.books import BookModel


class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required=True,
        help = 'This field can not be blank')

    parser.add_argument('author',
        type = str,
        required=True,
        help = 'This field can not be blank')

    parser.add_argument('rating',
        type = float,
        required=False,
        help = 'This field is not mandatory')

    @jwt_required()
    def get(self, name):
        book = BookModel.find_by_name(name)
        if book:
            return book.json()
        return {'message': 'Item not found'}
    
    # @jwt_required()
    def post(self, name):
        if  BookModel.find_by_name(name): 
            return {'message': 'Item already exisit'}, 400
        data = Book.parser.parse_args()
        book = BookModel(name, data['price'], data['author'], data['rating'])
        try: 
            book.save_to_db()
        except:
            return {'message': 'An error occured when inserting the item'} 
        return book.json(), 201

    # @jwt_required()
    def delete(self, name):
        book = BookModel.find_by_name(name)
        if book:
            book.delete_from_db()
        return {'message': 'item deleted'}
    
    # @jwt_required()
    def put(self, name):
        data = Book.parser.parse_args()
        book = BookModel.find_by_name(name)
        if book is None:
            book = BookModel(name, data['price'], data['author'], data['rating'])
        else: 
            book.price = data['price']
            book.author = data['author']
            book.rating = data['rating']
        book.save_to_db()
        return book.json()
        
class BooksList(Resource):
    # @jwt_required()
    def get(self):
        return {'books': [item.json() for item in BookModel.query.all()]}