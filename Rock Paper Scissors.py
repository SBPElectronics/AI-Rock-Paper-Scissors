import random

move_options = ["Rock", "Paper", "Scissors"]

transition_counts = {
    "Rock": {"Rock": 1, "Paper": 1, "Scissors": 1},
    "Paper": {"Rock": 1, "Paper": 1, "Scissors": 1},
    "Scissors": {"Rock": 1, "Paper": 1, "Scissors": 1}
}

beats = {
    "Rock": "Scissors",
    "Paper": "Rock",
    "Scissors": "Paper"
}

moves_array = []
score = {"Player": 0, "Bot": 0, "Draws": 0}

def predict_next_move(last_move):
    if last_move not in transition_counts:
        return random.choice(move_options)
    counts = transition_counts[last_move]
    max_count = max(counts.values())
    candidates = [move for move in move_options if counts[move] == max_count]
    return random.choice(candidates)

def get_bot_move():
    if len(moves_array) == 0:
        return random.choice(move_options)
    last_move = moves_array[-1]
    predicted_player_move = predict_next_move(last_move)
    for move in move_options:
        if beats[move] == predicted_player_move:
            return move

def update_transition_counts(last_move, current_move):
    if last_move:
        transition_counts[last_move][current_move] += 1

def print_transition_matrix():
    print("\nTransition Matrix:")
    for prev_move in transition_counts:
        row = transition_counts[prev_move]
        print(f"After {prev_move}: ", end="")
        for next_move in move_options:
            print(f"{next_move}={row[next_move]}  ", end="")
        print()
    print()

def print_player_history():
    print("\nMove History:")
    for i, move in enumerate(moves_array, start=1):
        print(f"Round {i}: You played {move}")
    print()

print("Rock, Paper, Scissors — Smart AI")
print("Type Rock, Paper, or Scissors to play. Type Exit to quit.\n")

while True:
    player_move = input("Your move: ").capitalize()
    if player_move == "Exit":
        print("\nGame over.")
        print(f"Final Score — You: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
        break

    if player_move not in move_options:
        print("Invalid input. Try Rock, Paper, or Scissors.\n")
        continue

    bot_move = get_bot_move()
    print(f"Bot played: {bot_move}")

    if bot_move == player_move:
        print("It's a draw.\n")
        score["Draws"] += 1
    elif beats[player_move] == bot_move:
        print("You win this round.\n")
        score["Player"] += 1
    else:
        print("Bot wins this round.\n")
        score["Bot"] += 1

    last_player_move = moves_array[-1] if moves_array else None
    update_transition_counts(last_player_move, player_move)
    moves_array.append(player_move)

    QTy_moves = len(moves_array)

    print_player_history()
    #print_transition_matrix()
    print(f"Current score — You: {score['Player']}, Bot: {score['Bot']}, Draws: {score['Draws']}")
    print(f"{QTy_moves} moves played so far.\n")
