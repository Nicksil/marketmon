CREATE TABLE invTypes (
    typeid INTEGER PRIMARY KEY NOT NULL,
    typename TEXT
);

CREATE TABLE regions (
    regionid INTEGER PRIMARY KEY NOT NULL,
    regionname TEXT
);

CREATE TABLE constellations (
    regionid INTEGER NOT NULL,
    constellationid INTEGER PRIMARY KEY NOT NULL,
    constellationname TEXT
);

CREATE TABLE solarSystems (
    regionid INTEGER NOT NULL,
    constellationid INTEGER NOT NULL,
    solarsystemid INTEGER PRIMARY KEY NOT NULL,
    solarsystemname TEXT
);
