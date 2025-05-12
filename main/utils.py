import pandas as pd

def parse_file(filepath):
    records = []
    with open(filepath, 'r') as file:
        line_count = int(file.readline().strip())  # first line
        for i in range(line_count):
            parts = file.readline().strip().split()
            entry_type = parts[0]
            tag_count = int(parts[1])
            tags = parts[2:2 + tag_count]

            if len(tags) != tag_count:
                raise ValueError(f"Expected {tag_count} tags, got {len(tags)} at line {_ + 2}")

            records.append({
                "id": i + 1,
                "type": "Landscape" if entry_type == 'L' else "Parser",
                "tag_count": tag_count,
                "tags": tags
            })

    df = pd.DataFrame(records)
    return df

def write_same_order(df, output_filepath):
    frameglasses = []
    i = 0
    records = df.to_dict('records')
    n = len(records)
    p = None

    while i < n:
        current = records[i]
        if current['type'] == 'Landscape':
            frameglasses.append([current['id']])
            i += 1
        elif current['type'] == 'Parser':
            if p is None:
                p = current['id']
                i+=1
            else:
                frameglasses.append([p, current['id']])
                p = None
                i += 1

    with open(output_filepath, 'w') as f:
        f.write(f"{len(frameglasses)}\n")
        for frame in frameglasses:
            f.write(" ".join(map(str, frame)) + "\n")