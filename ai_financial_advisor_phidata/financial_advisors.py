from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from constants import model
import os
from dotenv import load_dotenv
load_dotenv()

financial_agent = Agent(
    name="Financial Analyst Agent",
    model=Groq(id=model, api_key=os.getenv("GROQ_API_KEY")),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True, 
            stock_fundamentals=True
        )
    ],
    show_tool_calls=True,
    markdown=True,
    instructions="""
    You are a financial analyst agent.
    You can answer questions about stock prices, analyst recommendations, and stock fundamentals.
    Use the tools provided to fetch the necessary data.
    Always create tables for comparative analysis.
    If you don't know the answer, say "I don't know".
    """,
)


web_researcher = Agent(
    name="Web Researcher Agent",
    model=Groq(id=model, api_key=os.getenv("GROQ_API_KEY")),
    tools=[
        DuckDuckGo(),
    ],
    show_tool_calls=True,
    markdown=True,
    instructions="""
    You are a web researcher agent.
    Always include the source of the information you provide.
    Use the tools provided to fetch the necessary data.
    If you don't know the answer, say "I don't know".
    """,
)


agents_team = Agent(
    team=[
        financial_agent,
        web_researcher,
    ],
    model=Groq(id=model, api_key=os.getenv("GROQ_API_KEY")),
    tools=[],
    show_tool_calls=True,
    markdown=True,
    instructions="""
    You are a team of agents.
    You have a financial analyst agent and a web researcher agent.
    Use the financial analyst agent for questions related to stock prices, analyst recommendations, and stock fundamentals.
    Use the web researcher agent for questions related to general web research.
    If you don't know the answer, say "I don't know".
    Always include the source of the information you provide.
    Always create tables for comparative analysis.
    """,
    debug_mode=True,
)

agents_team.print_response("Summarize the analyst recommendations and share latest information about tesla")

