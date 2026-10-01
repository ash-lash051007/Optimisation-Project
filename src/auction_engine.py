import pandas as pd
import os

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
        # Convert base price from Lakhs to Crores (e.g., 200 Lakhs = 2.0 CR)
        base_price_cr = player['base_price'] / 100
        print(f"\nUp for grabs: {player['name']} ({player['role']}) | Base Price: {base_price_cr} CR | Rating: {player['rating']}")
        sold = False

    # franchieses details and adding player to squad who can afford 
        for team, details in franchises.items():
            if details["purse"]>= base_price_cr:
                details["purse"] -= base_price_cr
                details["squad"].append(player["name"])
                print(f" -> Sold to {team} for {base_price_cr} CR! (Remaining Purse: {round(details['purse'], 2)} CR)")   
                sold = True
                break
        if not sold:
            print("-> Unsold (Insufficient purse across all teasm)")
    
    print ("\n---Auction Simulation Completed---")

# printing the final squads and remianing purses
    for team, details in franchises.items():
        print(f"Team {team} Final Squad: {details['squad']} | Purse Left: {round(details['purse'], 2)} CR")    

if __name__ == "__main__":
    run_auction()    
