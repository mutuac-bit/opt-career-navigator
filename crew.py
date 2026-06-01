"""
OPT Career Navigator - CrewAI Crew
Orchestrates the three agents and tasks into a pipeline.
"""

from crewai import Crew
from agents import get_agents, get_student_profile
from tasks import get_tasks
import json
from datetime import datetime


class OptCareerCrew:
    """Main crew orchestrator for the job search pipeline"""

    def __init__(self):
        """Initialize the crew with agents and tasks"""
        self.agents = get_agents()
        self.tasks = get_tasks()
        self.profile = get_student_profile()

        # Assign agents to tasks
        self.tasks["search"].agent = self.agents["job_search"]
        self.tasks["sponsorship"].agent = self.agents["sponsorship"]
        self.tasks["fit_scoring"].agent = self.agents["fit_scoring"]

        # Create the crew
        self.crew = Crew(
            agents=[
                self.agents["job_search"],
                self.agents["sponsorship"],
                self.agents["fit_scoring"],
            ],
            tasks=[
                self.tasks["search"],
                self.tasks["sponsorship"],
                self.tasks["fit_scoring"],
            ],
            verbose=True,
            process="sequential",  # Sequential so each task builds on the previous
        )

    def search_jobs(self, role: str, city: str) -> dict:
        """
        Execute the job search pipeline for a given role and city.

        Args:
            role: Target job role (e.g., "Data Scientist", "Data Analyst", "Data Engineer")
            city: Target city (e.g., "Atlanta", "Austin", "Washington D.C.")

        Returns:
            dict: Pipeline results with search results, sponsorship screening, and fit scores
        """
        print(f"\n{'='*80}")
        print(f"OPT Career Navigator - Job Search Pipeline")
        print(f"{'='*80}")
        print(f"Role: {role}")
        print(f"City: {city}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")

        # Update task descriptions with specific role and city
        self.tasks["search"].description = (
            f"Search for current {role} job postings in {city} and other target cities "
            f"(Atlanta, Austin, Raleigh-Durham, Washington D.C.) that offer OPT and H-1B sponsorship. "
            f"Find 8-15 of the most promising current openings. Include job title, company, "
            f"location, key requirements, and posting URL for each."
        )

        try:
            # Execute the crew
            result = self.crew.kickoff()
            
            # Parse and structure the results
            structured_result = {
                "status": "success",
                "role": role,
                "city": city,
                "timestamp": datetime.now().isoformat(),
                "pipeline_output": result,
                "profile": self.profile,
            }

            return structured_result

        except Exception as e:
            error_result = {
                "status": "error",
                "role": role,
                "city": city,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
            print(f"Error during pipeline execution: {str(e)}")
            return error_result

    def get_profile(self) -> dict:
        """Return the student profile"""
        return self.profile


def run_example():
    """Run an example job search"""
    crew = OptCareerCrew()
    
    # Example search
    results = crew.search_jobs(
        role="Data Scientist",
        city="Atlanta"
    )
    
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    print(json.dumps(results, indent=2, default=str))
    
    return results


if __name__ == "__main__":
    run_example()
