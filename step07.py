import requests
import json
from recognizer import recognize

USER = "0221915013"
URL = "http://183.175.14.145:8006/step_07"

response = requests.get(URL, params={"user": USER})
data = response.json()

while True:

    if "message" in data:
        print("\n🎉 Step 7 completed!")
        print(data["message"])
        break

    level = data["level"]
    groups = data["groups"]

    print("\n==============================")
    print("Level:", level)

    answer = []

    for i, group in enumerate(groups, 1):
        result = recognize(group, level)
        answer.append(result)

        print(f"\nGroup {i}")
        print(group)
        print(result)

    payload = {
        
        "user": USER,
        "ans": json.dumps(answer)
    }

    print("\nSubmitting...")

    response = requests.post(URL, data=payload)

    data = response.json()

    with open("step07_log.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4))
        f.write("\n\n")

    print(json.dumps(data, indent=4))