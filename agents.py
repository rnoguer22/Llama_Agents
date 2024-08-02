from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process



model = Ollama(model="llama3")

email = 'nigerian prince sending me some gold'



classifier = Agent(
    role = 'email classifier',
    goal = 'accurately classify emails based on their importance. Give every email one of this rating: important, casual or spam',
    backstory = 'You are an AI assistant whose only job is to classify emails accurately and honestly. Do not be afraid to give emails bad rating if they are not important. Your job is to help the user manage their inbox.',
    verbose = True,
    allow_denegation = False,
    llm = model
)

responder = Agent(
    role = 'email responder',
    goal = 'Based on the importance of the email, write a concise and simple response. If the email is rated as important, wirte a formal response, if the email is rated as casual, write a casual response and if the email is rated as spam, do not respond.',
    backstory = 'You are an AI assistant whose only job is to write short responses to emails based on their importance. The importance will be provided to you by the classifier agent.',
    verbose = True,
    allow_denegation = False,
    llm = model
)

classify_email = Task(
    description = f"Classify the following email: '{email}'",
    agent = classifier,
    expected_output = "One of these three options: 'important', 'casual' or 'spam'",
)

respond_to_email = Task(
    description = f"Write a response to the email: '{email}' based on the importance provided by the 'classifier' agent",
    agent = responder,
    expected_output = "A very response to the email based on the importance provided by the 'classifier' agent",
)

crew = Crew(
    agents = [classifier, responder],
    tasks = [classify_email, respond_to_email],
    verbose = 2,
    process = Process.sequential
)



output = crew.kickoff()
print(output)