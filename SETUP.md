# 🚀 OPT Career Navigator - Setup Guide

Complete step-by-step instructions to get the system up and running.

## ⚙️ Prerequisites

- **Python 3.9+** - Check with `python --version`
- **pip** - Python package manager (comes with Python)
- **Internet connection** - For API calls
- **Two API keys:**
  - Groq (for LLM)
  - Tavily (for web search)

---

## 📥 Step 1: Get API Keys

### 1.1 Groq API Key

1. Visit https://console.groq.com/
2. Click "Sign Up" (or "Sign In" if you have an account)
3. Complete signup with email and password
4. Go to Dashboard → API Keys
5. Click "Create New API Key"
6. Copy the key (you'll need it soon)
7. Keep this key safe - don't share or commit to Git

### 1.2 Tavily API Key

1. Visit https://tavily.com/
2. Click "Get Started" or "Sign Up"
3. Create account
4. Go to dashboard
5. Find your API key in settings
6. Copy the key
7. Keep this key safe

---

## 💾 Step 2: Clone/Download Project

### Option A: Using Git
```bash
git clone <repository-url> opt-career-navigator
cd opt-career-navigator
```

### Option B: Download ZIP
1. Download ZIP file from repository
2. Extract to desired location
3. Open terminal/PowerShell in that folder
4. Run: `cd opt-career-navigator`

---

## 🐍 Step 3: Set Up Python Environment

### Option 1: Using venv (Recommended)

**Windows:**
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# You should see (venv) in your terminal
```

**macOS/Linux:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your terminal
```

### Option 2: Using Conda

```bash
conda create -n opt-navigator python=3.9
conda activate opt-navigator
```

---

## 📦 Step 4: Install Dependencies

With your virtual environment activated:

```bash
# Upgrade pip first (recommended)
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

This installs:
- `crewai` - Multi-agent framework
- `crewai-tools` - Tool integrations
- `groq` - Groq LLM client
- `streamlit` - Web UI framework
- `tavily-python` - Web search client
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation

**Verify installation:**
```bash
pip list | grep -E "crewai|groq|streamlit|tavily"
```

---

## 🔑 Step 5: Configure API Keys

### Option A: Using .env file (Recommended)

1. In the project folder, copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` in your text editor

3. Replace placeholders with your actual keys:
   ```
   GROQ_API_KEY=gsk_your_actual_groq_key_here
   TAVILY_API_KEY=tvly_your_actual_tavily_key_here
   ```

4. Save the file

5. The system will automatically load these keys

### Option B: Using Environment Variables

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY = "gsk_your_key_here"
$env:TAVILY_API_KEY = "tvly_your_key_here"

# Verify
echo $env:GROQ_API_KEY
echo $env:TAVILY_API_KEY
```

**Windows (Command Prompt):**
```cmd
setx GROQ_API_KEY "gsk_your_key_here"
setx TAVILY_API_KEY "tvly_your_key_here"
```

**macOS/Linux (Bash):**
```bash
export GROQ_API_KEY="gsk_your_key_here"
export TAVILY_API_KEY="tvly_your_key_here"

# Add to ~/.bashrc or ~/.zshrc to make permanent:
echo 'export GROQ_API_KEY="gsk_your_key_here"' >> ~/.bashrc
echo 'export TAVILY_API_KEY="tvly_your_key_here"' >> ~/.bashrc

# Then reload:
source ~/.bashrc
```

**Verify keys are set:**
```bash
echo $GROQ_API_KEY
echo $TAVILY_API_KEY
```

---

## 🎯 Step 6: Run the Application

### Option A: Streamlit Web UI (Recommended for First-Time Users)

```bash
streamlit run app.py
```

This will:
1. Start a local web server
2. Open browser to `http://localhost:8501`
3. Show the interactive UI

**In the UI:**
1. Select a job role from the sidebar
2. Select a target city
3. Click "Start Job Search"
4. Review results in tabs: Search → Sponsorship → Fit Scores

### Option B: Command-Line Examples

```bash
python example.py
```

This runs several examples showing:
- How to retrieve your profile
- How to search for Data Scientists
- How to search for Data Engineers
- How to search for Data Analysts
- How to search for custom roles

Edit `example.py` to customize which examples run.

### Option C: Python REPL

```bash
python
```

Then in the Python shell:
```python
from crew import OptCareerCrew

crew = OptCareerCrew()
results = crew.search_jobs(role="Data Scientist", city="Atlanta")
print(results)
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Virtual environment activated (see `(venv)` in terminal)
- [ ] All packages installed (`pip list` shows crewai, groq, streamlit, tavily)
- [ ] API keys set (echo $GROQ_API_KEY and echo $TAVILY_API_KEY both show values)
- [ ] Run `streamlit run app.py` successfully
- [ ] Web UI loads in browser at localhost:8501
- [ ] Can select role and city in sidebar
- [ ] "Start Job Search" button works (even if results take a minute)

---

## 🆘 Troubleshooting

### "Python not found"
```bash
# Check Python version
python --version

# If not found, install from python.org
```

### "Permission denied" (macOS/Linux)
```bash
# Fix permissions
chmod +x ./venv/bin/activate
```

### "GROQ_API_KEY not set"
```bash
# Verify it's in .env
cat .env | grep GROQ_API_KEY

# Or set manually
export GROQ_API_KEY="your_key"
```

### "No module named 'crewai'"
```bash
# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

### "Streamlit not found"
```bash
# Reinstall with pip
pip install streamlit

# Check installation
pip show streamlit
```

### "API call failed / timeout"
- Check internet connection
- Verify API keys are correct
- Groq free tier has rate limits (5000 tokens/min) - wait a minute
- Check API dashboards:
  - https://console.groq.com/ (for Groq status)
  - https://tavily.com/ (for Tavily status)

### "Port 8501 already in use"
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### "SSL certificate error"
```bash
# Disable SSL verification (not recommended for production)
export PYTHONHTTPSVERIFY=0
streamlit run app.py
```

---

## 📚 Next Steps

After successful setup:

1. **Customize your profile** - Edit `STUDENT_PROFILE` in `agents.py`
2. **Try different searches** - Experiment with roles and cities
3. **Understand results** - Read the sponsorship analysis
4. **Review output** - Check the "Raw Output" tab for detailed agent reasoning
5. **Iterate** - Refine your profile and search criteria

---

## 📖 Additional Resources

- [CrewAI Docs](https://docs.crewai.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Groq Console](https://console.groq.com/)
- [Tavily Documentation](https://docs.tavily.com/)
- [F-1 STEM OPT Guide](https://www.uscis.gov/opt)
- [H-1B Sponsorship Info](https://www.uscis.gov/h-1b)

---

## 🤝 Need Help?

If you encounter issues:

1. Check this troubleshooting guide
2. Review error messages carefully
3. Check API key validity
4. Try running `example.py` instead of web UI
5. Check terminal for full error traceback
6. Review README.md for more context

---

## ✨ You're Ready!

Once setup is complete, you're ready to start searching for jobs with visa sponsorship support. The system will:

1. ✅ Find real job postings matching your profile
2. ✅ Analyze visa sponsorship likelihood
3. ✅ Score jobs by fit (0-100)
4. ✅ Rank results by priority

Good luck with your job search! 🚀
