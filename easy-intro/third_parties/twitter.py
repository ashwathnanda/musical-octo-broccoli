import os
from datetime import datetime, timezone

import requests
import tweepy


def scrape_tweets(username, num_tweets=5, mock=False):
    """
    Scrapes a Twitter user's original tweets ( ie, not retweets or replies ) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" ( relative to now ), "text" and "url"
    """
    tweets_list = []

    if mock:
        twitter_gist = "https://gist.githubusercontent.com/ashwathnanda/7"
        tweets = requests.get(twitter_gist, timeout=5).json()

    else:
        auth = tweepy.OAuth1UserHandler(os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET"))
        auth.set_access_token(os.environ.get("TWITTER_ACCESS_TOKEN"), os.environ.get("TWITTER_ACCESS_SECRET"))
        api = tweepy.API(auth)
        tweets = api.user_timeline(screen_name=username, count=num_tweets)

    for twit in tweets:
        if "RT @" not in twit.text and not twit.text.startswith("@"):
            tweet_dict = {"time_posted": str(
                datetime.now(timezone.utc) - twit.created_at
            ), "text": twit.text, "url": f"https://twitter.com/{twit.user.screen_name}/status/{twit.id}"}
            tweets_list.append(tweet_dict)

    return tweets_list
