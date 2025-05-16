from main.utils import *
import time

start = time.time()

df = parse_file("data/0_example.txt")
fg = get_frameglasses(df)
fg_tags = get_frameglass_tags(df)
paintings_tags = get_tags_with_paintings_dict(df)
fg_gm =greedy_matching(fg, paintings_tags)
write_fg(fg_gm, "data/output/example_gm.txt")
print(global_score("data/output/example_gm.txt", df))

# df = parse_file("data/10_computable_moments.txt")
# paintings_tags = get_tags_with_paintings_dict(df)
# fg = greedy_matching(df, paintings_tags)
# write_fg(fg, "data/output/computable_gm.txt")
# print(global_score("data/output/computable_gm.txt", df))

end = time.time()
print(f"Execution time: {end - start:.4f} seconds")