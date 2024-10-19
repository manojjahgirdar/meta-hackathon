import logging
from src.core.llm import get_Bedrock_llm
import json
import logging
from src.core.agent import Agent
from langchain.tools import Tool, StructuredTool
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
from src.tools.ask_user import ask_user, AskUserInput
from src.tools.question_picker import question_picker, QuestionPickerInput
from src.tools.evaluate_response import evaluate_response, EvaluateResponseInput
from src.tools.final_summarizer import final_summarizer, FinalSummarizerInput
# Initialize the question_picker tool

question_picker_tool = StructuredTool.from_function(
    func=question_picker,
    name="question_picker",
    description="Use this tool to pick a question based on the difficulty and taxonomy. This tool takes a string of dictionary as input and returns a json.",
    args_schema=QuestionPickerInput
)

# Initialize the evaluate_response tool
evaluate_response_tool = StructuredTool.from_function(
    func=evaluate_response,
    name="evaluate_response",
    description="Use this tool to evaluate the user's response to a question. This tool takes a string of dictionary as input and returns a json.",
    args_schema=EvaluateResponseInput
)

# Initialize the ask_user tool
ask_user_tool = StructuredTool.from_function(
    func=ask_user,
    name="ask_user",
    description="Use this tool to ask the user a question. This tool takes a string of dictionary as input and returns the user's response as a string.",
    args_schema=AskUserInput
)

# Initialize the final_summarizer tool
final_summarizer_tool = StructuredTool.from_function(
    func=final_summarizer,
    name="final_summarizer",
    description="Use this tool to summarize the conversation. This tool takes a string of dictionary as input and returns the final summary as a string.",
    args_schema=FinalSummarizerInput
)

# Load planning prompt
with open(app_config.PLANNING_PROMPT, 'r') as ffile:
    agent_planning_prompt = ffile.read()

# Initialize the agent with both tools
agent = Agent(
    tools=[question_picker_tool, evaluate_response_tool, ask_user_tool, final_summarizer_tool],
    planning=agent_planning_prompt,
    llm=llm
)

logger.info("Invoking agent...")
agent_configurator = agent.invoke_agent(input_="")
logger.info("Agent invoked.")
logger.info("Output:")
print(agent_configurator.get('output'))

