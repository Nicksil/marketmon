import argparse
import sqlite3
import sys

import requests

"""
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
        return cursor.fetchall()


def construct_url(region_id, type_id):
    return "https://public-crest.eveonline.com/market/{regionid}/orders/sell/?type=https://public-crest.eveonline.com/types/{typeid}/".format(regionid=region_id, typeid=type_id)


def fetch_price_data(url):
    result = requests.get(url)
    return result.json()


def main(args):
    item = args.item
    price = args.price

    if args.region:
        location = args.region.capitalize()
    elif args.solarsystem:
        location = args.solarsystem.capitalize()
    else:
        sys.exit("ERROR: Please include a region or solar system to monitor.")
    # region_id_query = """SELECT regionid FROM solarsystems WHERE solarsystemname LIKE '%{}%'""".format(location)
    # region_id = query_db(region_id_query)[0][0]
    # type_id_query = """SELECT typeid FROM invTypes WHERE typename LIKE '%{}%'""".format(item)
    # type_id = query_db(type_id_query)[0][0]

    # url = construct_url(region_id, type_id)
    # price_data = fetch_price_data(url)

    # prices = []
    # for item in price_data['items']:
        # if location.capitalize() in item['location']['name']:
            # prices.append(item['price'])

    # prices = sorted(prices)
    # lowest_sell = prices[0]
    # print('{:,.2f}'.format(lowest_sell))
    pass

if __name__ == '__main__':
    args = parse_args()
    main(args)
