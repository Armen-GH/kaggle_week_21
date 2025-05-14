import sys

from main.utils import *
import time


start = time.time()

df = parse_file("data/110_oily_portraits.txt")
frameglasses = get_frameglasses(df)
order = greedy_matching(frameglasses, df, "data/output/ordered_oily.txt")
print(order)

end = time.time()
print(f"Execution time: {end - start:.4f} seconds")