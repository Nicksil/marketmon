Scratch Pad
===========

`prices = sorted([i['price'] for i in price_data['items']])`

    if args.buy:
        print("{:,.2f}".format(prices[-1]))
    else:
        print("{:,.2f}".format(prices[0]))

CREST market item look-up template:

`https://public-crest.eveonline.com/market/10000002/orders/sell/?type=https://public-crest.eveonline.com/types/683/`
