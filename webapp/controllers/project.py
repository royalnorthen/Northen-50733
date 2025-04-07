from flask import Blueprint, render_template, request
from .. import dbtools as db

project_page = Blueprint("project_page", __name__)

@project_page.route('/projects/<project>.html', methods=["GET", "POST"])
def index(project):

    form = request.form

    if "note" in form:
        note = form["note"]
        researcher = form["researcher"]
        db.addNote(researcher, project, note)

    notes = db.getNotes(project)

    template = {"notes": notes,
                "project": project}

    return render_template("project.html", **template)
