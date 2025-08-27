import random
import logging
import os

# === Logging Setup ===
log_file_path = os.path.join(os.path.dirname(__file__), "game_log.txt")
logging.basicConfig(
    filename=log_file_path,
    filemode="a",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
    force=True
)

def log_print(msg="", end="\n"):
    """Print once to console and log to file."""
    print(msg, end=end)
    logging.info(msg)

# === Game Setup ===
move_options = ["Rock", "Paper", "Scissors"]
beats = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
loses_to = {v: k for k, v in beats.items()}
moves_array = []
history = []  # (round_number, player_move, bot_move, result)
score = {"Player": 0, "Bot": 0, "Draws": 0}
win_streak = 0
current_algorithm = 1
blocked_algorithms = set()

# === Weighted Choice ===
def weighted_choice(prob_dict):
    rand = random.random()
    cumulative = 0.0
    for move, prob in prob_dict.items():
        cumulative += prob
        if rand < cumulative:
            return move
    return random.choice(list(prob_dict.keys()))

# === Bot Algorithms ===
def get_bot_move_algorithm_1():
    if len(moves_array) < 1:
        return random.choice(move_options)
    move_counts = {m: moves_array.count(m) for m in move_options}
    total = sum(move_counts.values())
    if total == 0:
        return random.choice(move_options)
    probabilities = {move: count / total for move, count in move_counts.items()}
    return weighted_choice(probabilities)

def get_bot_move_algorithm_2():
    if len(moves_array) < 5:
        return random.choice(move_options)
    recent_moves = moves_array[-5:]
    move_counts = {m: recent_moves.count(m) for m in move_options}
    total = sum(move_counts.values())
    if total == 0:
        return random.choice(move_options)
    probabilities = {move: count / total for move, count in move_counts.items()}
    return weighted_choice(probabilities)

def get_bot_move():
    if current_algorithm == 1:
        return get_bot_move_algorithm_1()
    elif current_algorithm == 2:
        return get_bot_move_algorithm_2()
    else:
        return random.choice(move_options)

def switch_algorithm():
    global current_algorithm, blocked_algorithms, win_streak
    log_print("\nBOT RUMBLED! You won 3 rounds in a row!")
    log_print(f"Switching strategy... (Avoiding Algorithm {current_algorithm})")
    blocked_algorithms.add(current_algorithm)
    available = [a for a in [1, 2] if a not in blocked_algorithms]
    if available:
        current_algorithm = random.choice(available)
    else:
        blocked_algorithms = set()
        current_algorithm = random.choice([1, 2])
        log_print("All strategies used. Resetting AI memory.")
    win_streak = 0
    log_print(f"[AI now using Algorithm {current_algorithm}]")
    log_print("-" * 40)

# === Move Stats Display (Table) ===
def print_move_stats():
    log_print("\n========================================== Move Statistics =========================================================================")
    if not history:
        log_print("No moves recorded yet.")
        return
    player_counts = {m: 0 for m in move_options}
    bot_counts = {m: 0 for m in move_options}
    for _, p, b, _ in history:
        player_counts[p] += 1
        bot_counts[b] += 1
    total_rounds = len(history)
    log_print(f"{'Move':<10}{'Player %':<12}{'Bot %'}")
    log_print("-" * 30)
    for move in move_options:
        p_pct = round((player_counts[move] / total_rounds) * 100, 1)
        b_pct = round((bot_counts[move] / total_rounds) * 100, 1)
        log_print(f"{move:<10}{p_pct:<12}{b_pct}")
    log_print("-" * 30)

# === Scoreboard ===
def print_scoreboard():
    log_print("Game Score:")
    log_print(f"  You   : {score['Player']}")
    log_print(f"  Bot   : {score['Bot']}")
    log_print(f"  Draws : {score['Draws']}")
    log_print("=" * 50 + "\n")

# === Game Intro ===
log_print("=" * 50)
log_print("       Rock, Paper, Scissors — Smart AI       ")
log_print("=" * 50)
log_print("Type Rock, Paper, or Scissors to play. Type Exit to quit.\n")

round_number = 1

# === Game Loop ===
while True:
    print_move_stats()
    log_print(f"Current Algorithm: {current_algorithm}")
    player_move = input(f"\nRound {round_number} — Your move: ").capitalize()
    if player_move == "Exit":
        log_print("\nGame Over.")
        print_scoreboard()
        break
    if player_move not in move_options:
        log_print("Invalid input. Try Rock, Paper, or Scissors.\n")
        continue
    bot_move = get_bot_move()
    log_print(f"\nBot played: {bot_move}")
    if bot_move == player_move:
        result = "Draw"
        log_print("It's a draw.\n")
        score["Draws"] += 1
        win_streak = 0
    elif beats[player_move] == bot_move:
        result = "Player"
        log_print("You win this round.\n")
        score["Player"] += 1
        win_streak += 1
        if win_streak >= 3:
            switch_algorithm()
    else:
        result = "Bot"
        log_print("Bot wins this round.\n")
        score["Bot"] += 1
        win_streak = 0
    moves_array.append(player_move)
    history.append((round_number, player_move, bot_move, result))
    logging.info(f"Round {round_number}: Player={player_move}, Bot={bot_move}, Result={result}")
    print_scoreboard()
    round_number += 1
    if round_number > 20:
        log_print("Reached 20 rounds. Ending game.")
        break