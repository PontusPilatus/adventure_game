import mysql.connector
import random
from datetime import datetime

cities_map = {
    "Malmö": {"north": "Lund", "south": "Trelleborg", "east": "Ystad"},
    "Lund": {"south": "Malmö", "north": "Eslöv", "west": "Landskrona", "east": "Sjöbo"},
    "Landskrona": {"south": "Malmö", "north": "Helsingborg", "east": "Eslöv"},
    "Helsingborg": {"south": "Landskrona", "north": "Ängelholm", "east": "Klippan"},
    "Ängelholm": {"south": "Helsingborg", "north": "Båstad", "west": "Höganäs", "east": "Örkelljunga"},
    "Höganäs": {"south": "Helsingborg", "east": "Ängelholm"},
    "Båstad": {"south": "Ängelholm", "west": "Torekov", "east": "Örkelljunga"},
    "Torekov": {"south": "Ängelholm", "east": "Ängelholm"},
    "Örkelljunga": {"south": "Klippan", "north": "Skånes-Fagerhult", "west": "Ängelholm", "east": "Hässleholm"},
    "Klippan": {"south": "Eslöv", "north": "Örkelljunga", "west": "Helsingborg", "east": "Hässleholm"},
    "Eslöv": {"south": "Lund", "north": "Klippan", "west": "Landskrona", "east": "Hörby"},
    "Trelleborg": {"north": "Malmö", "west": "Skanör-Falsterbo", "east": "Ystad"},
    "Ystad": {"north": "Sjöbo", "west": "Trelleborg", "east": "Simrishamn"},
    "Sjöbo": {"south": "Ystad", "north": "Hörby", "west": "Lund", "east": "Kivik"},
    "Hörby": {"south": "Sjöbo", "north": "Hässleholm", "west": "Eslöv", "east": "Åhus"},
    "Hässleholm": {"south": "Hörby", "north": "Osby", "west": "Klippan", "east": "Kristianstad"},
    "Osby": {"south": "Hässleholm", "west": "Skånes-Fagerhult"},
    "Skånes-Fagerhult": {"south": "Örkelljunga", "east": "Osby"},
    "Kristianstad": {"south": "Åhus", "north": "Osby", "west": "Hässleholm"},
    "Åhus": {"south": "Kivik", "north": "Kristianstad", "west": "Hörby"},
    "Kivik": {"south": "Simrishamn", "north": "Åhus", "west": "Sjöbo"},
    "Simrishamn": {"north": "Kivik", "west": "Ystad"},
    "Skanör-Falsterbo": {"east": "Trelleborg"},
}

city_trivia = {
    "Malmö": ["Features an unusual skyscraper, the 'Twisted Torso', inspired by a sculpture called 'Twisting Torso' by Santiago Calatrava."],
    "Lund": ["Lund has an annual celebration called 'Valborg', where students welcome spring by wearing funny hats and riding homemade rafts down the city’s canal."],
    "Landskrona": ["The city has an island, Ven, famous for its observatory built by the astronomer Tycho Brahe in the 16th century."],
    "Helsingborg": ["It's said that you can see Denmark on a clear day from the Kärnan tower in Helsingborg, as it's just 4 kilometers across the Øresund Strait."],
    "Ängelholm": ["Hosts a unique UFO memorial at 'Angel's Mountain' (Ängelholms I UFO-monument), dedicated to a supposed UFO landing in 1946."],
    "Höganäs": ["Known for its unique 'saluhall' (market hall), where local artisans sell their crafts and gourmet foods, including the famous Höganäs ceramics."],
    "Båstad": ["Not just for tennis, Båstad is also famous for its beautiful beaches and a vibrant nightlife scene during the summer."],
    "Torekov": ["A small coastal village, Torekov is known for its traditional Swedish wooden houses painted in Falu red."],
    "Örkelljunga": ["Famous for its scenic nature reserves like Rössjöholmsån Valley, which offers beautiful hiking trails."],
    "Klippan": ["The town's name literally means 'The Cliff' in Swedish, named after a cliff formation near the Rönne River."],
    "Eslöv": ["Has a unique circular town plan, one of the few in Sweden, which was part of a modern urban planning movement in the early 20th century."],
    "Trelleborg": ["Known for its ancient circular fortresses called 'trelleborgen', believed to have been built by the Vikings."],
    "Ystad": ["The town's medieval greyfriars' abbey is one of the best-preserved in Sweden, and its cloister garden is a peaceful retreat."],
    "Sjöbo": ["Famous for its large flea market, Sjöbo Marknad, which is one of the biggest in southern Sweden."],
    "Hörby": ["Known for its unusual tradition of 'egg picking', a game played at Easter where participants compete to break each other's boiled eggs."],
    "Hässleholm": ["Surrounded by dense forests, it's known for being close to some of the most extensive hiking trails in southern Sweden."],
    "Osby": ["Besides BRIO, Osby is also the home of the Klinten Kultur, a cultural festival with music, dance, and local crafts."],
    "Skånes-Fagerhult": ["This small village is known for its traditional Midsummer celebration, complete with maypole dancing and folk music."],
    "Kristianstad": ["Built on low-lying wetlands, the city has an extensive system of levees and pumps to protect it from flooding."],
    "Åhus": ["Besides Absolut Vodka, it's also known for its idyllic sandy beaches and a medieval church dating back to the 12th century."],
    "Kivik": ["Famous for its ancient tomb, Kiviksgraven, which is the largest Iron Age tomb in Scandinavia and features unique stone carvings."],
    "Simrishamn": ["The town's cobbled streets and brightly colored houses make it one of the most picturesque fishing villages in Sweden."],
    "Skanör-Falsterbo": ["Skanör-Falsterbo is famous for their annual migration of millions of birds, making it a paradise for birdwatchers."]
}


