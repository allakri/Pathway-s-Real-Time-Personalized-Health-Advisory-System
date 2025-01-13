# import pathway as pw

# # We define a schema for the table
# # It set all the columns and their types
# class InputSchema(pw.Schema):
#   value: int

# # We use the CSV input connector to connect to the directory.
# t = pw.io.csv.read(
#   './input_stream_dir/',
#   schema=InputSchema,
#   mode="streaming"
# )

# # We compute the sum (this part is independent of the connectors).
# t = t.reduce(sum=pw.reducers.sum(t.value))

# # We use a CSV output connector to write the results in an output file.
# pw.io.csv.write(t, "output_stream.csv")

# # We launch the computation.
# pw.run()

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
