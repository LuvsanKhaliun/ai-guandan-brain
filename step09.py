import requests
import time
import json
import re

from strategy import choose_move

USER = "0221915013"

PASSWORD = "1b6e1c49796c550e52422f402da6fa21d1f069e0df1087e64c17f56328207d6bf087df11ebf9282669410d721ec6bcfd329594634cf404f49023edc6a070e7b7e48d5c416294732434eb7984084ae524b4dc62bf198cc2f9a151c81ed9582e63ece71051a6395ff5bc1b788c99b3293cb8138d4f38111c8ddf9706948f6dad15"

BASE = "http://183.175.14.145:8006"

session = requests.Session()

print("===== TEST START =====")

r = session.get(BASE)

print("HOME STATUS:", r.status_code)
print("HOME TEXT:", r.text[:100])
print("HOME COOKIES:", session.cookies)
print("SET COOKIE:", r.headers.get("Set-Cookie"))

print("===== TEST END =====")

# ----- NEW CSRF DEBUG BLOCK -----
r = session.get(BASE + "/step_09")
print("STEP09 STATUS:", r.status_code)
print("STEP09 COOKIES:", session.cookies)
print("STEP09 SET-COOKIE:", r.headers.get("Set-Cookie"))

matches = re.findall(r'.{30}csrf.{30}', r.text, re.IGNORECASE)
print("CSRF MENTIONS IN STEP09 PAGE:")
for m in matches:
    print(m)

r2 = session.get(BASE + "/")
matches2 = re.findall(r'.{30}csrf.{30}', r2.text, re.IGNORECASE)
print("CSRF MENTIONS IN HOME PAGE:")
for m in matches2:
    print(m)


def join_game():
    url = BASE + "/join_game/"
    payload = {
        "user": USER,
        "password": PASSWORD
    }
    r = session.get(url, params=payload)
    try:
        data = r.json()
    except Exception:
        print("Join failed, non-JSON response:", r.text)
        return None
    if not data.get("is_success", True) or "game_id" not in data:
        print("Join failed:", data)
        return None
    return data["game_id"]


def play_game(game_id, cards):
    url = BASE + f"/play_game/{game_id}/"
    payload = {
        "user": USER,
        "password": PASSWORD,
        "coord": json.dumps(cards)
    }
    r = session.get(url, params=payload)   
    print("STATUS:", r.status_code)
    print(r.text)


def check_game(game_id):

    url = BASE + f"/check_game/{game_id}/"

    params = {
        "user": USER,
        "password": PASSWORD
    }

    r = session.get(
        url,
        params=params
    )

    return r.json()

game_id = join_game()

if game_id is None:
    print("Could not join game")
    exit()

print("GAME ID:", game_id)

while True:

    state = check_game(game_id)

    print("\n================")
    print(
    "Turn:",
    state.get("current_turn"),
    "| Your turn:",
    state.get("is_your_turn"),
    "| Cards left:",
    len(state.get("your_hand", []))
    )

    if state.get("completed"):
        print("GAME OVER")

        print("FINAL STATE:", json.dumps(state, indent=2, ensure_ascii=False))
        break

    if state.get("is_your_turn"):

        level = state["level"]
        hand = state["your_hand"]
        last_play = state["last_play"]
        last_player = state["last_player"]
        my_seat = state["your_seat"]
        teams = state["teams"]

        print("DEBUG teams:", teams, "my_seat:", my_seat, "last_player:", last_player)

        print("DEBUG last_play:", last_play, "level:", level)
        print("DEBUG hand:", hand)

        move = choose_move(
            hand,
            level,
            last_play,
            last_player,
            my_seat,
            teams,
            state.get("trick_history", []),
            state.get("hand_counts", [])
        )

        print(
            "AI PLAY:",
            move
        )

        play_game(
            game_id,
            move
        )

    else:

        print(
            "Waiting..."
        )

    time.sleep(5)