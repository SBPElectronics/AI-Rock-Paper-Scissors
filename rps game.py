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
outcome_history = []

correct_predictions = 0
total_predictions = 0

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
    if len(outcome_history) == 0 or len(player_history) < 1:
        return random.choice(move_options)
    last_result = outcome_history[-1]
    last_move = player_history[-1]
    if last_result == "Player":
        predicted = last_move
    elif last_result == "Bot":
        predicted = loses_to[last_move]
    else:
        choices = [m for m in move_options if m != last_move]
        predicted = random.choice(choices)
    return loses_to[predicted]

def blended_prediction():
    seq = algorithm_1()
    psych = algorithm_2()
    votes = {"Rock": 0, "Paper": 0, "Scissors": 0}
    votes[seq] += 0.5
    votes[psych] += 0.5
    return max(votes, key=votes.get)

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
    predicted_move = blended_prediction()
    if random.random() < 0.1:
        bot_move = random.choice(move_options)
    else:
        bot_move = predicted_move
    winner = get_winner(user_input, bot_move)
    outcome_history.append(winner)
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
    total_moves = sum(move_counts.values())
    move_percents = {m: round((move_counts[m] / total_moves) * 100, 1) for m in move_options}
    log_print(f"Player: {user_input} | Bot: {bot_move}")
    log_print(f"Current Score -> Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
    log_print(f"Move Percentages -> Rock: {move_percents['Rock']}% | Paper: {move_percents['Paper']}% | Scissors: {move_percents['Scissors']}%")
    log_print(f"AI Prediction Accuracy: {accuracy:.2f}%")

print("\nFinal Score:")
print(f"Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
log_print(f"Final Score: Player: {score['Player']} | Bot: {score['Bot']} | Draws: {score['Draws']}")
