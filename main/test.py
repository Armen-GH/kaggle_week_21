from main.utils import *
import time


start = time.time()

df = parse_file("data/110_oily_portraits.txt")
write_random_order(df, "data/output/oily.txt")

end = time.time()
print(f"Execution time: {end - start:.4f} seconds")