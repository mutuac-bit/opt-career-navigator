"""
OPT Career Navigator - Example Usage
Shows how to use the system programmatically without the Streamlit UI.
"""

from crew import OptCareerCrew
import json


def example_basic_search():
    """Basic example: Search for Data Scientist jobs in Atlanta"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Job Search for Data Scientist in Atlanta")
    print("="*80 + "\n")
    
    crew = OptCareerCrew()
    results = crew.search_jobs(role="Data Scientist", city="Atlanta")
    
    # Print results
    if results["status"] == "success":
        print("✅ Search completed successfully!\n")
        print(results["pipeline_output"])
    else:
        print(f"❌ Error: {results['error']}")


def example_data_engineer_search():
    """Search for Data Engineer jobs in Austin"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Data Engineer Job Search in Austin")
    print("="*80 + "\n")
    
    crew = OptCareerCrew()
    results = crew.search_jobs(role="Data Engineer", city="Austin")
    
    if results["status"] == "success":
        print("✅ Search completed successfully!\n")
        # Print just the first 1000 characters to avoid clutter
        output = results["pipeline_output"]
        if isinstance(output, str) and len(output) > 1000:
            print(output[:1000] + "\n... (truncated) ...")
        else:
            print(output)
    else:
        print(f"❌ Error: {results['error']}")


def example_analyst_search():
    """Search for Data Analyst jobs in Raleigh-Durham"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Data Analyst Job Search in Raleigh-Durham")
    print("="*80 + "\n")
    
    crew = OptCareerCrew()
    results = crew.search_jobs(role="Data Analyst", city="Raleigh-Durham")
    
    if results["status"] == "success":
        print("✅ Search completed successfully!\n")
        # Extract sponsorship-related results
        print("=== Sponsorship Screening Results ===\n")
        if isinstance(results["pipeline_output"], str):
            lines = results["pipeline_output"].split("\n")
            for i, line in enumerate(lines):
                if any(keyword in line.lower() for keyword in 
                       ["sponsorship", "green", "yellow", "red", "risk"]):
                    print(line)
                # Limit output
                if i > 100:
                    break
    else:
        print(f"❌ Error: {results['error']}")


def example_custom_role():
    """Search for custom role in Washington D.C."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Custom Role Search - 'ML Engineer' in Washington D.C.")
    print("="*80 + "\n")
    
    crew = OptCareerCrew()
    results = crew.search_jobs(role="ML Engineer", city="Washington D.C.")
    
    if results["status"] == "success":
        print("✅ Search completed successfully!\n")
        print("Profile used for scoring:")
        print(json.dumps(results["profile"], indent=2))
    else:
        print(f"❌ Error: {results['error']}")


def example_get_profile():
    """Retrieve and display the student profile"""
    print("\n" + "="*80)
    print("EXAMPLE 5: View Student Profile")
    print("="*80 + "\n")
    
    crew = OptCareerCrew()
    profile = crew.get_profile()
    
    print("Current Student Profile:")
    print("-" * 80)
    print(json.dumps(profile, indent=2))
    
    print("\nKey Information:")
    print(f"  Visa Status: {profile['visa_status']}")
    print(f"  Education: {profile['education']}")
    print(f"  Graduation: {profile['graduation']}")
    print(f"  OPT Timeline: {profile['opt_start_date']} to {profile['opt_end_date']}")
    print(f"  H-1B Timeline: {profile['h1b_timeline']}")
    print(f"\n  Target Roles: {', '.join(profile['target_roles'])}")
    print(f"  Target Cities: {', '.join(profile['target_cities'])}")
    print(f"  Skills: {', '.join(profile['skills'])}")


def main():
    """Run all examples"""
    import sys
    
    # Check for environment variables
    import os
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY environment variable not set")
        print("Set it with: export GROQ_API_KEY='your_key'")
        sys.exit(1)
    
    if not os.getenv("TAVILY_API_KEY"):
        print("❌ Error: TAVILY_API_KEY environment variable not set")
        print("Set it with: export TAVILY_API_KEY='your_key'")
        sys.exit(1)
    
    print("\n🎯 OPT Career Navigator - Example Usage Guide")
    print("This script demonstrates various ways to use the system.\n")
    
    # Run examples
    try:
        # Uncomment the examples you want to run:
        
        example_get_profile()  # Always show profile first
        
        # Basic search example
        # example_basic_search()
        
        # Data Engineer search
        # example_data_engineer_search()
        
        # Analyst search  
        # example_analyst_search()
        
        # Custom role search
        # example_custom_role()
        
        print("\n" + "="*80)
        print("✅ Examples completed!")
        print("="*80)
        print("\n📝 To run other examples, uncomment them in the main() function.\n")
        
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
