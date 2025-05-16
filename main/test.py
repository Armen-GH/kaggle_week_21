from main.utils import *
import time

start = time.time()

df = parse_file("data/0_example.txt")
fg = kmeans_chunked_match(df, k=10)
write_fg(fg, "data/output/example_kmeans.txt")
print(global_score("data/output/example_kmeans.txt", df))

end = time.time()
print(f"Execution time: {end - start:.4f} seconds")