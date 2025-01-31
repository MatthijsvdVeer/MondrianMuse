import os
from pathlib import Path
import sys
from detect_gpt_promptflow import flow_entry

folder = Path(__file__).parent.absolute().as_posix()
abstracts_folder = os.path.join(folder, "abstracts")

for filename in os.listdir(abstracts_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(abstracts_folder, filename), 'r') as file:
            abstract_content = file.read()
            result = flow_entry(abstract=abstract_content)
            print(f"{filename}: {result}")
