import argparse
import sqlite3
import sys

import requests

from eve import get_region_data
from eve import get_solarsystem_data
from eve import get_type_data

"""
CREST market item look-up template:
https://public-crest.eveonline.com/market/10000002/orders/sell/?type=https://public-crest.eveonline.com/types/683/
"""

CREST_BASE_URL = "https://public-crest.eveonline.com/"
DB_NAME_EVE = "eve.db"
DB_NAME_TASKS = "tasks.db"


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--item", help="Which item, or market type, to monitor.")
    parser.add_argument("-r", "--region", help="The region in which you want price data to be monitored.")
    parser.add_argument("-y", "--solarsystem", help="The solar system in which you want price data to be monitored.")
    parser.add_argument("-b", "--buy", action="store_true", help="Choose to monitor buy prices.")
    parser.add_argument("-s", "--sell", action="store_true", help="Choose to monitor sell prices.")
    parser.add_argument("-p", "--price", type=float, help="The price point you wish to compare to monitored data.")
    parser.add_argument("-g", "--greater", action="store_true", help="Notify when given price is GREATER than or EQUAL real-time market price.")
    parser.add_argument("-l", "--lesser", action="store_true", help="Notify when given price is LESS than or EQUAL real-time market price.")

    return parser.parse_args()


def construct_url(region_id, type_id, buy_or_sell):
    return "{baseurl}market/{regionid}/orders/{buyorsell}/?type={baseurl}types/{typeid}/".format(
        baseurl=CREST_BASE_URL, regionid=region_id, buyorsell=buy_or_sell, typeid=type_id)


def fetch_price_data(url):
    result = requests.get(url)
    return result.json()


def save_task(data):
    with sqlite3.connect(DB_NAME_TASKS) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (price, typeid, typename, locationtype, regionid, locationname, ordertype, interest) \
                        VALUES (:price, :typeid, :typename, :locationtype, :regionid, :locationname, :ordertype, :interest)', data)


def prepare_task(args):
    price = args.price

    type_name = args.item
    type_id, type_name = get_type_data(type_name)

    if args.region:
        location_type = "Region"
        region_name = args.region
        region_id, location_name = get_region_data(region_name)
    elif args.solarsystem:
        location_type = "SolarSystem"
        solarsystem_name = args.solarsystem
        region_id, location_name = get_solarsystem_data(solarsystem_name)
    else:
        sys.exit("ERROR: Please include a region or solar system to monitor.")

    if args.buy:
        order_type = "Buy"
    elif args.sell:
        order_type = "Sell"
    else:
        sys.exit("ERROR: Please include either the buy (-b, --buy), or sell (-s, --sell) option.")

    if args.greater:
        interest = "Greater"
    elif args.lesser:
        interest = "Lesser"
    else:
        sys.exit("Error: Please include GREATER (-g, --greater) or LESSER (-l, --lesser) interest option.")

    task_data = {
        "price": price,
        "typeid": type_id,
        "typename": type_name,
        "locationtype": location_type,
        "regionid": region_id,
        "locationname": location_name,
        "ordertype": order_type,
        "interest": interest,
    }

    return task_data


def narrow_to_solarsystem(data, solarsystem):
    results = []
    for item in data['items']:
        if solarsystem.lower() in item['location']['name'].lower():
            results.append(item)

    return results


def main():
    args = parse_args()
    task_data = prepare_task(args)
    save_task(task_data)

if __name__ == '__main__':
    main()
