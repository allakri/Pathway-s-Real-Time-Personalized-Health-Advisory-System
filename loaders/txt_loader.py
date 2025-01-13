import os

def extract_text_data(data_dir):
    """Extract data from all text files in the specified directory."""
    text_data = {}

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".txt"):
            file_path = os.path.join(data_dir, file_name)

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text_data[file_name] = file.read()

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    return text_data

# Test the loader
# if __name__ == "__main__":
#     print(extract_text_data("./data"))
