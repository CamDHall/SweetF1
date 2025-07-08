from dataclasses import dataclass
import os
import pickle
import json

@dataclass
class StorageService:
    def save_file(self, subdirectory: str, file_name: str, content):
        # Ensure the subdirectory exists
        os.makedirs(subdirectory, exist_ok=True)

        # Define the full path to the file
        file_path = os.path.join(subdirectory, file_name)
        with open(file_path, "w") as json_file:
            json.dump(content, json_file)

        print("Serialized data written to JSON file successfully!")