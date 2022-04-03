# Importing libs
from datetime import datetime
from flask import redirect, render_template, request, session, flash

# Importing .py from app
from app import app, db
from app.models import Announcement, Kindergarten
from app.myhelpers import errormessage,login_required

class thisAnnouncement:
    def __init__(self, title, date, content):
        self.content = content
        self.title = title
        self.date = date

@app.route("/add-announcement", methods=["POST"])
@login_required
def addAnouncement():

    # check if the user has the role parent --> so he is not allowed to create announcements
    if session["role"] == "parent":
        return errormessage("You are not allowed to modify content", 400)

    # get the input of the form
    title = request.form.get("title")
    content = request.form.get("content")

# check if user put in a title and content
    if len(title) == 0 or len(content) == 0:
        print("true")
        return errormessage("You have to put in a title or some content at least", 400)

    # create the announcement
    createannouncement(title, content, db, session["user_id"])

    flash("Your announcement was published")
    return redirect("/home")


@app.route("/delete-announcement", methods=["POST"])
@login_required
def deleteAnnouncement():

    if session["role"] == "parent":
        return errormessage("You are not allowed to modify content", 400)

    # get the date of the announcement which should be deletet
    todeletedate = request.form.get("my-date")

    # delete the entry in the database
    deleteannouncement(db, todeletedate, session["user_id"])
        
    return ("", 204)


def getannouncements(user_id):
    """Gets all the announcements in a list of ouf a database with the user_id"""

    # get the actual kindergarten user
    mykindergarten = Kindergarten.query.filter_by(id=session["user_id"]).first()
    mykindergarten = mykindergarten.kindergartenname


    # create a list of announcements
    announcements = []

    # get all the announcements out of the database from the current user and don't include deleted ones
    dbannouncements = Announcement.query.filter_by(kindergarten_id = user_id).filter(Announcement.deleted.is_(None)).order_by(Announcement.dateAdded.desc()).all()

    for announce in dbannouncements:

        # get everything out of announce
        title = announce.title
        content = announce.content
        date = announce.dateAdded

        announcement = thisAnnouncement(title, date, content)
        # create a new Announcement in our List
        announcements.append(announcement)

    return announcements


def createannouncement(title, content, db, user_id):
    """creates an announcement by the give content title and date and puts it into the database"""

    # put the announcement in the database
    newAnnouncement = Announcement(kindergarten_id = user_id, title = title, content = content)
    db.session.add(newAnnouncement)
    db.session.commit()

    return newAnnouncement


def deleteannouncement(db, date, user_id):
    """sets the delete status in the db of a announcement to deleted"""
    
    # get the current date and time
    deletedate = datetime.now()

    # update the database
    announcement = Announcement.query.filter_by(kindergarten_id = user_id).filter_by(dateAdded = date).first()
    announcement.deleted = deletedate
    db.session.commit()

    return