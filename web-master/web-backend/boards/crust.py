import os
import sys
import pathlib
from source import solution


def main():
    dir_path = str(pathlib.Path(__file__).parent.absolute()) + "/"
    print(dir_path)
    input_file_name = "input.txt"
    out_file_name_template = "output{0}.txt"

    input_file = open(dir_path + input_file_name, "r")
    input_num = int(input_file.readline())
    for i in range(1, input_num + 1):
        out_file_name = out_file_name_template.format(str(i))
        sys.stdout = open(dir_path + out_file_name, "w")
        solution(int(input_file.readline()))
        


if __name__ == "__main__":
    main()