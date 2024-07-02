from typing import Tuple

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_tweets

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent

from output_parsers import summary_parser, Summary

from dotenv import load_dotenv


def get_open_ai_llm():
    return ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=True
    )

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_tweets(username=twitter_username, mock=True)

    summary_template = """
    given the information about a person from linkedin {information},
    and their latest twitter posts {twitter_posts} I want you to create:
    1. A short summary
    2. two interesting facts about them 

    Use both information from twitter and Linkedin
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = get_open_ai_llm()

    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})
    return res, linkedin_data.get("profile_url")


if __name__ == '__main__':
    load_dotenv()
    ice_break_with(name="Ashwath Nandakumar")
