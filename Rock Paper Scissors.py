import random

# Static probability tree: What the opponent is likely to play next based on previous move
probability_tree = {
    "Rock":     {"Rock": 0.2, "Paper": 0.5, "Scissors": 0.3},
    "Paper":    {"Rock": 0.3, "Paper": 0.3, "Scissors": 0.4},
    "Scissors": {"Rock": 0.4, "Paper": 0.3, "Scissors": 0.3}
}

# Counter move to beat predicted opponent move
counter_move = {
    "Rock": "Paper",
    "Paper": "Scissors",
    "Scissors": "Rock"
}

# Select a move using weighted random choice
def weighted_choice(probabilities):
    moves = list(probabilities.keys())
    weights = list(probabilities.values())
    return random.choices(moves, weights=weights, k=1)[0]

# Bot chooses move based on player's last move
def bot_choice(last_player_move):
    if last_player_move is None:
        predicted = random.choice(["Rock", "Paper", "Scissors"])
    else:
        predicted = weighted_choice(probability_tree[last_player_move])
    return counter_move[predicted]

# Game loop
print("Rock, Paper, Scissors! Type your move or 'exit' to quit.")
last_player_move = None

while True:
    player_move = input("Your move: ").capitalize()
    if player_move == "Exit":
        break
    if player_move not in ["Rock", "Paper", "Scissors"]:
        print("Invalid input. Try Rock, Paper, or Scissors.")
        continue

    bot_move = bot_choice(last_player_move)
    print(f"Bot played: {bot_move}")

    if bot_move == player_move:
        print("It's a tie!\n")
    elif counter_move[player_move] == bot_move:
        print("You win!\n")
    else:
        print("Bot wins!\n")

    last_player_move = player_move
 