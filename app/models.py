from app import db

class Kindergarten(db.Model):
    id = db.Column(db.Integer, primary_key=True)