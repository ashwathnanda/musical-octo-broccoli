from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from thrid_parties.linkedin import scrape_linkedin_profile

from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    summary_template = """
    given the linkedin information {information} about a person from, I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    scraped_profile_info = scrape_linkedin_profile("https://www.linkedin.com/in/ashwath-nandakumar/")

    if not scraped_profile_info.get("error"):
        print(chain.run(information=scraped_profile_info))
