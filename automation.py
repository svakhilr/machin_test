import os
import json
from collections import defaultdict
from copy import deepcopy

# Load primary keys
with open("master_files/primary_keys.json") as f:
    primary_keys = json.load(f)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)["Table"]

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({"Table": data}, f, indent=2)

def get_key(record, keys):
    return tuple(record[k] for k in keys)

def process_file(filename, prev_day_path, curr_day_path, processed_day_path, keys):
    prev_records = load_json(os.path.join(prev_day_path, filename))
    curr_records = load_json(os.path.join(curr_day_path, filename))

    prev_map = {get_key(rec, keys): rec for rec in prev_records}
    final_map = deepcopy(prev_map)

    inserted = updated = deleted = 0

    for rec in curr_records:
        pk = get_key(rec, keys)
        flag = rec.get("flag")

        if pk not in prev_map:
            if flag in ("A", "O"):
                final_map[pk] = rec
                inserted += 1
        else:
            if flag == "D":
                if pk in final_map:
                    del final_map[pk]
                    deleted += 1
            elif flag in ("A", "O"):
                final_map[pk] = rec
                updated += 1

    save_json(list(final_map.values()), os.path.join(processed_day_path, filename))
    print(f"File: {filename} Inserted: {inserted} Updated: {updated} Deleted: {deleted}")


def process_day(day, prev_day):
    day_folder = f"master_files/day_{day}/"
    prev_folder = f"master_files/day_{prev_day}/" if prev_day == 0 else f"processed/day_{prev_day}/"
    processed_folder = f"processed/day_{day}/"

    for filename in os.listdir(day_folder):
        table_name = filename.replace(".json", "")
        keys = primary_keys[table_name]
        process_file(filename, prev_folder, day_folder, processed_folder, keys)




for day in range(1, 3): 
    process_day(day, day - 1)
