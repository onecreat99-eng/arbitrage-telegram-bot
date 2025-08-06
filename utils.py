def calculate_profit(odds_a, odds_b):
    if not odds_a or not odds_b:
        return 0
    prob_sum = (1 / odds_a) + (1 / odds_b)
    profit_percent = (1 - prob_sum) * 100
    return round(profit_percent, 2)

def normalize_team_name(name):
    return name.strip().lower().replace("-", " ").replace(".", "").replace("fc", "").strip()
