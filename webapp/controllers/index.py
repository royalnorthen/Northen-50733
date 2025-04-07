from flask import Blueprint, render_template, request
from .. import dbtools as db

index_page = Blueprint("index_page", __name__)

@index_page.route('/', methods=["GET", "POST"])
def index():

    form = request.form

    if "project" in form:
        new_name = form["project"]
        db.addProject(new_name)

    projects = db.getProjects()

    template = {"projects": projects}

    return render_template("index.html", **template)
