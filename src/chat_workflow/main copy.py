#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start,router
from markdown_to_json import jsonify, dictify

from .crews.poem_crew.poem_crew import PoemCrew
from .crews.chat_assistant_crew.chat_assistant_crew import chat_assistant_crew
from .crews.generic_response_crew.generic_response_crew import generic_response_crew
from .crews.database_response_crew.database_response_crew import database_response_crew

#Define the state of the chatbot (Structured Data)
class ChatBotState(BaseModel):
    user_input: str = ""
    isDBquery: bool = False
    generic_output: str = ""

#Initiate teh workflow
class ChatWorkflow(Flow[ChatBotState]):

    @start()
    def check_user_input(self):
        print("check_user_input")
        self.state.user_input = input("Enter your input: ")

    @listen(check_user_input)
    def define_input_type(self):
        print("define_input_type")
        print( chat_assistant_crew().crew)
        result = (
            chat_assistant_crew()
            .crew()
            .kickoff(inputs={"user_input": self.state.user_input })
        )

        print("Query--> is it a DB Query?: Ans-->", result)
        # print(self.state.isDBquery, ' | ',result.raw.upper(),'||',str.capitalize(result.raw) == "TRUE" )
        if(result.raw.upper() == "TRUE"):
            self.state.isDBquery = True
        else:
            self.state.isDBquery = False

    
    @router(define_input_type)
    def route_input(self):
        if self.state.isDBquery:
            return 'db_query'
        else:
            return 'generic_response'
        

        
    @listen('db_query')
    def db_resp(self):
        print("This is a DB Query, initiating DB Agent")
        result = (
            database_response_crew()
            .crew()
            .kickoff(inputs={"user_input": self.state.user_input })
        )
        print('SQL Query:',result.raw)
        jsonresult = result.raw.replace("```json","").replace("```","")
        # finalresult = str(jsonresult.get('root')).replace("'",'').replace('`','').replace(' ','')
        print("==========jsonresult=================")
        print(jsonresult)
        
        # jsonoutput1=result.raw.split('[')
        # jsonoutput2=jsonoutput1[1].split(']')
        # print("(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)")
        # print("["+jsonoutput2+"]")
        
        
    @listen('generic_response')
    def generic_resp(self):
        print("Responding with generic response")
        result = (
            generic_response_crew()
            .crew()
            .kickoff(inputs={"user_input": self.state.user_input })
        )
        print(result.raw)
        # with open("poem.txt", "w") as f:
        #     f.write(self.state.poem)
def kickoff():
    workflow = ChatWorkflow()
    workflow.kickoff()


def plot():
    workflow = ChatWorkflow()
    workflow.plot()


if __name__ == "__main__":
    kickoff()
