import sqlite3

DB_NAME = "eve.db"


def query_db(query):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query)

        return cursor.fetchone()


def get_type_data(type_name):
    query_str = """SELECT * FROM invTypes WHERE typename LIKE '%{}%'""".format(type_name)
    query_result = query_db(query_str)

    return query_result


def get_type_id(type_name):
    query_str = """SELECT typeid FROM invTypes WHERE typename LIKE '%{}%'""".format(type_name)
    query_result = query_db(query_str)

    return query_result[0]


def get_region_data(region_name):
    query_str = """SELECT * FROM regions WHERE regionname LIKE '%{}%'""".format(region_name)
    query_result = query_db(query_str)

    return query_result


def get_region_id(region_name):
    query_str = """SELECT regionid FROM regions WHERE regionname LIKE '%{}%'""".format(region_name)
    query_result = query_db(query_str)

    return query_result[0]


def get_solarsystem_data(solarsystem_name):
    query_str = """SELECT * FROM solarsystems WHERE solarsystemname LIKE '%{}%'""".format(solarsystem_name)
    query_result = query_db(query_str)

    return query_result


def get_solarsystem_id(solarsystem_name):
    query_str = """SELECT solarsystemid FROM solarsystems WHERE solarsystemname LIKE '%{}%'""".format(solarsystem_name)
    query_result = query_db(query_str)

    return query_result[0]
