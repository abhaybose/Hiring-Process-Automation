#!/usr/bin/env python
from random import randint
from typing import List

from pydantic import BaseModel
import json

from crewai.flow.flow import Flow, listen, start,router
# from crews.poem_crew.poem_crew import PoemCrew
# from crews.chat_assistant_crew.chat_assistant_crew import chat_assistant_crew
# from crews.generic_response_crew.generic_response_crew import generic_response_crew
# from crews.database_response_crew.database_response_crew import database_response_crew
from .crews.efficient_hiring_process_design_guide.efficient_hiring_process_design_guide_crew import EfficientHiringProcessDesignGuideCrew
# from flask_cors import CORS
# from flask import Flask,request
from crewai.tasks.task_output import TaskOutput

#Define the state of the chatbot (Structured Data)
class HiringProcessState(BaseModel):
    JobRole: str = ""
    Cityofwork: str = ""
    OtherRequirements: str = ""
    output: str = ""
    profileApproved: bool = False
    
# app = Flask(__name__)
# CORS(app)
# user_query = ""
profileApproved = False

# @app.route('/query', methods=['POST'])
# def query():
#     jsonBody = request.get_json('query')
#     print("Agua")
#     print( jsonBody['query'])
#     # user_query = "show all the issues in both  DQA_MESSEDUP_DATA and DQA_LOAN_SYSTEM Tables"
#     user_query = jsonBody['query']
#     response = Initiate_Workflow(user_query)
#     print("response======",response)
#     return response

#Initiate teh workflow
class HringProcessWorkflow(Flow[HiringProcessState]):
    
    # @start()
    # def check_user_input(self):
    #     print("check_user_input")
    #     self.state.user_input = input("Enter your input: ")
    
    @start()
    def check_user_input(self):
        self.state.JobRole = input("Please Enter Job Role: ") 
        self.state.Cityofwork = input("Please Enter City(ies) [Example: New York, Greate Clevaland, Remote]: ")
        self.state.OtherRequirements = input("Please tell us more about the above Role: ") 
        print("check_user_input")
        print("Role:---> ",self.state.JobRole)
        print("City:---> ",self.state.Cityofwork)
        print("More Info:---> ",self.state.OtherRequirements)
   

    @listen(check_user_input)
    def startProfileCreation(self):
        print("startProfileCreation")
        result = (
            EfficientHiringProcessDesignGuideCrew()
            .crew()
            .kickoff(inputs={"job_role_name": self.state.JobRole, "job_location": self.state.Cityofwork, "project_requirements": self.state.OtherRequirements})
        )

        print("profile:", result)
        print("----------------------------------------------------------")
        isprofileApproved = input("Do you Apporve the Profile? [Y/N]: ")
        print("----------------------------------------------------------")
        print("isprofileApproved: ",isprofileApproved)
        # print(self.state.isDBquery, ' | ',result.raw.upper(),'||',str.capitalize(result.raw) == "TRUE" )
        if(isprofileApproved == "Y"):
            self.state.profileApproved = True
        else:
            self.state.profileApproved = False

    
    
    @router(startProfileCreation)
    def route_input(self):
        if self.state.profileApproved == True:
            print("ABApproved")
            return 'Approved'
        else:
            print("ABRejected")
            return 'Rejected'
        
    @listen('Approved')
    def approved(self):
        print("Profile Approved")
        
    
    @listen('Rejected')
    def rejected(self):
        print("Profile Rejected")

        
    # @listen('db_query')
    # def db_resp(self):
    #     print("This is a DB Query, initiating DB Agent")
    #     result = (
    #         database_response_crew()
    #         .crew()
    #         .kickoff(inputs={"user_input": self.state.user_input })
    #     )
    #     print('SQL Query:',result.raw)
    #     jsonresult = result.raw.replace("```json","").replace("```","").replace("\\","")
    #     # finalresult = str(jsonresult.get('root')).replace("'",'').replace('`','').replace(' ','')
    #     print("==========jsonresult=================")
    #     print(jsonresult)
    #     return json.dumps(jsonresult).replace("\\n", "")
        
    #     # jsonoutput1=result.raw.split('[')
    #     # jsonoutput2=jsonoutput1[1].split(']')
    #     # print("(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)(-)")
    #     # print("["+jsonoutput2+"]")
        
        
    # @listen('generic_response')
    # def generic_resp(self):
    #     print("Responding with generic response")
    #     result = (
    #         generic_response_crew()
    #         .crew()
    #         .kickoff(inputs={"user_input": self.state.user_input })
    #     )
    #     print(result.raw)
    #     # genresp= json.dumps('{"generic_response":"'+result.raw+'"}')
    #     genresp= json.dumps(result.raw.replace("```json","").replace("```","").replace("\\",""))
    #     return genresp.replace("\\n", "")
    #     # with open("poem.txt", "w") as f:
    #     #     f.write(self.state.poem)
def kickoff():
    workflow = HringProcessWorkflow()
    response = workflow.kickoff()
    return response


def plot():
    workflow = HringProcessWorkflow()
    workflow.plot()



if __name__ == "__main__":
    kickoff() # runcrewai flow locally 
    # app.run(debug=True)