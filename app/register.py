from app import app, db
from flask import request, render_template
from werkzeug.security import generate_password_hash
from app.myhelpers import mailValidater
from app.models import Kindergarten

@app.route("/register", methods=["GET" , "POST"])
def register():

    # check if user came here via post (filling out the register form)
    if request.method == "POST":

        kindergartenname = request.form.get("nameofkindergarten")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
        
        validator = registerNewUser(db, kindergartenname, email, password, confirmpassword)
        
        if validator != "user created":
            return render_template("register_error.html", text = validator)

        # TODO: Return login() here from login.py

        return render_template("register.html")
        
    # user came via GET Request
    else:
        return render_template("register.html")


def registerNewUser(db, kindergartenname, email, password, confirmpassword):
    """this function creates a new Admin in the database and checks everything before
    
    Keyword arguments:
    Return: "Please provide a useful kindergartenname", "Kindergarten allready exists", "Mail is not valid", "Email is allready used", "Passwords do not match", "user created"
    """

    # check if kindergartenname is useful (alphas and spaces)
    if not all(x.isalpha() or x.isspace() for x in kindergartenname):
        return "Please provide a useful kindergartenname"

    # check if a kindergarten exists with the name allready
    kindergarten = Kindergarten.query.filter_by(kindergartenname=kindergartenname).all()
    if (kindergarten != []):
        return "Kindergarten allready exists"

    # check if email is valid
    if not mailValidater(email):
        return "Mail is not valid"

    # check if email is allready used
    emailcheck = Kindergarten.query.filter_by(email=email).all()
    if (emailcheck != []):
        return "Email is allready used"

     # check if paswords match
    if password != confirmpassword:
        return "Passwords do not match"

    # all checks passed, new user can be integrated into database

    # hash password
    userpassword = generate_password_hash(password)

    # put new user in database
    newKindergarten = Kindergarten(kindergartenname = kindergartenname, email = email, password = userpassword)
    db.session.add(newKindergarten)
    db.session.commit()

    return "user created"