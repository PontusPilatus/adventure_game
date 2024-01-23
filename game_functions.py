import mysql.connector
from datetime import datetime
from db_connection import connect_to_database


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

