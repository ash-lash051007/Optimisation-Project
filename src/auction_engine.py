import pandas as pd
import os
import random 

def run_auction():
    print("Initializing Auction Engine...")

    # load data
    data_path = os.path.join("data", "processed", "cleaned_players.csv")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found, Make sure the data pipeline has been run")
        return 

    # reading players data
    players_df = pd.read_csv(data_path)
    print(f"Loaded {len(players_df)} players for the auction simulation.")

    # franchieses  
    franchises = {
        "MI": {"purse": 100.0, "squad": []},
        "CSK": {"purse": 100.0, "squad": []},
        "RCB": {"purse": 100.0, "squad": []}
    }

    #players details 
    print("\n---Starting Sequential Auction Loop---\n")
    
    for index, player in players_df.iterrows():
       
        base_price_cr = player['base_price'] / 100
        
        baseline_value = player['rating'] / 10
        current_bid = base_price_cr
        winning_team = None
        active_teams = list(franchises.keys())

        while len(active_teams) > 1 or (len(active_teams) == 1 and not winning_team):
            random.shuffle(active_teams)
            bid_placed = False

            for team in active_teams[:]:
                team_purse = franchises[team]["purse"]
                team_max_valuation = baseline_value * random.uniform(0.8, 1.2)

                if current_bid < team_max_valuation and team_purse >= (current_bid + 0.5):
                    
                    if winning_team != team:
                        current_bid += 0.5
                        winning_team = team
                        bid_placed = True
                        print(f"  -> {team} raises paddle! Bid is now {current_bid} CR")
                        break 
                else:
                    
                    if team in active_teams and team != winning_team:
                        print(f"  -> {team} drops out.")
                        active_teams.remove(team)
            
            if not bid_placed:
                break

        if winning_team:
            franchises[winning_team]["purse"] -= current_bid
            franchises[winning_team]["squad"].append(player['name'])
            print(f"\n SOLD to {winning_team} for {current_bid} CR!")
        else:
            print("\n Unsold (No bids)")

    print("\n--- Auction Simulation Completed ---")
    for team, details in franchises.items():
        print(f"Team {team} Final Squad: {details['squad']} | Purse Left: {round(details['purse'], 2)} CR")

if __name__ == "__main__":
    run_auction()

