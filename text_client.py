import json
from houndify_api import houndify
from houndify_api.settings import CLIENT_ID, CLIENT_KEY, USER, LOCATION

client = houndify.TextHoundClient(CLIENT_ID, CLIENT_KEY, USER, LOCATION)

print('How can I help you?')
user_input = input()
while user_input != 'q':
    response = client.query(user_input)
    #print(response)
    print(response['AllResults'][0]['WrittenResponse'])
    print(response['AllResults'][0]['WrittenResponseLong'])
    #print(json.dumps(response['AllResults'], indent=4, sort_keys=True))
    print()
    user_input = input()
