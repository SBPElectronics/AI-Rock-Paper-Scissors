import logging
import random

logging.basicConfig(filename='smart_rps_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

dev_mode = 1

def log_print(msg=""):
    if dev_mode:
        print(msg)
    logging.info(msg)

move_options = ["Rock", "Paper", "Scissors"]
beats = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
loses_to = {v: k for k, v in beats.items()}

score = {"Player": 0, "Bot": 0, "Draws": 0}
player_history = []
bot_history = []
after_move_patterns = {m: {"Rock": 0, "Paper": 0, "Scissors": 0} for m in move_options}
move_counts = {"Rock": 0, "Paper": 0, "Scissors": 0}

algo_scores = {
    "Algorithm 1": {"Wins": 0, "Losses": 0, "Draws": 0, "Recent": []},
    "Algorithm 2": {"Wins": 0, "Losses": 0, "Draws": 0, "Recent": []}
}
rumbled_algos = set()

correct_predictions = 0
total_predictions = 0

def get_winner(player_move, bot_move):
    if player_move == bot_move:
        return "Draw"
    elif beats[player_move] == bot_move:
        return "Player"
    else:
        return "Bot"

def update_algo_performance(algo_name, outcome_label):
    plural_map = {"Win": "Wins", "Loss": "Losses", "Draw": "Draws"}
    key = plural_map.get(outcome_label)
    if key:
        algo_scores[algo_name][key] += 1

    algo_scores[algo_name]["Recent"].append(outcome_label)
    if len(algo_scores[algo_name]["Recent"]) > 3:
        algo_scores[algo_name]["Recent"].pop(0)

    if len(algo_scores[algo_name]["Recent"]) >= 3 and \
       algo_scores[algo_name]["Recent"][-3:] == ["Loss", "Loss", "Loss"]:
        rumbled_algos.add(algo_name)

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
    freqs = {m: move_counts[m] / total for m in move_options}
    most_common = max(freqs, key=freqs.get)
    least_common = min(freqs, key=freqs.get)
    predicted = most_common if random.random() < 0.7 else least_common
    return loses_to[predicted]

def choose_algorithm():
    if len(rumbled_algos) == len(algo_scores):
        rumbled_algos.clear()

    valid_algos = [a for a in algo_scores if a not in rumbled_algos]
    if not valid_algos:
        valid_algos = list(algo_scores.keys())

    if len(valid_algos) == 1:
        return valid_algos[0]

    # Use recent window (last up to 3 results) to pick the best performing algorithm
    scores = {}
    for a in valid_algos:
        recent = algo_scores[a]["Recent"][-3:]
        wins = recent.count("Win")
        losses = recent.count("Loss")
        scores[a] = wins - losses

    best = max(scores, key=lambda k: (scores[k], random.random()))
    return best

def pretty_recent(lst):
    return ",".join(lst[-3:]) if lst else ""

while True:
    user_input = input("Enter your move (Rock, Paper, Scissors) or 'Quit' to stop: ").capitalize()
    if user_input == "Quit":
        log_print("Game ended by player.")
        break

    if user_input not in move_options:
        print("Invalid input! Please try again.")
        continue

    player_history.append(user_input)
    move_counts[user_input] += 1

    if len(player_history) > 1:
        after_move_patterns[player_history[-2]][player_history[-1]] += 1

    # Both algorithms make predictions for the bot move (they return the bot move)
    algo1_bot_move = algorithm_1()
    algo2_bot_move = algorithm_2()

    # Choose which algorithm to use this round (based on recent performance and rumble)
    chosen_algo = choose_algorithm()
    predicted_bot_move = algo1_bot_move if chosen_algo == "Algorithm 1" else algo2_bot_move

    # Small randomness to make bot less predictable
    if random.random() < 0.1:
        bot_move = random.choice(move_options)
    else:
        bot_move = predicted_bot_move

    bot_history.append(bot_move)

    winner = get_winner(user_input, bot_move)

    if winner == "Draw":
        score["Draws"] += 1
        log_print("It's a draw!")
    elif winner == "Player":
        score["Player"] += 1
        log_print("You win this round!")
    else:
        score["Bot"] += 1
        log_print("Bot wins this round!")

    total_predictions += 1
    if loses_to[user_input] == bot_move:
        correct_predictions += 1
    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0

    # Update performance for both algorithms based on what they predicted (bot move they would have played)
    for name, alg_bot_move in (("Algorithm 1", algo1_bot_move), ("Algorithm 2", algo2_bot_move)):
        # Compare algorithm's bot-move against the actual player's move
        outcome = get_winner(user_input, alg_bot_move)
        if outcome == "Bot":
            update_algo_performance(name, "Win")
        elif outcome == "Player":
            update_algo_performance(name, "Loss")
        else:
            update_algo_performance(name, "Draw")

    total_moves = sum(move_counts.values())
    move_percents = {m: round((move_counts[m] / total_moves) * 100, 1) for m in move_options}

    log_print(f"Player: {user_input} | Bot: {bot_move}")
    log_print(f"Bot used algorithm: {chosen_algo}")
    log_print(f"Current Score -> Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
    log_print(f"Move Percentages -> Rock: {move_percents['Rock']}% | Paper: {move_percents['Paper']}% | Scissors: {move_percents['Scissors']}%")
    log_print(f"AI Prediction Accuracy: {accuracy:.2f}%")
    log_print("--------------------------------------------------")
    log_print(f"{'Algorithm':15} | {'Wins':>6} | {'Losses':>6} | {'Draws':>6} | {'Recent(3)':>12} | {'Rumbled':>7}")
    for alg_name, data in algo_scores.items():
        rec = pretty_recent(data["Recent"])
        rum = "YES" if alg_name in rumbled_algos else "NO"
        log_print(f"{alg_name:15} | {data['Wins']:6} | {data['Losses']:6} | {data['Draws']:6} | {rec:12} | {rum:7}")
    log_print("--------------------------------------------------")

    # Also print the table to console for immediate feedback
    print(f"\nBot used: {chosen_algo} | Bot Move: {bot_move}")
    print(f"Player: {user_input} | Bot: {bot_move} -> {winner}")
    print(f"Score -> Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
    print(f"Move Percentages -> Rock: {move_percents['Rock']}% | Paper: {move_percents['Paper']}% | Scissors: {move_percents['Scissors']}%")
    print(f"AI Prediction Accuracy: {accuracy:.2f}%")
    print("--------------------------------------------------")
    print(f"{'Algorithm':15} | {'Wins':>6} | {'Losses':>6} | {'Draws':>6} | {'Recent(3)':>12} | {'Rumbled':>7}")
    for alg_name, data in algo_scores.items():
        rec = pretty_recent(data["Recent"])
        rum = "YES" if alg_name in rumbled_algos else "NO"
        print(f"{alg_name:15} | {data['Wins']:6} | {data['Losses']:6} | {data['Draws']:6} | {rec:12} | {rum:7}")
    print("--------------------------------------------------\n")

print("\nFinal Score:")
print(f"Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
log_print(f"Final Score: Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
