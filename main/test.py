from main.utils import *
import time

start = time.time()

# df = parse_file("data/0_example.txt")
# gm = greedy_match(df)
# write_fg(gm, "data/output/example_gm.txt")
# print(global_score("data/output/example_gm.txt", df))

df = parse_file("data/10_computable_moments.txt")
gm = greedy_match(df)
write_fg(gm, "data/output/computable_gm.txt")
print(global_score("data/output/computable_gm.txt", df))

end = time.time()
print(f"Execution time: {end - start:.4f} seconds")