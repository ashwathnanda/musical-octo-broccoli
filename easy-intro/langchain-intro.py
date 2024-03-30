from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_tweets

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent

from dotenv import load_dotenv


def get_open_ai_llm():
    return ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")


def linkedin_lookup():
    summary_template = """
       given the linkedin information {information} about a person from, I want you to create:
       1. A short summary
       2. Two interesting facts about them
       Add some spicy fun element to the 2nd point basen on the information provided
       """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    llm = get_open_ai_llm()

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    linkedin_profile_url = linkedin_lookup_agent(name="Ashwath Nandakumar")

    scraped_profile_info = scrape_linkedin_profile(linkedin_profile_url)

    if not scraped_profile_info.get("error"):
        print(chain.run(information=scraped_profile_info))


def twitter_lookup():
    summary_template = """
    given the twitter information {information} about a person from, I want you to create something about them from Twitter: 
    1. A short summary
    2. Two interesting facts about
    Add some spicy fun element to the {information}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    llm = get_open_ai_llm()

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    twitter_profile_handle = twitter_lookup_agent(name="Ashwath Nanda")

    scraped_profile_info = scrape_tweets(twitter_profile_handle)

    if not scraped_profile_info.get("error"):
        print(chain.run(information=scraped_profile_info))


if __name__ == '__main__':
    load_dotenv()

    # linkedin_lookup()
    twitter_lookup()

    scrape_tweets("Elon Musk")
