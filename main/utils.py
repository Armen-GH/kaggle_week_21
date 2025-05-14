from collections import defaultdict

import pandas as pd
import random


def parse_file(filepath):
    records = []

    with open(filepath, 'r') as file:
        line_count = int(file.readline().strip())  # first line
        for i in range(line_count):
            parts = file.readline().strip().split()
            entry_type = parts[0]
            tag_count = int(parts[1])
            tags = parts[2:2 + tag_count]

            records.append({
                "id": i+1,
                "type": entry_type,
                "tag_count": tag_count,
                "tags": tags
            })

    df = pd.DataFrame(records)
    return df

def get_frameglasses(df):
    frameglasses = []
    records = df.to_dict('records')
    n = len(records)
    i = 0
    p = None

    while i < n:
        current = records[i]
        if current['type'] == 'L':
            frameglasses.append([current['id']])
            i += 1
        elif current['type'] == 'P':
            if p is None:
                p = current['id']
                i += 1
            else:
                frameglasses.append([p, current['id']])
                p = None
                i += 1

    if p is not None:
        frameglasses.append([p])  # Handle unpaired P

    return frameglasses

def write_same_order(df, output_filepath):
    return get_frameglasses(df)

def write_reverse_order(df):
    frameglasses = get_frameglasses(df)
    return frameglasses.reverse()

def write_random_order(df):
    frameglasses = get_frameglasses(df)
    return random.shuffle(frameglasses)

def write_tags_order(df):
    frameglasses = get_frameglasses(df)
    return frameglasses.sort(key=lambda x: x[0])

def write_fg(frameglasses, output_filepath):
    with open(output_filepath, 'w') as f:
        f.write(f"{len(frameglasses)}\n")
        for frame in frameglasses:
            f.write(" ".join(map(str, frame)) + "\n")

def write_dict(output_filepath, tag_to_paintings):
    with open(output_filepath, 'w') as f:
        for tag in sorted(tag_to_paintings.keys()):
            paintings = tag_to_paintings[tag]
            painting_ids_str = " ".join(map(str, paintings))
            f.write(f"{tag}: {painting_ids_str}\n")

def tags_with_paintings(df):
    tag_to_paintings = defaultdict(list)

    for _, row in df.iterrows():
        painting_id = row['id']
        tags = row['tags']
        for tag in tags:
            tag_to_paintings[tag].append(painting_id)
    return tag_to_paintings