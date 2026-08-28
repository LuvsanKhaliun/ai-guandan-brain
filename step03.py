import requests
import re

response = requests.get("http://183.175.14.145:8006/context/crypto_intro")
text = response.text

print(f"Page length: {len(text)} characters")
print(f"Number of lines: {len(text.splitlines())}")

urls = re.findall(r'https?://183\.175\.14\.145:8006/context/[a-f0-9]+', text)

print("\nFound URLs:")
for url in urls:
    print(f"  {url}")

print("\n" + "="*60)
print("LAST 2000 CHARACTERS:")
print("="*60)
print(text[-2000:])