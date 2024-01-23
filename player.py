from game_functions import save_highscore

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