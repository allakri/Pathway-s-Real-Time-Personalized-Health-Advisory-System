import pathway as pw

class InputSchema(pw.Schema):
    """
    Define the schema for the JSON Lines data.
    """
    key: int = pw.column_definition(primary_key=True)
    recipient: str
    sender: str

def load_jsonl_data(file_path, schema=InputSchema, mode="streaming"):
    """
    Load data from a JSON Lines (.jsonl) file or directory using Pathway.
    
    Parameters:
        file_path (str): Path to the JSON Lines file or directory.
        schema (pw.Schema): The schema defining the structure of the data.
        mode (str): Mode for loading the data, "streaming" or "static".
    
    Returns:
        pw.Table: Pathway table containing the loaded data.
    """
    try:
        table = pw.io.jsonlines.read(path=file_path, schema=schema, mode=mode)
        return table
    except Exception as e:
        print(f"Error loading JSON Lines data: {e}")
        return None

def save_jsonl_data(table, output_file):
    """
    Save a Pathway table to a JSON Lines (.jsonl) file.

    Parameters:
        table (pw.Table): The Pathway table to save.
        output_file (str): Path to the output JSON Lines file.
    """
    try:
        pw.io.jsonlines.write(table, output_file)
    except Exception as e:
        print(f"Error saving JSON Lines data: {e}")

# Example Usage
if __name__ == "__main__":
    # Load data from a JSON Lines file in streaming mode
    input_file = "./input_file.jsonl"
    table = load_jsonl_data(input_file, mode="static")  # Use "static" for one-time loading
    
    if table:
        # Debugging: Print the table content
        pw.debug.compute_and_print(table)
        
        # Save the data to a new JSON Lines file
        output_file = "./output_file.jsonl"
        save_jsonl_data(table, output_file)

    # Run the Pathway engine (required to finalize operations)
    pw.run()
