import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

def parse_showroom(filepath, showroom_name):
    frame_data = []

    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == 'L':
                frame_id = parts[1]
                tags = parts[2:]
                frame_data.append({
                    'showroom': showroom_name,
                    'orientation': 'L',
                    'frame_id': frame_id,
                    'tags': tags
                })

            elif parts[0] == 'P':
                items = parts[1:]
                i = 0
                while i < len(items):
                    frame_id = items[i]
                    i += 1
                    tags = []
                    while i < len(items) and not items[i].isdigit():
                        tags.append(items[i])
                        i += 1
                    frame_data.append({
                        'showroom': showroom_name,
                        'orientation': 'P',
                        'frame_id': frame_id,
                        'tags': tags
                    })

    return frame_data

def analyze_showrooms(folder_path):
    all_data = []

    # Loop through each file in folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            showroom_name = filename.replace('.txt', '')
            filepath = os.path.join(folder_path, filename)
            showroom_data = parse_showroom(filepath, showroom_name)
            all_data.extend(showroom_data)

    df = pd.DataFrame(all_data)

    # Summary Table
    df['num_tags'] = df['tags'].apply(len)
    summary = df.groupby('showroom').agg(
        total_frames=('frame_id', 'count'),
        avg_tags_per_frame=('num_tags', 'mean')
    ).reset_index()

    print("\n🧾 Summary Table:")
    print(summary)

    # Tag Frequency Analysis
    all_tags = [tag for tags in df['tags'] for tag in tags]
    tag_counter = Counter(all_tags)

    total_unique_tags = len(tag_counter)
    most_common = tag_counter.most_common(10)
    least_common = tag_counter.most_common()[-10:]

    print(f"\nTotal Unique Tags: {total_unique_tags}")
    print("\nMost Common Tags:")
    for tag, count in most_common:
        print(f"{tag}: {count}")

    print("\n Least Common Tags:")
    for tag, count in least_common:
        print(f"{tag}: {count}")

    # Plot Histogram
    plt.figure(figsize=(12, 6))
    plt.bar(*zip(*most_common))
    plt.title("Top 10 Most Common Tags")
    plt.xlabel("Tag")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return summary, tag_counter

# 🔁 Run analysis
if __name__ == "__main__":
    folder = "../data"
    analyze_showrooms(folder)
