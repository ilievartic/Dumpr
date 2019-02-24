import requests

url = "http://35.188.64.208:80/create"

payload = "first_name=asdf&last_name=asd&plate_num=qwerty"
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Postman-Token': "ef1ecc98-41eb-42cb-bb1b-290cdd7a6e15"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)