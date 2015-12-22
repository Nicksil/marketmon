import sqlite3
import os

import requests

"""
Given an item, region or solar system, buy or sell, and a price to compare, fetch market data for given location and
compare real-time market data to price point. If market price meets price point's goal, send notification.
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREST_BASE_URL = "https://public-crest.eveonline.com/"
DB_NAME_TASKS = "tasks.db"


def get_tasks():
    with sqlite3.connect(os.path.join(BASE_DIR, 'db', DB_NAME_TASKS)) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM tasks""")

        return cursor.fetchall()


def parse_task(task):
    price = task[1]
    typeid = task[2]
    typename = task[3]
    locationtype = task[4]
    regionid = task[5]
    locationname = task[6]
    ordertype = task[7]
    interest = task[8]

    task_data = {
        "price": price,
        "type_id": typeid,
        "type_name": typename,
        "location_type": locationtype,
        "region_id": regionid,
        "location_name": locationname,
        "order_type": ordertype,
        "interest": interest,
    }

    return task_data


def construct_url(region_id, type_id, order_type):
    return "{baseurl}market/{regionid}/orders/{ordertype}/?type={baseurl}types/{typeid}/".format(
        baseurl=CREST_BASE_URL, regionid=region_id, ordertype=order_type, typeid=type_id)


def fetch_price_data(url):
    result = requests.get(url)
    return result.json()


def main():
    tasks = get_tasks()
    for task in tasks:
        task_data = parse_task(task)
        url = construct_url(
            task_data['region_id'],
            task_data['type_id'],
            task_data['order_type'])

        price_data = fetch_price_data(url)
        prices = sorted([i['price'] for i in price_data['items']])

        if task_data['interest'] == "Greater":
            if task_data['order_type'] == "buy":
                current_price = prices[-1]
            else:
                current_price = prices[0]

            print("Is current market price ({:,.2f}) >= your price ({:,.2f})?\t{}".format(current_price, task_data['price'], current_price >= task_data['price']))
        else:
            if task_data['order_type'] == "buy":
                current_price = prices[-1]
            else:
                current_price = prices[0]

            print("Is current market price ({:,.2f}) <= your price ({:,.2f})?\t{}".format(current_price, task_data['price'], current_price <= task_data['price']))

if __name__ == '__main__':
    main()
