# program to get all keys from a json
import json
import sys


def main():
    # give a json input here
    input1 = """
    {"id": 1, "name": "Koteswara Rao Bade",
    "address": {"city": "Hyderabad", "state": "Telangana"}}
    """
    obj = json.loads(input1)

    # get all keys from the json, also the keys from nested json
    if "city" in obj["address"]:
        print('city is present in the json')
    else:
        print('city is not present in the json')


if __name__ == '__main__':
    main()
