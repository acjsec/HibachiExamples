from aws_get_secret import get_secret
import json

try:
  secret = get_secret()
except Exception as e:
    print(e)

openai_api_key = json.loads(secret)['OpenAI-Test']

