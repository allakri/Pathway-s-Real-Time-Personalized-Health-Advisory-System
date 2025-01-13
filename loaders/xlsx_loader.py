import os
import pandas as pd

def extract_xlsx_data(data_dir):
    """Extract data from all Excel files in the specified directory."""
    xlsx_data = {}

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            file_path = os.path.join(data_dir, file_name)

            try:
                df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets
                xlsx_data[file_name] = {sheet: df[sheet].to_dict(orient="records") for sheet in df}

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    return xlsx_data

# Test the loader
if __name__ == "__main__":
    print(extract_xlsx_data("./data"))
