import re
from functools import wraps
from flask import request, redirect, url_for, session, render_template


# https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/
def mailValidater(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email):
        return True
    else:
        return False

# https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def errormessage(message, code=400):
    """give the user an error message"""

    return render_template("error.html", message=message), 400