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
''''

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
        return [quest for quest in self.quests if quest.location == location and not quest.completed]

class Quest:
    def __init__(self, name, description, location, reward):
        self.name = name
        self.description = description
        self.location = location
        self.completed = False
        self.reward = reward

    def complete(self):
        self.completed = True
        print(f"Quest completed! You earned: {self.reward}")

# Location system
class LocationSystem:
    def __init__(self):
        self.locations = {
            "start": {"description": "You are at the starting point. There's a path leading to a forest and a cave.", "connections": ["forest", "cave"]},
            "forest": {"description": "You are in a dense forest. You can see a clearing ahead.", "connections": ["start", "clearing"]},
            "cave": {"description": "You are at the entrance of a dark cave. It looks ominous.", "connections": ["start"]},
            "clearing": {"description": "You are in a peaceful clearing in the forest.", "connections": ["forest"]}
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
            # Here you would typically add logic to complete the quest
            chosen_quest.complete()
            self.state.player_inventory.append(chosen_quest.reward)
        except (ValueError, IndexError):
            print("Invalid choice. No quest taken.")

# Initialize and start the game
if __name__ == "__main__":
    game = GameEngine()
    
    # Add some sample quests
    game.quest_system.add_quest(Quest("Forest Exploration", "Explore the forest and find a rare flower", "forest", "Rare Flower"))
    game.quest_system.add_quest(Quest("Cave Mystery", "Investigate the strange noises coming from the cave", "cave", "Ancient Artifact"))
    
    game.start_game()
