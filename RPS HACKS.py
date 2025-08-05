def get_computer_move(player_move):
    beats = {
        "rock": "paper",
        "paper": "scissors",
        "scissors": "rock"
    }
    return beats[player_move]

def main():
    print("Let's play Rock, Paper, Scissors! (Type 'quit' to stop)")
    
    while True:
        player_move = input("Enter your move (rock, paper, scissors): ").lower()
        
        if player_move == "quit":
            print("Thanks for playing! Goodbye!")
            break
        
        if player_move not in ["rock", "paper", "scissors"]:
            print("Invalid move! Please choose rock, paper, or scissors.")
            continue
        
        computer_move = get_computer_move(player_move)
        print(f"Computer chose: {computer_move}")
        print("Computer wins! Sorry, you lost.\n")

if __name__ == "__main__":
    main()
