import logging
import random

# "Smart Rock Paper Scissors Engine"

dev_mode = 2  # 0=silent, 1=full output + prompt, 2=output but no prompt text

logger = logging.getLogger("SmartRPS")
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.propagate = False  # Avoid duplicate prints

file_handler = logging.FileHandler("smart_rps_log.txt", mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
logger.addHandler(file_handler)

if dev_mode in (1, 2):
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console_handler)

def log_print(msg="", detailed=False):
    """
    Prints message.
    If detailed=True, print on console only if dev_mode==1,
    else log only to file.
    """
    if detailed:
        if dev_mode == 1:
            logger.info(msg)
        else:
            # Log only to file, bypass console handler
            file_handler.emit(logging.makeLogRecord({"msg": msg, "levelno": logging.INFO, "levelname": "INFO"}))
    else:
        logger.info(msg)

move_options = ["Rock", "Paper", "Scissors"]
beats = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
loses_to = {v: k for k, v in beats.items()}

score = {"Player": 0, "Bot": 0, "Draws": 0}
player_history = []
after_move_patterns = {m: {"Rock": 0, "Paper": 0, "Scissors": 0} for m in move_options}
move_counts = {"Rock": 0, "Paper": 0, "Scissors": 0}

correct_predictions = 0
total_predictions = 0

algo_scores = {
    "Algorithm 1": {"Wins": 0, "Losses": 0, "Draws": 0, "Recent": []},
    "Algorithm 2": {"Wins": 0, "Losses": 0, "Draws": 0, "Recent": []}
}

rumbled_algos = set()
disliked_algos = set()

def get_winner(player, bot):
    if player == bot:
        return "Draw"
    elif beats[player] == bot:
        return "Player"
    else:
        return "Bot"

def algorithm_1():
    if len(player_history) < 2:
        return random.choice(move_options)
    last = player_history[-1]
    next_likely = max(after_move_patterns[last], key=after_move_patterns[last].get)
    return loses_to[next_likely]

def algorithm_2():
    total = sum(move_counts.values())
    if total == 0:
        return random.choice(move_options)
    freq = {m: move_counts[m] / total for m in move_options}
    most = max(freq, key=freq.get)
    least = min(freq, key=freq.get)
    if freq[most] > 0.5:
        return loses_to[most]
    else:
        return loses_to[least]

def update_algo_performance(algo_name, outcome):
    m = {"Win": "Wins", "Loss": "Losses", "Draw": "Draws"}
    key = m.get(outcome)
    if not key:
        return
    algo_scores[algo_name][key] += 1
    r = algo_scores[algo_name]["Recent"]
    r.append(outcome)
    if len(r) > 5:
        r.pop(0)
    if len(r) >= 3:
        last3 = r[-3:]
        if last3 == ["Loss", "Loss", "Loss"]:
            rumbled_algos.add(algo_name)
        else:
            rumbled_algos.discard(algo_name)
        if last3 == ["Draw", "Draw", "Draw"]:
            disliked_algos.add(algo_name)
        else:
            disliked_algos.discard(algo_name)

def choose_algorithm():
    if len(rumbled_algos) == len(algo_scores):
        rumbled_algos.clear()
    available = [a for a in algo_scores if a not in rumbled_algos]
    if not available:
        available = list(algo_scores.keys())
    best = max(available, key=lambda a: algo_scores[a]["Wins"], default=random.choice(available))
    if algo_scores[best]["Wins"] == 0:
        best = random.choice(available)
    return best

def get_algo_prediction(algo):
    if algo == "Algorithm 1":
        return algorithm_1()
    elif algo == "Algorithm 2":
        return algorithm_2()
    return random.choice(move_options)

round_num = 1
while True:
    log_print(player_history)
    log_print("\n" + "=" * 60)
    log_print(f"ROUND {round_num}")
    log_print("=" * 60)

    if dev_mode == 1:
        user_input = input("Enter your move (Rock, Paper, Scissors) or 'Quit' to stop: ")
    else:
        user_input = input()

    user = user_input.capitalize()

    if user == "Quit":
        log_print("Game ended by player.")
        break
    if user not in move_options:
        log_print("Invalid input! Try again.")
        continue
    player_history.append(user)
    move_counts[user] += 1
    if len(player_history) > 1:
        after_move_patterns[player_history[-2]][player_history[-1]] += 1
    pred1 = algorithm_1()
    pred2 = algorithm_2()
    algo = choose_algorithm()
    pred = get_algo_prediction(algo)
    bot = pred if random.random() > 0.1 else random.choice(move_options)
    result = get_winner(user, bot)
    if result == "Draw":
        score["Draws"] += 1
        outcome = "Draw"
        msg = "It's a draw!"
    elif result == "Player":
        score["Player"] += 1
        outcome = "Loss"
        msg = "You win this round!"
    else:
        score["Bot"] += 1
        outcome = "Win"
        msg = "Bot wins this round!"
    for name, p in [("Algorithm 1", pred1), ("Algorithm 2", pred2)]:
        res = "Draw" if p == user else ("Win" if beats[p] == user else "Loss")
        update_algo_performance(name, res)
    total_predictions += 1
    if loses_to[user] == bot:
        correct_predictions += 1
    acc = (correct_predictions / total_predictions) * 100
    total_moves = sum(move_counts.values())
    move_percents = {m: round((move_counts[m] / total_moves) * 100, 1) for m in move_options}

    log_print("\n" + "-" * 60)
    log_print(f"Algo Used: {algo}")
    log_print(f"Player Move: {user}")
    log_print(f"Bot Move: {bot}")
    log_print(msg)  
    log_print("-" * 60)
    log_print(f"Score -> Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
    
    

    # Detailed stats:
    log_print(f"Move Percentages -> Rock: {move_percents['Rock']}% | Paper: {move_percents['Paper']}% | Scissors: {move_percents['Scissors']}%", detailed=True)
    log_print(f"Prediction Accuracy: {acc:.2f}%", detailed=True)
    log_print("Algorithm Performance:", detailed=True)
    log_print(f"{'Algorithm':<12} | {'Wins':>4} | {'Losses':>6} | {'Draws':>5} | {'Recent (5)':<20} | {'Status':<9}", detailed=True)
    log_print("-" * 75, detailed=True)
    for name, d in algo_scores.items():
        if name in rumbled_algos:
            status = "Rumbled"
        elif name in disliked_algos:
            status = "Disliked"
        else:
            status = "Active"
        rec = ','.join(d["Recent"])
        log_print(f"{name:<12} | {d['Wins']:>4} | {d['Losses']:>6} | {d['Draws']:>5} | {rec:<20} | {status:<9}", detailed=True)

    log_print("=" * 60)
    round_num += 1

log_print("\nFINAL SCORE")
log_print(f"Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
