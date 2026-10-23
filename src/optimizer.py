import pandas as pd
import json
import os

def load_rules():
    config_path = os.path.join("config", "auction_rules.yaml")
    rules = {
        "min_batters": 3, "min_bowlers": 3, "min_allrounders": 1, "min_wicketkeepers": 1,
        "max_squad_budget": 1500.0
    }
    if os.path.exists(config_path):
        try:
            import yaml
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data and "playing_xi_constraints" in data:
                    rules.update(data["playing_xi_constraints"])
                if data and "auction_settings" in data:
                    rules["max_squad_budget"] = data["auction_settings"].get("total_purse_crores", 100.0) * 10
        except Exception:
            pass
    return rules

def generate_interactive_html(df, html_path, rules):
    players_json = df.to_json(orient="records")
    default_budget = rules.get("max_squad_budget", 1500.0)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>IPL Dynamic Interactive Optimization Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; font-family: 'Inter', sans-serif; }}
        body {{ background-color: #0f172a; color: #e2e8f0; margin: 0; padding: 30px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ margin-bottom: 25px; border-bottom: 2px solid #1e293b; padding-bottom: 20px; }}
        .header h1 {{ margin: 0; font-size: 28px; color: #38bdf8; }}
        .header p {{ margin: 5px 0 0 0; color: #94a3b8; font-size: 14px; }}
        
        .section-title {{ font-size: 13px; color: #94a3b8; text-transform: uppercase; font-weight: 700; margin-bottom: 10px; letter-spacing: 0.5px; }}
        
        .controls-container {{ display: grid; grid-template-columns: 3fr 1fr; gap: 20px; margin-bottom: 25px; }}
        .controls-card {{ background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }}
        
        .role-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }}
        
        .control-group {{ display: flex; flex-direction: column; gap: 8px; }}
        .control-group label {{ font-size: 11px; color: #38bdf8; font-weight: 600; text-transform: uppercase; }}
        .control-group input {{ width: 100%; accent-color: #38bdf8; cursor: pointer; }}
        .control-group span {{ font-size: 14px; font-weight: bold; color: #f8fafc; }}

        .budget-card {{ border-color: #4ade80; background: #1e293b; }}
        .budget-card label {{ color: #4ade80; }}
        .budget-card input {{ accent-color: #4ade80; }}

        .metrics-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px; }}
        .card {{ background: #1e293b; border-radius: 12px; padding: 18px; border: 1px solid #334155; }}
        .card-title {{ font-size: 12px; color: #94a3b8; text-transform: uppercase; font-weight: 600; }}
        .card-value {{ font-size: 22px; font-weight: 700; color: #f8fafc; margin-top: 6px; }}
        .card-value.highlight {{ color: #38bdf8; }}
        .card-value.success {{ color: #4ade80; }}
        .card-value.danger {{ color: #f87171; }}

        .table-container {{ background: #1e293b; border-radius: 12px; border: 1px solid #334155; overflow: hidden; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; }}
        th {{ background-color: #0f172a; color: #94a3b8; font-weight: 600; text-transform: uppercase; font-size: 12px; padding: 16px; border-bottom: 1px solid #334155; }}
        td {{ padding: 14px 16px; border-bottom: 1px solid #334155; color: #cbd5e1; }}
        tr:hover {{ background-color: #334155; }}
        
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
            <h1>🏏 Dynamic IPL Squad & Budget Optimization Dashboard</h1>
            <p>Adjust role constraints and budget cap in real time to re-optimize the playing XI squad.</p>
        </div>

        <div class="controls-container">
            <!-- Section 1: Role Constraints -->
            <div>
                <div class="section-title">⚙️ Minimum Role Requirements</div>
                <div class="controls-card">
                    <div class="role-grid">
                        <div class="control-group">
                            <label>Min Batters: <span id="val-bat">{rules.get('min_batters', 3)}</span></label>
                            <input type="range" id="input-bat" min="1" max="6" value="{rules.get('min_batters', 3)}" oninput="updateOptimization()">
                        </div>
                        <div class="control-group">
                            <label>Min Bowlers: <span id="val-bowl">{rules.get('min_bowlers', 3)}</span></label>
                            <input type="range" id="input-bowl" min="1" max="6" value="{rules.get('min_bowlers', 3)}" oninput="updateOptimization()">
                        </div>
                        <div class="control-group">
                            <label>Min All-Rounders: <span id="val-ar">{rules.get('min_allrounders', 1)}</span></label>
                            <input type="range" id="input-ar" min="0" max="4" value="{rules.get('min_allrounders', 1)}" oninput="updateOptimization()">
                        </div>
                        <div class="control-group">
                            <label>Min Wicketkeepers: <span id="val-wk">{rules.get('min_wicketkeepers', 1)}</span></label>
                            <input type="range" id="input-wk" min="1" max="3" value="{rules.get('min_wicketkeepers', 1)}" oninput="updateOptimization()">
                        </div>
                    </div>
                </div>
            </div>

            <!-- Section 2: Budget Control -->
            <div>
                <div class="section-title">💰 Financial Purse Limit</div>
                <div class="controls-card budget-card">
                    <div class="control-group">
                        <label>Max Budget Cap: ₹<span id="val-budget">{default_budget:.0f}</span> L</label>
                        <input type="range" id="input-budget" min="500" max="2500" step="50" value="{default_budget:.0f}" oninput="updateOptimization()">
                    </div>
                </div>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="card"><div class="card-title">Squad Size</div><div class="card-value" id="m-size">11 Players</div></div>
            <div class="card"><div class="card-title">Total Rating</div><div class="card-value highlight" id="m-rating">0.00 Pts</div></div>
            <div class="card"><div class="card-title">Budget Allocation</div><div class="card-value success" id="m-cost">₹0.0 / ₹0.0 L</div></div>
            <div class="card"><div class="card-title">Role Composition</div><div class="card-value" style="font-size: 14px; margin-top: 8px;" id="m-comp">-</div></div>
        </div>

        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Rank</th><th>ID</th><th>Player Name</th><th>Role</th><th>Base Price</th>
                        <th>Strike Rate</th><th>Batting Avg</th><th>Economy</th><th>Wkts/Match</th><th>Rating</th>
                    </tr>
                </thead>
                <tbody id="squad-tbody"></tbody>
            </table>
        </div>
    </div>

    <script>
        const allPlayers = {players_json};

        function updateOptimization() {{
            const minBat = parseInt(document.getElementById('input-bat').value);
            const minBowl = parseInt(document.getElementById('input-bowl').value);
            const minAR = parseInt(document.getElementById('input-ar').value);
            const minWK = parseInt(document.getElementById('input-wk').value);
            const maxBudget = parseFloat(document.getElementById('input-budget').value);

            document.getElementById('val-bat').innerText = minBat;
            document.getElementById('val-bowl').innerText = minBowl;
            document.getElementById('val-ar').innerText = minAR;
            document.getElementById('val-wk').innerText = minWK;
            document.getElementById('val-budget').innerText = maxBudget;

            const available = allPlayers.slice();
            const selectedIndices = new Set();
            const squad = [];

            function getTopByRole(roleName, count) {{
                const sub = available.filter((p, i) => p.role === roleName && !selectedIndices.has(i));
                sub.sort((a, b) => b.rating - a.rating);
                for (let p of sub) {{
                    const currentCost = squad.reduce((sum, item) => sum + item.base_price, 0);
                    if (currentCost + p.base_price <= maxBudget) {{
                        const idx = available.indexOf(p);
                        selectedIndices.add(idx);
                        squad.push(p);
                        if (squad.filter(item => item.role === roleName).length >= count) break;
                    }}
                }}
            }}

            getTopByRole('Wicketkeeper', minWK);
            getTopByRole('Batter', minBat);
            getTopByRole('Bowler', minBowl);
            getTopByRole('All-Rounder', minAR);

            const remainingNeeded = 11 - squad.length;
            if (remainingNeeded > 0) {{
                const remaining = available.filter((p, i) => !selectedIndices.has(i));
                remaining.sort((a, b) => b.rating - a.rating);
                for (let p of remaining) {{
                    const currentCost = squad.reduce((sum, item) => sum + item.base_price, 0);
                    if (currentCost + p.base_price <= maxBudget) {{
                        const idx = available.indexOf(p);
                        selectedIndices.add(idx);
                        squad.push(p);
                        if (squad.length >= 11) break;
                    }}
                }}
            }}

            squad.sort((a, b) => b.rating - a.rating);

            const totalRating = squad.reduce((sum, p) => sum + p.rating, 0);
            const totalCost = squad.reduce((sum, p) => sum + p.base_price, 0);
            
            const counts = {{ Batter: 0, Bowler: 0, 'All-Rounder': 0, Wicketkeeper: 0 }};
            squad.forEach(p => counts[p.role] = (counts[p.role] || 0) + 1);

            document.getElementById('m-size').innerText = squad.length + " Players";
            document.getElementById('m-rating').innerText = totalRating.toFixed(2) + " Pts";
            
            const costElem = document.getElementById('m-cost');
            costElem.innerText = "₹" + totalCost.toFixed(1) + " / ₹" + maxBudget.toFixed(0) + " L";
            if (totalCost > maxBudget) {{
                costElem.className = "card-value danger";
            }} else {{
                costElem.className = "card-value success";
            }}

            document.getElementById('m-comp').innerHTML = `🏏 ${{counts.Batter}} Bat | 🎯 ${{counts.Bowler}} Bowl<br>⚡ ${{counts['All-Rounder']}} AR | 🧤 ${{counts.Wicketkeeper}} WK`;

            const tbody = document.getElementById('squad-tbody');
            tbody.innerHTML = '';
            squad.forEach((p, idx) => {{
                const roleClass = p.role.toLowerCase().replace('-', '').replace(' ', '');
                const row = `<tr>
                    <td><strong>#${{idx + 1}}</strong></td>
                    <td>${{p.player_id}}</td>
                    <td style="font-weight: 600; color: #ffffff;">${{p.name}}</td>
                    <td><span class="badge badge-${{roleClass}}">${{p.role}}</span></td>
                    <td>₹${{p.base_price.toFixed(1)}} L</td>
                    <td>${{p.batting_strike_rate}}</td>
                    <td>${{p.batting_average}}</td>
                    <td>${{p.bowling_economy}}</td>
                    <td>${{p.wickets_per_match}}</td>
                    <td style="font-weight: bold; color: #00e676;">${{p.rating.toFixed(2)}}</td>
                </tr>`;
                tbody.innerHTML += row;
            }});
        }}

        updateOptimization();
    </script>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

def optimize_playing_xi():
    data_path = os.path.join("data", "processed", "cleaned_players.csv")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Run data pipeline first.")
        return
    
    df = pd.read_csv(data_path)
    rules = load_rules()
    
    output_dir = os.path.join("data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    
    html_path = os.path.join(output_dir, "optimal_xi.html")
    generate_interactive_html(df, html_path, rules)
    
    print(f"\n[Dynamic Dashboard Generated]")
    print(f" - Interactive HTML Dashboard: {html_path}")

if __name__ == "__main__":
    optimize_playing_xi()