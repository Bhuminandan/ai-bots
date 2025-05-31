from pydantic import BaseModel
from crewai import Task
from agents import property_researcher

class ResearchOutput(BaseModel):
    market_analysis: str
    top_investments: list[str]
    financial_projections: str
    risk_assessment: str
    recommendations: str

research_task = Task(
    description="""Conduct a comprehensive analysis of potential retail property investments...""",
    agent=property_researcher,
    expected_output="""Detailed report...""",
    output_json=ResearchOutput 
)

analysis_task = Task(
    description="""Analyze the financial viability of the top retail properties identified...""",
    agent=property_researcher,
    expected_output="""Financial analysis report...""",
    output_json=ResearchOutput
)