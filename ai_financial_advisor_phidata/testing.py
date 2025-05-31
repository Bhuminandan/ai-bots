from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from constants import model
import os
from dotenv import load_dotenv
load_dotenv()


def get_company_symbols(company : str) -> str:
    """
    Returns the stock symbol for a given company name.
    """
    company_symbols = {
        "bhumi": "AAPL",
        "tesla": "TSLA",
        "google": "GOOGL",
        "microsoft": "MSFT",
        "amazon": "AMZN"
    }
    return company_symbols.get(company.lower(), None)

agent = Agent(
    model=Groq(id=model, api_key=os.getenv("GROQ_API_KEY")),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True, 
            stock_fundamentals=True
        ),
        get_company_symbols
    ],
    show_tool_calls=True,
    markdown=True,
    instructions="""
    You are a financial analyst agent.
    Always get symbols for companies using the get_company_symbols tool. 
    For example, if the user asks about "bhumi", use the get_company_symbols(bhumi) tool to get "AAPL"
    and use it for further queries.
    You can answer questions about stock prices, analyst recommendations, and stock fundamentals.
    Use the tools provided to fetch the necessary data.
    Always create tables for comparative analysis.
    If you don't know the answer, say "I don't know".
    """,
    debug_mode=True,
)

# Test the agent with a simple prompt
agent.print_response("Summarize the analyst recommendations for bhumi and tesla.")