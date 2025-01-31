import os
from pathlib import Path
import sys
from detect_gpt_promptflow import flow_entry

folder = Path(__file__).parent.absolute().as_posix()
abstracts_folder = os.path.join(folder, "abstracts")

csv_results = []
check_results = []

for filename in os.listdir(abstracts_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(abstracts_folder, filename), 'r') as file:
            abstract_content = file.read()
            result = flow_entry(abstract=abstract_content)
            if result == "✅":
                check_results.append(filename)
            else:
                csv_items = result.split(',')
                csv_results.append((filename, len(csv_items), result))

# Sort csv_results by the number of items in the csv in descending order
csv_results.sort(key=lambda x: x[1], reverse=True)

# Print the results
for filename, count, csv in csv_results:
    print(f"{filename}:\n{count}\n{csv}")

for filename in check_results:
    print(f"{filename}: ✅")
