from datetime import datetime
from app import db
from app.models import Kindergarten, Dish
from flask import session

COMBINEDWEEKDAY = ["lunchmonday", "dessertmonday", "lunchtuesday", "desserttuesday", "lunchwednesday", "dessertwednesday",
                    "lunchthursday", "dessertthursday", "lunchfriday", "dessertfriday"]

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
    
        extract = db.execute("SELECT dish FROM menu WHERE kindergarten_id = ? AND combined = ? AND cw = ? AND deleted IS NULL ORDER BY dateadded DESC LIMIT 1", user_id, combined, cw)
        extract = Dish.query.filter_by(id = session["user_id"]).filter_by(combined = combined).filter_by(cw = cw).filter_by(deleted == None).first()

        # check if there is a dish for that specific day in the database
        if extract == []:

            # there is no dish so we have to fill in a -
            menudict[combined] = "-"

        else:
            # there is a dish so we have to put it into the dict
            menudict[combined] = extract[0]["dish"]

            # check if it is a dessert, so we can make dessert = True
            if "dessert" in combined:
                dessert = True

    return menudict, dessert