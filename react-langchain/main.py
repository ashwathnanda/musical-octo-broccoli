from dotenv import load_dotenv
from langchain.agents import tool
from langchain.tools.render import render_text_description
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """Returns length of a text by characters"""
    return len(text.strip("'\n").strip('"'))


if __name__ == "__main__":
    print("Hello World!")
    tools = [get_text_length]

    template = """
    """
    prompt_template = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=",".join([t.name for t in tools]),
    )

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        model_kwargs={"stop": ["\nObservation", "Observation"]},
    )
