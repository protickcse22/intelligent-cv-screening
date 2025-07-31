import os

import yaml
from crewai import Agent, Task, Crew

from .model.final_decision_model import FinalDecisionOutput
from .tools.pdf_reader import pdf_reader


# Load YAML
def load_yaml(filename):
    with open(os.path.join(os.path.dirname(__file__), "config", filename), "r") as f:
        return yaml.safe_load(f)

agents_config = load_yaml("agents.yaml")
tasks_config = load_yaml("tasks.yaml")

# Create agents
cv_analyst_agent = Agent(**agents_config["cv_analyst_agent"])
linkedin_agent = Agent(**agents_config["linkedin_agent"])
verification_agent = Agent(**agents_config["verification_agent"])
supervisor_agent = Agent(**agents_config["supervisor_agent"])

# Create tasks
cv_analysis_task = Task(**tasks_config["cv_analysis_task"], tools=[pdf_reader], agent=cv_analyst_agent)
linkedin_analysis_task = Task(**tasks_config["linkedin_analysis_task"], tools=[pdf_reader], agent=linkedin_agent)
verification_task = Task(**tasks_config["verification_task"], agent=verification_agent, context=[cv_analysis_task, linkedin_analysis_task])
final_decision_task = Task(**tasks_config["final_decision_task"], agent=supervisor_agent, context=[cv_analysis_task, verification_task], output_json=FinalDecisionOutput)

# Create crew
crew = Crew(
    agents=[cv_analyst_agent, linkedin_agent, verification_agent, supervisor_agent],
    tasks=[cv_analysis_task, linkedin_analysis_task,verification_task, final_decision_task],
    # verbose=True,
)