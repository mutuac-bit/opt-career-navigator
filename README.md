# OPT Career Navigator

## What This Is
A three-agent AI pipeline that helps international students 
on F-1 STEM OPT find jobs that will sponsor them. Users enter 
their profile and target role, and three AI agents work 
sequentially to search, screen, and score real job postings.

## Live Demo
https://opt-career-navigator-mauvmvrdfx6mylxs7ptluo.streamlit.app/

## The Problem It Solves
International students waste hours applying to jobs that will 
never sponsor them. This tool searches real job boards, screens 
each posting for OPT/H-1B sponsorship signals, and ranks results 
by fit — in under 2 minutes.


## System Architecture
Three agents working sequentially:

### Agent 1 — Job Search Agent
- Model: llama-3.1-8b-instant, temperature=0.1
- Tool: Tavily web search
- Why this model: Fast and cheap — search only needs speed 
  and formatting, not deep reasoning
- Output: List of real job postings from Indeed, LinkedIn, 
  Glassdoor, ZipRecruiter

### Agent 2 — Sponsorship Screening Agent  
- Model: llama-3.3-70b-versatile, temperature=0.0
- Why this model: Visa risk assessment must be precise and 
  consistent — zero temperature eliminates randomness
- Output: GREEN/YELLOW/RED rating per posting with reasoning

### Agent 3 — Fit Scoring Agent
- Model: llama-3.3-70b-versatile, temperature=0.2
- Why this model: Nuanced scoring requires smarter model 
  with slight creativity for recommendations
- Output: 0-100 score per posting with breakdown and 
  application priority

## Agentic Pattern
Each agent receives the previous agent's output as context.
Sponsorship analysis feeds into fit scoring so final rankings
incorporate both skill match and visa risk. This creates 
reasoning impossible from a single prompt.

## Prompt Engineering Decisions
- Each agent has a dedicated system prompt with explicit 
  instructions and output format
- Sponsorship agent uses GREEN/YELLOW/RED classification 
  for clear signal
- Fit scoring agent breaks score into four components: 
  Skills (0-30), Role (0-30), Location (0-20), Sponsorship (0-20)
- All agents instructed to say "uncertain" rather than guess

## Grounding Strategy
- User profile collected via sidebar: visa status, skills, 
  experience, target role, target city
- Profile passed into all three agents as context
- Tavily search grounds Agent 1 in real current job postings

## Real Run Example
Search: Data Analyst in Atlanta
- Total postings found: 9
- Top result: Entry Level Data Analyst - Indeed
  - Fit Score: 76/100
  - Skill Match: 25/30
  - Role Match: 30/30
  - Location Match: 20/20
  - Sponsorship Score: 1/20 (uncertain)
  - Application Priority: HIGH
- Sponsorship Analysis: YELLOW (uncertain) for most postings
  due to search results being aggregator pages

## Iteration Log
- Draft: CrewAI framework — failed due to Python 3.14 
  incompatibility. Switched to manual agent pipeline.
- Draft: All agents used same model and temperature — 
  fixed by implementing model routing with documented reasoning.
- Draft: API keys missing from Streamlit Cloud — fixed by 
  adding secrets in Streamlit dashboard.
- Draft: crew.py existed but was never used — deleted.
- Draft: Tavily returning 0 results — fixed by simplifying 
  search queries and adding domain filtering.

## Tech Stack
- Python, Streamlit
- Groq API (llama-3.1-8b-instant, llama-3.3-70b-versatile)
- Tavily API (real-time web search)
- python-dotenv for key management
- Deployed on Streamlit Community Cloud
- Version controlled on GitHub

## Where It Works and Where It Breaks
### Works well
- Finds real current job postings from major job boards
- Sponsorship screening catches explicit visa language
- Fit scoring provides detailed breakdown per posting

### Limitations
- Search results are often aggregator pages not individual 
  postings, limiting sponsorship signal detection
- Cannot access paywalled job boards
- Sponsorship assessment is based on language signals only, 
  not verified USCIS data


C:\Users\User\OneDrive\Desktop\opt-career-navigator> 