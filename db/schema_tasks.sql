CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    price REAL NOT NULL,
    typeid INTEGER NOT NULL,
    typename TEXT NOT NULL,
    locationtype TEXT NOT NULL,
    regionid INTEGER NOT NULL,
    locationname TEXT NOT NULL,
    ordertype TEXT NOT NULL,
    interest TEXT NOT NULL
);
