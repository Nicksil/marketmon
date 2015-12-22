Scratch Pad
===========

`prices = sorted([i['price'] for i in price_data['items']])`

    if args.buy:
        print("{:,.2f}".format(prices[-1]))
    else:
        print("{:,.2f}".format(prices[0]))
