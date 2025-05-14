from collections import defaultdict, Counter
from itertools import combinations

import pandas as pd
import matplotlib.pyplot as plt
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

def read_order_file(order_filepath):
    frameglasses = []
    with open(order_filepath, 'r') as file:
        line_count = int(file.readline().strip())  # first line = frameglass count
        for _ in range(line_count):
            line = file.readline()
            if not line.strip():
                continue  # skip empty lines
            ids = list(map(int, line.strip().split()))
            frameglasses.append(ids)
    return frameglasses

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

def local_score(tags1, tags2):
    tags1 = set(tags1)
    tags2 = set(tags2)
    return min(
        len(tags1 & tags2),
        len(tags1 - tags2),
        len(tags2 - tags1)
    )

def global_score(order_filepath, df_paintings):
    frameglasses = read_order_file(order_filepath)

    frameglass_tags = []
    for frame in frameglasses:
        tags = set()
        for painting_id in frame:
            # Safely get tags of this painting
            painting_tags = df_paintings.loc[df_paintings['id'] == painting_id, 'tags'].values
            if painting_tags.size > 0:
                tags.update(painting_tags[0])
        frameglass_tags.append(tags)

    local_scores = []
    for i in range(len(frameglass_tags) - 1):
        score = local_score(frameglass_tags[i], frameglass_tags[i+1])
        local_scores.append(score)

    return sum(local_scores)

def same_order(df):
    return get_frameglasses(df)

def reverse_order(df):
    frameglasses = get_frameglasses(df)
    return frameglasses.reverse()

def random_order(df):
    frameglasses = get_frameglasses(df)
    random.shuffle(frameglasses)
    return frameglasses

def tags_order(df):
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

def get_tags_with_paintings_dict(df):
    tag_to_paintings = defaultdict(list)

    for _, row in df.iterrows():
        painting_id = row['id']
        tags = row['tags']
        for tag in tags:
            tag_to_paintings[tag].append(painting_id)
    return tag_to_paintings

def df_analysis(df, output_filepath="data/output/analysis_output.txt", plot=False):
    def write(line=""):
        with open(output_filepath, 'a', encoding='utf-8') as f:
            f.write(line + "\n")

    open(output_filepath, 'w', encoding='utf-8').close()
    write("Dataset Analysis\n")

    # Type distribution
    total_paintings = df['id'].nunique()
    type_counts = df['type'].value_counts()
    write("1 - ️Type Distribution (L vs P):")
    write(f"Total number of paintings: {total_paintings}")
    write(type_counts.to_string())
    write()

    # Tag frequency
    all_tags = [tag for tags in df['tags'] for tag in tags]
    tag_freq = Counter(all_tags)
    write("2 - Tag Frequency (top 10):")
    for tag, count in tag_freq.most_common(10):
        write(f"{tag}: {count}")
    write()

    # Paintings per tag
    tag_to_paintings = get_tags_with_paintings_dict(df)
    tag_paintings_count = {tag: len(set(ids)) for tag, ids in tag_to_paintings.items()}
    write("3 - Tags with Most Paintings (top 10):")
    for tag, count in sorted(tag_paintings_count.items(), key=lambda x: x[1], reverse=True)[:10]:
        write(f"{tag}: {count}")
    write()

    # Tag co-occurrence
    co_occurrence = Counter()
    for tags in df['tags']:
        for pair in combinations(sorted(tags), 2):
            co_occurrence[pair] += 1
    write("4 - Tag Co-occurrence (top 5 pairs):")
    for pair, count in co_occurrence.most_common(5):
        write(f"{pair}: {count}")
    write()

    # Average tags per painting
    avg_tags = df['tag_count'].mean()
    write(f"5 -  Average Tags per Painting: {avg_tags:.2f}\n")

    # Rare tags
    threshold = total_paintings * (10 / 100)
    rare_tags = [tag for tag, count in tag_freq.items() if count <= threshold]
    write(f"6 -  Number of Rare Tags (appear in less than 5% of all paintings): {len(rare_tags)}")
    if len(rare_tags) > 0:
        write(f"Example rare tags: {rare_tags[:5]}\n")

    # Optional plotting
    if plot:
        plt.figure(figsize=(10, 5))
        tags, freqs = zip(*tag_freq.most_common(15))
        plt.bar(tags, freqs)
        plt.xticks(rotation=45, ha='right')
        plt.title('Top 15 Tag Frequencies')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.show()

        plt.figure()
        type_counts.plot.pie(autopct='%1.1f%%', startangle=90, title='Type Distribution')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()

def get_frameglass_tags(frameglass, df):
    tags = set()
    for painting_id in frameglass:
        row = df.loc[df['id'] == painting_id, 'tags'].values
        if row.size > 0:
            tags.update(row[0])
    return tags

def greedy_matching(frameglasses, df_paintings, output_filepath = "data/output/ordered_tags.txt"):
    remaining = frameglasses.copy()
    current = remaining.pop(0)
    ordering = [current]
    current_tags = get_frameglass_tags(current, df_paintings)

    while remaining:
        best_score = float('inf')
        best_index = -1

        for idx, candidate in enumerate(remaining):
            candidate_tags = get_frameglass_tags(candidate, df_paintings)
            score = local_score(current_tags, candidate_tags)
            if score < best_score:
                best_score = score
                best_index = idx

        next_frame = remaining.pop(best_index)
        ordering.append(next_frame)
        current_tags = get_frameglass_tags(next_frame, df_paintings)

    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(f"{len(frameglasses)}\n")
        for frame in frameglasses:
            line = ' '.join(map(str, frame))
            f.write(f"{line}\n")