from aws_get_secret import get_secret
import json
import argparse

parser = argparse.ArgumentParser(description="Summarize Reddit posts using OpenAI")

parser.add_argument("-r", "--subreddit", 
                    default="popular", 
                    help="Subreddit")
parser.add_argument("-s", "--sort", 
                    default="top", 
                    choices=["best", "hot", "new", "top", "rising"],
                    required=True,
                    help="Sort method")
parser.add_argument("-t", "--top", 
                    default="day", 
                    choices=["hour", "day", "week", "month", "year", "all"],
                    help="Sort method")

args = parser.parse_args()


try:
  secret = get_secret()
except Exception as e:
    print(e)

openai_api_key = json.loads(secret)['OpenAI-Test']

subreddit = args.subreddit
sort = args.sort
top = args.top
url = f"https://www.reddit.com/r/{subreddit}/{sort}" 
#if sort == "top":
#    url += f"?t={top}"

print(args)

print(url)

