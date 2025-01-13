import os
from langchain_community.document_loaders import PyMuPDFLoader

def extract_pdf_data(data_dir):
    """Extract data from all PDF files in the specified directory."""
    pdf_data = {}

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(data_dir, file_name)
            loader = PyMuPDFLoader(file_path)

            try:
                file_docs = loader.load()
                pdf_data[file_name] = [doc.page_content for doc in file_docs]

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    return pdf_data

# Test the loader
if __name__ == "__main__":
    print(extract_pdf_data("./data"))
