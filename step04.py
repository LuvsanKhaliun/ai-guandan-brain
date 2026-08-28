import requests
import re

def fast_pow_mod(base, exponent, modulus):
    """Fast modular exponentiation: (base^exponent) % modulus"""
    result = 1
    base = base % modulus
    
    while exponent > 0:
        if exponent & 1:  
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1  
    
    return result

response = requests.get("http://183.175.14.145:8006/step_04")
data = response.json()
print("Response:", data)

questions = data["questions"]
print(f"\nNumber of questions: {len(questions)}")

answers = []
for i, (a, b, c) in enumerate(questions, 1):
    result = fast_pow_mod(a, b, c)
    answers.append(str(result))
    print(f"Q{i}: {a}^{b} % {c} = {result}")

answer_string = ",".join(answers)
print(f"\nAnswer string: {answer_string}")

submit_response = requests.get(
    "http://183.175.14.145:8006/step_04",
    params={"ans": answer_string}
)

print("\nSubmit response:", submit_response.text)
try:
    print("Parsed:", submit_response.json())
except:
    print("Raw:", submit_response.text)