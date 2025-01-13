import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini with API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(input_text, image, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_text, image[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"An error occurred while getting the response: {str(e)}")
        return None

# Function to set up image for Gemini API
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the image file as bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app setup
st.set_page_config(page_title="Real-Time Personalized Health Advisory System")

st.header("Gemini Health Management App")

# Text input for user prompt
input_prompt = st.text_input("Enter additional instructions (optional)", key="input")

# File uploader for the image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Button to trigger calorie analysis
submit_button = st.button("submit")

# Prompt for nutritionist to calculate calories and provide details
nutritionist_prompt = """
Your name is **MR. Bittu**.

### **Role**:
You are a genius in analyzing images related to health and food. Your task is to analyze the provided image of food items or health-related images (like X-rays) and provide detailed information about each item or condition depicted.

---

### **Instructions**:
1. **Image Analysis**:
   - Carefully examine the uploaded image to identify all distinct food items or health indicators.
   - For each identified item or condition, provide:
     - The name of the item or condition
     - Relevant information (e.g., nutritional values for food items, potential health implications for medical images)

2. **For Food Items**:
   - Calculate and present the calorie content for each recognized food item.
   - Format your response as follows:
     - Item 1 - calories
     - Item 2 - calories
     - ...
     - Total Calorie Count: total calories

3. **For Health Images (e.g., X-rays)**:
   - Provide an analysis of the visible conditions or abnormalities.
   - Include potential implications for health and recommendations for further action if necessary.

4. **General Guidelines**:
   - Ensure clarity and precision in your analysis.
   - Use evidence-based practices to support your findings.
   - Maintain a professional tone throughout your response.

---

### **Context**:
Current Date: {current_date}
Current Weather: {weather_context}

### **User Question**:
{user_input}

---

### **Professional Response**:
Provide a structured and professional response, focusing on the analysis of food items or health-related images based on the question. Always incorporate relevant details and context when applicable.
"""

# If submit button is clicked, process the image and get the response
if submit_button:
    if uploaded_file is not None:
        # Prepare the image for processing
        image_data = input_image_setup(uploaded_file)
        # Get response from the Gemini API
        response = get_gemini_response(input_prompt, image_data, nutritionist_prompt)

        # Display the response from Gemini
        if response:
            st.subheader("Calorie Analysis Result:")
            st.write(response)
        else:
            st.error("Unable to get a valid response. Please try again.")
    else:
        st.error("Please upload an image of the food items.")

