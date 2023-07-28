import json
import sys
from collections import defaultdict

NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3


def main():
    count_by_id = {}
    for line in sys.stdin:
        if line[-1] == '\n':
            line = line[:-1]
        obj = json.loads(line)
        prices = obj['prices']['region_wise']
        if obj['state'] not in count_by_id:
            count_by_id[obj['state']] = prices[SOUTH]
        else:
            count_by_id[obj['state']] += prices[SOUTH]

    print(count_by_id)


SOUTH_REGION = 1


def for_ss():
    total_prices = {}
    for line in sys.stdin:
        obj = json.loads(line)
        prices = obj['prices']['region_wise']
        if obj['state'] not in total_prices:
            total_prices[obj['state']] = prices[1]
        else:
            total_prices[obj['state']] += prices[1]


if __name__ == '__main__':
    main()
