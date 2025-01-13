import streamlit as st 
import os
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import time
import requests
from gtts import gTTS
import tempfile
# Import loaders
from loaders.pdf_loader import extract_pdf_data
from loaders.csv_loader import extract_csv_data
from loaders.docx_loader import extract_docx_data
from loaders.pptx_loader import extract_pptx_data
from loaders.xlsx_loader import extract_xlsx_data

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="Real-Time Personalized Health Advisory System")
# Initialize session state for audio cache
if 'audio_cache' not in st.session_state:
    st.session_state.audio_cache = {}

def text_to_speech(text, message_id):
    """Convert text to speech and cache the audio file"""
    if message_id not in st.session_state.audio_cache:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts = gTTS(text=text, lang='en')
            tts.save(fp.name)
            st.session_state.audio_cache[message_id] = fp.name
    return st.session_state.audio_cache[message_id]

# Add custom CSS for the speaker button
st.markdown("""
    <style>
    .speaker-button {
        padding: 0.5rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        border: none;
        cursor: pointer;
        margin-top: 0.5rem;
    }
    .speaker-button:hover {
        background-color: #e0e2e6;
    }
    </style>
""", unsafe_allow_html=True)

# Load the API key for Google Generative AI
google_api_key = os.environ["GOOGLE_API_KEY"]

# Weather API function
def fetch_weather(city):
    """Fetch weather information for a given city."""
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=d18165a3b71ab18fc6223d005233acfd"
    response = requests.get(api).json()
    if response.get("cod") != 200:
        return {"error": f"City '{city}' not found."}
    return {
        "condition": response['weather'][0]['main'],
        "temp": int(response['main']['temp'] - 273.15),
        "min_temp": int(response['main']['temp_min'] - 273.15),
        "max_temp": int(response['main']['temp_max'] - 273.15),
        "pressure": response['main']['pressure'],
        "humidity": response['main']['humidity'],
        "wind_speed": response['wind']['speed'],
        "sunrise": time.strftime('%I:%M:%S', time.gmtime(response['sys']['sunrise'])),
        "sunset": time.strftime('%I:%M:%S', time.gmtime(response['sys']['sunset'])),
    }

# Store weather data in session state
if 'current_weather' not in st.session_state:
    st.session_state.current_weather = None

# Sidebar for weather
st.sidebar.title("Weather Information")
default_city = "Hyderabad"
city = st.sidebar.text_input("Enter your city:", default_city)

weather = fetch_weather(city)
if "error" in weather:
    st.sidebar.error(weather["error"])
    st.session_state.current_weather = None
else:
    st.session_state.current_weather = weather
    st.sidebar.write(f"**City**: {city}")
    st.sidebar.write(f"**Condition**: {weather['condition']}")
    st.sidebar.write(f"**Temperature**: {weather['temp']}°C")
    st.sidebar.write(f"**Min Temp**: {weather['min_temp']}°C")
    st.sidebar.write(f"**Max Temp**: {weather['max_temp']}°C")
    st.sidebar.write(f"**Pressure**: {weather['pressure']} hPa")
    st.sidebar.write(f"**Humidity**: {weather['humidity']}%")
    st.sidebar.write(f"**Wind Speed**: {weather['wind_speed']} m/s")
    st.sidebar.write(f"**Sunrise**: {weather['sunrise']}")
    st.sidebar.write(f"**Sunset**: {weather['sunset']}")

# Function to get weather context
def get_weather_context():
    if st.session_state.current_weather:
        return f"""Current weather conditions:
- Temperature: {st.session_state.current_weather['temp']}°C
- Weather: {st.session_state.current_weather['condition']}
- Humidity: {st.session_state.current_weather['humidity']}%
- Wind Speed: {st.session_state.current_weather['wind_speed']} m/s"""
    return "Weather information not available."

