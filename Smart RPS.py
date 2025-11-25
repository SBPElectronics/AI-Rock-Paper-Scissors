import logging
import random

logging.basicConfig(filename='smart_rps_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

dev_mode = 1

def log_print(message=""):
    if dev_mode == 1:
        print(message)
    logging.info(message)

move_options = ["Rock", "Paper", "Scissors"]
beats = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
loses_to = {v: k for k, v in beats.items()}

score = {"Player": 0, "Bot": 0, "Draws": 0}
player_history = []
after_move_patterns = {m: {"Rock": 0, "Paper": 0, "Scissors": 0} for m in move_options}
move_counts = {"Rock": 0, "Paper": 0, "Scissors": 0}

correct_predictions = 0
total_predictions = 0

# Track performance of each algorithm (wins, losses, draws, and recent outcomes)
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

def weighted_choice():
    total = sum(move_counts.values())
    if total == 0:
        return random.choice(move_options)
    weights = {m: move_counts[m] / total for m in move_options}
    most_common = max(weights, key=weights.get)
    return loses_to[most_common]

def algorithm_1():
    if len(player_history) < 2:
        return random.choice(move_options)
    last = player_history[-1]
    next_likely = max(after_move_patterns[last], key=after_move_patterns[last].get)
    return loses_to[next_likely]

def algorithm_2():
    # Frequency Analysis: Predict player will favor or counter their most frequent move
    total = sum(move_counts.values())
    if total == 0:
        return random.choice(move_options)
    frequencies = {m: move_counts[m] / total for m in move_options}
    most_freq = max(frequencies, key=frequencies.get)
    least_freq = min(frequencies, key=frequencies.get)
    # Decide which tendency is stronger: leaning on frequent or balancing least frequent
    if frequencies[most_freq] > 0.5:
        # Player likely to keep playing most frequent move, so counter it
        return loses_to[most_freq]
    else:
        # Player might balance by using least frequent move, so counter that
        return loses_to[least_freq]

def update_algo_performance(algo_name, outcome):
    # Existing mapping...
    mapping = {
        "Win": "Wins",
        "Loss": "Losses",
        "Draw": "Draws"
    }
    key = mapping.get(outcome)
    if key is None:
        return

    algo_scores[algo_name][key] += 1
    recent = algo_scores[algo_name]["Recent"]
    recent.append(outcome)
    if len(recent) > 5:
        recent.pop(0)

    # Check for 3 losses in a row -> Rumbled
    if len(recent) >= 3:
        last_three = recent[-3:]
        if last_three == ["Loss", "Loss", "Loss"]:
            rumbled_algos.add(algo_name)
        else:
            rumbled_algos.discard(algo_name)

    # Check for 3 draws in a row -> Disliked
    if len(recent) >= 3:
        last_three = recent[-3:]
        if last_three == ["Draw", "Draw", "Draw"]:
            disliked_algos.add(algo_name)
        else:
            disliked_algos.discard(algo_name)



def choose_algorithm():
    # If all algorithms are rumbled, clear rumbled set (reset)
    if len(rumbled_algos) == len(algo_scores):
        rumbled_algos.clear()

    # Filter only unrumbled algorithms
    available_algos = [algo for algo in algo_scores if algo not in rumbled_algos]
    if not available_algos:
        available_algos = list(algo_scores.keys())  # fallback in case all are rumbled

    # Compare wins in last 3 rounds (or total wins if preferred)
    # For now, using total wins as simpler proxy
    best_algo = None
    best_wins = -1
    for algo in available_algos:
        wins = algo_scores[algo]["Wins"]
        if wins > best_wins:
            best_wins = wins
            best_algo = algo

    # If tie or no clear best, pick random
    if best_wins == 0:
        best_algo = random.choice(available_algos)

    return best_algo

def get_algo_prediction(algo_name):
    if algo_name == "Algorithm 1":
        return algorithm_1()
    elif algo_name == "Algorithm 2":
        return algorithm_2()
    else:
        return random.choice(move_options)

while True:
    user_input = input(f"Enter your move (Rock, Paper, Scissors) or 'Quit' to stop: ").capitalize()

    if user_input == "Quit":
        log_print("Game ended by player.")
        break

    if user_input not in move_options:
        print("Invalid input! Please try again.")
        continue

    player_history.append(user_input)
    move_counts[user_input] += 1

    if len(player_history) > 1:
        last_move = player_history[-2]
        current_move = player_history[-1]
        after_move_patterns[last_move][current_move] += 1

    # Get predictions from both algorithms
    prediction_1 = algorithm_1()
    prediction_2 = algorithm_2()

    # Choose the bot move from the best algorithm
    chosen_algo = choose_algorithm()
    predicted_move = get_algo_prediction(chosen_algo)

    if random.random() < 0.1:  # randomness to keep AI less predictable
        bot_move = random.choice(move_options)
    else:
        bot_move = predicted_move

    winner = get_winner(user_input, bot_move)

    if winner == "Draw":
        score["Draws"] += 1
        log_print("It's a draw!")
        outcome = "Draw"
    elif winner == "Player":
        score["Player"] += 1
        log_print("You win this round!")
        outcome = "Loss"  # Bot perspective
    else:
        score["Bot"] += 1
        log_print("Bot wins this round!")
        outcome = "Win"  # Bot perspective

    # Now update performance for both algorithms separately
    # Determine Algorithm 1 outcome against player move
    algo1_outcome = "Draw" if prediction_1 == user_input else (
        "Win" if beats[prediction_1] == user_input else "Loss"
    )
    update_algo_performance("Algorithm 1", algo1_outcome)

    # Determine Algorithm 2 outcome against player move
    algo2_outcome = "Draw" if prediction_2 == user_input else (
        "Win" if beats[prediction_2] == user_input else "Loss"
    )
    update_algo_performance("Algorithm 2", algo2_outcome)

    total_predictions += 1
    if loses_to[user_input] == bot_move:
        correct_predictions += 1
    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0

    total_moves = sum(move_counts.values())
    move_percents = {m: round((move_counts[m] / total_moves) * 100, 1) for m in move_options}

    # Print game state and algorithm performance table
    print(f"\nPlayer: {user_input} | Bot: {bot_move}")
    print(f"Current Score -> Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
    print(f"Move Percentages -> Rock: {move_percents['Rock']}% | Paper: {move_percents['Paper']}% | Scissors: {move_percents['Scissors']}%")
    print(f"AI Prediction Accuracy: {accuracy:.2f}%")
    print("\nAlgorithm Performance:")
    print(f"{'Algorithm':<12} | {'Wins':>4} | {'Losses':>6} | {'Draws':>5} | {'Recent (last 5)':<20} | {'Status':<7}")
    print("-" * 70)
    for algo, data in algo_scores.items():
        status = "Rumbled" if algo in rumbled_algos else "Active"
        recent_str = ','.join(data["Recent"])
        print(f"{algo:<12} | {data['Wins']:>4} | {data['Losses']:>6} | {data['Draws']:>5} | {recent_str:<20} | {status:<7}")

print("\nFinal Score:")
print(f"Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
log_print(f"Final Score: Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
