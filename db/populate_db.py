import csv
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db_filename_eve = 'eve.db'
db_filename_tasks = 'tasks.db'
schema_filename_eve = 'schema_eve.sql'
schema_filename_tasks = 'schema_tasks.sql'

invtypes = []
regions = []
constellations = []
solarsystems = []

with sqlite3.connect(os.path.join(BASE_DIR, 'db', db_filename_eve)) as conn:
    with open(os.path.join(BASE_DIR, 'db', schema_filename_eve), 'rt') as f:
        schema = f.read()
    conn.executescript(schema)

    with open(os.path.join(BASE_DIR, 'data', 'invTypes.csv')) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            invtypes.append((int(row[0]), row[1].strip()))

    conn.executemany('INSERT INTO invTypes VALUES (?, ?)', invtypes)

    with open(os.path.join(BASE_DIR, 'data', 'mapRegions.csv')) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            regions.append((int(row[0]), row[1]))

    conn.executemany('INSERT INTO regions VALUES (?, ?)', regions)

    with open(os.path.join(BASE_DIR, 'data', 'mapConstellations.csv')) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            constellations.append((int(row[0]), int(row[1]), row[2]))

    conn.executemany('INSERT INTO constellations VALUES (?, ?, ?)', constellations)

    with open(os.path.join(BASE_DIR, 'data', 'mapSolarSystems.csv')) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            solarsystems.append((int(row[0]), int(row[1]), int(row[2]), row[3]))

    conn.executemany('INSERT INTO solarsystems VALUES (?, ?, ?, ?)', solarsystems)

with sqlite3.connect(os.path.join(BASE_DIR, 'db', db_filename_tasks)) as conn:
    with open(os.path.join(BASE_DIR, 'db', schema_filename_tasks), 'rt') as f:
        schema = f.read()
    conn.executescript(schema)
