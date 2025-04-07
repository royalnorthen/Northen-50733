import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('research.sql') as f:
        db.cursor().executescript(f.read().decode('utf8'))
    
    curr = db.execute("SELECT * from sqlite_master")
    print(curr.fetchall())


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def getProjects():
    db = get_db()
    cur = db.execute(
        """SELECT *
              FROM project
          ORDER BY pk DESC""",
    )
    return cur.fetchall()


def addProject(name):
    db = get_db()
    db.execute(
        """INSERT INTO project (name)
        VALUES (?)
        """, [name]
    )
    db.commit()


def getResearchers():
    db = get_db()
    cur = db.execute(
        """SELECT *
              FROM researcher
          ORDER BY pk DESC""",
    )
    return cur.fetchall()


def getResearcher(name):
    db = get_db()
    cur = db.execute(
        f"""SELECT *
              FROM researcher
          where name = '{name}';""",
    )
    return cur.fetchall()


def getProject(name):
    db = get_db()
    cur = db.execute(
        f"""SELECT *
              FROM project
          where name = '{name}';""",
    )
    return cur.fetchall()


def addResearcher(name):
    db = get_db()
    db.execute(
        """INSERT INTO researcher (name)
        VALUES (?)
        """, [name]
    )
    db.commit()


def addResearcherToProject(researcher, project):
    researcher_db = getResearcher(researcher)
    exists = len(researcher_db) > 0
    if not exists:
        addResearcher(researcher)
        researcher_db = getResearcher(researcher)
    researcher = researcher_db[0]
    project = getProject(project)[0]
    db = get_db()
    db.execute("""INSERT INTO researcher_to_project 
               (researcher_pk, project_pk) 
               VALUES (?, ?)""",
               [researcher["pk"], project["pk"]]
              )
    db.commit()


def addNote(researcher, project, note):
    db = get_db()
    cur = db.execute(
        f"""SELECT * from researcher_to_project as r2p
             JOIN project AS p ON r2p.project_pk = p.pk
             JOIN researcher AS r ON r.pk = r2p.researcher_pk
             WHERE p.name = '{project}' and r.name = '{researcher}';""",
    )
    if len(cur.fetchall()) == 0:
        addResearcherToProject(researcher, project)
    p = getProject(project)[0]
    r = getResearcher(researcher)[0]
    db.execute(
        """INSERT INTO note 
        (researcher_pk, project_pk, content)
         VALUES (?, ?, ?)
        """,  [r["pk"], p["pk"], note]
    )
    db.commit()


def getNotes(project):
    db = get_db()
    cur = db.execute(
        f"""SELECT c.name as researcher, n.content
              FROM note as n
              JOIN researcher as c on c.pk = n.researcher_pk
              JOIN project as p on p.pk = n.project_pk
          WHERE p.name = '{project}';""",
    )
    return cur.fetchall()
