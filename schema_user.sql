CREATE TABLE invTypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    typeid INTEGER NOT NULL,
    typename TEXT NOT NULL,
    locationtype TEXT NOT NULL,
    locationid INTEGER NOT NULL,
    locationname TEXT NOT NULL
);
