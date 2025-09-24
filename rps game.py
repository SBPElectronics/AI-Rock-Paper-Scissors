import logging

# Logging Setup
logging.basicConfig(filename='game_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

dev_mode = 1

def log_print(message=""):
    if dev_mode == 1:
        print(message)
    logging.info(message)

input_options = ["Rock", "Paper", "Scissors", "Quit", "Change Algorithm", "Block Algorithm", "Unblock Algorithm"]
move_options = ["Rock", "Paper", "Scissors"]
beats = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
loses_to = {v: k for k, v in beats.items()}
moves_array = []
score = {"Player": 0, "Bot": 0, "Draws": 0}
win_streak = 0
current_algorithm = 1
blocked_algorithms = set()

user_prompt = (f"Enter your move ({', '.join(move_options)}) or 'Quit' to stop): ")
print(user_prompt)

user_input = input().capitalize()
while user_input not in input_options:
    print("Invalid input! Please try again.")
    print(user_prompt)
    user_input = input().capitalize()

if user_input not in input_options:
    print("Invalid input! Please try again.")
    print(user_prompt)
    user_input = input().capitalize()

