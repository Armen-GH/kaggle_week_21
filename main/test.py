from main.utils import *
import time


start = time.time()

df = parse_file("data/10_computable_moments.txt")

print(f"Execution time: {end - start:.4f} seconds")