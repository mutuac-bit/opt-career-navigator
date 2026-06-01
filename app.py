"""
OPT Career Navigator - Streamlit UI
Interactive web interface for the manual multi-agent job search system.
"""

import streamlit as st
from agents import run_job_search_pipeline

# Page configuration
st.set_page_config(
    page_title="OPT Career Navigator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main-title {
        color: #0066cc;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #555;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    .section-header {
        color: #0066cc;
        font-size: 1.5em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 2px solid #0066cc;
        padding-bottom: 10px;
    }
    .job-card {
        background-color: #f8f9fa;
        border-left: 4px solid #0066cc;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .green-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 10px;
        margin: 10px 0;
        border-radius: 3px;
    }
    .yellow-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 10px;
        margin: 10px 0;
        border-radius: 3px;
    }
    .red-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 10px;
        margin: 10px 0;
        border-radius: 3px;
    }
    .score-high {
        background-color: #28a745;
        color: white;
        padding: 5px 10px;
        border-radius: 3px;
        font-weight: bold;
    }
    .score-medium {
        background-color: #ffc107;
        color: black;
        padding: 5px 10px;
        border-radius: 3px;
        font-weight: bold;
    }
    .score-low {
        background-color: #dc3545;
        color: white;
        padding: 5px 10px;
        border-radius: 3px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def display_profile(profile):
    """Display user-defined profile in sidebar"""
    st.sidebar.markdown("### 📋 Your Profile")
    st.sidebar.write(f"**Visa Status:** {profile['visa_status']}")
    st.sidebar.write(f"**Years of Experience:** {profile['years_experience']}")
    
    st.sidebar.markdown("**Skills:**")
    if profile['skills']:
        for skill in profile['skills']:
            st.sidebar.write(f"• {skill}")
    else:
        st.sidebar.write("• No skills entered yet")
    
    st.sidebar.markdown("**Target Role:**")
    st.sidebar.write(f"• {profile['target_role']}")
    
    st.sidebar.markdown("**Target City:**")
    st.sidebar.write(f"• {profile['target_city']}")


def build_profile(selected_visa_status, skills_text, years_experience, search_role, search_city):
    """Construct the user profile dictionary from sidebar input."""
    skills_list = [skill.strip() for skill in skills_text.split(",") if skill.strip()]
    if not skills_list:
        skills_list = ["Python", "R", "SQL", "Power BI", "ETL", "Machine Learning"]

    return {
        "visa_status": selected_visa_status,
        "skills": skills_list,
        "years_experience": years_experience,
        "target_role": search_role,
        "target_city": search_city,
    }


def main():
    """Main Streamlit app"""
    
    # Main content
    st.markdown(
        '<div class="main-title">🎯 OPT Career Navigator</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitle">Agentic Job Search for F-1 STEM OPT Students</div>',
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        Find jobs that sponsor **OPT immediately** and **H-1B within 3 years**.
        
        This system uses AI agents to:
        1. 🔍 **Search** for relevant job postings in your target cities
        2. 📋 **Screen** for OPT and H-1B sponsorship signals
        3. ⭐ **Score** jobs based on your skills and profile
        """
    )
    
    st.markdown("---")
    
    # Sidebar for profile input
    st.sidebar.markdown("### 👤 Your Profile")
    visa_status_options = ["F-1 OPT", "F-1 STEM OPT", "H-1B", "Other"]
    selected_visa_status = st.sidebar.selectbox(
        "Visa status",
        visa_status_options,
        index=1,
        help="Select your current visa status"
    )

    skills_text = st.sidebar.text_input(
        "Skills",
        value="Python, R, SQL, Power BI, ETL, Machine Learning",
        help="List your skills separated by commas"
    )

    years_experience = st.sidebar.slider(
        "Years of experience",
        0,
        10,
        0,
        help="Select how many years of experience you have"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔎 Search Parameters")
    
    role_options = ["Data Analyst", "Data Engineer", "Data Scientist", "Custom"]
    selected_role = st.sidebar.selectbox(
        "Select Target Role",
        role_options,
        help="Choose from common roles or enter a custom role"
    )
    
    if selected_role == "Custom":
        custom_role = st.sidebar.text_input("Enter custom role", placeholder="e.g., ML Engineer")
        search_role = custom_role if custom_role else "Data Scientist"
    else:
        search_role = selected_role
    
    city_options = ["Atlanta", "Austin", "Raleigh-Durham", "Washington D.C.", "All"]
    selected_city = st.sidebar.selectbox(
        "Select Target City",
        city_options,
        help="Choose a primary search location"
    )
    
    search_city = selected_city if selected_city != "All" else "Atlanta"

    profile = build_profile(
        selected_visa_status,
        skills_text,
        years_experience,
        search_role,
        search_city,
    )

    display_profile(profile)
    
    st.sidebar.markdown("---")
    search_button = st.sidebar.button(
        "🚀 Start Job Search",
        use_container_width=True,
        help="Execute the multi-agent pipeline"
    )
    
    # Execute search when button clicked
    if search_button:
        with st.spinner("🔄 Running AI agents... This may take a minute."):
            results = run_job_search_pipeline(
                role=search_role,
                city=search_city,
                profile=profile,
            )
        
        if results["status"] == "success":
            st.success("✅ Search completed!")
            
            # Display results tabs
            tab1, tab2, tab3 = st.tabs(
                ["🔍 Job Search", "📋 Sponsorship Analysis", "⭐ Fit Scores & Rankings"]
            )
            
            with tab1:
                st.markdown("### Job Search Results")
                st.info(
                    f"Searching for {search_role} positions in {search_city} "
                    f"that sponsor F-1 OPT and H-1B visas."
                )
                st.markdown(results["search_results"])
            
            with tab2:
                st.markdown("### Sponsorship Screening")
                st.info("Analysis of OPT and H-1B sponsorship likelihood for each posting")
                st.markdown(results["sponsorship_analysis"])
            
            with tab3:
                st.markdown("### Ranked Job Recommendations")
                st.info("Jobs scored 0-100 and ranked by fit with your profile")
                st.markdown(results["fit_scores"])
        
        else:
            st.error(f"❌ Error during search: {results.get('error', 'Unknown error')}")
            st.info("Make sure GROQ_API_KEY and TAVILY_API_KEY environment variables are set.")
    
    # Display instructions
    st.markdown("---")
    st.markdown("### ℹ️ How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 1️⃣ Job Search Agent")
        st.write(
            "Searches Tavily for real job postings matching your skills "
            "(Python, R, SQL, Power BI, ETL, ML) in target cities and roles."
        )
    
    with col2:
        st.markdown("#### 2️⃣ Sponsorship Agent")
        st.write(
            "Analyzes each job for OPT and H-1B visa sponsorship signals. "
            "Rates each as Green (likely sponsors), Yellow (uncertain), or Red (unlikely)."
        )
    
    with col3:
        st.markdown("#### 3️⃣ Fit Scoring Agent")
        st.write(
            "Scores jobs 0-100 based on skill match, role fit, location, "
            "and sponsorship capability. High scores = priority applications."
        )
    
    # Setup instructions
    st.markdown("---")
    st.markdown("### 🔧 Setup")
    st.code(
        """
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export GROQ_API_KEY="your_groq_api_key"
export TAVILY_API_KEY="your_tavily_api_key"

# 3. Run the app
streamlit run app.py
        """,
        language="bash"
    )


if __name__ == "__main__":
    main()
