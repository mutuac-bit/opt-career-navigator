"""
OPT Career Navigator - Manual Multi-Agent Pipeline
Three agent functions for job search, sponsorship screening, and fit scoring.
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()

# Initialize API clients
groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY environment variable not set")

groq_client = Groq(api_key=groq_api_key)
tavily_client = TavilyClient(api_key=tavily_api_key)

# ============================================================================
# PROFILE DEFINITION - Hardcoded for F-1 STEM OPT Student
# ============================================================================

STUDENT_PROFILE = {
    "name": "F-1 STEM OPT Candidate",
    "visa_status": "F-1 STEM OPT",
    "education": "MS Data Science, Grand Valley State University",
    "graduation": "December 2026",
    "opt_start_date": "January 2024",
    "opt_end_date": "January 2027",
    "h1b_timeline": "Within 3 years",
    "work_authorized": "OPT eligible now, H-1B sponsorship required within 3 years",
    "skills": ["Python", "R", "SQL", "Power BI", "ETL", "Machine Learning", "Data Visualization"],
    "target_cities": ["Atlanta", "Austin", "Raleigh-Durham", "Washington D.C."],
    "target_roles": ["Data Analyst", "Data Engineer", "Data Scientist"],
    "preferred_company_size": ["Startup", "Mid-size", "Enterprise"],
    "requirements": {
        "must_sponsor_opt": True,
        "h1b_sponsorship": "Required within 3 years",
        "remote_friendly": False,
        "visa_sponsorship_proven": True,
    },
}


def get_student_profile():
    """Return the hardcoded student profile"""
    return STUDENT_PROFILE


# ============================================================================
# AGENT 1: SEARCH AGENT
# ============================================================================

def search_agent(role: str, city: str, profile: dict) -> str:
    """
    Search Agent: Uses Tavily to search for real job postings matching the profile.
    
    Args:
        role: Target job role (e.g., "Data Scientist", "Data Analyst", "Data Engineer")
        city: Target city (e.g., "Atlanta", "Austin", "Washington D.C.")
        profile: User-defined candidate profile dictionary
    
    Returns:
        str: Formatted search results with job postings
    """
    
    print(f"\n🔍 Search Agent: Searching for {role} positions in {city}...")
    
    # Primary search: keep query simple and avoid visa/sponsorship language
    primary_query = f"{role} jobs {city}"

    all_results = []
    seen_urls = set()

    try:
        results = tavily_client.search(
            query=primary_query,
            search_depth="basic",
            max_results=10,
            include_domains=["indeed.com", "linkedin.com", "glassdoor.com", "ziprecruiter.com"],
        )
        print(f"Raw Tavily response for query '{primary_query}':\n{json.dumps(results, indent=2, default=str)}\n")

        results_list = results.get("results", []) if isinstance(results, dict) else (results if isinstance(results, list) else [])

        for result in results_list:
            url = result.get("url", "N/A")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            all_results.append({
                "title": result.get("title", "No title"),
                "url": url,
                "content": result.get("content", ""),
                "source": result.get("source", "N/A"),
            })

    except Exception as e:
        print(f"Error in primary search query '{primary_query}': {str(e)}")
        results_list = []

    # Fallback: if no results, try a second, broader query and combine
    if len(results_list) == 0:
        fallback_query = f"{role} {city} hiring 2025"
        try:
            fb_results = tavily_client.search(
                query=fallback_query,
                search_depth="basic",
                max_results=10,
                include_domains=["indeed.com", "linkedin.com", "glassdoor.com", "ziprecruiter.com"],
            )
            print(f"Raw Tavily response for fallback query '{fallback_query}':\n{json.dumps(fb_results, indent=2, default=str)}\n")

            fb_list = fb_results.get("results", []) if isinstance(fb_results, dict) else (fb_results if isinstance(fb_results, list) else [])

            for result in fb_list:
                url = result.get("url", "N/A")
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                all_results.append({
                    "title": result.get("title", "No title"),
                    "url": url,
                    "content": result.get("content", ""),
                    "source": result.get("source", "N/A"),
                })

        except Exception as e:
            print(f"Error in fallback search query '{fallback_query}': {str(e)}")
    
    # Format results for next agent
    # Fast lightweight model (llama-3.1-8b-instant, temp=0.1) - search only needs speed and formatting, not deep reasoning
    formatted_output = f"SEARCH RESULTS FOR: {role} in {city}\n"
    formatted_output += f"Total Postings Found: {len(all_results)}\n"
    formatted_output += "="*80 + "\n\n"
    
    for idx, job in enumerate(all_results, 1):
        formatted_output += f"{idx}. {job['title']}\n"
        formatted_output += f"   URL: {job['url']}\n"
        formatted_output += f"   Source: {job['source']}\n"
        formatted_output += f"   Content Preview: {job['content'][:300]}\n\n"
    
    print(f"✅ Search Agent: Found {len(all_results)} job postings")
    return formatted_output


# ============================================================================
# AGENT 2: SPONSORSHIP AGENT
# ============================================================================

def sponsorship_agent(job_results: str, profile: dict) -> str:
    """
    Sponsorship Agent: Uses Groq to analyze job postings for OPT/H-1B sponsorship signals.
    Returns GREEN (likely sponsors), YELLOW (uncertain), or RED (unlikely to sponsor).
    
    Args:
        job_results: Formatted job search results from search_agent
        profile: User-defined candidate profile dictionary
    
    Returns:
        str: Sponsorship screening analysis with GREEN/YELLOW/RED ratings
    """
    
    print("\n📋 Sponsorship Agent: Analyzing job postings for visa sponsorship signals...")
    
    system_prompt = f"""You are a visa sponsorship expert with deep knowledge of OPT and H-1B requirements. 
