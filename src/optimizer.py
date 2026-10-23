import pandas as pd
import os

def optimize_playing_xi():
    print("Loading processed player dataset...")
    data_path = os.path.join("data", "processed", "cleaned_players.csv")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Run data pipeline first.")
        return
    
    df = pd.read_csv(data_path)
    print(f"Dataset loaded with {len(df)} available players.")
    
    top_xi = df.sort_values(by="rating", ascending=False).head(11)
    
    # Terminal Display
    print("\n=== OPTIMAL PLAYING XI ===")
    print(top_xi[['name', 'role', 'rating', 'base_price']])
    print(f"\nTotal Selected Rating: {top_xi['rating'].sum():.2f}")
    
    # Option B: Export HTML & CSV Reports
    output_dir = os.path.join("data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, "optimal_xi.csv")
    html_path = os.path.join(output_dir, "optimal_xi.html")
    
    top_xi.to_csv(csv_path, index=False)
    top_xi.to_html(html_path, index=False)
    
    print(f"\n[Option B UI] Reports successfully generated:")
    print(f" - CSV Report:  {csv_path}")
    print(f" - HTML Report: {html_path}")

if __name__ == "__main__":
    optimize_playing_xi()
