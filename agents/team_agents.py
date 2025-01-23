import os
from dotenv import load_dotenv

# Phidata
from phi.agent import Agent
from phi.model.google import Gemini

# Tools
from phi.tools.googlesearch import GoogleSearch
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.tools.firecrawl import FirecrawlTools

load_dotenv()

# Load API keys
gemini_api_key = os.getenv("GOOGLE_API_KEY")
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

def initialize_agents(debug_mode=False):
    """Initialize and return all agents"""
    search_agent = Agent(
        name="Search Agent",
        tools=[GoogleSearch(), DuckDuckGo()],
        model=Gemini(id="gemini-2.0-flash-exp", api_key=gemini_api_key),
        # debug_mode=True,
        markdown=True,
    )

    finance_agent = Agent(
        name="Finance Agent",
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True)],
        model=Gemini(id="gemini-2.0-flash-exp", api_key=gemini_api_key),
        # debug_mode=True,
        markdown=True,
    )

    scraping_agent = Agent(
        name="Scraping Agent",
        tools=[FirecrawlTools(scrape=True, api_key=firecrawl_api_key)],
        model=Gemini(id="gemini-2.0-flash-exp", api_key=gemini_api_key),
        # debug_mode=True,
        markdown=True,
    )

    coordinator_agent = Agent(
        name="Coordinator Agent",
        instructions=[
            "Combine information from specialized agents to provide comprehensive answers",
            "Give a high-level explanation followed by a low-level explanation",
            "Provide real-world examples, especially within the context of Africa; otherwise, use a global context",
        ],
        # debug_mode=True,
        markdown=True,
        model=Gemini(id="gemini-2.0-flash-exp", api_key=gemini_api_key),
    )

    return {
        "search_agent": search_agent,
        "finance_agent": finance_agent,
        "scraping_agent": scraping_agent,
        "coordinator_agent": coordinator_agent
    }

def run_team(query: str, agents):
    """Process query through all agents and return final response"""
    search_results = agents["search_agent"].run(query)
    finance_results = agents["finance_agent"].run(query)
    scraping_results = agents["scraping_agent"].run(query)

    combined_results = f"""
    Search Results: {search_results.content}
    Finance Results: {finance_results.content}
    Scraping Results: {scraping_results.content}
    """
    
    final_response = agents["coordinator_agent"].run(combined_results)
    return final_response.content