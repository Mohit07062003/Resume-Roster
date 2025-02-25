import streamlit as st
import pdfplumber
from docx import Document
import uuid
from astrapy import DataAPIClient
from dotenv import load_dotenv
import os
import time
from openai import OpenAI
import urllib.parse  # For URL encoding the tweet

# Load environment variables
load_dotenv()

# Set up AstraDB connection
@st.cache_resource
def get_db_collection():
    token = os.getenv("ASTRA_TOKEN")
    client = DataAPIClient(token)
    db = client.get_database_by_api_endpoint(
        "https://4507fefd-398c-4604-bde7-dfd354ce1c30-us-east-2.apps.astra.datastax.com"
    )
    try:
        collection = db.create_collection("roasts", dimension=1536)  # Optional vector dimension
    except Exception:
        collection = db.get_collection("roasts")
    return collection

collection = get_db_collection()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(prompt):
    try:
        if len(prompt.split()) > 2250:
            prompt = " ".join(prompt.split()[:2250]) + " [Trimmed for length]"
            st.warning("Resume text was trimmed to fit OpenAI’s context limit.")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI API Error: {e}")
        return "Oops, the roast machine broke!"

# Resume text extraction
def extract_text(file):
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            text = "".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX.")
        return None
    return text

# Custom CSS for frontend styling
st.markdown("""
    <style>
    .big-title {
        font-size: 60px;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 20px;
    }
    .content-box {
        background-color: #F5F5F5;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 0px;
    }
    .no-margin {
        margin-bottom: 10px;
    }
    .stSpinner > div {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
        color: #FF4B4B;
        font-weight: bold;
    }
    .stSpinner > div::before {
        content: '';
        animation: textSpin 3s infinite;
    }
    @keyframes textSpin {
        0% { content: 'Spicing things up...'; }
        20% { content: 'Cooking up a roast...'; }
        40% { content: 'Grilling opinions...'; }
        60% { content: 'Serving up some heat...'; }
        80% { content: 'Dishing out sass...'; }
        100% { content: 'Basting in brilliance...'; }
    }
    </style>
""", unsafe_allow_html=True)

# Custom loading text animation function
def custom_spinner():
    loading_texts = ["Spicing things up...", "Cooking up a roast...", "Grilling opinions...", 
                     "Serving up some heat...", "Dishing out sass...", "Basting in brilliance..."]
    for _ in range(5):  
        for loading_text in loading_texts:
            st.spinner(loading_text)
            time.sleep(0.5)

# Main app logic
st.markdown("<h1 class='big-title'>Resume Roster</h1>", unsafe_allow_html=True)

query_params = st.query_params
roast_id = query_params.get("roast_id")

if roast_id:
    try:
        data = collection.find_one({"_id": roast_id})
        if data:
            st.markdown("<div class='content-box'>", unsafe_allow_html=True)
            st.subheader("Your Resume Roast")
            st.write(data["roast"])
            st.subheader("Improvement Tips")
            st.write(data["tips"])
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("Roast not found.")
    except Exception as e:
        st.error(f"Error fetching roast: {e}")
else:
    with st.container():
        uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"], help="Upload a PDF or DOCX file")
        
        if uploaded_file:
            resume_text = extract_text(uploaded_file)
            if resume_text:
                st.success("Resume uploaded successfully!", icon="✅")
                
                with st.spinner():
                    custom_spinner()  # Show loading animation

                    # Generate Roast and Tips
                    roast_prompt = f"Roast this resume with funny, sarcastic humor like a comedian: {resume_text}"
                    tips_prompt = f"Provide three specific improvement tips for this resume in a bulleted list: {resume_text}"
                    roast = generate_response(roast_prompt)
                    tips = generate_response(tips_prompt)

                    # Generate tweet link after roast is created
                    tweet_text = f"Just got my resume absolutely roasted!🔥😂'{roast[:100]}...'💀 Want to see how your resume holds up? Try it here: resume-roster.streamlit.app/"
                    tweet_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet_text)}"

                # Display the roast and tips
                st.markdown("<div class='content-box no-margin'>", unsafe_allow_html=True)
                st.subheader("Your Resume Roast")
                st.write(roast)
                st.subheader("Improvement Tips")
                st.write(tips)

                # Display "Share on X" button **only after roast is generated**
                st.markdown(f"""
                    <a href="{tweet_url}" target="_blank">
                        <button style="background-color: black; color: white; border: none; padding: 10px 20px; font-size: 16px; cursor: pointer;">
                            Share on X
                        </button>
                    </a>
                """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("Failed to extract text from the resume.")
        
        st.write("Want a detailed critique? Coming soon!")

# Add X handle and link at the bottom
st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        Created by <a href='https://x.com/MohitMahajan07' target='_blank'>@MohitMahajan07</a>
    </div>
""", unsafe_allow_html=True)
