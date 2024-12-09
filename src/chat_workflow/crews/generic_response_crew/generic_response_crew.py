from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from tools.oracleDBConnector import connectToDB, executeSqlQuery
from crewai_tools import SerperDevTool


seper_dev_tool = SerperDevTool()
@CrewBase
class generic_response_crew():
	"""User Assistant Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	llm = ChatOpenAI(model="gpt-4o")

	
	#Agent method name should mavtch the agent name in the agents.yaml file
	@agent
	def Generic_Agent(self) -> Agent:
		return Agent(
			config=self.agents_config['Generic_Agent'],
			llm = self.llm,
			verbose=True,
			tools=[				
         		seper_dev_tool
			],
			backstory= '''
   				You are an expert editor. You use your expertise to edit the response from the database agent and return the response in a JSON Array format.
			    Do Not Allow Markfown or HTML in the response. always convert True and False to all lower case

         		if Tabular data is present in the response, Please provide below details as JSON : 
					type: table
					label: "Best Suited Title for the response"
					coldef:JSON Array  of columns with filter, sortable, floatingFilter, resizable, wrapHeaderText, autoHeaderHeight
					data: JSON Array of rows with column values

				if you want to provide an introduction to the response then create below response as JSON and 
					type: paragraph
					label: "Introduction"
					data: " I am a  Human Who can code any thing in the world, GEN AI be like  Hold my beer you mere Human"
				
				If you user asked for a chart to be built please add teh belwo JSOn to the response JSON Array 
					type: "chart",
					label: "Best Suited Title for a chart respresentatiomn ",
					data(JSON Array): data(JSOn Array ): JSON Array of columns and values to be plotted in the chart and series to be used in the chart      
				If the response is not clear send below JSON Array response:
						type: "paragraph",
						label: "Sorry ! System Failed! Please try again...",
						data: "AI Agent failed to provide the response. Please try again...\n"
							
				IMPORTANT: 
				1. DO NOT Respons with Markdown or HTML
				2. Convert Markdown response to JSON Array
				3. Markdown or HTMl response is not allowed
				4. As an expert Editor you arer responsible for editing response in the best possible way again only JSON ARRAY.
				5. ONLY JSON ARRAY is allowed as a response '''
		)

	@task
	def generic_response(self) -> Task:
		return Task(
			config=self.tasks_config['generic_response'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Generic Chat Bot Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
