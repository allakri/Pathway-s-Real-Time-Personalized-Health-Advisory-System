import os
from langchain_community.document_loaders import Docx2txtLoader

def extract_docx_data(data_dir):
    """Extract data from all DOCX files in the specified directory."""
    docx_data = {}

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".docx"):
            file_path = os.path.join(data_dir, file_name)
            loader = Docx2txtLoader(file_path)

            try:
                file_docs = loader.load()
                docx_data[file_name] = [doc.page_content for doc in file_docs]

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    return docx_data

# # Test the loader
# if __name__ == "__main__":
#     print(extract_docx_data("./data"))
