import logging
from src.core.llm import get_Bedrock_llm
import json
import logging
from src.core.agent import Agent
from pydantic import BaseModel
from langchain.tools import StructuredTool, Tool
import os
from config.app_config import AppConfig
app_config = AppConfig()

# Set up logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'ERROR'))
logger = logging.getLogger(__name__)

logger.info("initializing llm")
llm = get_Bedrock_llm()
logger.info("llm initialized")

# Import tools
from src.tools.ask_user import ask_user
from src.tools.question_picker import question_picker
from src.tools.evaluate_response import evaluate_response

# Initialize the question_picker tool
class QuestionPickerInput(BaseModel):
    difficulty: str
    taxonomy: str

def question_picker_tool(difficulty: str, taxonomy: str) -> dict:
    return question_picker(difficulty, taxonomy)

question_picker_tool = StructuredTool(
    name="question_picker",
    func=question_picker_tool,
    description="Use this tool to pick a question based on the difficulty and taxonomy.",
    args_schema=QuestionPickerInput
)

class EvaluateResponseInput(BaseModel):
    user_response: str
    correct_answer: str
    difficulty: str
    taxonomy: str

def evaluate_response_tool(input: EvaluateResponseInput) -> dict:
    return evaluate_response(input.user_response, input.correct_answer, input.difficulty, input.taxonomy)

evaluate_response_tool = StructuredTool(
    name="evaluate_response",
    func=evaluate_response_tool,
    description="Use this tool to evaluate the user's response to a question.",
    args_schema=EvaluateResponseInput
)

# Initialize the ask_user tool
ask_user_tool = Tool(
    name="ask_user",
    func=ask_user,
    description="Use this tool to ask the user a question."
)

# Load planning prompt
with open(app_config.PLANNING_PROMPT, 'r') as ffile:
    agent_planning_prompt = ffile.read()

# Initialize the agent with both tools
agent = Agent(
    tools=[question_picker_tool, evaluate_response_tool, ask_user_tool],
    planning=agent_planning_prompt,
    llm=llm
)

logger.info("Invoking agent...")
agent_configurator = agent.invoke_agent(input_="")
logger.info("Agent invoked.")
logger.info("Output:")
print(agent_configurator.get('output'))

