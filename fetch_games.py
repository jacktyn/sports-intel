import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4"

# The leagues we care about
LEAGUES = {
    "basketball_nba": "NBA",
    "basketball_ncaab": "College Basketball",
    "icehockey_nhl": "NHL",
    "baseball_mlb": "MLB",
    "americanfootball_nfl": "NFL"
}

def fetch_games(sport_key, sport_name):
    url = f"{BASE_URL}/sports/{sport_key}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "h2h,spreads,totals",
        "oddsFormat": "american"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        games = response.json()
        if not games:
            return
        
        print(f"\n{'='*50}")
        print(f"  {sport_name} — {len(games)} game(s) today")
        print(f"{'='*50}")
        
        for game in games:
            home = game['home_team']
            away = game['away_team']
            commence = game['commence_time']
            
            # Parse tip-off time
            tip = datetime.fromisoformat(commence.replace('Z', '+00:00'))
            tip_et = tip.strftime("%a %b %d, %I:%M %p UTC")
            
            print(f"\n  {away} @ {home}")
            print(f"  {tip_et}")
            
            # Pull odds from first available bookmaker
            if game.get('bookmakers'):
                book = game['bookmakers'][0]
                for market in book['markets']:
                    if market['key'] == 'spreads':
                        for outcome in market['outcomes']:
                            print(f"  Spread — {outcome['name']}: {outcome['point']:+.1f} ({outcome['price']:+d})")
                    if market['key'] == 'totals':
                        for outcome in market['outcomes']:
                            if outcome['name'] == 'Over':
                                print(f"  Total — O/U: {outcome['point']}")
                    if market['key'] == 'h2h':
                        ml = [f"{o['name']} {o['price']:+d}" for o in market['outcomes']]
                        print(f"  Moneyline — {' | '.join(ml)}")
    
    elif response.status_code == 404:
        pass  # League not in season, skip silently
    else:
        print(f"  Error fetching {sport_name}: {response.status_code}")

def main():
    print(f"\n🏆 SPORTS INTEL — Daily Game Feed")
    print(f"📅 {datetime.now().strftime('%A, %B %d, %Y')}")
    
    for sport_key, sport_name in LEAGUES.items():
        fetch_games(sport_key, sport_name)
    
    print(f"\n{'='*50}")
    print("  End of daily feed")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()