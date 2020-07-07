from db import db

class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    author = db.Column(db.String(80))
    rating = db.Column(db.Float(precision=2))

    def __init__(self, name, price, author, rating):
        self.name = name
        self.price = price
        self.author = author
        self.rating = rating

    def json(self):
        return {'name': self.name, 'price': self.price, 'author': self.author, 'rating': self.rating}
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()    


