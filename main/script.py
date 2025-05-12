from main.utils import *

df = parse_file("data/110_oily_portraits.txt")
write_same_order(df, "data/5_same_order.txt")