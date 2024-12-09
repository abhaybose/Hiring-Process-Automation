from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from tools.oracleDBConnector import connectToDB, executeSqlQuery

@CrewBase
class chat_assistant_crew():
	"""User Assistant Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	llm = ChatOpenAI(model="gpt-4o")

	#Agent method name should mavtch the agent name in the agents.yaml file
	@agent
	def user_query_router(self) -> Agent:
		return Agent(
			config=self.agents_config['user_query_router'],
			llm = self.llm,
			verbose=True,
			tools=[
				connectToDB,
				executeSqlQuery
			]
		)

	@task
	def define_user_input(self) -> Task:
		return Task(
			config=self.tasks_config['define_user_input'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Chat Bot Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
