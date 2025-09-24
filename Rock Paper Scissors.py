import random
import logging

# Logging Setup
logging.basicConfig(filename='game_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

dev_mode = 1 # 1 meaning development mode, 2 meaning user mode

def log_print(message=""):
    if dev_mode == 1:
        print(message)
    logging.info(message)

# Moves & Rules
move_options = ["Rock", "Paper", "Scissors"]
beats = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
loses_to = {v: k for k, v in beats.items()}

# Game State
moves_array = []
score = {"Player": 0, "Bot": 0, "Draws": 0}
win_streak = 0
current_algorithm = 1
blocked_algorithms = set()

# --- Probability Printers ---
def print_combined_table(prob_data, round_number):
    log_print(f"\n=== Prediction Probabilities (Round {round_number}) ===")
    header = f"{'Algorithm':<12}{'Predicted':<12}{'Rock%':<10}{'Paper%':<10}{'Scissors%'}"
    log_print(header)
    log_print("-" * len(header))
    for algo, data in prob_data.items():
        pred = data['predicted']
        rock = round(data['probs']['Rock'] * 100, 1)
        paper = round(data['probs']['Paper'] * 100, 1)
        scissors = round(data['probs']['Scissors'] * 100, 1)
        log_print(f"{algo:<12}{pred:<12}{rock:<10}{paper:<10}{scissors}")
    log_print("=" * len(header))

# --- Probability Generators ---
def get_probabilities_algo_1():
    if len(moves_array) < 2:
        probs = {m: 1/3 for m in move_options}
    else:
        move_counts = {m: moves_array.count(m) for m in move_options}
        total = sum(move_counts.values())
        probs = {m: move_counts[m] / total for m in move_options}
    predicted = weighted_choice(probs)
    return {"probs": probs, "predicted": predicted}

def get_probabilities_algo_2():
    if len(moves_array) < 2:
        probs = {m: 1/3 for m in move_options}
    else:
        recent = moves_array[-5:]
        move_counts = {m: recent.count(m) for m in move_options}
        total = sum(move_counts.values())
        probs = {m: move_counts[m] / total for m in move_options}
    predicted = weighted_choice(probs)
    return {"probs": probs, "predicted": predicted}

def get_probabilities_algo_3():
    if not moves_array:
        predicted = random.choice(move_options)
    else:
        last = moves_array[-1]
        cycle = {"Rock": "Paper", "Paper": "Scissors", "Scissors": "Rock"}
        predicted = cycle[last]
    probs = {m: 1.0 if m == predicted else 0.0 for m in move_options}
    return {"probs": probs, "predicted": predicted}

def weighted_choice(prob_dict):
    rand = random.random()
    cumulative = 0.0
    for move, prob in prob_dict.items():
        cumulative += prob
        if rand < cumulative:
            return move
    return random.choice(list(prob_dict.keys()))

# --- Gather All Probabilities ---
def calculate_all_probabilities():
    return {
        "Algorithm 1": get_probabilities_algo_1(),
        "Algorithm 2": get_probabilities_algo_2(),
        "Algorithm 3": get_probabilities_algo_3()
    }

# --- Choose Bot Move ---
def get_bot_move(prob_data):
    global current_algorithm
    algo_key = f"Algorithm {current_algorithm}"
    predicted_move = prob_data[algo_key]["predicted"]
    return loses_to[predicted_move]

# --- Algorithm Switch ---
def switch_algorithm():
    global current_algorithm, blocked_algorithms, win_streak
    log_print("\nBOT RUMBLED! You won 3 rounds in a row!")
    log_print(f"Switching strategy... (Avoiding Algorithm {current_algorithm})")
    blocked_algorithms.add(current_algorithm)
    available = [a for a in [1, 2, 3] if a not in blocked_algorithms]
    if available:
        current_algorithm = random.choice(available)
    else:
        blocked_algorithms.clear()
        current_algorithm = random.choice([1, 2, 3])
        log_print("All strategies used. Resetting AI memory.")
    win_streak = 0
    log_print(f"[AI now using Algorithm {current_algorithm}]")
    log_print("-" * 50)

# --- Display Player History ---
def print_player_history():
    log_print("\nYour move history:")
    for i, move in enumerate(moves_array, 1):
        log_print(f"  Round {i}: {move}")
        print("Your move history:")
        print(f"  Round {i}: {move}")
        print("-" * 40)
    
    log_print("-" * 40)


# --- Scoreboard ---
def print_scoreboard():
    log_print("Game Score:")
    log_print(f"  You   : {score['Player']}")
    log_print(f"  Bot   : {score['Bot']}")
    log_print(f"  Draws : {score['Draws']}")
    log_print(f"=" * 100 + "\n")
    if dev_mode == 2:
        print("Game Score:")
        print(f"  You   : {score['Player']}")
        print(f"  Bot   : {score['Bot']}")
        print(f"  Draws : {score['Draws']}")
        print("=" * 100 + "\n")

# --- Intro ---
log_print("=" * 100)
log_print("       Rock, Paper, Scissors — Smart AI       ")
log_print("=" * 100)
log_print("Type Rock, Paper, or Scissors to play. Type Exit to quit.\n")

if dev_mode == 2:
    print("=" * 100)
    print("       Rock, Paper, Scissors — Smart AI       ")    
    print("=" * 100)
    print("Type Rock, Paper, or Scissors to play. Type Exit to quit.\n")

# --- Game Loop ---
round_number = 1
while True:
    prob_data = calculate_all_probabilities()
    print_combined_table(prob_data, round_number)
    log_print(f"Current Algorithm: {current_algorithm}")
    if dev_mode == 2:
        print(f"Current Algorithm: {current_algorithm}")


    player_move = input(f"\nRound {round_number} — Your move: ").capitalize()
    if player_move == "Exit":
        log_print("\nGame Over.")
        print_scoreboard()
        break
    if player_move not in move_options:
        log_print("Invalid input. Try Rock, Paper, or Scissors.\n")
        if dev_mode == 2:
            print("Invalid input. Try Rock, Paper, or Scissors.\n")
        continue

    bot_move = get_bot_move(prob_data)
    log_print(f"\nBot played: {bot_move}")
    if dev_mode == 2:
        print(f"\nBot played: {bot_move}")

    # Outcome
    if bot_move == player_move:
        log_print("It's a draw.\n")
        if dev_mode == 2:
            print("It's a draw.\n")
        score["Draws"] += 1
        win_streak = 0
    elif beats[player_move] == bot_move:
        log_print("You win this round.\n")
        if dev_mode == 2:
            print("You win this round.\n")
        score["Player"] += 1
        win_streak += 1
        if win_streak >= 3:
            switch_algorithm()
    else:
        log_print("Bot wins this round.\n")
        if dev_mode == 2:
            print("Bot wins this round.\n")
        score["Bot"] += 1
        win_streak = 0

    moves_array.append(player_move)
    print_player_history()
    print_scoreboard()
    round_number += 1
    if round_number > 20:
        log_print("Reached 20 rounds. Ending game to prevent fatigue.\n")
        if dev_mode == 2:
            print("Reached 20 rounds. Ending game to prevent fatigue.\n")
        break