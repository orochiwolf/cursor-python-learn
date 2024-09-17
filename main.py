#####################
# Welcome to Cursor #
#####################

'''
Step 1: Try generating with Cmd+K or Ctrl+K on a new line. Ask for CLI-based game of TicTacToe.

Step 2: Hit Cmd+L or Ctrl+L and ask the chat what the code does. 
   - Then, try running the code

Step 3: Try highlighting all the code with your mouse, then hit Cmd+k or Ctrl+K. 
   - Instruct it to change the game in some way (e.g. add colors, add a start screen, make it 4x4 instead of 3x3)

Step 4: To try out cursor on your own projects, go to the file menu (top left) and open a folder.
'''

import random

# Game state
class GameState:
    def __init__(self):
        self.player_name = ""
        self.player_health = 100
        self.player_inventory = []
        self.current_location = "start"

# Quest system
class QuestSystem:
    def __init__(self):
        self.quests = []

    def add_quest(self, quest):
        self.quests.append(quest)

    def get_available_quests(self, location):
        return [quest for quest in self.quests if quest.location == location and not quest.completed and not quest.played]

class Quest:
    def __init__(self, name, description, location, reward):
        self.name = name
        self.description = description
        self.location = location
        self.reward = reward
        self.played = False
        self.completed = False
        self.success = False
        self.attempts = 0

    def complete(self):
        self.completed = True
        self.success = True
        print(f"Quest completed! You earned: {self.reward}")

    def fail(self):
        self.completed = True
        self.success = False
        print(f"Quest failed. Better luck next time!")

    def attempt(self):
        self.played = True
        self.attempts += 1

# Location system
class LocationSystem:
    def __init__(self):
        self.locations = {
            "start": {"description": "You are at the starting point. There's a path leading to a forest, a cave, and a mountain.", "connections": ["forest", "cave", "mountain"]},
            "forest": {"description": "You are in a dense forest. You can see a clearing ahead.", "connections": ["start", "clearing"]},
            "cave": {"description": "You are at the entrance of a dark cave. It looks ominous.", "connections": ["start"]},
            "clearing": {"description": "You are in a peaceful clearing in the forest.", "connections": ["forest"]},
            "mountain": {"description": "You are at the base of a tall mountain. The air is thin and crisp.", "connections": ["start", "peak"]},
            "peak": {"description": "You've reached the mountain peak. The view is breathtaking.", "connections": ["mountain"]}
        }

    def get_location_description(self, location):
        return self.locations[location]["description"]

    def get_connections(self, location):
        return self.locations[location]["connections"]

