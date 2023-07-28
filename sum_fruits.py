# author: Koteswara Rao Bade

"""
JSON data:
{'mangoes': 2, 'apples':3}
{'pears': 5, 'apples': 2}
{'mangoes': 1, 'apples': 1, 'pears': 1}
"""
import json
import sys


def find_total_fruits(json_data):
    """
    Find total number of fruits in the given JSON data.
    :param json_data: JSON data
    :return: total number of fruits
    """
    numbers = []
    for key, value in json_data.items():
        numbers.append(value)
    return numbers


def find_total_fruits_assoonas_line_is_read(json_data):
    """
    Find total number of fruits in the given JSON data.
    :param json_data: JSON data
    :return: total number of fruits
    """
    total = 0
    for key, value in json_data.items():
        total += value
    return total



def read_input_and_sum_fruits():
    """
    Read input from file.
    :param filename: input file name
    :return: total number of fruits
    """
    all_numbers = []
    for line in sys.stdin:
        if line[-1] == '\n':
            line = line[:-1]
        json_data = json.loads(line)
        all_numbers.extend(find_total_fruits(json_data))
    return sum(all_numbers)


def main():
    total_fruits = read_input_and_sum_fruits()
    print(total_fruits)


if __name__ == '__main__':
    main()
