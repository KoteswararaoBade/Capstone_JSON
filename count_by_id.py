# author: Koteswara Rao Bade

"""
JSON data:
{'mangoes': 2, 'apples':3}
{'pears': 5, 'apples': 2}
{'mangoes': 1, 'apples': 1, 'pears': 1}
"""
import json
import sys


def main():
    count_by_id = {}
    for line in sys.stdin:
        if line[-1] == '\n':
            line = line[:-1]
        obj = json.loads(line)
        if obj['id'] not in count_by_id:
            count_by_id[obj['id']] = obj['count']
        else:
            count_by_id[obj['id']] += obj['count']


if __name__ == '__main__':
    main()
