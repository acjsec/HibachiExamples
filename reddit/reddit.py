from aws_get_secret import get_secret
import json
import argparse
import requests
from openai import OpenAI

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

client = OpenAI(api_key=openai_api_key)

subreddit = args.subreddit
sort = args.sort
top = args.top
url = f"https://www.reddit.com/r/{subreddit}/{sort}/.json" 

if sort == "top":
   url += f"?t={top}"

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"}
web_response = requests.get(url, headers=headers)

def find_all_titles(obj):
  titles = []

  if isinstance(obj, dict):
    for key, value in obj.items():
      if key == "title":
        titles.append(value)
      titles.extend(find_all_titles(value))

  elif isinstance(obj, list):
    for item in obj:
      titles.extend(find_all_titles(item))

  return titles

all_titles = find_all_titles(web_response.json())

openai_response = client.chat.completions.create(
    model="gpt-5.1",
    messages=[
        {"role": "user", "content": f"Summarize the following Reddit post titles in a concise manner. Summarize in paragraph form and do not simply provide a list:\n\n{all_titles}"}
    ]
)

print(openai_response.choices[0].message.content)

#print(all_titles)
#print(args)
#print(url)