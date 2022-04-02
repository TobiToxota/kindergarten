from app import app
from flask import session, request, render_template, redirect
from app.myhelpers import mailValidater
from werkzeug.security import check_password_hash

@app.route("/login", methods=["POST", "GET"])
def login():

    # Forget any user_id
    session.clear()

    # Check if user came here via POST
    if request.method == "POST":

        # Get the user data from the form
        email = request.form.get("email")
        password = request.form.get("password")
        
        # check everything and log user in
        validator = loginUser(db, email, password, session)

        # check if login workend and if not throw message to user
        if validator != "User successfully logged in":
            return render_template("login_error.html", text = validator)

        # redirect user to the home page
        return redirect("/home")

    # user reachead route via get
    else:
        return render_template("login.html")

def loginUser(db, email, password, session):
    """Logs a user in
    
    Keyword arguments:
    Return: "Input is missing", "Email is not valid", "There is no user with that mail", "User successfully logged in"
    """

    # check if user filled in data
    if email == "" or password == "":
        return "Input is missing"

    # check if email is valid 
    if not mailValidater(email):
        return "Email is not valid"

    # check database for Admins (kindergartens) and for Parents
    checkAdmins = db.execute("SELECT * FROM kindergartens WHERE email = ?", email)
    checkParents = db.execute("SELECT * FROM parents WHERE email = ?", email)

    # check if it is an admin or a parent
    if checkAdmins != [] and checkParents == []:

        # it is an kindergarten
        role = "admin"
        check = checkAdmins

    elif checkParents != [] and checkAdmins == []:
        
        # it is a parent
        role = "parent"
        check = checkParents

    # otherwise there is no user with that mail
    else:
        return "There is no user with that mail"

    # check if the password is correct
    passwordcheck = check_password_hash(check[0]["password"], password)
    if not passwordcheck:
        return "Password is not correct"

    # all checks passed

    # to keep the user logged in, we have to create a session depending on the role
    if role == "admin":
        session["user_id"] = check[0]["id"]
        session["role"] = role

    if role == "parent":
        session["user_id"] = check[0]["kindergarten_id"]
        session["role"] = role

    return "User successfully logged in"