def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mypassword",
        database="adventure_game"
    )


def save_highscore(name, score):
    global db, cursor
    try:
        db = connect_to_database()
        cursor = db.cursor()
        today = datetime.now().date()
        cursor.execute("INSERT INTO highscores (player_name, score, score_date) VALUES (%s, %s, %s)", (name, score, today))
        db.commit()
        print(f"Highscore for {name} saved successfully!")
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()



def show_highscores():
    print("\n=================== Highscores: Legends of Skåne ===================")
    print("Behold the champions who ventured bravely through the lands of Skåne,")
    print("unraveling its mysteries and leaving their mark in history!")
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT player_name, score, score_date FROM highscores ORDER BY score DESC, score_date ASC LIMIT 10")
    for index, (name, score, date) in enumerate(cursor, start=1):
        print(f"{index}. {name}: {score} points on {date}")
    print("===================================================================\n")
    cursor.close()
    db.close()


class Player:
    def __init__(self, name, starting_city, spettekaka_location):
        self.name = name
        self.current_city = starting_city
        self.visited_cities = set()
        self.spettekaka_location = spettekaka_location
        self.score = 0
        self.bonus_score = 500

    def travel_to(self, new_city):
        self.current_city = new_city
        if new_city not in self.visited_cities:
            self.visited_cities.add(new_city)
            self.score += 10
            self.bonus_score -= 20

            if new_city == self.spettekaka_location:
                self.score += max(self.bonus_score, 0)
                print("\n=====================================================")
                print(f"Victory! {self.name}, you have achieved the unimaginable!")
                print("In the annals of Skåne, your name shall be etched as the one")
                print(f"who uncovered the legendary Spettekaka in {new_city}.")
                print("Let your extraordinary feat be celebrated across the lands!")
                print("=====================================================\n")
                print(f"Your final score is: {self.score}.")
                save_highscore(self.name, self.score)
                return True
        return False


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
    player_name = input("Enter your name, brave soul: ")
    starting_city = random.choice(list(cities_map.keys()))
    adjacent_cities = set(cities_map[starting_city].values())
    possible_locations = [city for city in cities_map.keys() if city not in adjacent_cities and city != starting_city]
    spettekaka_location = random.choice(possible_locations)
    player = Player(player_name, starting_city, spettekaka_location)

    print("\n===================================================")
    print(f"Greetings, {player.name}! Your legend begins in the ancient city of {player.current_city}.")
    print("As you traverse the mystical lands of Skåne, seek out the hidden Spettekaka.")
    print("Your journey will be filled with trials, wonders, and discoveries.")
    print("May your wit guide you and your courage shine bright.")
    print("===================================================\n")

    while True:
        print(f"\n{player.name}, you are in {player.current_city}. Available directions: {', '.join(cities_map[player.current_city].keys())}")
        print(f"Your current score is: {player.score}.")
        direction = input("Choose your direction (or type 'exit' to end your journey): ").lower()

        if direction == 'exit':
            print(
                f"Goodbye, {player.name}! You visited {len(player.visited_cities)} cities and scored {player.score} points. Thanks for playing!")
            break

        if direction in cities_map[player.current_city]:
            new_city = cities_map[player.current_city][direction]
            if player.travel_to(new_city):
                break
            trivia = random.choice(city_trivia[new_city])
            print(f"\nWelcome to {new_city}, {player.name}! Did you know? {trivia}")
        else:
            print(f"That's not a valid direction from {player.current_city}, {player.name}. Try again.")


if __name__ == "__main__":
    main()
