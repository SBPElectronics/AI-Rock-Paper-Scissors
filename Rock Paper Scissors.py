import random

# Initialize transition counts for learning (Markov-style)
move_options = ["Rock", "Paper", "Scissors"]
transition_counts = {
    "Rock":     {"Rock": 1, "Paper": 1, "Scissors": 1},
    "Paper":    {"Rock": 1, "Paper": 1, "Scissors": 1},
    "Scissors": {"Rock": 1, "Paper": 1, "Scissors": 1}
}

# Correct logic: which move beats which
beats = {
    "Rock": "Scissors",
    "Paper": "Rock",
    "Scissors": "Paper"
}

# Get probabilities from counts (normalize)
def get_probabilities(last_move):
    counts = transition_counts[last_move]
    total = sum(counts.values())
    return {move: counts[move] / total for move in move_options}

# Pick move based on weighted probabilities
def weighted_choice(probabilities):
    moves = list(probabilities.keys())
    weights = list(probabilities.values())
    return random.choices(moves, weights=weights, k=1)[0]

# Bot decision: predict player’s next move, counter it
def bot_choice(last_player_move):
    if last_player_move is None:
        predicted = random.choice(move_options)
    else:
        probs = get_probabilities(last_player_move)
        predicted = weighted_choice(probs)
    # To beat the predicted move, use the move that beats it
    for move in move_options:
        if beats[move] == predicted:
            return move

# Game loop
print("Rock, Paper, Scissors! Type your move or 'exit' to quit.")
last_player_move = None

while True:
    player_move = input("Your move: ").capitalize()
    if player_move == "Exit":
        print("Game ended.")
        break
    if player_move not in move_options:
        print("Invalid input. Try Rock, Paper, or Scissors.")
        continue

    bot_move = bot_choice(last_player_move)
    print(f"Bot played: {bot_move}")

    if bot_move == player_move:
        print("It's a tie!\n")
    elif beats[player_move] == bot_move:
        print("You win!\n")
    else:
        print("Bot wins!\n")

    # Update learning counts
    if last_player_move is not None:
        transition_counts[last_player_move][player_move] += 1

    last_player_move = player_move
