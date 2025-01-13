import os
import pandas as pd

def extract_csv_data(data_dir):
    """Extract data from all CSV files in the specified directory."""
    csv_data = {}

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".csv"):
            file_path = os.path.join(data_dir, file_name)

            try:
                df = pd.read_csv(file_path)
                csv_data[file_name] = df.to_dict(orient="records")  # Convert rows to dicts

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    return csv_data

# # Test the loader
# if __name__ == "__main__":
#     print(extract_csv_data("./data"))
