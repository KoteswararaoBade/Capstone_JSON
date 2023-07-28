# author: Koteswara Rao Bade
import json
import subprocess
import sys
import time
import random

import jsonpath_ng

MAX_ITERATIONS = 20


def main():
    if len(sys.argv) > 2:
        filename = sys.argv[1]
        program_name = sys.argv[2]

        print("Reduction started...")
        start = time.time()
        start_iterations_of_reduction(filename, program_name)
        print('Time taken: ', time.time() - start)
    else:
        print("Usage: python3 reduction_program.py <filename> <program_name>")


def shuffle_input(input_as_list):
    """
    Shuffle the input.
    :param input_as_list: input as list
    :return: shuffled input
    """
    random.shuffle(input_as_list)
    return '\n'.join(input_as_list)


def start_iterations_of_reduction(filename, program_name):
    # read file and check the error and number of lines
    number_of_lines = 0
    initial_input = ""
    with open(filename, 'r') as f:
        for line in f:
            initial_input += line
            number_of_lines += 1
    output = subprocess.run(['python3', program_name], input=initial_input, capture_output=True, text=True)
    error = output.stderr

    print("Error before itertaion: ", error)
    i = 1
    while True:
        print('Iteration Number: ', i)
        if number_of_lines == 1 or i == MAX_ITERATIONS:
            break

        # call subprocess for first half of the initial input
        input_as_list = initial_input.split('\n')
        first_half = '\n'.join(input_as_list[:number_of_lines // 2])

        output_1 = subprocess.run(['python3', program_name], input=first_half, capture_output=True, text=True)
        if output_1.stderr and output_1.stderr == error:
            i += 1
            print('First half produced an error.', error)
            initial_input = first_half
            print('First half is: \n', initial_input)
            number_of_lines = number_of_lines // 2
            continue

        # call subprocess for second half of the initial input
        second_half = '\n'.join(input_as_list[number_of_lines // 2:])
        output_2 = subprocess.run(['python3', program_name], input=second_half, capture_output=True, text=True)
        if output_2.stderr and output_2.stderr == error:
            i += 1
            print('Second half produced an error.', error)
            initial_input = second_half
            print('Second half is: \n', initial_input)
            number_of_lines = number_of_lines - number_of_lines // 2
            continue

        # if both halves do not produce any error, then shuffle the input and try again
        if (not output_1.stderr or output_1.stderr != error) and \
                (not output_2.stderr or output_2.stderr != error):
            print('Both halves did not produce any error or produced a different error.')
            i += 1
            print('Shuffling the input...')
            initial_input = shuffle_input(input_as_list)
            number_of_lines = len(initial_input.split('\n'))

    print('input after initial reduction is: \n', initial_input, '\n')
    print('Removing the keys one by one...')
    # remove the keys from the input
    initial_input = reduce_input_by_removing_keys(error, initial_input, program_name)
    print('input after removing keys is: \n', initial_input, '\n')

    print('Reducing the arrays...')
    initial_input = remove_elements_from_list(error, initial_input, program_name)
    print('input after removing elements from arrays is: \n', initial_input, '\n')

    # write the final input to a file
    with open('data/reduced_input.jsonl', 'w') as f:
        f.write(initial_input)


def reduce_input_by_removing_keys(error, initial_input, program_name):
    keys = set()
    temp_input = initial_input.split('\n')
    for line in temp_input:
        keys.update(json.loads(line).keys())

    print('keys before adding nested keys: ', keys)
    get_all_nested_keys(keys, temp_input)
    print('keys after adding nested keys: ', keys)

    for key in keys:
        # remove key from the input
        for i in range(len(temp_input)):
            temp = json.loads(temp_input[i])
            jsonpath_ng.parse(f'$.{key}').filter(lambda x: True, temp)
            temp_input[i] = json.dumps(temp)

        # call the subprocess with the new input
        input_to_program = '\n'.join(temp_input)
        output = subprocess.run(['python3', program_name], input=input_to_program, capture_output=True, text=True)

        current_error = output.stderr
        if not current_error or current_error != error:
            temp_input = initial_input.split('\n')
        else:
            initial_input = input_to_program
    return initial_input


def check_if_key_exists_in_input(key, path, input_as_json):
    try:
        new_input = input_as_json
        for each_key in path:
            new_input = new_input[each_key]
    except KeyError:
        return False

    return key in new_input


def remove_elements_from_list(error, initial_input, program_name):
    temp_input = initial_input.split('\n')
    for i in range(len(temp_input)):
        temp = json.loads(temp_input[i])
        keys = set()
        for key in temp.keys():
            if type(temp[key]) == list:
                keys.add(key)

        print('keys before adding nested array type keys: ', keys)
        get_all_nested_keys(keys, [temp_input[i]], 'list')
        print('keys after adding nested array type keys: ', keys)

        # traverse through the json keys
        for key in keys:
            num_iterations = 0
            while True:
                # get the initial elements of the array for the key using jsonpath_ng
                jsonpath_expr = jsonpath_ng.parse(f'$.{key}')
                initial_elements = jsonpath_expr.find(temp)[0].value
                if len(initial_elements) == 1 or num_iterations >= MAX_ITERATIONS // 2:
                    break
                array_length = len(initial_elements)
                # divide elements in two halves
                first_half = initial_elements[:array_length // 2]
                second_half = initial_elements[array_length // 2:]

                jsonpath_expr.update(temp, first_half)
                temp_input[i] = json.dumps(temp)
                # call the subprocess with the new input
                input_to_program = '\n'.join(temp_input)
                output1 = subprocess.run(['python3', program_name], input=input_to_program, capture_output=True,
                                         text=True)

                if output1.stderr and output1.stderr == error:
                    num_iterations += 1
                    print('First half of the array produced an error.')
                    initial_input = input_to_program
                    print('First half is: \n', initial_input)
                    continue

                jsonpath_expr.update(temp, second_half)
                temp_input[i] = json.dumps(temp)
                # call the subprocess with the new input
                input_to_program = '\n'.join(temp_input)
                output2 = subprocess.run(['python3', program_name], input=input_to_program, capture_output=True,
                                         text=True)

                if output2.stderr and output2.stderr == error:
                    num_iterations += 1
                    print('Second half of the array produced an error.')
                    initial_input = input_to_program
                    print('Second half is: \n', initial_input)

                # if both halves do not produce any error, then shuffle the input and try again
                if (not output1.stderr or output1.stderr != error) and \
                        (not output2.stderr or output2.stderr != error):
                    print('Both halves did not produce any error or produced a different error.')
                    print('Shuffling the array elements...')
                    num_iterations += 1
                    random.shuffle(initial_elements)
                    jsonpath_expr.update(temp, initial_elements)
                    temp_input[i] = json.dumps(temp)
                    initial_input = '\n'.join(temp_input)

    return initial_input


def get_all_nested_keys(keys, temp_input, type_of_key='dict'):
    for i in range(len(temp_input)):
        temp = json.loads(temp_input[i])
        for key in temp.keys():
            if type(temp[key]) is dict:
                for nested_key in temp[key].keys():
                    if type(temp[key][nested_key]) is type_of_key:
                        get_keys_recursively(keys, temp[key][nested_key], key + '.' + nested_key)
                    keys.add(key + '.' + nested_key)


def get_keys_recursively(keys, temp_json, key):
    for each_key in temp_json.keys():
        if type(temp_json[each_key]) is dict:
            get_keys_recursively(keys, temp_json[each_key], key + '.' + each_key)
        keys.add(key + '.' + each_key)


if __name__ == '__main__':
    main()
