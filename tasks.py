import argparse
import os
import sqlite3

import requests


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--delete", type=int, help="Delete single task using given task ID.")
    parser.add_argument("-l", "--list", action="store_true", help="List all tasks.")

    return parser.parse_args()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREST_BASE_URL = "https://public-crest.eveonline.com/"
DB_NAME_TASKS = "tasks.db"


def get_tasks():
    with sqlite3.connect(os.path.join(BASE_DIR, 'db', DB_NAME_TASKS)) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM tasks""")

        return cursor.fetchall()


def parse_task(task):
    task_id = task[0]
    price = task[1]
    typeid = task[2]
    typename = task[3]
    locationtype = task[4]
    regionid = task[5]
    locationname = task[6]
    ordertype = task[7]
    interest = task[8]

    task_data = {
        "task_id": task_id,
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


def print_task(task):
    print("Task ID: {}".format(task["task_id"]))
    print("Price: {:,.2f}".format(task["price"]))
    print("Type ID: {}".format(task["type_id"]))
    print("Type Name: {}".format(task["type_name"]))
    print("Location Type: {}".format(task["location_type"]))
    print("Region ID: {}".format(task["region_id"]))
    print("Location Name: {}".format(task["location_name"]))
    print("Order Type: {}".format(task["order_type"]))
    print("Interest: {}".format(task["interest"]))
    print()


def delete_task(task_id):
    with sqlite3.connect(os.path.join(BASE_DIR, 'db', DB_NAME_TASKS)) as conn:
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM tasks WHERE id={}""".format(task_id))


def construct_url(region_id, type_id, order_type):
    return "{baseurl}market/{regionid}/orders/{ordertype}/?type={baseurl}types/{typeid}/".format(
        baseurl=CREST_BASE_URL, regionid=region_id, ordertype=order_type, typeid=type_id)


def fetch_price_data(url):
    result = requests.get(url)
    return result.json()


def main():
    args = parse_args()
    tasks = get_tasks()

    if args.list:
        parsed_tasks = []
        for task in tasks:
            parsed_tasks.append(parse_task(task))

        for task in parsed_tasks:
            print_task(task)

    elif args.delete:
        delete_task(args.delete)

    # for task in tasks:
    #     task_data = parse_task(task)
    #     url = construct_url(
    #         task_data['region_id'],
    #         task_data['type_id'],
    #         task_data['order_type'])

    #     price_data = fetch_price_data(url)
    #     prices = sorted([i['price'] for i in price_data['items']])

    #     if task_data['interest'] == "Greater":
    #         if task_data['order_type'] == "buy":
    #             current_price = prices[-1]
    #         else:
    #             current_price = prices[0]

    #         print("{}: Is current market price ({:,.2f}) >= your price ({:,.2f})? {}".format(task_data['type_name'], current_price, task_data['price'], current_price >= task_data['price']))
    #     else:
    #         if task_data['order_type'] == "buy":
    #             current_price = prices[-1]
    #         else:
    #             current_price = prices[0]

    #         print("{}: Is current market price ({:,.2f}) <= your price ({:,.2f})? {}".format(task_data['type_name'], current_price, task_data['price'], current_price <= task_data['price']))

if __name__ == '__main__':
    main()
