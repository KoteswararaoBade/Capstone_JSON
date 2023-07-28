# {"product": "IPhone 11", "brand": "Apple", "prices": [699, 799, 899, 999, 1099]}
import json
import sys


def main():
    for line in sys.stdin:
        if line[-1] == '\n':
            line = line[:-1]
        obj = json.loads(line)
        prices = obj['prices']
        avg_price = sum(prices) / len(prices)
        print('Average price of {} is {}'.format(obj['product'], avg_price))

    for line in sys.stdin:
        obj = json.loads(line)
        prices = obj['prices']
        avg_price = sum(prices) / len(prices)






if __name__ == '__main__':
    main()
