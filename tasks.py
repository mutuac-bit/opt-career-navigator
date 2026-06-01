"""
OPT Career Navigator - CrewAI Tasks
Three sequential tasks that build on each other's outputs.
"""

from crewai import Task
from crewai_tools import tool
import os
from tavily import TavilyClient

# Initialize Tavily client for web search
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY environment variable not set")

tavily_client = TavilyClient(api_key=tavily_api_key)


# ============================================================================
# TAVILY SEARCH TOOL
# ============================================================================

@tool
def search_jobs_tavily(query: str) -> str:
    """
    Search for job postings using Tavily web search.
    Query should be specific like: "Data Scientist jobs Atlanta F-1 OPT sponsorship"
    """
    try:
        results = tavily_client.search(
            query=query,
            max_results=10,
            include_answer=True,
        )
        
        # Format results into readable text
        formatted_results = f"Search Query: {query}\n\n"
        formatted_results += f"Answer: {results.get('answer', 'No direct answer')}\n\n"
        formatted_results += "Job Postings Found:\n"
        
        for i, result in enumerate(results.get("results", []), 1):
            formatted_results += f"\n{i}. {result.get('title', 'No title')}\n"
            formatted_results += f"   URL: {result.get('url', 'N/A')}\n"
            formatted_results += f"   Source: {result.get('source', 'N/A')}\n"
            formatted_results += f"   Content: {result.get('content', 'N/A')[:500]}\n"
        
        return formatted_results
    except Exception as e:
        return f"Error searching jobs: {str(e)}"


# ============================================================================
# TASK 1: JOB SEARCH TASK
# ============================================================================

task_search_jobs = Task(
    description=(
        "Search for current job postings using Tavily. Search for:\n"
        "1. Data Analyst jobs in Atlanta, Austin, Raleigh-Durham, Washington D.C.\n"
        "2. Data Engineer jobs in the same cities\n"
        "3. Data Scientist jobs in the same cities\n"
        "Each search should include terms like 'F-1 OPT sponsorship' or 'visa sponsorship'.\n"
        "Compile a comprehensive list of 8-15 of the most promising current openings.\n"
        "Include job title, company, location, key requirements, and posting URL for each."
    ),
    expected_output=(
        "A structured list of 8-15 current job postings with:\n"
        "- Job Title\n"
        "- Company Name\n"
        "- Location\n"
        "- Key Skills Required\n"
        "- Visa Sponsorship Mention (if any)\n"
        "- URL\n"
        "- Brief Description"
    ),
    tools=[search_jobs_tavily],
    agent=None,  # Will be set in crew.py
)


# ============================================================================
# TASK 2: SPONSORSHIP SCREENING TASK
# ============================================================================

task_screen_sponsorship = Task(
    description=(
        "Analyze each job posting from the previous search results for visa sponsorship likelihood.\n"
        "For each job, assess:\n"
        "1. Explicit visa sponsorship mentions in posting\n"
        "2. Company size and industry (larger companies more likely to sponsor)\n"
        "3. Known visa sponsorship track record (tech companies, finance, etc.)\n"
        "4. Geographic location (major tech hubs more likely to sponsor)\n"
        "5. Role seniority (roles requiring experience more likely to sponsor)\n\n"
        "Rate each as GREEN (likely sponsors OPT+H1B), YELLOW (uncertain), or RED (unlikely to sponsor).\n"
        "Provide reasoning for each rating. "
        "Focus especially on OPT sponsorship for immediate work and H-1B sponsorship within 3 years."
    ),
    expected_output=(
        "For each job posting:\n"
        "- Job Title & Company\n"
        "- Sponsorship Risk Rating: GREEN / YELLOW / RED\n"
        "- OPT Sponsorship Likelihood: High/Medium/Low\n"
        "- H-1B Sponsorship Likelihood: High/Medium/Low\n"
        "- Key Sponsorship Signals Found\n"
        "- Risk Assessment Reasoning\n"
        "- Confidence Level: High/Medium/Low"
    ),
    agent=None,  # Will be set in crew.py
)


# ============================================================================
# TASK 3: FIT SCORING TASK
# ============================================================================

task_fit_scoring = Task(
    description=(
        "Score each remaining job posting 0-100 based on fit with the candidate's profile.\n"
        "The candidate is an F-1 STEM OPT holder (MS Data Science, graduating Dec 2026) with skills in:\n"
        "Python, R, SQL, Power BI, ETL, Machine Learning.\n"
        "Target roles: Data Analyst, Data Engineer, Data Scientist\n"
        "Target cities: Atlanta, Austin, Raleigh-Durham, Washington D.C.\n\n"
        "Scoring components:\n"
        "- Skill Match (0-30): How well job requirements align with candidate's skills\n"
        "- Role Match (0-30): How well role aligns with target roles and career goals\n"
        "- Location Match (0-20): Whether in target cities\n"
        "- Sponsorship (0-20): Likelihood company sponsors OPT and H-1B\n\n"
        "Provide detailed reasoning for each component. Scores 70+ are strong fits and priority applications."
    ),
    expected_output=(
        "Ranked list of jobs (highest score first) with:\n"
        "- Job Title & Company\n"
        "- Overall Fit Score: XX/100\n"
        "- Skill Match: XX/30 (skills match: list aligned skills)\n"
        "- Role Match: XX/30 (role alignment reasoning)\n"
        "- Location Match: XX/20 (in/near target city?)\n"
        "- Sponsorship Score: XX/20 (visa sponsorship likelihood)\n"
        "- Top 3 Reasons to Apply\n"
        "- Potential Gaps or Concerns\n"
        "- Application Priority: HIGH / MEDIUM / LOW"
    ),
    agent=None,  # Will be set in crew.py
)


def get_tasks():
    """Return all three tasks for use in the crew"""
    return {
        "search": task_search_jobs,
        "sponsorship": task_screen_sponsorship,
        "fit_scoring": task_fit_scoring,
    }
