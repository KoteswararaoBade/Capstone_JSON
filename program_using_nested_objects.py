import json
import sys


def main():
    count_by_id = {}
    for line in sys.stdin:
        if line[-1] == '\n':
            line = line[:-1]
        obj = json.loads(line)
        if obj['state_id'] not in count_by_id:
            count_by_id[obj['id']] = obj['nested']['nested1']['count']
        else:
            count_by_id[obj['id']] += obj['nested']['nested1']['count']


if __name__ == '__main__':
    main()