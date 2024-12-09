from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import SerperDevTool

seper_dev_tool = SerperDevTool()
scrape_website_tool = ScrapeWebsiteTool()
@CrewBase
class EfficientHiringProcessDesignGuideCrew():
    """EfficientHiringProcessDesignGuide crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
 
    @agent
    def hiring_manager_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['hiring_manager_assistant'],
            tools=[				
         		seper_dev_tool
			]
            
        )

    @agent
    def trend_and_salary_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_and_salary_analyzer'],
            tools=[				
         		seper_dev_tool,
                scrape_website_tool                
			]
        )

    @agent
    def profile_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['profile_generator'],
            tools=[				
         		seper_dev_tool,
                scrape_website_tool                
			]
        )


    @task
    def collect_job_role_information(self) -> Task:
        return Task(
            config=self.tasks_config['collect_job_role_information'],
            
        )

    @task
    def scrape_current_profiles_and_salary_data(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_current_profiles_and_salary_data'],
            tools=[ScrapeWebsiteTool()],
        )

    @task
    def generate_position_description(self) -> Task:
        return Task(
            config=self.tasks_config['generate_position_description'],
            
        )

    @task
    def define_objectives_roles(self) -> Task:
        return Task(
            config=self.tasks_config['define_objectives_roles'],
            
        )

    @task
    def outline_future_duties_and_responsibilities(self) -> Task:
        return Task(
            config=self.tasks_config['outline_future_duties_and_responsibilities'],
            
        )

    @task
    def specify_required_qualifications(self) -> Task:
        return Task(
            config=self.tasks_config['specify_required_qualifications'],
            
        )

    @task
    def identify_required_competencies(self) -> Task:
        return Task(
            config=self.tasks_config['identify_required_competencies'],
            
        )

    @task
    def identify_good_to_have_competencies(self) -> Task:
        return Task(
            config=self.tasks_config['identify_good_to_have_competencies'],
            
        )

    @task
    def list_must_have_certifications(self) -> Task:
        return Task(
            config=self.tasks_config['list_must_have_certifications'],
            
        )

    @task
    def list_good_to_have_certifications(self) -> Task:
        return Task(
            config=self.tasks_config['list_good_to_have_certifications'],
            
        )

    @task
    def incorporate_salary_range(self) -> Task:
        return Task(
            config=self.tasks_config['incorporate_salary_range'],
            
        )

    @task
    def finalize_rm_profile(self) -> Task:
        return Task(
            config=self.tasks_config['finalize_rm_profile'],
            
        )


    @crew
    def crew(self) -> Crew:
        """Creates the EfficientHiringProcessDesignGuide crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
