import os
from langchain_community.document_loaders import UnstructuredPowerPointLoader

def extract_pptx_data(data_dir):
    """Extract data from all PowerPoint (.pptx) files in the specified directory."""
    all_ppt_data = {}  # Store data for all files

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".pptx"):
            file_path = os.path.join(data_dir, file_name)
            loader = UnstructuredPowerPointLoader(file_path, mode="elements")
            
            try:
                file_docs = loader.load()
                ppt_data = {}  # Store data for the current file by page

                for doc in file_docs:
                    page = doc.metadata.get("page_number", 0)  # Default to 0 if no page_number
                    ppt_data[page] = ppt_data.get(page, "") + "\n\n" + doc.page_content

                all_ppt_data[file_name] = ppt_data  # Associate pages with the file name

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    return all_ppt_data


# result = extract_pptx_data("./data")
# print(result)
