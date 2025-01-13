import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import tempfile

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
st.set_page_config(page_title="Real-Time Personalized Health Advisory System")
st.title("🔬 Health Report Analyzer")
st.markdown("Quick analysis of your health reports")

st.error("**Note:** Always consult healthcare professionals for medical advice")

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="Llama3-8b-8192",
    temperature=0.3,
    max_tokens=2048
)

analysis_prompt = ChatPromptTemplate.from_template(
    """Analyze this report section briefly. Provide key insights in 2-3 sentences maximum.
    Report Section: {report_content}
    Question: {user_input}
    
    Give a direct, focused response:"""
)

def extract_pdf_text(pdf_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_file.seek(0)
            pdf_reader = PdfReader(tmp_file.name)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None
    finally:
        if 'tmp_file' in locals():
            os.unlink(tmp_file.name)

def chunk_text(text, chunk_size=1000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_length += len(word) + 1
        if current_length > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def analyze_chunk(chunk, question):
    try:
        formatted_prompt = analysis_prompt.format(
            report_content=chunk,
            user_input=question
        )
        response = llm.invoke(formatted_prompt)
        return response.content
    except Exception as e:
        return f"Error analyzing this section: {str(e)}"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "report_chunks" not in st.session_state:
    st.session_state.report_chunks = None

uploaded_file = st.file_uploader("Upload health report (PDF)", type="pdf")
if uploaded_file:
    with st.spinner("Processing..."):
        report_text = extract_pdf_text(uploaded_file)
        if report_text:
            st.session_state.report_chunks = chunk_text(report_text)
            st.success("Report processed!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your report"):
    if not st.session_state.report_chunks:
        st.warning("Please upload a report first!")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                analyses = [analyze_chunk(chunk, prompt) for chunk in st.session_state.report_chunks]
                final_response = " ".join(filter(None, analyses))
                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})

with st.sidebar:
    st.markdown("""
    ### 📊 Quick Guide
    - Lab results
    - Vital signs
    - Test results
    - Measurements
    """)