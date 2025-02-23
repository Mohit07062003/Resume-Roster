
# import streamlit as st
# import pdfplumber
# from docx import Document
# import uuid
# from astrapy import DataAPIClient
# from dotenv import load_dotenv
# import os
# from langchain_community.llms import HuggingFaceHub
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# # Load environment variables
# load_dotenv()

# # Set up AstraDB connection
# @st.cache_resource
# def get_db_collection():
#     token = os.getenv("ASTRA_TOKEN")
#     client = DataAPIClient(token)
#     db = client.get_database_by_api_endpoint(
#         "https://4507fefd-398c-4604-bde7-dfd354ce1c30-us-east-2.apps.astra.datastax.com"
#     )
#     try:
#         collection = db.create_collection("roasts", dimension=1536)  # Optional vector dimension
#     except Exception:
#         collection = db.get_collection("roasts")
#     return collection

# collection = get_db_collection()

# # Set up Hugging Face with LangChain
# hf_api_token = os.getenv("HF_API_TOKEN")
# llm = HuggingFaceHub(
#     repo_id="google/flan-t5-large",
#     huggingfacehub_api_token=hf_api_token,
#     model_kwargs={"temperature": 0.7, "max_length": 200}  # Adjust creativity and length
# )

# # Define prompts
# roast_prompt = PromptTemplate(
#     input_variables=["resume"],
#     template="Roast this resume in detail. Go full throttle. Bully as much as you can : {resume}"
# )
# tips_prompt = PromptTemplate(
#     input_variables=["resume"],
#     template="Provide three improvement tips for the resume given below, check for correct action words: {resume}"
# )

# # Create chains
# roast_chain = LLMChain(llm=llm, prompt=roast_prompt)
# tips_chain = LLMChain(llm=llm, prompt=tips_prompt)

# # Resume text extraction
# def extract_text(file):
#     if file.type == "application/pdf":
#         with pdfplumber.open(file) as pdf:
#             text = "".join([page.extract_text() for page in pdf.pages])
#     elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#         doc = Document(file)
#         text = "\n".join([para.text for para in doc.paragraphs])
#     else:
#         st.error("Unsupported file type. Please upload a PDF or DOCX.")
#         return None
#     return text

# # Main app logic
# query_params = st.query_params
# roast_id = query_params.get("roast_id")

# if roast_id:
#     try:
#         data = collection.find_one({"_id": roast_id})
#         if data:
#             st.subheader("Your Resume Roast")
#             st.write(data["roast"])
#             st.subheader("Improvement Tips")
#             st.write(data["tips"])
#         else:
#             st.error("Roast not found.")
#     except Exception as e:
#         st.error(f"Error fetching roast: {e}")
# else:
#     uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
#     if uploaded_file:
#         resume_text = extract_text(uploaded_file)
#         if resume_text:
#             st.success("Resume uploaded successfully!")
#             with st.spinner("Generating your roast and tips..."):
#                 roast = roast_chain.run(resume_text)
#                 tips = tips_chain.run(resume_text)
#             st.subheader("Your Resume Roast")
#             st.write(roast)
#             st.subheader("Improvement Tips")
#             st.write(tips)
#             if st.button("Save and Share"):
#                 roast_id = str(uuid.uuid4())
#                 collection.insert_one({
#                     "_id": roast_id,
#                     "resume_text": resume_text,
#                     "roast": roast,
#                     "tips": tips
#                 })
#                 share_url = f"https://your-app-name.streamlit.app?roast_id={roast_id}"
#                 st.markdown(f"Share this link: [{share_url}]({share_url})")
#     st.write("Want a detailed critique? Coming soon!")


# import streamlit as st
# import pdfplumber
# from docx import Document
# import uuid
# from astrapy import DataAPIClient
# from dotenv import load_dotenv
# import os
# from langchain_community.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# # Load environment variables
# load_dotenv()

# # Set up AstraDB connection
# @st.cache_resource
# def get_db_collection():
#     token = os.getenv("ASTRA_TOKEN")
#     client = DataAPIClient(token)
#     db = client.get_database_by_api_endpoint(
#         "https://4507fefd-398c-4604-bde7-dfd354ce1c30-us-east-2.apps.astra.datastax.com"
#     )
#     try:
#         collection = db.create_collection("roasts", dimension=1536)  # Optional vector dimension
#     except Exception:
#         collection = db.get_collection("roasts")
#     return collection

# collection = get_db_collection()

# # Set up Langchain with OpenAI
# openai_api_key = os.getenv("OPENAI_API_KEY")
# llm = OpenAI(api_key=openai_api_key)

