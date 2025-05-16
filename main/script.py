import os

from main.utils import *

df = parse_file("data/11_randomizing_paintings.txt")


input_files = [
    "data/0_example.txt",
    "data/1_binary_landscapes.txt",
    "data/10_computable_moments.txt",
    "data/11_randomizing_paintings.txt",
    "data/110_oily_portraits.txt"
]
#Same Order
def same_order(file_indices, output_dir="data/output"):

    for idx in file_indices:
        input_file = input_files[idx]
        output_file = os.path.join(output_dir, f"{idx}_{os.path.basename(input_file).replace('.txt', '')}_output.txt")

        # Parse the file (assuming parse_file function is defined)
        df = parse_file(input_file)
        write_same_order(df, output_file)

        print(f"Processed {input_file} -> {output_file}")

# parsing 1st and 2nd files
same_order([0,1])