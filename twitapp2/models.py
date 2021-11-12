'''buile database'''

from flask_sqlalchemy import SQLAlchemy

# Create a DB Object
DB = SQLAlchemy()

# Make a User table by creating a User class


class User(DB.Model):
    '''Creates a User Table with SQLAlchemy'''
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # username column
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return f'[User: {self.name}]'


# Make a Tweet table by creating a Tweet class
class Tweet(DB.Model):
    '''Creates a Tweet Table with SQLAlchemy'''
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    vect = DB.Column(DB.PickleType, nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f'[Tweet: {self.text}]'
