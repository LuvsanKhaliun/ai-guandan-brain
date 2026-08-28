# AI Guandan Brain

An AI project developed as part of a step-by-step programming challenge to build an intelligent player for **Guandan (掼蛋)**, a popular Chinese card game.

The project gradually develops an AI from basic server communication and card processing to card-pattern recognition, playing strategy, and eventually playing against other players and bots.

## Project Goal

The goal of this project is to build a Guandan AI capable of:

* Understanding its cards and the current game state
* Recognizing valid Guandan card combinations
* Considering the opponent's previous play
* Selecting appropriate moves
* Playing autonomously against other players and bots
* Improving its performance based on game results and Elo ranking

## Technologies that I used for this project

* **Python**
* **REST API / HTTP**
* **JSON**
* **Public-key encryption**
* **Python Requests**
* **Object-oriented and modular programming**

## My Project Progress

The project is developed through multiple stages:

| Step  | Description                 | Status         |
| ----- | --------------------------- | -------------- |
| 01    | Server communication        |   Completed    |
| 02    | JSON data processing        |   Completed    |
| 03    | Public-key encryption       |   Completed    |
| 04–06 | Game and card logic         |   Completed    |
| 07    | Card-pattern recognition    |   Completed    |
| 08    | Playing strategy            |   Completed    |
| 09    | AI table gameplay           |   Completed    |
| 10    | Elo ranking and improvement |   Completed    |

##  Step 7 — Card Pattern Recognition

One of the main components of the project is the card-pattern recognition system.

The recognizer can identify:

* Single
* Pair
* Triple
* Full House
* Straight
* Plate (three consecutive pairs)
* Steel (two consecutive triples)
* Bomb
* Straight Flush
* Four Kings

The system also handles **wildcards (逢人配)** based on the current level card and considers all possible valid combinations when wildcards are present.

### Example

If the current level is `7`:

```text
H7 → Wildcard
```

For example:

```text
H7 D6 C8 S9 HT
```

can be recognized as:

```text
6 - 7 - 8 - 9 - 10
```

and therefore:

```json
{
  "type": "straight",
  "rank": "T"
}
```

## Server Workflow

The AI communicates with the challenge server to receive game data and submit its decisions.

```text
Challenge Server
       ↓
Level + Cards / Game State
       ↓
Python AI
       ↓
Card Recognition
       ↓
Decision / Strategy
       ↓
JSON Answer
       ↓
Challenge Server
```

## Project Structure

```text
AI-Guandan/
│
├── recognizer.py
├── step07_submit.py
├── test.py
├── ...
└── README.md
```

## What I Learned

Through this project, I gained practical experience with:

* Building and consuming HTTP APIs
* Processing structured JSON data
* Implementing card-game rules programmatically
* Designing a modular card-pattern recognition system
* Handling wildcard-based combinations
* Debugging client-server communication
* Developing an AI incrementally through multiple stages
* Thinking about game states and decision-making algorithms



**Language:** Python
**Status:** In Progress
