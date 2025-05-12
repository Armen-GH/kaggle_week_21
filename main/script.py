from main.utils import *

df = parse_file("data/11_randomizing_paintings.txt")
write_same_order(df, "data/5_same_order.txt")