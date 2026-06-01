# 📋 OPT Career Navigator - Quick Reference

## File Summary

| File | Purpose | Key Content |
|------|---------|-------------|
| **agents.py** | Define AI agents | 3 agents + student profile |
| **tasks.py** | Define tasks | Search, screening, scoring |
| **crew.py** | Orchestrate pipeline | Main execution logic |
| **app.py** | Streamlit UI | Web interface |
| **requirements.txt** | Dependencies | All Python packages |
| **.env.example** | API key template | Copy to .env |
| **.gitignore** | Git exclusions | Don't commit secrets |
| **SETUP.md** | Installation guide | Step-by-step setup |
| **README.md** | Full documentation | Architecture & usage |
| **example.py** | Usage examples | Programmatic examples |

---

## Quick Commands

### Setup
```bash
python -m venv venv
./venv/Scripts/activate  # Windows
source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
```

### Configure
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Run
```bash
streamlit run app.py           # Web UI
python example.py              # Examples
python -c "from crew import OptCareerCrew; ..." # Inline
```

---

## System Prompt Overview

### Job Search Agent
- **Goal:** Find 8-15 current job postings
- **Tools:** Tavily web search
- **Focus:** Data roles + sponsorship signals
- **Expertise:** International student placement

### Sponsorship Agent
- **Goal:** Rate visa sponsorship likelihood
- **Output:** GREEN/YELLOW/RED ratings
- **Signals:** Company size, industry, track record
- **Factors:** OPT now, H-1B within 3 years

### Fit Scoring Agent
- **Goal:** Score jobs 0-100 by profile match
- **Components:** Skills (30), Role (30), Location (20), Sponsorship (20)
- **Expertise:** Data science career coaching
- **Threshold:** 70+ = high priority

---

## API Keys

| Service | Get Key | Free Tier |
|---------|---------|-----------|
| **Groq** | https://console.groq.com/ | Yes, rate limited |
| **Tavily** | https://tavily.com/ | Yes, limited searches |

---

## Profile (Hardcoded)

```
Visa: F-1 STEM OPT
Education: MS Data Science, GVSU
Graduation: Dec 2026
OPT Valid: Jan 2024 - Jan 2027

Skills: Python, R, SQL, Power BI, ETL, ML
Roles: Data Analyst, Engineer, Scientist
Cities: Atlanta, Austin, Raleigh-Durham, DC

Requirements:
- OPT sponsorship now
- H-1B sponsorship within 3 years
```

---

## Customization

**Profile:** Edit `STUDENT_PROFILE` in `agents.py`
**LLM:** Edit `create_groq_llm()` in `agents.py`
**Search:** Edit tasks in `tasks.py`
**UI:** Edit styling in `app.py`

---

## Output Format

Each job gets scored:
```
Score: XX/100
├─ Skill Match: XX/30
├─ Role Match: XX/30
├─ Location: XX/20
└─ Sponsorship: XX/20

Risk: 🟢 GREEN / 🟡 YELLOW / 🔴 RED
Priority: HIGH / MEDIUM / LOW
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No API key | Set GROQ_API_KEY and TAVILY_API_KEY |
| Port in use | `streamlit run app.py --server.port 8502` |
| Module not found | `pip install -r requirements.txt` |
| API timeout | Wait 1 min (rate limit) or upgrade to paid |
| No results | Try broader search terms |

---

## Workflow

1. **Input:** Role (Data Scientist) + City (Atlanta)
2. **Agent 1:** Search for jobs → 10 postings
3. **Agent 2:** Screen for sponsorship → RED/YELLOW/GREEN
4. **Agent 3:** Score by fit → 0-100 ranked list
5. **Output:** Sorted by score, ready to apply

---

## Example Usage

```python
from crew import OptCareerCrew

crew = OptCareerCrew()

# Search for jobs
results = crew.search_jobs(
    role="Data Scientist",
    city="Atlanta"
)

# View results
print(results["pipeline_output"])

# Get profile
profile = crew.get_profile()
```

---

## URLs

- **Groq:** https://console.groq.com/
- **Tavily:** https://tavily.com/
- **CrewAI:** https://docs.crewai.com/
- **Streamlit:** https://streamlit.io/
- **F-1 OPT:** https://www.uscis.gov/opt
- **H-1B:** https://www.uscis.gov/h-1b

---

## Support

1. Check SETUP.md for installation issues
2. Check README.md for usage questions
3. Review example.py for code examples
4. Check API key validity
5. Review error messages in terminal

---

**Last Updated:** 2026-05-31
**Version:** 1.0.0
**Status:** Ready to use ✅
