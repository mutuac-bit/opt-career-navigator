#  OPT Career Navigator

An agentic job search system designed for international students on F-1 STEM OPT. Uses CrewAI, Groq, and Tavily to search for jobs, screen for visa sponsorship, and score positions based on your profile.

##  Overview

**OPT Career Navigator** is a multi-agent AI pipeline that helps F-1 STEM OPT students find job opportunities that:
-  Sponsor **OPT work authorization immediately**
-  Offer **H-1B visa sponsorship within 3 years**
-  Match your **skills and career goals**
-  Are located in your **target cities**

### Use Case
You're an F-1 STEM OPT student (MS Data Science, graduating Dec 2026) with skills in Python, R, SQL, Power BI, ETL, and ML. You need to find roles in Atlanta, Austin, Raleigh-Durham, or Washington D.C. that will sponsor both your OPT and future H-1B visa.

---

## 🏗️ Architecture

The system uses three specialized AI agents working sequentially:

### 1. **Job Search Agent** 🔍
- **Role:** Find current job postings
- **Tools:** Tavily web search
- **Output:** 8-15 relevant job postings with titles, companies, requirements, locations, and URLs
- **Focus:** Data roles (Analyst, Engineer, Scientist) in target cities with sponsorship signals

### 2. **Sponsorship Screening Agent** 📋
- **Role:** Analyze visa sponsorship likelihood
- **Input:** Job postings from Agent 1
- **Output:** Sponsorship risk ratings (🟢 Green/🟡 Yellow/🔴 Red)
- **Scoring:** 
  - Explicit sponsorship mentions
  - Company size and track record
  - Industry and location
  - Role requirements
- **Timeline:** OPT sponsorship now, H-1B within 3 years

### 3. **Fit Scoring Agent** ⭐
- **Role:** Score jobs by fit with your profile
- **Input:** Job postings + sponsorship ratings
- **Output:** Ranked list with 0-100 fit scores
- **Components:**
  - Skill Match (0-30): Python, R, SQL, Power BI, ETL, ML alignment
  - Role Match (0-30): Data Analyst/Engineer/Scientist fit
  - Location (0-20): Target city proximity
  - Sponsorship (0-20): OPT + H-1B capability
