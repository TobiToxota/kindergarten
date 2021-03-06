CREATE TABLE kindergarten (id INTEGER PRIMARY KEY, kindergartenname TEXT NOT NULL,
email TEXT NOT NULL, password TEXT NOT NULL);

CREATE TABLE menu (id INTEGER PRIMARY KEY, kindergarten_id INTEGER NOT NULL, dish TEXT NOT NULL,
weekday TEXT NOT NULL, menutype TEXT NOT NULL, combined TEXT NOT NULL, dateadded TEXT NOT NULL,
cw TEXT NOT NULL, deleted TEXT);

CREATE TABLE announcements (id INTEGER PRIMARY KEY, kindergarten_id INTEGER NOT NULL, 
title TEXT NOT NULL, dateadded TEXT NOT NULL, content TEXT NOT NULL, deleted TEXT);

CREATE TABLE uploads (id INTEGER PRIMARY KEY, kindergarten_id INTEGER NOT NULL,
filename TEXT NOT NULL, dateadded TEXT NOT NULL, deleted TEXT);

CREATE TABLE parents (id INTEGER PRIMARY KEY, kindergarten_id INTEGER NOT NULL, email TEXT NOT NULL,
token TEXT NOT NULL, password TEXT, access TEXT);