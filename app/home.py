from app import app, db
from flask import session, render_template
from app.models import Kindergarten, Dish, Announcement, Upload
from app.menu import menuview
from app.myhelpers import login_required

@app.route("/", methods=["GET"])
def index():

    # check first if the visitor is logged in
    if not "user_id" in session:
        return render_template("login/login.html")
    
    return home()


@app.route("/home", methods=["GET"])
@login_required
def home():

    # get the actual kindergarten user
    mykindergarten = Kindergarten.query.filter_by(id=session["user_id"]).first()
    mykindergarten = mykindergarten.kindergartenname

    # Part 1: Create the menuview
    mymenuview = menuview(db, session["user_id"],)

    # Part 2: Create the announcementview
    # announcements = getannouncements(db, session["user_id"])

    # Part 3: Create the fileview
    # files = fileview(db, session["user_id"])

    menudict = mymenuview[0]
    dessert = mymenuview[1]
        
    # return render_template("home/home.html", nameofkindergarten = mykindergarten["kindergartenname"], menudict = menudict, dessert = dessert, announcements = announcements, files = files, role = session["role"])
    return render_template("home/home.html", nameofkindergarten = mykindergarten, menudict = menudict, dessert = dessert, role = session["role"])

