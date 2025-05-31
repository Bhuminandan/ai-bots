import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
import chromadb
import csv
import uuid


# Import dotenv to load environment variables
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

st.title("Enter Url")

url = st.text_input("Enter job posting URL", placeholder="https://example.com/job-posting")
if not url:
    st.warning("Please enter a job posting URL to proceed.")
    st.stop()

# Scraping the job posting URL
loader = WebBaseLoader(url)
page_data = None
try:
    page_data = loader.load()
except Exception as e:
    st.error(f"An error occurred while loading the URL: {e}")
    st.write("Please check the URL and try again.")

# Sending this data to LLM to get skills and experience

# # Initialize the LLM with Groq
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

# Writing system prompt for the LLM 

prompt_extract = PromptTemplate.from_template(
    """
    I will give you scraped text from the job posting. 
    Your job is to extract the job details & requirements in a JSON format containing the following keys: 'role', 'experience', 'skills', and 'description'. 
    Only return valid JSON. No preamble, please.
    Here is the scraped text: {page_data}
    """
)

chain = prompt_extract | llm

response = chain.invoke(input={"page_data" : page_data})
print(response.content)
print(type(response.content))

# Parsing the response
parser = JsonOutputParser()
try:
    parsed_response = parser.parse(response.content)
except Exception as e:
    st.error(f"An error occurred while parsing the response: {e}")

# Extract csv data
def extract_csv_data(file_path):
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)

            for row in csv_reader:
                skills = tuple(row[:-1]) 
                project_link = row[-1]
                data.append({
                    "skills": skills,
                    "project_link": project_link
                })
        return data
    except Exception as e:
        st.error(f"An error occurred while reading the CSV file: {e}")
    return data


# Load the CSV data
csv_file_path = "sample_portfolio.csv"
csv_data = extract_csv_data(csv_file_path)



# Create chromadb and collection to store company potfolio
client = chromadb.PersistentClient()
collection = client.get_or_create_collection("company_portfolio")

if not collection.count():
    for skills, project_link in csv_data:
        collection.add(
            documents=str(skills),
            metadatas={"project_link": project_link},
            ids=[str(uuid.uuid4())]
        )

# Displaying the company portfolio
project_urls = collection.query(
    query_texts=[str(parsed_response['skills'])],
    n_results=2,
)

# Writing email prompt for the LLM
email_prompt = PromptTemplate.from_template(
    """
    I will give you a role and a task that you have to perform in that specific role.
    Your Role: Your name is Hassan, You are an incredible business development officer who knows how to get clients. You work for X Consulting firm, your firm works with all sorts of IT clients and provide solutions in the domain of Data Science and AI. 
    X AI focuses on efficient tailored solutions for all clients keeping costs down. 
    Your Job: Your Job is to write cold emails to clients regarding the Job openings that they have advertised. Try to pitch your clients with an email hook that opens a conversation about a possibility of working with them. Add the most relevant portfolio URLs from
    the following (shared below) to showcase that we have the right expertise to get the job done. 
    I will now provide you with the Job description and the portfolio URLs:
    No preamble, just write the email in a professional tone.
    JOB DESCRIPTION: {job_description}
    ------
    PORTFOLIO URLS: {project_urls}
    """
)
chain_email = email_prompt | llm

res = chain_email.invoke({"job_description" : parsed_response["description"], "project_urls" :project_urls })
st.subheader("Generated Email")
st.code(res.content)
