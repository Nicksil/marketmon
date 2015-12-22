import csv
import sqlite3

db_filename = 'eve.db'
scema_filename = 'schema.sql'

invtypes = []
regions = []
constellations = []
solarsystems = []

with sqlite3.connect(db_filename) as conn:
    with open(scema_filename, 'rt') as f:
        schema = f.read()
    conn.executescript(schema)

    with open('invTypes.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            invtypes.append((int(row[0]), row[1]))

    conn.executemany('INSERT INTO invTypes VALUES (?, ?)', invtypes)

    with open('mapRegions.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            regions.append((int(row[0]), row[1]))

    conn.executemany('INSERT INTO regions VALUES (?, ?)', regions)

    with open('mapConstellations.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            constellations.append((int(row[0]), int(row[1]), row[2]))

    conn.executemany('INSERT INTO constellations VALUES (?, ?, ?)', constellations)

    with open('mapSolarSystems.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            solarsystems.append((int(row[0]), int(row[1]), int(row[2]), row[3]))

    conn.executemany('INSERT INTO solarsystems VALUES (?, ?, ?, ?)', solarsystems)
