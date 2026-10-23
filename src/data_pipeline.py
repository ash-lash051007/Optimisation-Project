import pandas as pd
import numpy as np
import os

def generate_large_dataset():
    np.random.seed(42)
    names = [
        "Virat Kohli", "Jasprit Bumrah", "Rashid Khan", "MS Dhoni", "Rohit Sharma",
        "KL Rahul", "Hardik Pandya", "Rishabh Pant", "Shreyas Iyer", "Suryakumar Yadav",
        "Shubman Gill", "Yuzvendra Chahal", "Ravindra Jadeja", "Mohammed Shami", "Trent Boult",
        "David Warner", "Jos Buttler", "Kagiso Rabada", "Glenn Maxwell", "Sunil Narine",
        "Sanju Samson", "Ishant Sharma", "Kuldeep Yadav", "Axar Patel", "Mohammed Siraj",
        "Marcus Stoinis", "Liam Livingstone", "Nicholas Pooran", "Quinton de Kock", "Faf du Plessis",
        "Mitchell Starc", "Pat Cummins", "Sam Curran", "Travis Head", "Heinrich Klaasen",
        "Arshdeep Singh", "Rinku Singh", "Yashasvi Jaiswal", "Tilak Varma", "Shivam Dube",
        "Ruturaj Gaikwad", "Abhishek Sharma", "Varun Chakravarthy", "Harshal Patel", "Avesh Khan",
        "Rahul Chahar", "Riyan Parag", "Devdutt Padikkal", "Rahul Tewatia", "Shahrukh Khan"
    ]
    roles = ["Batter", "Bowler", "All-Rounder", "Wicketkeeper"]
    
    players = []
    for i, name in enumerate(names, start=101):
        role = np.random.choice(roles, p=[0.35, 0.35, 0.18, 0.12])
        base_price = float(np.random.choice([50.0, 75.0, 100.0, 150.0, 200.0]))
        
        if role == "Batter":
            sr = np.random.uniform(120.0, 165.0)
            avg = np.random.uniform(25.0, 48.0)
            econ, wpm = 0.0, 0.0
        elif role == "Bowler":
            sr, avg = np.random.uniform(80.0, 110.0), np.random.uniform(8.0, 15.0)
            econ = np.random.uniform(6.5, 9.5)
            wpm = np.random.uniform(1.0, 2.2)
        elif role == "All-Rounder":
            sr = np.random.uniform(125.0, 155.0)
            avg = np.random.uniform(20.0, 35.0)
            econ = np.random.uniform(7.0, 9.8)
            wpm = np.random.uniform(0.6, 1.5)
        else: # Wicketkeeper
            sr = np.random.uniform(125.0, 150.0)
            avg = np.random.uniform(28.0, 42.0)
            econ, wpm = 0.0, 0.0
            
        players.append({
            "player_id": i,
            "name": name,
            "role": role,
            "base_price": round(base_price, 2),
            "batting_strike_rate": round(sr, 2),
            "batting_average": round(avg, 2),
            "bowling_economy": round(econ, 2),
            "wickets_per_match": round(wpm, 2)
        })
    return pd.DataFrame(players)

def run_pipeline():
    raw_dir = os.path.join("data", "raw")
    processed_dir = os.path.join("data", "processed")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    
    raw_path = os.path.join(raw_dir, "ipl_players.csv")
    if os.path.exists(raw_path):
        print(f"Loading dataset from {raw_path}...")
        df = pd.read_csv(raw_path)
    else:
        print("Raw dataset not found. Generating large 50-player auction dataset...")
        df = generate_large_dataset()
        df.to_csv(raw_path, index=False)
        
    # Calculate Composite Performance Valuation Rating
    df["rating"] = (
        (df["batting_strike_rate"] * 0.4) +
        (df["batting_average"] * 0.3) +
        ((12.0 - df["bowling_economy"].replace(0, 12.0)) * 5.0) +
        (df["wickets_per_match"] * 25.0)
    ).round(2)
    
    output_path = os.path.join(processed_dir, "cleaned_players.csv")
    df.to_csv(output_path, index=False)
    print(f"Success! Processed dataset with {len(df)} players saved to: {output_path}")

if __name__ == "__main__":
    run_pipeline()