# # Define prompts
# roast_prompt = PromptTemplate(
#     input_variables=["resume"],
#     template="Give a funny and sarcastic roast of this resume: {resume}"
# )
# tips_prompt = PromptTemplate(
#     input_variables=["resume"],
#     template="Provide three specific improvement tips for this resume in a bulleted list: {resume}"
# )

# # Create chains
# roast_chain = LLMChain(llm=llm, prompt=roast_prompt)
# tips_chain = LLMChain(llm=llm, prompt=tips_prompt)

# # Resume text extraction
# def extract_text(file):
#     if file.type == "application/pdf":
#         with pdfplumber.open(file) as pdf:
#             text = "".join([page.extract_text() for page in pdf.pages])
#     elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#         doc = Document(file)
#         text = "\n".join([para.text for para in doc.paragraphs])
#     else:
#         st.error("Unsupported file type. Please upload a PDF or DOCX.")
#         return None
#     return text

# # Main app logic
# query_params = st.query_params
# roast_id = query_params.get("roast_id")

# if roast_id:
#     try:
#         data = collection.find_one({"_id": roast_id})
#         if data:
#             st.subheader("Your Resume Roast")
#             st.write(data["roast"])
#             st.subheader("Improvement Tips")
#             st.write(data["tips"])
#         else:
#             st.error("Roast not found.")
#     except Exception as e:
#         st.error(f"Error fetching roast: {e}")
# else:
#     uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
#     if uploaded_file:
#         resume_text = extract_text(uploaded_file)
#         if resume_text:
#             st.success("Resume uploaded successfully!")
#             with st.spinner("Generating your roast and tips..."):
#                 roast = roast_chain.run(resume_text)
#                 tips = tips_chain.run(resume_text)
#             st.subheader("Your Resume Roast")
#             st.write(roast)
#             st.subheader("Improvement Tips")
#             st.write(tips)
#             if st.button("Save and Share"):
#                 roast_id = str(uuid.uuid4())
#                 collection.insert_one({
#                     "_id": roast_id,
#                     "resume_text": resume_text,
#                     "roast": roast,
#                     "tips": tips
#                 })
#                 share_url = f"https://your-app-name.streamlit.app?roast_id={roast_id}"
#                 st.markdown(f"Share this link: [{share_url}]({share_url})")
#     st.write("Want a detailed critique? Coming soon!")

import streamlit as st
import pdfplumber
from docx import Document
import uuid
from astrapy import DataAPIClient
from dotenv import load_dotenv
import os
import requests
import time

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

# Hugging Face Inference API setup
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MODEL = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"  # Adjust if needed
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def generate_response(prompt, max_retries=5, wait_seconds=10):
    for attempt in range(max_retries):
        payload = {
            "inputs": prompt,
            "parameters": {"max_length": 200, "temperature": 0.6}
        }
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        elif "Model too busy" in response.text:
            st.warning(f"Model is busy, retrying in {wait_seconds} seconds... (Attempt {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:  # Don’t wait after the last attempt
                time.sleep(wait_seconds)
        else:
            st.error(f"API Error: {response.text}")
            return "Oops, the roast machine broke!"
    st.error("Gave up after max retries. The model’s too busy—try again later!")
    return "Sorry, the roast chef’s on a break!"

# Resume text extraction
def extract_text(file):
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            text = "".join([page.extract_text() for page in pdf.pages])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX.")
        return None
    return text

# Main app logic
query_params = st.query_params
roast_id = query_params.get("roast_id")

if roast_id:
    try:
        data = collection.find_one({"_id": roast_id})
        if data:
            st.subheader("Your Resume Roast")
            st.write(data["roast"])
            st.subheader("Improvement Tips")
            st.write(data["tips"])
        else:
            st.error("Roast not found.")
    except Exception as e:
        st.error(f"Error fetching roast: {e}")
else:
    uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
    if uploaded_file:
        resume_text = extract_text(uploaded_file)
        if resume_text:
            st.success("Resume uploaded successfully!")
            with st.spinner("Generating your roast and tips... This might take a bit if the model’s busy!"):
                roast_prompt = f"Roast this resume with funny, sarcastic humor like a comedian: {resume_text}"
                tips_prompt = f"Provide three specific improvement tips for this resume in a bulleted list: {resume_text}"
                roast = generate_response(roast_prompt)
                tips = generate_response(tips_prompt)
            st.subheader("Your Resume Roast")
            st.write(roast)
            st.subheader("Improvement Tips")
            st.write(tips)
            if st.button("Save and Share"):
                roast_id = str(uuid.uuid4())
                collection.insert_one({
                    "_id": roast_id,
                    "resume_text": resume_text,
                    "roast": roast,
                    "tips": tips
                })
                share_url = f"https://your-app-name.streamlit.app?roast_id={roast_id}"
                st.markdown(f"Share this link: [{share_url}]({share_url})")
    st.write("Want a detailed critique? Coming soon!")