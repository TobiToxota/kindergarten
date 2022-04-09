# Importing libs
from datetime import datetime
from flask import redirect, render_template, request, session, flash, url_for, send_from_directory
from genericpath import isfile
from importlib.resources import path
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

    validator = isValid(file, session["user_id"])
    if not validator[0]:
        return errormessage(validator[1], 400)

    uploadFile(session["user_id"], file)
    flash("File was successfully uploaded to the server (:")
    return redirect("/home")


@app.route("/download/<path:filename>")
@login_required
def downloadFile(filename):

    if isFileavailabe(filename, session["user_id"]):
        path = os.path.join("upload", str(session["user_id"]))
        print(path)
        return send_from_directory(path, filename)

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
        return redirect ("/home")

    return errormessage("Something went wrong", 400)
    

def uploadFile(user_id, file):

    UPLOAD_FOLDER = "app/upload/" + str(user_id) + "/"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    file = request.files['file']

    # make sure that the filename is secure (cut of unwanted parts)
    filename = secure_filename(file.filename)

    # create the parent folder
    parent_dir = "app/upload"
    path = os.path.join(parent_dir, str(user_id))

    # check if the folder exists, if not create it
    if not os.path.isdir(path):
        os.makedirs(path)

    # save the file
    file.save(os.path.join(path, filename))

    # insert the upload into the database
    upload = Upload(kindergarten_id = user_id, filename = filename)
    db.session.add(upload)
    db.session.commit()


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
    print(Upload.query.filter_by(filename= file.filename).first())
    if not Upload.query.filter_by(filename= file.filename).first() == None:
        message = "There is allready a file with that name uploaded, delete it first or upload a file with a diffrent name"
        return False, message
    
    return True, ""

def fileview(db, user_id):
    """this function gets all the files a user has"""

    files = Upload.query.filter_by(kindergarten_id = user_id).filter(Upload.deleted.is_(None)).all()
    print(files)

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


def deleteFile(filename, user_id):
    """sets the delete status for a file in the database"""

    # create the current date
    date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    # delete file
    filetodelete = Upload.query.filter_by(filename = filename).filter_by(kindergarten_id = user_id).first()
    filetodelete.deleted = datetime.now()
    db.session.commit()

    return


def fileDeleteable(filename, user_id):
    """checks if a file is deleteable"""

    if not Upload.query.filter_by(filename = filename, kindergarten_id = user_id).filter(Upload.deleted.is_(None)).first == None:
        
        return True
    
    else:
        return False
        
def isFileavailabe(filename, user_id):
    """checks if a File is there to be downloaded"""
    
    if not Upload.query.filter_by(filename = filename, kindergarten_id = user_id).filter(Upload.deleted.is_(None)).first == None:
        return True
    
    else:
        return False

 