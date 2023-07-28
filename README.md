# MINIMIZATION PROGRAM

## Description
This program is designed to minimize the large JSON input which is producing an error while running on the program.

## Files description
- `generate_jsonl_files.py` - this is the file to generate input jsonl files which can be used for the program.
- `main.py` - this is the program on which inputs might be failing.
- `reduction_program.py` - this is the file which contains the main logic of the program.

## How to run the program
- Run the reduction program using the command `python3 reduction_program.py <input_file_path> <program_name>`