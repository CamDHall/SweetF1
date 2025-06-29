from dataclasses import dataclass
import os
import pickle
import zipfile

@dataclass
class StorageService:
    def save_file(self, subdirectory: str, file_name: str, content):
        # Ensure the subdirectory exists
        os.makedirs(subdirectory, exist_ok=True)

        # Define the full path to the file
        file_path = os.path.join(subdirectory, file_name)
        with open(file_path, "wb") as binary_file:
            pickle.dump(content, binary_file)

        print("Serialized data written to binary file successfully!")

    def zip_data_dir(self):

        directories = [d for d in os.listdir("data")]

        for sub_dir in directories:
            zip_name = sub_dir
            zip_path = f"events/{zip_name}.zip"
            dir_path = os.path.join("data", sub_dir)

            if not os.path.exists(zip_path):
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(dir_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, dir_path))
                print(f"Directory {dir_path} zipped to {zip_path} successfully!")
            else:
                print(f"Zip file {zip_path} already exists, skipping...")
