import requests
import re

first_response = requests.get("http://183.175.14.145:8006/step_01")
data = first_response.json()
next_url = re.search(r'https?://[^\s]+', data["message"]).group()

your_name = "tianmi"
your_student_number = "2024001"  

step2_url = "http://183.175.14.145:8006/step_02"
response = requests.get(step2_url, params={
    "name": your_name,
    "student_number": your_student_number
})

result = response.json()
print("Step 2 response:", result)

next_url = re.search(r'https?://[^\s]+', result["message"]).group()
print("Extracted URL:", next_url)

step3_response = requests.get(next_url)
print("Step 3 page loaded!")
print(step3_response.text[:800])  