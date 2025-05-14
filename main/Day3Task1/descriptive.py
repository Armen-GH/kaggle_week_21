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
    per_showroom_summaries = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            showroom_name = filename.replace('.txt', '')
            filepath = os.path.join(folder_path, filename)
            showroom_data = parse_showroom(filepath, showroom_name)

            df = pd.DataFrame(showroom_data)
            df['num_tags'] = df['tags'].apply(len)

            tag_counter = Counter(tag for tags in df['tags'] for tag in tags)

            showroom_summary = {
                'showroom': showroom_name,
                'total_frames': len(df),
                'avg_tags_per_frame': df['num_tags'].mean(),
                'total_unique_tags': len(tag_counter)
            }

            per_showroom_summaries.append(showroom_summary)

            # 🔥 Print top 10 tags for this showroom
            top_10_tags = tag_counter.most_common(10)
            top_df = pd.DataFrame(top_10_tags, columns=['tag', 'count'])
            print(f"\nTop 10 Tags for \n{showroom_name}:")
            print(top_df.to_string(index=False))


    # Show individual showroom summaries
    per_showroom_df = pd.DataFrame(per_showroom_summaries)
    print("\nPer-Showroom Summary:")
    print(per_showroom_df)
    print(per_showroom_df.to_string(index=False))
    per_showroom_df.to_csv("per_showroom_summary.csv", index=False)

    # Combined Summary Table
    df_all = pd.DataFrame(all_data)
    df_all['num_tags'] = df_all['tags'].apply(len)

    combined_summary = df_all.groupby('showroom').agg(
        total_frames=('frame_id', 'count'),
        avg_tags_per_frame=('num_tags', 'mean')
    ).reset_index()

    print("\nCombined Summary Table (From GroupBy):")
    print(combined_summary)

    # Overall Tag Frequency
    all_tags = [tag for tags in df_all['tags'] for tag in tags]
    tag_counter = Counter(all_tags)

    total_unique_tags = len(tag_counter)
    most_common = tag_counter.most_common(10)
    least_common = tag_counter.most_common()[-10:]

    print(f"\nTotal Unique Tags Across All Showrooms: {total_unique_tags}")
    print("\nMost Common Tags:")
    for tag, count in most_common:
        print(f"{tag}: {count}")

    print("\nLeast Common Tags:")
    for tag, count in least_common:
        print(f"{tag}: {count}")

    # Plot Histogram
    plt.figure(figsize=(12, 6))
    plt.bar(*zip(*most_common))
    plt.title("Top 10 Most Common Tags Across All Showrooms")
    plt.xlabel("Tag")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return per_showroom_df, combined_summary

# 🔁 Run analysis
if __name__ == "__main__":
    folder = "../data"  # 👈 Update this to match your folder location
    analyze_showrooms(folder)
