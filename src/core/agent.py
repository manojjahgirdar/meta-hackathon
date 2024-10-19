import json
import os
import logging
import time
from langchain.tools import Tool
from langchain.tools.render import render_text_description
from langchain.agents import AgentExecutor
from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from .output_parser import CustomJSONAgentOutputParser
from config.app_config import AppConfig

app_config = AppConfig()

# Set up logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'ERROR'))
logger = logging.getLogger(__name__)

class Agent:
    def __init__(self, tools, planning, llm) -> None:
        self.tools = tools
        self.planning = planning
        self.llm = llm
        # Initialize the agent
        self._init_agent()

    def _init_agent(self) -> None:
        """Initializes the LLM agent with WatsonxLLM and custom settings."""
        try:
            my_llm = self.llm

            system_prompt = self.planning
            user_input = '{input}\n{agent_scratchpad}\n'

            tool_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
            tool_names = ", ".join([tool.name for tool in self.tools])

            system_prompt = self.planning.replace("{tools}", tool_descriptions).replace("{tool_names}", tool_names)

            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder(variable_name="chat_history", optional=True),
                    ("user", user_input)
                ]
            )

            tools_chat = self.tools
            prompt_chat = prompt.partial(
                tools=render_text_description(list(tools_chat)),
                tool_names=", ".join([t.name for t in tools_chat]),
            )

            # print(prompt_chat.messages[0].prompt.template)
            # exit()


            # Create the chain of runnables for agent chat handling
            agent_chat = (
                RunnablePassthrough.assign(
                    agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"]),
                )
                | prompt_chat
                | my_llm
                | CustomJSONAgentOutputParser()
            )

            # Set up the agent executor
            self.agent_executor_chat = AgentExecutor(
                agent=agent_chat,
                tools=tools_chat,
                verbose=app_config.AGENT_VERBOSE,
                handle_parsing_errors=True,
                max_iterations=50
            )

            # Message history for session management
            message_history = ChatMessageHistory()
            self.agent_with_chat_history = RunnableWithMessageHistory(
                self.agent_executor_chat,
                get_session_history=lambda session_id: message_history,
                input_messages_key="input",
                history_messages_key="chat_history",
            )
        
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            raise

    def invoke_agent(self, input_: str) -> dict:
        """Invokes the agent to process the input and return the result."""
        try:
            start_time = time.time()
            answer = self.agent_with_chat_history.invoke(
                {"input": input_},
                config={"configurable": {"session_id": "meta-llama-hackathon"}}
            )
            end_time = time.time()
            execution_time = round(end_time - start_time, 2)

            logger.info(f"Agent execution completed in {execution_time} seconds.")
            return {
                "output": answer['output'],
                "execution_time": f"{execution_time} sec"
            }
        except Exception as e:
            logger.error(f"Error during agent invocation: {e}")
            raise