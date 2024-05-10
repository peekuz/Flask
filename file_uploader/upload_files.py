import os
from flask import Flask, flash, request, redirect, render_template

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"mp4"}
CHUNK_SIZE = 1024 * 20

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY= b'_5#y2L"F4Q8z\n\xec]/',
    UPLOAD_FOLDER = UPLOAD_FOLDER
)

def allowed_file(filename):
    """this method will allow only predefined extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_to_mpd(filename):
    """This method will change file name extension to .mpd."""
    original_name = os.path.splitext(filename)[0]
    original_name = original_name + ".mpd"
    return original_name


def create_folder_if_not_exist():
    """This method will create the directory path if it is not exists."""
    path = app.config["UPLOAD_FOLDER"]
    if not os.path.exists(path):
        os.makedirs(path)


def check_file_exist(new_path):
    """This method will check file is already existing or not."""
    if os.path.exists(new_path):
        return True
    return False


def get_file_size(file):
    """This method will return the file size."""
    file.seek(0, 2)
    bytes_left = file.tell()
    file.seek(0, 0)
    return bytes_left

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    """This method will upload files as a chunk."""
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        create_folder_if_not_exist()
        files = request.files.getlist("file")
        for file in files:
            if file and allowed_file(file.filename):
                new_file_name = convert_to_mpd(file.filename)
                new_path = os.path.join("uploads", new_file_name)
                if check_file_exist(new_path):
                    continue
                bytes_left = get_file_size(file)
                with open(new_path, "wb") as upload:
                    chunk_size = CHUNK_SIZE
                    if chunk_size > bytes_left:
                        chunk_size = bytes_left
                    while bytes_left > 0:
                        chunk = file.stream.read(chunk_size)
                        upload.write(chunk)
                        bytes_left -= len(chunk)

        return "<h1>Files Uploaded Successfully.!</h1>"
    return render_template("upload.html")