# Function to load and aggregate data from all loaders
def load_all_data(data_dir):
    """Load and aggregate data from all loaders."""
    docs = []

    # Load documents from each loader
    pdf_data = extract_pdf_data(data_dir)
    csv_data = extract_csv_data(data_dir)
    docx_data = extract_docx_data(data_dir)
    pptx_data = extract_pptx_data(data_dir)
    xlsx_data = extract_xlsx_data(data_dir)

    # Flatten the data structure to create a unified list
    for data in [pdf_data, csv_data, docx_data, pptx_data, xlsx_data]:
        for file_name, content in data.items():
            for item in content:
                docs.append({"source": file_name, "content": item})
    
    return docs

# Directory containing files
data_dir = r"D:\pathway\loaders\data"  # Use raw string to avoid escape sequence issues

# Check and initialize session state variables
if "vector" not in st.session_state:
    try:
        # Initialize embeddings with Google Generative AI
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(
            api_key=google_api_key, 
            model="models/embedding-001"
        )
    except Exception as e:
        st.error(f"Error initializing Google Generative AI Embeddings: {e}")
        st.stop()

    # Load and process documents
    st.session_state.docs = load_all_data(data_dir)
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Create Document objects for the text splitter
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(
        [Document(page_content=doc["content"], metadata={"source": doc["source"]}) for doc in st.session_state.docs[:50]]
    )

    # Create FAISS vector store
    st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

# Streamlit app interface
# st.title("ChatGroq Demo")
llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model_name="mixtral-8x7b-32768"
)

prompt = ChatPromptTemplate.from_template(
    """
    Your name is MR.Bittu 
    
    You are an expert in multiple health-related fields, including but not limited to, general medicine, fitness and yoga, nutrition, and wellness. Your task is to provide personalized and actionable health advice based on a variety of inputs from individuals, taking into account the current weather conditions when relevant.

    Current Weather Information:
    {weather_context}

    Your recommendations should be informed by:
    1. Evidence-based medical practices
    2. Fitness principles
    3. Dietary guidelines
    4. Holistic wellness strategies
    5. Current weather conditions and their potential impact on health
    
    
    
    When answering questions:
    - If the question is weather-related, incorporate the current weather conditions into your advice
    - Consider how the weather might affect health recommendations
    - Provide specific precautions or modifications based on weather conditions
    - Keep answers concise (2-5 sentences unless detailed version is requested)

    Context:
    {context}

    Question: {input}
    """
)

document_chain = create_stuff_documents_chain(llm, prompt)
retriever = st.session_state.vectors.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Add a chat-like UI for interaction
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize chat history

st.title("Pathway’s Real-Time Personalized Health Advisory System")
st.write("HI! my name is BITTU ,I am your Personalized Health Advisor")

# Display existing chat history with speaker buttons
for idx, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            col1, col2 = st.columns([0.9, 0.1])
            with col2:
                if st.button("🔊", key=f"speak_{idx}"):
                    audio_file = text_to_speech(message["content"], f"msg_{idx}")
                    st.audio(audio_file, format='audio/mp3')

# Input field for the user to type their message
if user_input := st.chat_input("Ask your question here..."):
    # Add the user's question to the chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate a response using the retrieval chain
    with st.spinner("Generating response..."):
        start = time.process_time()
        response = retrieval_chain.invoke({
            "input": user_input,
            "weather_context": get_weather_context()
        })
        response_time = time.process_time() - start
        bot_response = response["answer"]

    # Add the bot's response to the chat history
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
        # Add speaker button for the new message
        col1, col2 = st.columns([0.9, 0.1])
        with col2:
            if st.button("🔊", key=f"speak_{len(st.session_state.chat_history)-1}"):
                audio_file = text_to_speech(bot_response, f"msg_{len(st.session_state.chat_history)-1}")
                st.audio(audio_file, format='audio/mp3')

    # Display response time
    st.write(f"Response generated in {response_time:.2f} seconds")