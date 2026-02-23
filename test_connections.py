import requests
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

# Test Odds API
odds_key = os.getenv("ODDS_API_KEY")
url = "https://api.the-odds-api.com/v4/sports"
response = requests.get(url, params={"apiKey": odds_key})

if response.status_code == 200:
    sports = response.json()
    active = [s['title'] for s in sports if s['active']]
    print("✅ Odds API connected!")
    print(f"Active sports today: {len(active)}")
    for s in active[:10]:
        print(f"  - {s}")
else:
    print(f"❌ Odds API failed: {response.status_code}")

# Test Anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=50,
    messages=[{"role": "user", "content": "Say 'Sports Intel online' and nothing else."}]
)
print(f"\n✅ Anthropic connected!")
print(f"Claude says: {message.content[0].text}")