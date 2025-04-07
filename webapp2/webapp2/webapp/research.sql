PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS researcher;
DROP TABLE IF EXISTS researcher_to_project;
DROP TABLE IF EXISTS note;

CREATE TABLE project(
    pk INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE researcher(
    pk INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    title TEXT
);

CREATE TABLE researcher_to_project(
    pk INTEGER PRIMARY KEY AUTOINCREMENT,
    researcher_pk INTEGER NOT NULL,
    project_pk INTEGER NOT NULL,
    FOREIGN KEY(researcher_pk) REFERENCES researcher(pk),
    FOREIGN KEY(project_pk) REFERENCES project(pk)
);

CREATE TABLE note(
    pk INTEGER PRIMARY KEY AUTOINCREMENT,
    researcher_pk INTEGER NOT NULL,
    project_pk INTEGER NOT NULL,
    content TEXT,
    FOREIGN KEY(researcher_pk) REFERENCES researcher(pk),
    FOREIGN KEY(project_pk) REFERENCES project(pk)
);
