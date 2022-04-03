# import libs
from datetime import datetime
from flask import redirect, session, request, flash

# import .py from app
from app import app, db
from app.models import Kindergarten, Dish
from app.myhelpers import errormessage, login_required

COMBINEDWEEKDAY = ["lunchmonday", "dessertmonday", "lunchtuesday", "desserttuesday", "lunchwednesday", "dessertwednesday",
                    "lunchthursday", "dessertthursday", "lunchfriday", "dessertfriday"]


@app.route("/home-edit-menu", methods=["GET", "POST"])
@login_required
def homeeditmenu():

    if session["role"] == "parent":
        return errormessage("You are not allowed to modify content", 400)

    # get the actual kindergarten user
    mykindergarten = Kindergarten.query.filter_by(id=session["user_id"]).first()
    mykindergarten = mykindergarten.kindergartenname

    # check first if user came here via POST
    if request.method == "POST":
            
        # get the forms the user filled into a dict
        menudict = {}
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        dessert = False

        # fill in all the data from the form into the dict
        for day in weekdays:
            lunchstring = "lunch" + day
            dessertstring = "dessert" + day
            menudict[lunchstring] = request.form.get(lunchstring)
            menudict[dessertstring] = request.form.get(dessertstring)
        
            # check if the user filled in any data into the dessert column
            if not menudict[dessertstring] == "":
                dessert = True
        
        # now we have to fill the database with the current menu
        editMenu(db, session["user_id"], menudict)
                
        flash("Your menu was added (:")
        return redirect("/home")


def menuview(db, user_id):

    # get the actual kindergarten user
    mykindergarten = Kindergarten.query.filter_by(id = session["user_id"]).first()
    mykindergarten = mykindergarten.kindergartenname
        
    # create the dict, which will contain the data for the actual menu. 
    menudict = {}

    # We also have to secure that the menu is displaying the current calender week
    cw = datetime.now().isocalendar()[1]

    dessert = False

    # extract every dish or dessert from the database which has the cw and is the newest and only show 1 of each category
    for combined in COMBINEDWEEKDAY:
    
        # get the latest dish with the name and user_id for the given combinedweekday
        extract = Dish.query.filter(Dish.deleted.is_(None)).filter_by(kindergarten_id = session["user_id"]).filter_by(combined = combined).filter_by(cw = cw).order_by(Dish.dateAdded.desc()).first()

        # check if there is a dish for that specific day in the database
        if extract == None:

            # there is no dish so we have to fill in a -
            menudict[combined] = "-"

        else:
            # there is a dish so we have to put it into the dict
            menudict[combined] = extract.dish

            # check if it is a dessert, so we can make dessert = True
            if "dessert" in combined:
                dessert = True

    return menudict, dessert


def editMenu(db, user_id, menudict):
    """creates the menu in the database which is given via a dict"""
    
    # get the current date and time, and the cw
    date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    cw = datetime.now().isocalendar()[1]

    # now we have to fill the database with the current menu
    for key in menudict:

        # check first if the user submitted any value in the given form
        if not menudict[key] == "":
            
            if "lunch" not in key:
                menutype = "dessert"
                weekday = key.split("dessert", 1)[1]
            else:
                menutype = "lunch"
                weekday = key.split("lunch", 1)[1]

            # the form has values in it, so it should be put into the database
            newDish = Dish(kindergarten_id = user_id, dish = menudict[key], weekday = weekday, menutype = menutype, combined = key, cw = cw)
            db.session.add(newDish)
            db.session.commit()

    return