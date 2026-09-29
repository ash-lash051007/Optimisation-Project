import pandas as pd
import os

def load_and_clean_data():
    print("Loading raw IPL data...")
    
    # Define paths
    raw_path = os.path.join("data", "raw", "ipl_players.csv")
    output_dir = os.path.join("data", "processed")
    output_path = os.path.join(output_dir, "cleaned_players.csv")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if raw data exists; if not, use a robust fallback template so the pipeline doesn't crash
    if os.path.exists(raw_path):
        df = pd.read_csv(raw_path)
    else:
        print(f"Warning: '{raw_path}' not found. Using extended template data for testing.")
        df = pd.DataFrame({
            'player_id': [101, 102, 103, 104],
            'name': ['Virat Kohli', 'Jasprit Bumrah', 'Rashid Khan', 'MS Dhoni'],
            'role': ['Batter', 'Bowler', 'All-Rounder', 'Wicketkeeper'],
            'base_price': [200.0, 200.0, 150.0, 150.0],
            'batting_strike_rate': [135.0, 45.0, 125.0, 137.0],
            'batting_average': [37.2, 10.5, 20.1, 39.0],
            'bowling_economy': [0.0, 6.8, 6.3, 0.0],
            'wickets_per_match': [0.0, 1.5, 1.2, 0.0]
        })

    # --- 1. HANDLING MISSING VALUES ---
    # Fill missing numerical stats with 0 or median values
    df['base_price'] = df['base_price'].fillna(20.0) # Default base price if missing
    df['batting_strike_rate'] = df['batting_strike_rate'].fillna(df['batting_strike_rate'].median())
    df['batting_average'] = df['batting_average'].fillna(df['batting_average'].median())
    df['bowling_economy'] = df['bowling_economy'].fillna(9.0) # Penalty default economy for non-bowlers
    df['wickets_per_match'] = df['wickets_per_match'].fillna(0.0)

    # --- 2. PLAYER VALUATION METRIC ---
    # Creating a composite performance rating based on role/stats
    # (You can tweak these weights later for your game theory model!)
    def calculate_rating(row):
        batting_score = (row['batting_strike_rate'] * 0.4) + (row['batting_average'] * 1.5)
        bowling_score = (row['wickets_per_match'] * 20) + max(0, (12 - row['bowling_economy']) * 5)
        return round(batting_score + bowling_score, 2)

    df['rating'] = df.apply(calculate_rating, axis=1)

    # --- 3. EXPORT CLEANED DATA ---
    df.to_csv(output_path, index=False)
    print(f"Success! Cleaned data with valuations saved to: {output_path}")

if __name__ == "__main__":
    load_and_clean_data()