You've helped hundreds of international students identify companies most likely to sponsor their visas. 
You analyze job postings, company reputation, and industry trends to assess visa sponsorship likelihood. 
You look for explicit sponsorship mentions, company size, industry, recent H-1B filings, and recruiter signals. 

Student Profile Context:
{json.dumps(profile, indent=2)}

For each job posting provided, you MUST:
1. Rate sponsorship likelihood as GREEN (likely sponsors both OPT+H1B), YELLOW (uncertain), or RED (unlikely)
2. Assess OPT sponsorship likelihood: High/Medium/Low
3. Assess H-1B sponsorship likelihood: High/Medium/Low
4. Identify key sponsorship signals found
5. Provide risk assessment reasoning
6. Rate confidence level: High/Medium/Low

Focus especially on OPT sponsorship for immediate work and H-1B sponsorship within 3 years."""
    
    user_prompt = f"""Analyze the following job postings for visa sponsorship likelihood:

{job_results}

For each job, provide a detailed sponsorship analysis with the rating categories mentioned in my instructions."""
    
    try:
        response = groq_client.chat.completions.create(
            # Precision model - visa risk assessment must be consistent and accurate, zero temperature
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            max_tokens=4096,
        )
        
        sponsorship_analysis = response.choices[0].message.content
        print("✅ Sponsorship Agent: Analysis complete")
        return sponsorship_analysis
    
    except Exception as e:
        error_msg = f"Error in sponsorship analysis: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


# ============================================================================
# AGENT 3: FIT SCORING AGENT
# ============================================================================

def fit_scoring_agent(job_results: str, sponsorship_analysis: str, profile: dict) -> str:
    """
    Fit Scoring Agent: Uses Groq to score each job 0-100 based on profile match.
    
    Scoring components:
    - Skill Match (0-30): How well job requirements align with candidate's skills
    - Role Match (0-30): How well role aligns with target roles and career goals
    - Location Match (0-20): Whether in target cities
    - Sponsorship (0-20): Likelihood company sponsors OPT and H-1B
    
    Args:
        job_results: Formatted job search results from search_agent
        sponsorship_analysis: Sponsorship screening from sponsorship_agent
        profile: User-defined candidate profile dictionary
    
    Returns:
        str: Ranked list of jobs with fit scores and application priority
    """
    
    print("\n⭐ Fit Scoring Agent: Scoring jobs against candidate profile...")
    
    system_prompt = f"""You are an expert career coach specializing in data science and analytics roles. 
