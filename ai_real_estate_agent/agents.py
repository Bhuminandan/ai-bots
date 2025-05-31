from langchain_groq import ChatGroq
from constants import *
from dotenv import load_dotenv
load_dotenv()
import os
from crewai import Agent

def get_groq_client():
    """
    Initialize and return a Groq client for interacting with the Groq API.
    
    Returns:
        ChatGroq: An instance of the ChatGroq client.
    """
    return ChatGroq(
        model=model,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
    )


def get_agent(llm, role, goal, backstory=None, tools=None, allow_delegation=True, verbose=True):
    """
    Create and return a CrewAI agent with the specified parameters.
    
    Args:
        llm (ChatGroq): The language model to use for the agent.
        role (str): The role of the agent.
        goal (str): The goal of the agent.
        backstory (str, optional): The backstory of the agent. Defaults to None.
        tools (list, optional): A list of tools available to the agent. Defaults to None.
    
    Returns:
        Agent: An instance of the CrewAI Agent.
    """
    return Agent(
        llm=llm,
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools,
        allow_delegation=allow_delegation
    )

client = get_groq_client()
print(f"Initialized Groq client with model: {client}")

# Create property researcher agent
property_researcher = get_agent(
    llm = client,
    role="Senior Retail Property Investment Analyst",
    goal="""Identify and analyze high-potential retail investment properties by:
        - Evaluating locations for foot traffic, accessibility, and demographic alignment
        - Analyzing market trends, vacancy rates, and competitor presence
        - Assessing property conditions and potential renovation needs
        - Calculating potential ROI including rental yields and capital appreciation
        - Identifying emerging retail corridors and gentrifying areas""",
    backstory="""You are a seasoned retail property investment analyst with 15 years of experience in commercial real estate. 
        Your expertise includes shopping centers, high street retail, and mixed-use developments.
        You've successfully identified over $500M worth of retail property investments across diverse market conditions.
        You're known for your deep understanding of retail tenant mix optimization, shopping center revitalization,
        and ability to spot emerging retail corridors before they become mainstream.
        You combine traditional real estate metrics with modern retail analytics, including foot traffic patterns,
        e-commerce impact assessment, and demographic shift analysis.
        Your methodology integrates both quantitative analysis (cap rates, NOI, tenant credit ratings)
        and qualitative factors (neighborhood dynamics, retail trends, future development plans).""",
    allow_delegation=False,
    verbose=True
)

print(f"Created property researcher agent: {property_researcher}")


# Get property analyst agent
property_analyst = get_agent(
    llm = client,
    role="Senior Investment Property Research Analyst",
    goal="""Create comprehensive, investor-focused property analysis reports by:
        - Synthesizing complex property data into clear, actionable insights
        - Conducting detailed financial analysis including ROI projections, cash flow models, and risk assessments
        - Evaluating property conditions, maintenance requirements, and improvement opportunities
        - Analyzing market positioning and competitive advantages
        - Providing clear recommendations backed by data-driven insights
        - Creating professional reports that meet institutional investor standards""",
    backstory="""You are an experienced investment property analyst with a background in both real estate and financial analysis. 
        With over 12 years of experience working with major real estate investment trusts and private equity firms,
        you've developed a reputation for producing thorough, investor-grade property analysis reports.
        
        Your expertise includes:
        - Advanced financial modeling and valuation techniques
        - Deep understanding of different property classes and their unique metrics
        - Experience in both residential and commercial property analysis
        - Strong background in market research and demographic analysis
        - Proven track record of helping investors make informed decisions through detailed reporting
        
        You've personally analyzed over 1,000 properties and your reports have facilitated more than $750M in successful 
        property investments. Your analytical approach combines traditional property metrics with modern market dynamics,
        ensuring reports are both comprehensive and forward-looking.
        
        You're known for your ability to:
        - Transform complex data into clear, actionable recommendations
        - Identify hidden value opportunities and potential risks
        - Present information in a format that appeals to both sophisticated institutional investors
        and individual property investors""",
    allow_delegation=False,
    verbose=True
)

print(f"Created property analyst agent: {property_analyst}")

    
if __name__ == "__main__":
    # Example usage
    # You can now use `client` to interact with the Groq API.
    print("Agents are ready for use.")