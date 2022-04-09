# import libs
from secrets import token_hex
from werkzeug.security import generate_password_hash
from flask import session, render_template, request

# import .py from app
from app import app, db
from app.models import Parent
from app.login import login
from app.myhelpers import login_required, errormessage, mailValidater


@app.route("/invite-parents", methods=["POST", "GET"])
@login_required
def inviteParents():

    if session["role"] == "parent":
        return errormessage("You are not allowed to modify content", 400)

    if request.method == "GET":
        return render_template("parents/invite_parents.html")

    else:
        parentsEmail = request.form.get("email")

        if validParents(session["user_id"], parentsEmail) == "email wrong":
            return errormessage("You have to type in a real email adress", 400)

        if validParents(session["user_id"], parentsEmail) == "allready invited":
            existingToken = Parent.query.filter_by(email = parentsEmail).filter_by(kindergarten_id = session["user_id"]).first().token
            return render_template("parents/invite_parents_key.html", key = "This Key was allready generated. It is: " + existingToken)

        if validParents(session["user_id"], parentsEmail) == "invite valid":
            newtoken = createParents(session["user_id"], parentsEmail)
            return render_template("parents/invite_parents_key.html", key = "The new generated key is: " + newtoken)

    return errormessage("Something went wrong", 400)


@app.route("/invitation", methods=["POST", "GET"])
def registerParents():

    if request.method == "GET":
        return render_template("parents/invitation.html")

    email = request.form.get("email")
    token = request.form.get("token")
    password = request.form.get("password")
    confirmpassword = request.form.get("confirmpassword")

    validator = parentsAcceptInvite(email, token, password, confirmpassword)

    if validator == "parents are not invited":
        return render_template("parents/invitation_error.html", text = "You are not invited from the kindergarten. You should ask the staff for an invite")

    if validator == "passwords missmatch":
        return render_template("parents/invitation_error.html", text = "Passwords do not match")
    
    if validator == "token wrong":
        return render_template("parents/invitation_error.html", text = "Token is wrong")

    elif validator == "parents registered":
        return login()

    else:
        return render_template("parents/invitation_error.html", text = "Parents with this email and token allready are registered")


def createToken():
    """creates a random token out of 12 chars and makes sure that it is unique"""
    newtoken = token_hex(12)

    # make sure that the token is not allready generated
    while (newtoken in Parent.query.all()):
        newtoken = token_hex(12)

    return newtoken


def createParents(kindergarten_id, email):
    """creates a entry in the database for the parents"""

    # create a token
    newtoken = createToken()
   
    # put the parents in the database
    newParents = Parent(kindergarten_id = session["user_id"], email = email, token = newtoken)
    db.session.add(newParents)
    db.session.commit()

    # return the new created token
    return newtoken


def validParents(kindergarten_id, email):
    """looks into the database and checks if the parents can be invited
    Keyword arguments:
    Return: function can return "invite valid", "email wrong", "parents allready registered" and "allready invited" 
    """

    # check first if the email is valid
    if not mailValidater(email):
        return "email wrong"

    # check if the invite is valid (noone invited for this kindergarten with this email)
    if Parent.query.filter_by(kindergarten_id = kindergarten_id).filter_by(email = email).first() == None:
        return "invite valid"
    
    # check if parents are allready registered as parents for this kindergarten
    if not Parent.query.filter_by(kindergarten_id = kindergarten_id).filter_by(email = email).filter(Parent.password.isnot(None)).first() == None:
        return "parents allready registered"

    # otherwise the parents can only be allready invited
    return "allready invited"


def parentsAcceptInvite(email, token, password, confirmpassword):
    """takes input from parents after getting invited and puts them into the database
    
    Keyword arguments:
    Return: returns either "parents registered", "parents are not invited", "token wrong", "passwords missmatch" or "parents not registered"
    """

    # check if password and confirmpassword are equal
    if password != confirmpassword:
        return "passwords missmatch"

    # check if those parents are invited
    if Parent.query.filter_by(email = email).first == None:
        return "parents are not invited"
    
    # check if the token is right
    if token != Parent.query.filter_by(email = email).first().token:
        return "token wrong"

    # check if those parents are allready registered
    if Parent.query.filter_by(email = email).filter(Parent.password.isnot(None)).first() == None:
        
        # hash the password
        parentspassword = generate_password_hash(password)

        # put those parents into the database
        newParent = Parent.query.filter_by(email = email).first()
        newParent.password = parentspassword
        db.session.commit()

        return "parents registered"

    else:
        return "parents not registered"
