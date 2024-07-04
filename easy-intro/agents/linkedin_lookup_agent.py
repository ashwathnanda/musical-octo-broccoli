from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """
    Given the full name {name_Of_Person}, I want you to find the linkedin profile of the person
    Your answer should only contain the linkedin profile URL
    """

    tools_for_agents = [
        Tool(
            "Crawl google 4 linkedin profile page",
            func=get_profile_url,
            description="Crawl google to find the linkedin profile page of the person",
        )
    ]

    # Get the prompt to use - you can modify this!
    prompt = hub.pull("hwchase17/react")

    # Construct the ReAct agent
    agent = create_react_agent(llm, tools_for_agents, prompt)

    # Create an agent executor by passing in the agent and tools
    # verbose=True is very imp. This enables the agent to print the logs.
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agents, verbose=True)

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_Of_Person"]
    )

    # Invoke will take a dict of inputs.
    execution_chain = agent_executor.invoke(
        {"input": {"name_Of_Person": name}, "prompt": prompt_template}
    )
    return execution_chain.get("output")
