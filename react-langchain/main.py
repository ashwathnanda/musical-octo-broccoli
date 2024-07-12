from typing import List, Union

from dotenv import load_dotenv
from langchain.agents import tool
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """Returns length of a text by characters"""
    return len(text.strip("'\n").strip('"'))


def find_tool_by_name(toolList: List[Tool], name: str):
    for tool in toolList:
        if tool.name == name:
            return tool
    raise ValueError(f"Tool with name {name} not found in the list of tools")


if __name__ == "__main__":
    print("Hello World!")
    tools = [get_text_length]

    template = """
    Answer the following questions as best you can. You have access to the following tools:
    
    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought:{agent_scratchpad}
    """

    # We feed the name and description of the tools ( decorated with @tools ) to the prompt template
    # which is fed to the agent along with the prompt
    prompt_template = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=",".join([t.name for t in tools]),
    )

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        model_kwargs={"stop": ["\nObservation", "Observation"]},
    )

    agent = (
        {"input": lambda x: x["input"]}
        | prompt_template
        | llm
        | ReActSingleInputOutputParser()
    )

    # This will determine which tool to use based on the input
    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        {"input": "What is the length of 'Hello World? by characters'"}
    )

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_input = agent_step.action_input
        tool_to_use = find_tool_by_name(tools, tool_name)

        tool_output = tool_to_use.func(str(tool_input))

        agent_step = agent.invoke({"input": tool_output})