- **Threshold:** Scores 70+ = high priority applications

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- API keys for:
  - [Groq](https://console.groq.com/) - LLM provider
  - [Tavily](https://tavily.com/) - Web search

### Installation

1. **Clone/Download the project:**
   ```bash
   cd opt-career-navigator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API keys
   GROQ_API_KEY=your_groq_key_here
   TAVILY_API_KEY=your_tavily_key_here
   ```

   Or set them directly in your terminal:
   ```bash
   export GROQ_API_KEY="your_groq_key"
   export TAVILY_API_KEY="your_tavily_key"
   ```

### Run the Streamlit UI

```bash
streamlit run app.py
```

Then:
1. Open your browser to `http://localhost:8501`
2. Select target role and city
3. Click "Start Job Search"
4. Review results across three tabs: Search → Sponsorship → Fit Scores

### Run Programmatically

```python
from crew import OptCareerCrew

crew = OptCareerCrew()
results = crew.search_jobs(
    role="Data Scientist",
    city="Atlanta"
)

print(results)
```

---

## 📁 Project Structure

```
opt-career-navigator/
├── agents.py                 # Three CrewAI agents with system prompts
├── tasks.py                  # Three sequential tasks + Tavily search tool
├── crew.py                   # Pipeline orchestrator
├── app.py                    # Streamlit UI
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

### File Details

#### `agents.py`
Defines three specialized AI agents with detailed system prompts:

- **Job Search Agent:** Searches for current openings
  - Expertise: International student placement, company visa sponsorship
  - Skills: Job search strategies, skill matching, current market knowledge

- **Sponsorship Screening Agent:** Evaluates visa sponsorship likelihood
  - Expertise: OPT/H-1B visa requirements, company sponsorship patterns
  - Inputs: Job postings, company profiles, industry knowledge
  - Outputs: GREEN/YELLOW/RED risk ratings

- **Fit Scoring Agent:** Scores jobs 0-100 by profile match
  - Expertise: Career coaching, data science/analytics roles
  - Scoring: Skill match, role alignment, location, sponsorship capability

**Student Profile (Hardcoded):**
```python
visa_status: F-1 STEM OPT
education: MS Data Science, GVSU
graduation: December 2026
opt_period: January 2024 - January 2027
skills: Python, R, SQL, Power BI, ETL, Machine Learning
target_roles: Data Analyst, Data Engineer, Data Scientist
target_cities: Atlanta, Austin, Raleigh-Durham, Washington D.C.
requirements:
  - OPT sponsorship required immediately
  - H-1B sponsorship within 3 years
```

#### `tasks.py`
Three sequential tasks with specific expected outputs:

1. **Task 1 - Search:** Find job postings via Tavily
   - Input: Role + City
   - Output: 8-15 job listings with details and URLs
   - Tools: `search_jobs_tavily(query)`

2. **Task 2 - Sponsorship:** Screen for visa sponsorship
   - Input: Previous job listings
   - Output: Risk ratings + reasoning for each job
   - Ratings: GREEN/YELLOW/RED

3. **Task 3 - Scoring:** Score by profile fit
   - Input: Jobs + sponsorship ratings
   - Output: Ranked list with component breakdown
   - Scores: 0-100 (70+ = priority)

#### `crew.py`
Orchestrates the pipeline:
- Initializes agents with Groq LLM
- Chains tasks sequentially (Agent 1 → Agent 2 → Agent 3)
- Handles API calls and error management
- Returns structured results

#### `app.py`
Streamlit web interface:
- **Sidebar:**
  - Profile summary
  - Role and city selector
  - Search controls

- **Main tabs:**
  - 🔍 Job Search: Raw postings
  - 📋 Sponsorship: Risk analysis
  - ⭐ Fit Scores: Ranked results
  - 📊 Raw Output: Full agent responses

---

## ⚙️ Configuration

### Hardcoded Profile

The system is pre-configured for:
- **Visa:** F-1 STEM OPT (July 2024 - July 2027)
- **Education:** MS Data Science, Grand Valley State University
- **Graduation:** December 2026
- **Skills:** Python, R, SQL, Power BI, ETL, Machine Learning
- **Roles:** Data Analyst, Data Engineer, Data Scientist
- **Cities:** Atlanta, Austin, Raleigh-Durham, Washington D.C.

To modify, edit `agents.py` `STUDENT_PROFILE` dict.

### LLM Configuration

Currently using:
- **Provider:** Groq
- **Model:** `llama-3.3-70b-versatile`
- **Temperature:** 0.7
- **Max tokens:** 2048

To change, update `create_groq_llm()` in `agents.py`.

### Search Configuration

- **Web Search Tool:** Tavily
- **Results per search:** 10
- **Search queries:** Role + City combinations (3-5 searches)

---

## 🔑 API Keys

### Groq
1. Visit https://console.groq.com/
2. Sign up / Log in
3. Create API key in Dashboard
4. Copy key to `.env` or environment

### Tavily
1. Visit https://tavily.com/
2. Sign up
3. Get API key
4. Add to environment

---

## 📊 Sample Output

```
Job Title: Senior Data Scientist
Company: TechCorp (Atlanta)
Role Match: 28/30 ⭐
Skill Match: 29/30 ⭐
Location: 20/20 ✅ (Target city)
Sponsorship: 18/20 🟢 (Likely sponsors)
---
OVERALL SCORE: 95/100 ⭐⭐⭐

Why Apply:
✓ Perfect skill alignment (Python, SQL, ML expertise needed)
✓ Company known for OPT/H-1B sponsorship (TechCorp sponsors 50+ annually)
✓ Growing team with career progression opportunities
✓ Competitive compensation + relocation assistance

Apply Priority: HIGH
```

---

## 🛠️ Development

### Adding Custom Locations

Edit `STUDENT_PROFILE['target_cities']` in `agents.py`:
```python
target_cities: ["New York", "San Francisco", "Seattle", "Boston"]
```

### Modifying Skills

Edit `STUDENT_PROFILE['skills']`:
```python
skills: ["Java", "Scala", "Spark", "Hadoop", "Kubernetes"]
```

### Changing LLM

Update `create_groq_llm()` in `agents.py`:
```python
def create_groq_llm():
    return {
        "model": "groq/llama-2-70b-chat",  # Different model
        "temperature": 0.5,
        ...
    }
```

### Using Different Search Tool

Replace Tavily in `tasks.py`:
```python
@tool
def search_jobs_google(query: str) -> str:
    # Custom search implementation
    pass
```

---

## ⚠️ Limitations

- **Search quality:** Results depend on Tavily's web coverage
- **Sponsorship signals:** Analysis based on public information (not guaranteed)
- **Real-time data:** Information may be outdated if job posting removed
- **LLM hallucination:** Agents may create plausible-sounding but false details
- **Rate limits:** Groq and Tavily have usage limits (free tier: 5000 tokens/min for Groq)

---

## 🤔 Troubleshooting

### "GROQ_API_KEY not set"
```bash
export GROQ_API_KEY="your_key"
echo $GROQ_API_KEY  # Verify
```

### "TAVILY_API_KEY not set"
```bash
export TAVILY_API_KEY="your_key"
```

### Pipeline times out
- Groq free tier has rate limits
- Try again after a minute
- Consider paid tier for production

### No results found
- Try broader search terms (e.g., "Data" instead of "Senior Data Scientist")
- Check internet connection
- Verify Tavily API key works

### Poor sponsorship scores
- Agents may need company-specific training data
- Add known sponsorship companies to system prompt
- Manually review company websites

---

## 📚 References

- [CrewAI Documentation](https://docs.crewai.com/)
- [Groq Console](https://console.groq.com/)
- [Tavily API Docs](https://docs.tavily.com/)
- [F-1 STEM OPT Info](https://www.uscis.gov/opt)
- [H-1B Visa Info](https://www.uscis.gov/h-1b)

---

## 📝 License

MIT

---

## 👨‍💻 Author

Built for international students navigating F-1 STEM OPT and H-1B visa sponsorship.

---

## 🙋 Contributing

Have ideas? Found a bug? PRs welcome!

Current ideas:
- [ ] LinkedIn scraping for sponsor history
- [ ] Company sponsorship database integration
- [ ] Resume tailoring recommendations
- [ ] Interview preparation guides
- [ ] Visa timeline calculator
- [ ] Multi-language support
