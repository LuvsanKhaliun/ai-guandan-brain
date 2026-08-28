import requests
import json

from strategy import choose_move

USER = "0221915013"

URL = "http://183.175.14.145:8006/step_08"

response = requests.get(
    URL,
    params={
        "user": USER
    }
)

data = response.json()

print("===== SERVER DATA =====")
print(json.dumps(
    data,
    indent=2
))

questions = data["questions"]

answers = []

for i, q in enumerate(questions):

    print("\n====================")
    print("Question", i+1)

    level = q["level"]

    hand = q["hand"]

    last_play = q["last_play"]

    last_player = q["last_player"]

    print("Level:", level)
    print("Hand:", hand)
    print("Last:", last_play)
    print("Player:", last_player)

    move = choose_move(
        hand,
        level,
        last_play,
        last_player
    )

    print("AI move:", move)

    answers.append(move)

payload = {
    "user": USER,
    "ans": json.dumps(
        answers
    )
}

print("\n===== SUBMIT =====")
print(payload)

result = requests.post(
    URL,
    json=payload
)

print("\n===== RESULT =====")
print(result.text)