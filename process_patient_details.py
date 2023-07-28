import json
import sys


def main():
    # modify_value_to_int('data/patient_details.jsonl', 'data/patient_details_int.jsonl')
    count_descharged_patients()


def count_descharged_patients():
    discharged_patients = {}
    for line in sys.stdin:
        if line[-1] == '\n':
            line = line[:-1]
        obj = json.loads(line)

        if obj['provider_state'] not in discharged_patients:
            discharged_patients[obj['provider_state']] = obj['total_discharges']
        else:
            discharged_patients[obj['provider_state']] += obj['total_discharges']
    for key, value in discharged_patients.items():
        print(key, value)


def modify_value_to_int(jsonl_input_path, jsonl_output_path):
    with open(jsonl_input_path, 'r') as input_file, open(jsonl_output_path, 'w') as output_file:
        index = 0
        for line in input_file:
            json_obj = json.loads(line)
            # Modify the specific value from string to integer
            if index % 5000 != 0:
                json_obj['total_discharges'] = int(json_obj['total_discharges'])
            else:
                json_obj['total_discharges'] = json_obj['total_discharges']
            # Write the modified JSON object to the output file
            output_file.write(json.dumps(json_obj) + '\n')
            index += 1


if __name__ == '__main__':
    main()
