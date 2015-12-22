import argparse
import sqlite3
import sys

import requests

"""
CREST market item look-up template:
https://public-crest.eveonline.com/market/10000002/orders/sell/?type=https://public-crest.eveonline.com/types/683/
"""

CREST_BASE_URL = "https://public-crest.eveonline.com/"
DB_NAME = "eve.db"


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


def query_db(query):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()


def construct_url(region_id, type_id, buy_or_sell):
    return "{baseurl}market/{regionid}/orders/{buyorsell}/?type={baseurl}types/{typeid}/".format(
        baseurl=CREST_BASE_URL, regionid=region_id, buyorsell=buy_or_sell, typeid=type_id)


def fetch_price_data(url):
    result = requests.get(url)
    return result.json()


def main(args):
    if args.region:
        region_name = args.region.capitalize()
        location_query_str = """SELECT regionid FROM regions WHERE regionname='{}'""".format(region_name)
        location_query = query_db(location_query_str)
        region_id = location_query[0]
    elif args.solarsystem:
        solarsystem_name = args.solarsystem.capitalize()
        location_query_str = """SELECT regionid FROM solarsystems WHERE solarsystemname='{}'""".format(solarsystem_name)
        location_query = query_db(location_query_str)
        region_id = location_query[0]
    else:
        sys.exit("ERROR: Please include a region or solar system to monitor.")

    if args.buy:
        buy_or_sell = "buy"
    elif args.sell:
        buy_or_sell = "sell"
    else:
        sys.exit("ERROR: Please include either the buy (-b, --buy), or sell (-s, --sell) option.")

    item = args.item
    price = args.price

    type_query_str = """SELECT typeid FROM invTypes WHERE typename LIKE '%{}%'""".format(item)
    type_query = query_db(type_query_str)
    type_id = type_query[0]

    url = construct_url(region_id, type_id, buy_or_sell)

    price_data = fetch_price_data(url)
    prices = sorted([i['price'] for i in price_data['items']])

    if args.buy:
        print("{:,.2f}".format(prices[-1]))
    else:
        print("{:,.2f}".format(prices[0]))

if __name__ == '__main__':
    args = parse_args()
    main(args)
