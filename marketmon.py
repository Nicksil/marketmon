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

    args = parser.parse_args()

    return args


def save_to_db(data):
    with sqlite3.connect(DB_NAME_TASKS) as conn:
        conn.execute('INSERT INTO tasks (price, typeid, typename, locationtype, regionid, locationname) VALUES (?, ?, ?, ?, ?, ?)', data)


def construct_url(region_id, type_id, buy_or_sell):
    return "{baseurl}market/{regionid}/orders/{buyorsell}/?type={baseurl}types/{typeid}/".format(
        baseurl=CREST_BASE_URL, regionid=region_id, buyorsell=buy_or_sell, typeid=type_id)


def fetch_price_data(url):
    result = requests.get(url)
    return result.json()


def save_task(data):
    save_to_db(data)


def main(args):
    if args.region:
        location_type = "Region"
        region_name = args.region
        region_id, location_name = get_region_data(region_name)
    elif args.solarsystem:
        location_type = "SolarSystem"
        solarsystem_name = args.solarsystem
        solarsystem_data = get_solarsystem_data(solarsystem_name)
        region_id = solarsystem_data[0]
        location_name = solarsystem_data[3]
    else:
        sys.exit("ERROR: Please include a region or solar system to monitor.")

    if args.buy:
        buy_or_sell = "buy"
    elif args.sell:
        buy_or_sell = "sell"
    else:
        sys.exit("ERROR: Please include either the buy (-b, --buy), or sell (-s, --sell) option.")

    type_name = args.item
    price = args.price

    type_id, type_name = get_type_data(type_name)

    url = construct_url(region_id, type_id, buy_or_sell)

    price_data = fetch_price_data(url)
    prices = sorted([i['price'] for i in price_data['items']])

    data = [price, type_id, type_name, location_type, region_id, location_name]
    save_task(data)

    # if args.buy:
    #     print("{:,.2f}".format(prices[-1]))
    # else:
    #     print("{:,.2f}".format(prices[0]))

if __name__ == '__main__':
    args = parse_args()
    main(args)