You understand skill requirements, career progression, and what makes an ideal fit for international students. 
You know this candidate deeply:

{json.dumps(profile, indent=2)}

You score jobs based on these components:
1. Skill Match (0-30): How well job requirements align with candidate's skills ({', '.join(profile.get('skills', []))})
2. Role Match (0-30): How well role aligns with target roles ({profile.get('target_role', '')})
3. Location Match (0-20): Whether in target cities ({profile.get('target_city', '')})
4. Sponsorship Score (0-20): OPT and H-1B sponsorship capability

For each job:
- Provide Overall Fit Score (0-100)
- Break down component scores
- List Top 3 Reasons to Apply
- Identify Potential Gaps or Concerns
- Assign Application Priority: HIGH / MEDIUM / LOW

A score of 70+ means this candidate is a strong fit and should apply immediately.
Rank all jobs by overall score (highest first)."""
    
    user_prompt = f"""Here are the job search results and sponsorship analysis.
Score each job based on fit with the candidate's profile and provide a ranked list.

JOB SEARCH RESULTS:
{job_results}

SPONSORSHIP ANALYSIS:
{sponsorship_analysis}

Provide a comprehensive ranked list with detailed scoring for each job."""
    
    try:
        response = groq_client.chat.completions.create(
            # Reasoning model - scoring nuance requires smarter model with slight creativity for recommendations
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=4096,
        )
        
        fit_scores = response.choices[0].message.content
        print("✅ Fit Scoring Agent: Scoring complete")
        return fit_scores
    
    except Exception as e:
        error_msg = f"Error in fit scoring: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


# ============================================================================
# PIPELINE ORCHESTRATOR
# ============================================================================

def run_job_search_pipeline(role: str, city: str, profile: dict) -> dict:
    """
    Execute the complete job search pipeline sequentially.
    
    Args:
        role: Target job role
        city: Target city
        profile: User-defined candidate profile dictionary
    
    Returns:
        dict: Pipeline results with all three agents' outputs
    """

    print(f"\n{'='*80}")
    print(f"OPT Career Navigator - Job Search Pipeline")
    print(f"{'='*80}")
    print(f"Role: {role}")
    print(f"City: {city}")
    print(f"{'='*80}")
    
    try:
        # Step 1: Search for jobs
        search_results = search_agent(role, city, profile)
        
        # Step 2: Screen for sponsorship
        sponsorship_results = sponsorship_agent(search_results, profile)
        
        # Step 3: Score fit
        fit_scores = fit_scoring_agent(search_results, sponsorship_results, profile)
        
        pipeline_result = {
            "status": "success",
            "role": role,
            "city": city,
            "search_results": search_results,
            "sponsorship_analysis": sponsorship_results,
            "fit_scores": fit_scores,
            "profile": profile,
        }
        
        print("\n✅ Pipeline complete!")
        return pipeline_result
    
    except Exception as e:
        error_result = {
            "status": "error",
            "role": role,
            "city": city,
            "error": str(e),
        }
        print(f"\n❌ Pipeline error: {str(e)}")
        return error_result


if __name__ == "__main__":
    # Example usage
    results = run_job_search_pipeline(
        role="Data Scientist",
        city="Atlanta"
    )
    
    print("\n" + "="*80)
    print("SEARCH RESULTS")
    print("="*80)
    print(results["search_results"])
    
    print("\n" + "="*80)
    print("SPONSORSHIP ANALYSIS")
    print("="*80)
    print(results["sponsorship_analysis"])
    
    print("\n" + "="*80)
    print("FIT SCORES")
    print("="*80)
    print(results["fit_scores"])
