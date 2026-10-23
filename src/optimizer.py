import pandas as pd
import os

def generate_styled_html(df, top_xi, html_path):
    total_rating = top_xi['rating'].sum()
    total_cost = top_xi['base_price'].sum()
    total_players = len(top_xi)
    
    table_rows = ""
    for idx, row in top_xi.reset_index(drop=True).iterrows():
        role_class = row['role'].lower().replace('-', '').replace(' ', '')
        table_rows += f"""
        <tr>
            <td><strong>#{idx+1}</strong></td>
            <td>{row['player_id']}</td>
            <td style="font-weight: 600; color: #ffffff;">{row['name']}</td>
            <td><span class="badge badge-{role_class}">{row['role']}</span></td>
            <td>?{row['base_price']:.1f} L</td>
            <td>{row['batting_strike_rate']}</td>
            <td>{row['batting_average']}</td>
            <td>{row['bowling_economy']}</td>
            <td>{row['wickets_per_match']}</td>
            <td style="font-weight: bold; color: #00e676;">{row['rating']:.2f}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>IPL Auction Optimization Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; font-family: 'Inter', sans-serif; }}
        body {{ background-color: #0f172a; color: #e2e8f0; margin: 0; padding: 30px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 2px solid #1e293b; padding-bottom: 20px; }}
        .header h1 {{ margin: 0; font-size: 28px; color: #38bdf8; letter-spacing: -0.5px; }}
        .header p {{ margin: 5px 0 0 0; color: #94a3b8; font-size: 14px; }}
        
        .metrics-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 35px; }}
        .card {{ background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); }}
        .card-title {{ font-size: 13px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }}
        .card-value {{ font-size: 28px; font-weight: 700; color: #f8fafc; margin-top: 8px; }}
        .card-value.highlight {{ color: #38bdf8; }}
        .card-value.success {{ color: #4ade80; }}

        .table-container {{ background: #1e293b; border-radius: 12px; border: 1px solid #334155; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; }}
        th {{ background-color: #0f172a; color: #94a3b8; font-weight: 600; text-transform: uppercase; font-size: 12px; padding: 16px; border-bottom: 1px solid #334155; }}
        td {{ padding: 14px 16px; border-bottom: 1px solid #334155; color: #cbd5e1; }}
        tr:hover {{ background-color: #334155; transition: background-color 0.2s ease; }}
        
        .badge {{ padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }}
        .badge-batter {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid #38bdf8; }}
        .badge-bowler {{ background: rgba(248, 113, 113, 0.15); color: #f87171; border: 1px solid #f87171; }}
        .badge-allrounder {{ background: rgba(250, 204, 21, 0.15); color: #facc15; border: 1px solid #facc15; }}
        .badge-wicketkeeper {{ background: rgba(192, 132, 252, 0.15); color: #c084fc; border: 1px solid #c084fc; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>?? IPL Squad Optimization Analytics</h1>
                <p>Optimal Playing XI Selection Engine Output</p>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="card">
                <div class="card-title">Selected Playing Squad</div>
                <div class="card-value">{total_players} Players</div>
            </div>
            <div class="card">
                <div class="card-title">Total Cumulative Rating</div>
                <div class="card-value highlight">{total_rating:.2f} Pts</div>
            </div>
            <div class="card">
                <div class="card-title">Total Squad Base Cost</div>
                <div class="card-value success">?{total_cost:.1f} Lakhs</div>
            </div>
        </div>

        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>ID</th>
                        <th>Player Name</th>
                        <th>Role</th>
                        <th>Base Price</th>
                        <th>Strike Rate</th>
                        <th>Batting Avg</th>
                        <th>Economy</th>
                        <th>Wkts / Match</th>
                        <th>Rating</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

def optimize_playing_xi():
    print("Loading processed player dataset...")
    data_path = os.path.join("data", "processed", "cleaned_players.csv")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Run data pipeline first.")
        return
    
    df = pd.read_csv(data_path)
    print(f"Dataset loaded with {len(df)} available players.")
    
    top_xi = df.sort_values(by="rating", ascending=False).head(11)
    
    print("\n=== OPTIMAL PLAYING XI ===")
    print(top_xi[['name', 'role', 'rating', 'base_price']])
    print(f"\nTotal Selected Rating: {top_xi['rating'].sum():.2f}")
    
    output_dir = os.path.join("data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, "optimal_xi.csv")
    html_path = os.path.join(output_dir, "optimal_xi.html")
    
    top_xi.to_csv(csv_path, index=False)
    generate_styled_html(df, top_xi, html_path)
    
    print(f"\n[Option B Dashboard] Successfully updated:")
    print(f" - CSV Report:  {csv_path}")
    print(f" - HTML Report: {html_path}")

if __name__ == "__main__":
    optimize_playing_xi()
