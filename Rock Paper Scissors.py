import random

# Moves and outcomes
move_options = ["Rock", "Paper", "Scissors"]
beats = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
loses_to = {v: k for k, v in beats.items()}

# Game state
moves_array = []
score = {"Player": 0, "Bot": 0, "Draws": 0}
win_streak = 0
current_algorithm = 1
blocked_algorithms = set()

# AI memory (optional, used to display transition matrix)
transition_matrix = {
    "Rock": {"Rock": 1, "Paper": 1, "Scissors": 1},
    "Paper": {"Rock": 1, "Paper": 1, "Scissors": 1},
    "Scissors": {"Rock": 1, "Paper": 1, "Scissors": 1}
}

# === Display transition memory
def print_transition_matrix():
    print("\nAI Transition Memory Matrix:")
    print("        Rock   Paper  Scissors")
    for prev_move in move_options:
        row = transition_matrix[prev_move]
        print(f"{prev_move:<8} {row['Rock']:<6} {row['Paper']:<6} {row['Scissors']}")
    print("-" * 40)

# === Display prediction probabilities
def print_probabilities(prob_dict, context, round_number):
    print(f"\nRound {round_number} | {context} Prediction Probabilities:")
    for move in move_options:
        percent = round(prob_dict.get(move, 0) * 100, 1)
        print(f"  {move:<9}: {percent}%")
    print("-" * 40)

# === Choose based on probability weights
def weighted_choice(prob_dict):
    rand = random.random()
    cumulative = 0.0
    for move, prob in prob_dict.items():
        cumulative += prob
        if rand < cumulative:
            return move
    return random.choice(list(prob_dict.keys()))

# === Algorithm 1 — Full history
def get_bot_move_algorithm_1(round_number):
    if len(moves_array) < 2:
        return random.choice(move_options)
    move_counts = {m: moves_array.count(m) for m in move_options}
    total = sum(move_counts.values())
    probabilities = {move: count / total for move, count in move_counts.items()}
    print_probabilities(probabilities, "Algorithm 1 (Full History)", round_number)
    predicted_move = weighted_choice(probabilities)
    return loses_to[predicted_move]

# === Algorithm 2 — Last 5 moves
def get_bot_move_algorithm_2(round_number):
    if len(moves_array) < 2:
        return random.choice(move_options)
    recent_moves = moves_array[-5:]
    move_counts = {m: recent_moves.count(m) for m in move_options}
    total = sum(move_counts.values())
    probabilities = {move: count / total for move, count in move_counts.items()}
    print_probabilities(probabilities, "Algorithm 2 (Last 5 Moves)", round_number)
    predicted_move = weighted_choice(probabilities)
    return loses_to[predicted_move]

# === Choose which algorithm to use
def get_bot_move(round_number):
    if current_algorithm == 1:
        return get_bot_move_algorithm_1(round_number)
    elif current_algorithm == 2:
        return get_bot_move_algorithm_2(round_number)
    else:
        return random.choice(move_options)

# === Switch algorithm when rumbled
def switch_algorithm():
    global current_algorithm, blocked_algorithms, win_streak
    print("\nBOT RUMBLED! You won 3 rounds in a row!")
    print(f"Switching strategy... (Avoiding Algorithm {current_algorithm})")
    blocked_algorithms.add(current_algorithm)
    available = [a for a in [1, 2] if a not in blocked_algorithms]
    if available:
        current_algorithm = random.choice(available)
    else:
        blocked_algorithms = set()
        current_algorithm = random.choice([1, 2])
        print("All strategies used. Resetting AI memory.")
    win_streak = 0
    print(f"[AI now using Algorithm {current_algorithm}]")
    print("-" * 40)

# === Update transition matrix (optional learning)
def update_transition_matrix(last_move, current_move):
    if last_move:
        transition_matrix[last_move][current_move] += 1

# === Display player move history
def print_player_history():
    print("\nYour move history:")
    for i, move in enumerate(moves_array, 1):
        print(f"  Round {i}: {move}")
    print("-" * 40)

# === Display score at bottom
def print_scoreboard():
    print("Game Score:")
    print(f"  You   : {score['Player']}")
    print(f"  Bot   : {score['Bot']}")
    print(f"  Draws : {score['Draws']}")
    print("=" * 50 + "\n")

# === Game intro
print("Rock, Paper, Scissors — Smart AI")
print("Type Rock, Paper, or Scissors to play. Type Exit to quit.\n")

round_number = 1

# === Game loop
while True:
    print_transition_matrix()
    print(f"Current Algorithm: {current_algorithm}")
    player_move = input(f"\nRound {round_number} — Your move: ").capitalize()

    if player_move == "Exit":
        print("\nGame Over.")
        print_scoreboard()
        break

    if player_move not in move_options:
        print("Invalid input. Try Rock, Paper, or Scissors.\n")
        continue

    bot_move = get_bot_move(round_number)
    print(f"\nBot played: {bot_move}")

    if bot_move == player_move:
        print("It's a draw.\n")
        score["Draws"] += 1
        win_streak = 0
    elif beats[player_move] == bot_move:
        print("You win this round.\n")
        score["Player"] += 1
        win_streak += 1
        if win_streak >= 3:
            switch_algorithm()
    else:
        print("Bot wins this round.\n")
        score["Bot"] += 1
        win_streak = 0

    last_move = moves_array[-1] if moves_array else None
    update_transition_matrix(last_move, player_move)
    moves_array.append(player_move)

    print_player_history()
    print_scoreboard()
    round_number += 1
