#SERPER_API_KEY=""

from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool

# Setup the tool for internet searching capabilities
google_search_tool = SerperDevTool()