# Game engine
class GameEngine:
    def __init__(self):
        self.state = GameState()
        self.quest_system = QuestSystem()
        self.location_system = LocationSystem()

    def start_game(self):
        print("Welcome to the Text Adventure Game!")
        self.state.player_name = input("What's your name, adventurer? ")
        print(f"Welcome, {self.state.player_name}! Your adventure begins...")
        self.main_game_loop()

    def main_game_loop(self):
        while True:
            print("\n" + "="*40)
            print(f"Location: {self.state.current_location}")
            print(f"Health: {self.state.player_health}")
            print(f"Inventory: {', '.join(self.state.player_inventory)}")
            print("="*40)

            print(self.location_system.get_location_description(self.state.current_location))

            # Trigger location-specific encounters
            self.encounter_by_location()

            # Display available quests
            available_quests = self.quest_system.get_available_quests(self.state.current_location)
            if available_quests:
                print("Available Quests:")
                for i, quest in enumerate(available_quests, 1):
                    print(f"{i}. {quest.name}: {quest.description}")

            # Display possible actions
            print("\nWhat would you like to do?")
            print("1. Move to a new location")
            print("2. Check inventory")
            print("3. Take on a quest")
            print("4. Quit game")

            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                self.move_player()
            elif choice == "2":
                self.check_inventory()
            elif choice == "3":
                self.take_quest(available_quests)
            elif choice == "4":
                print("Thanks for playing! Goodbye.")
                break
            else:
                print("Invalid choice. Please try again.")

    def move_player(self):
        connections = self.location_system.get_connections(self.state.current_location)
        print("You can move to these locations:")
        for i, location in enumerate(connections, 1):
            print(f"{i}. {location}")
        
        choice = input("Enter the number of your destination: ")
        try:
            new_location = connections[int(choice) - 1]
            self.state.current_location = new_location
            print(f"You have moved to {new_location}.")
        except (ValueError, IndexError):
            print("Invalid choice. You stay where you are.")

    def encounter_by_location(self):
        location = self.state.current_location
        if location == "forest":
            self.guess_number_quest()
        elif location == "cave":
            print("The darkness of the cave is pierced by strange, glowing fungi on the walls.")
            self.rock_paper_scissors_game()
        elif location == "mountain":
            print("You feel the thin air at this altitude. The view from here is breathtaking.")
        elif location == "start":
            print("You're at the beginning of your journey. The path ahead looks promising.")
        else:
            print(f"You explore the {location}, taking in the unique sights and sounds.")

    def guess_number_quest(self):
        quest = next((q for q in self.quest_system.quests if q.name == "Guess Number"), None)
        if quest and not quest.played:
            quest.attempt()
            print("As you enter the forest, you encounter a drunk man who challenges you to a game.")
            print("He says: 'If you can guess my number between 1 and 100 in 10 tries or less, I'll let you pass and give you a sword!'")
            
            secret_number = random.randint(1, 100)
            guesses_left = 10

            while guesses_left > 0:
                try:
                    guess = int(input(f"Enter your guess (1-100), you have {guesses_left} guesses left: "))
                    if guess < 1 or guess > 100:
                        print("Please enter a number between 1 and 100.")
                        continue

                    if guess == secret_number:
                        print("Congratulations! You guessed the number correctly!")
                        print("The drunk man lets you pass and hands you a shiny sword.")
                        self.state.player_inventory.append("Sword")
                        quest.complete()
                        return

                    if guess < secret_number:
                        print("Too low!")
                    else:
                        print("Too high!")

                    guesses_left -= 1

                except ValueError:
                    print("Please enter a valid number.")

            print(f"Sorry, you've run out of guesses. The number was {secret_number}.")
            print("The drunk man blocks your path. You'll have to find another way around.")
            quest.fail()

    def check_inventory(self):
        if not self.state.player_inventory:
            print("Your inventory is empty.")
        else:
            print("Your inventory contains:")
            for item in self.state.player_inventory:
                print(f"- {item}")

    def take_quest(self, available_quests):
        if not available_quests:
            print("There are no quests available here.")
            return

        print("Which quest would you like to take?")
        for i, quest in enumerate(available_quests, 1):
            print(f"{i}. {quest.name}")

        choice = input("Enter the number of the quest: ")
        try:
            chosen_quest = available_quests[int(choice) - 1]
            print(f"You have taken on the quest: {chosen_quest.name}")
            
            if chosen_quest.name == "Guess Number":
                self.guess_number_quest()
            elif chosen_quest.name == "Rock Paper Scissors":
                self.rock_paper_scissors_game()
            else:
                chosen_quest.attempt()
                # Here you would typically add logic to complete the quest
                if random.choice([True, False]):  # Simulating quest completion
                    chosen_quest.complete()
                    self.state.player_inventory.append(chosen_quest.reward)
                else:
                    chosen_quest.fail()
        except (ValueError, IndexError):
            print("Invalid choice. No quest taken.")

    def rock_paper_scissors_game(self):
        quest = next((q for q in self.quest_system.quests if q.name == "Rock Paper Scissors"), None)
        if quest and not quest.played:
            quest.attempt()
            print("You encounter a mysterious stranger who challenges you to a game of Rock, Paper, Scissors.")
            print("If you win, you'll receive a magical item. If you lose, you'll lose some health. Do you accept? (yes/no)")
            
            if input().lower() != 'yes':
                print("You decline the challenge and continue on your journey.")
                return
            
            choices = ['rock', 'paper', 'scissors']
            player_choice = input("Enter your choice (rock/paper/scissors): ").lower()
            if player_choice not in choices:
                print("Invalid choice. Game cancelled.")
                return
            
            computer_choice = random.choice(choices)
            print(f"The stranger chose {computer_choice}.")
            
            if player_choice == computer_choice:
                print("It's a tie! Nothing happens.")
            elif (player_choice == 'rock' and computer_choice == 'scissors') or \
                 (player_choice == 'paper' and computer_choice == 'rock') or \
                 (player_choice == 'scissors' and computer_choice == 'paper'):
                print("You win! You receive a magical amulet.")
                self.state.player_inventory.append("Magical Amulet")
                quest.complete()
            else:
                print("You lose! You feel a bit weaker.")
                self.state.player_health -= 10
                if self.state.player_health < 0:
                    self.state.player_health = 0
                print(f"Your health is now {self.state.player_health}")
                quest.fail()

# Initialize and start the game
if __name__ == "__main__":
    game = GameEngine()
    
    # Add some sample quests
    game.quest_system.add_quest(Quest("Forest Exploration", "Explore the forest and find a rare flower", "forest", "Rare Flower"))
    game.quest_system.add_quest(Quest("Cave Mystery", "Investigate the strange noises coming from the cave", "cave", "Ancient Artifact"))
    game.quest_system.add_quest(Quest("Mountain Climb", "Reach the peak of the mountain", "mountain", "Golden Compass"))
    game.quest_system.add_quest(Quest("Guess Number", "Play the guessing game in the forest", "forest", "Sword"))
    game.quest_system.add_quest(Quest("Rock Paper Scissors", "Play rock paper scissors in the cave", "cave", "Magical Amulet"))
    
    game.start_game()
