# Importing libs
from datetime import datetime
from flask import redirect, render_template, request, session, flash, url_for, send_from_directory
from genericpath import isfile
from importlib.resources import path
from operator import truediv
import os
from werkzeug.utils import secure_filename

# Importing .py from app
from app import app, db
from app.models import Upload
from app.myhelpers import errormessage,login_required

# Allowed Filenames
ALLOWED_EXTENSIONS = {'pdf'}

@app.route("/upload-file", methods=["POST"])
@login_required
def upload_File():

    if session["role"] == "parent":
        return errormessage("You are not allowed to modify content", 400)

    if not request.method == "POST":
        return errormessage("You should not came her via that way", 400)

    file = request.files

    validator = isValid(file, db, session["user_id"])
    if not validator[0]:
        return errormessage(validator[1], 400)

    uploadFile(session["user_id"], file, app, db)
    flash("File was successfully uploaded to the server (:")
    return redirect("/home")


@app.route("/download/<path:filename>")
@login_required
def downloadFile(filename):

    if isFileavailabe(filename, session["user_id"]):
        path = os.path.join("upload", str(session["user_id"]))
        print(path)
        return send_from_directory(path, filename, as_attachment=True)

    else:
        return errormessage("Something went wrong", 400)


@app.route("/delete", methods=["POST", "GET"])
@login_required
def deleteUpload():

    if session["role"] == "parent":
        return errormessage("You are not allowed to modify content", 400)
    
    # check for method
    if request.method =="GET":
        return errormessage("You should not came her via that way", 400)

    # get the filename
    filename = request.form["filenamebutton"]
    print(filename)

    # check first if file is deleteable
    if fileDeleteable(filename, session["user_id"]):
        deleteFile(filename, session["user_id"])
        flash("Your file was succesufully deleted")
        redirect ("/home")

    return errormessage("Something went wrong", 400)
    

def uploadFile(user_id, file, app):

    UPLOAD_FOLDER = "/upload/" + str(user_id) + "/"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    file = request.files['file']

    # make sure that the filename is secure (cut of unwanted parts)
    filename = secure_filename(file.filename)

    # create the parent folder
    parent_dir = "upload"
    path = os.path.join(parent_dir, str(user_id))

    # check if the folder exists, if not create it
    if not os.path.isdir(path):
        os.makedirs(path)

    # save the file
    file.save(os.path.join(path, filename))

    # insert the upload into the database
    upload = Upload(kindergarten_id = user_id, filename = filename)

    return "File Uploaded"

def isValid(file, user_id):
    """checks if a user has submitted a valid file (in case of filename, file itself and db)"""

    if 'file' not in file:
        message = "You have to select a file"
        return False, message

    file = request.files['file']

    # User has not selected a file
    if file.filename == "":
        message = "You have to select a file"
        return False, message

    # check if the file has a file and checks if the file is an allowed file
    if not file or not allowed_file(file.filename):
        message = "Something went wrong here, either you did not submit a file or you didnt submit an .pdf"
        return False, message

    # make sure there is not a file allready with that filename
    if not db.execute("SELECT * FROM uploads WHERE kindergarten_id = ? AND filename = ? AND deleted IS NULL", user_id, file.filename) == []:
        message = "There is allready a file with that name uploaded, delete it first or upload a file with a diffrent name"
        return False, message
    
    return True, ""

def fileview(db, user_id):
    """this function gets all the files a user has"""

    files = db.execute("SELECT * FROM uploads where kindergarten_id = ? AND deleted IS NULL", user_id)

    return files

def getFile(user_id, filename, app):
    """this function serves a file from the files"""

    # create the parent folder
    parent_dir = "upload"
    path = os.path.join(parent_dir, str(user_id))

    return send_from_directory(app.config("path"), filename)

def allowed_file(filename):
    """Checks if a filename is an allowed file"""
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def deleteFile(db, filename, user_id):
    """sets the delete status for a file in the database"""

    # create the current date
    date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    db.execute("UPDATE uploads SET deleted = ? WHERE filename = ? AND kindergarten_id = ?", date, filename, user_id)

def fileDeleteable(db, filename, user_id):
    """checks if a file is deleteable"""

    if not db.execute("SELECT * FROM uploads WHERE filename = ? AND kindergarten_id = ? and deleted IS NULL", filename, user_id) == []:
        return True
    
    else:
        return False
        
def isFileavailabe(db, filename, user_id):
    """checks if a File is there to be downloaded"""
    
    if not db.execute("SELECT * FROM uploads WHERE filename = ? AND kindergarten_id = ? and deleted IS NULL", filename, user_id) == []:
        return True
    
    else:
        return False

 