from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    summary_template = """
    given the linkedin information {information} about a person from, I want you to create:
    1. A short summary
    2. Two interesting facts about them
    Add some spicy fun element to the 2nd point basen on the information provided
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    linkedin_profile_url = linkedin_lookup_agent(name="Ashwath Nandakumar")

    scraped_profile_info = scrape_linkedin_profile(linkedin_profile_url)

    if not scraped_profile_info.get("error"):
        print(chain.run(information=scraped_profile_info))
