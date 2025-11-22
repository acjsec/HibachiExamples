from aws_get_secret import get_secret

# from aws.get_secret import get_secret

try:
  secret = get_secret()
except Exception as e:
    print(e)

print(secret)
print(type(secret))