import requests

first_response = requests.get("http://183.175.14.145:8006/step_01")
data = first_response.json()
next_url = data["message"].replace("Please visit ", "")

page_response = requests.get(next_url)

print(page_response.text)