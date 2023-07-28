# author: Koteswara Rao Bade

def generate_jsonl_file(filename, fruits, lines=1000):
    """
    Generate a JSONL file with 1000 lines.
    :return: None
    """
    # create file if it doesn't exist
    with open(filename, 'w') as f:
        for line_number in range(1, lines + 1):
            fruit_name1 = fruits[line_number % len(fruits)]
            fruit_name2 = fruits[(line_number + 1) % len(fruits)]
            f.write("{")
            f.write("\"" + fruit_name1 + "\": " + str(line_number) + ", ")
            f.write("\"" + fruit_name2 + "\": " + str(line_number + 1))
            f.write("}\n")


def read_fruits(fruits_file):
    """
    Read fruits from a file.
    :param fruits_file: fruits file
    :return: fruits
    """
    fruits = []
    with open(fruits_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            fruits.append(line.strip())
    return fruits


def main():
    file_name = 'data/random.jsonl'
    fruits = read_fruits('data/fruits.txt')
    generate_jsonl_file(file_name, fruits)


if __name__ == '__main__':
    main()
