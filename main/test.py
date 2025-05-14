from main.utils import *
import time


start = time.time()

df = parse_file("data/10_computable_moments.txt")
#get_tags_with_paintings(df, "data/output/tags_paintings_frq.tags")
#df_analysis(df, plot=True)
print(global_score("data/output/output_yuke.txt", df))
end = time.time()
print(f"Execution time: {end - start:.4f} seconds")