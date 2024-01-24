from game_functions import show_highscores, cities_map, city_trivia
from player import Player
import random


def main_menu():
    print("===========================================")
    print("  Welcome to the Great Skåne Adventure!  ")
    print("===========================================")
    print("Embark on a journey through the beautiful landscapes of Skåne.")
    print("Discover hidden secrets, learn fascinating trivia, and search")
    print("for the elusive Spettekaka to become a legend in the highscores!")
    print("\nWhat would you like to do?")
    print("1. Start your adventure")
    print("2. View the legends (Highscores)")
    print("3. Exit")
    choice = input("Enter your choice (1,2 or 3): ")
    return choice



def main():
    while True:
        choice = main_menu()
        if choice == '1':
            play_game()
        elif choice == '2':
            print("Top Highscores:")
            show_highscores()
        elif choice == '3':
            print("\nFarewell, brave adventurer!")
            print("May your tales be told through the ages and your bravery remembered forever.")
            print("Until we meet again in the lands of Skåne...\n")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def play_game():
    map_data = cities_map()
    trivia_city = city_trivia()

    player_name = input("Enter your name, brave soul: ")
    starting_city = random.choice(list(map_data.keys()))
    adjacent_cities = set(filter(None, map_data[starting_city].values()))
    possible_locations = [city for city in map_data.keys() if city not in adjacent_cities and city != starting_city]
    spettekaka_location = random.choice(possible_locations)
    player = Player(player_name, starting_city, spettekaka_location)

    print("\n===================================================")
    print(f"Greetings, {player.name}! Your legend begins in the ancient city of {player.current_city}.")
    print("As you traverse the mystical lands of Skåne, seek out the hidden Spettekaka.")
    print("Your journey will be filled with trials, wonders, and discoveries.")
    print("May your wit guide you and your courage shine bright.")
    print("===================================================\n")

    while True:
        available_directions = {direction: city for direction, city in map_data[player.current_city].items() if city}
        print(f"\n{player.name}, you are in {player.current_city}. Available directions: {', '.join(available_directions.keys())}")
        print(f"Your current score is: {player.score}.")
        direction = input("Choose your direction (or type 'exit' to end your journey): ").lower()

        if direction == 'exit':
            print(
                f"Goodbye, {player.name}! You visited {len(player.visited_cities)} cities and scored {player.score} points. Thanks for playing!")
            break

        if direction in available_directions:
            new_city = map_data[player.current_city][direction]
            if player.travel_to(new_city):
                break
            trivia = random.choice(trivia_city[new_city])
            print(f"\nWelcome to {new_city}, {player.name}! Did you know? {trivia}")
        else:
            print(f"That's not a valid direction from {player.current_city}, {player.name}. Try again.")


if __name__ == "__main__":
    main()
