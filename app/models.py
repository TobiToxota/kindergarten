from app import db
from datetime import datetime

class Kindergarten(db.Model):
    """representing: id, kindergartenname, email and hashed password"""
    
    id = db.Column(db.Integer, primary_key=True)
    kindergartenname = db.Column(db.String(120), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    dishs = db.relationship('Dish', backref='author', lazy=True)
    announcements = db.relationship('Announcement', backref='author', lazy=True)
    uploads = db.relationship('Upload', backref='uploader', lazy=True)
    parents = db.relationship('Parent', backref='kindergarten', lazy=True)

    def __repr__(self):
        return f"Kindergarten('{self.kindergartenname}', '{self.email}')"


class Dish(db.Model):
    """representing: id, kindergarten_id, dish, weekday, menutype, combined,
    dateadded, cw and deleted"""

    id = db.Column(db.Integer, primary_key=True)
    kindergarten_id = db.Column(db.Integer, db.ForeignKey('kindergarten.id'), nullable = False)
    dish = db.Column(db.String(120), nullable = False)
    weekday = db.Column(db.String(20), nullable = False)
    menutype = db.Column(db.String(20), nullable = False)
    combined = db.Column(db.String(30), nullable = False)
    dateAdded = db.Column(db.DateTime, nullable = False, default = datetime.now)
    cw = db.Column(db.Integer, nullable = False)
    deleted = db.Column(db.String(20), nullable = True)

    def __repr__(self):
        return f"Dish('{self.dish}', '{self.weekday}', '{self.menutype}')"


class Announcement(db.Model):
    """representing: id, kindergarten_id, title, content, dateadded, deleted"""

    id = db.Column(db.Integer, primary_key=True)
    kindergarten_id = db.Column(db.Integer, db.ForeignKey('kindergarten.id'), nullable = False)
    title = db.Column(db.String(120), nullable = False)
    content = db.Column(db.Text, nullable = False)
    dateAdded = db.Column(db.DateTime, nullable = False, default = datetime.now)
    deleted = db.Column(db.DateTime)

    def __repr__(self):
        return f"Announcement('{self.title}', '{self.dateAdded}')"

class Upload(db.Model):
    """representing: id, kindergarten_id, filename, dateadded, deleted"""
    
    id = db.Column(db.Integer, primary_key=True)
    kindergarten_id = db.Column(db.Integer, db.ForeignKey('kindergarten.id'), nullable = False)
    filename = db.Column(db.String(200), nullable = False)
    dateAdded = db.Column(db.DateTime, nullable = False, default = datetime.now)
    deleted = db.Column(db.DateTime)

    def __repr__(self):
        return f"Upload('{self.filename}', '{self.dateAdded}')"

class Parent(db.Model):
    """representing: id, kindergarten_id, email, token, password"""
    
    id = db.Column(db.Integer, primary_key=True)
    kindergarten_id = db.Column(db.Integer, db.ForeignKey('kindergarten.id'), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    token = db.Column(db.String(12), unique = True, nullable = False)
    password = db.Column(db.String(100))
    access = db.Column(db.String(20))

    def __repr__(self):
        return f"Parent('{self.email}', '{self.kindergarten_id}')"


    