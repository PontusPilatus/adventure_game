import mysql.connector
import random
from datetime import datetime
from db_connection import connect_to_database



def save_highscore(name, score):
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

def cities_map():
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT city_name, north, south, east, west FROM cities")
    cities_map = {row[0]: {"north": row[1], "south": row[2], "east": row[3], "west": row[4]} for row in cursor}
    cursor.close()
    db.close()
    return cities_map


def city_trivia():
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT cities.city_name, trivia_text FROM trivia JOIN cities ON trivia.city_id = cities.city_id")

    city_trivia = {}
    for city, trivia in cursor:
        if city not in city_trivia:
            city_trivia[city] = []
        city_trivia[city].append(trivia)

    cursor.close()
    db.close()

    return city_trivia