from dotenv import load_dotenv
import mysql.connector
import os
import time
import spot_func as spf


def get_last_increment():
    cursor.execute("SELECT LAST_INSERT_ID()")
    return cursor.fetchone()[0]


def get_db_values(table, column):
    cursor.execute(f"SELECT {column} FROM {table}")
    return [item[0] for item in cursor.fetchall()]


def insert_query(table: str, values: list):
    # skip if no values
    if len(values) == 0:
        return

    s_values = "%s, " * len(values)
    query = f"INSERT INTO {table} VALUES ({s_values[:-2]})"
    # values_str = [str(value) for value in values]
    # print(", ".join(values_str), '->', table)

    cursor.execute(query, values)


def insert_track(
    track_obj: str,
    audio_features,
    album_obj: str,
    artist_objs: list,
    today: str,
    db_values: dict,
):
    result = {"artist_ids": [], "album_ids": [], "track_ids": [], "genres": []}

    # collect objects with Spotify API

    # album
    if album_obj["id"] not in db_values["album_ids"]:
        album_vars = [
            album_obj["id"],
            album_obj["name"],
            album_obj["release_date"][:4],
        ]
        insert_query("album", album_vars)
        result["album_ids"].append(album_obj["id"])
    else:
        print("Album exists")

    # track
    insert_query(
        "track",
        [
            track_obj["id"],
            track_obj["name"],
            album_obj["id"],
            str(track_obj["duration_ms"]),
            str(track_obj["popularity"]),
            int(track_obj["explicit"]),
            str(round(audio_features["acousticness"], 3)),
            str(round(audio_features["danceability"], 3)),
            str(round(audio_features["energy"], 3)),
            str(round(audio_features["instrumentalness"], 3)),
            str(round(audio_features["liveness"], 3)),
            int(audio_features["mode"]),
            str(round(audio_features["time_signature"], 3)),
            str(round(audio_features["valence"], 3)),
        ],
    )
    result["track_ids"].append(track_obj["id"])

    for artist_obj in artist_objs:
        if artist_obj["id"] not in db_values["artist_ids"]:
            # artist
            insert_query(
                "artist",
                [
                    artist_obj["id"],
                    artist_obj["name"],
                    str(artist_obj["popularity"]),
                ],
            )
            # genre
            print("Genres:", ", ".join(artist_obj["genres"]))
            for genre in artist_obj["genres"]:
                if (
                    genre not in db_values["genres"]
                    and genre not in result["genres"]
                ):
                    insert_query("genre", [0] + [genre])
                    # artist_genre
                    result["genres"].append(genre)
                insert_query("artist_genre", [0] + [artist_obj["id"], genre])
        else:
            print(f'Artist "{artist_obj["name"]}" exists')

        # track-artist
        insert_query("track_artist", [0] + [track_obj["id"], artist_obj["id"]])
        result["artist_ids"].append(artist_obj["id"])

    return result


def fetch_day(day, artist_params, track_params, genre_params):
    arguments = [
        ",".join(artist_params),
        ",".join(track_params),
        ",".join(genre_params),
    ]

    # load pre-existing values
    db_values = {
        "artist_ids": get_db_values("artist", "artist_id"),
        "album_ids": get_db_values("album", "album_id"),
        "track_ids": get_db_values("track", "track_id"),
        "genres": get_db_values("genre", "genre"),
    }

    for i, track in enumerate(
        spf.get_recommendations(
            spf.token, arguments[0], arguments[2], arguments[1]
        )
    ):
        track_obj = spf.get_object(spf.token, track["id"], "track")
        artist_names = ", ".join(
            artist["name"] for artist in track_obj["artists"]
        )
        print("")
        print(f"{i + 1}. {artist_names} - {track_obj['name']}")
        if track["id"] not in db_values["track_ids"]:
            audio_features = spf.get_audio_features(spf.token, track["id"])

            album_obj = spf.get_object(
                spf.token, track_obj["album"]["id"], "album"
            )
            artist_objs = []
            for artist_obj in track_obj["artists"]:
                artist_objs.append(
                    spf.get_object(spf.token, artist_obj["id"], "artist")
                )
            new_values = insert_track(
                track_obj,
                audio_features,
                album_obj,
                artist_objs,
                day,
                db_values,
            )

            for key in db_values.keys():
                for key in db_values:
                    db_values[key].extend(new_values[key])
            print("Track successfully inserted in DB")
        else:
            print("Track already exists in DB")

        # insert parameters and date if it's the first track of the day
        # todo: make function
        if i == 0:
            # date
            try:
                insert_query("date", [0] + [day])
            except mysql.connector.IntegrityError:  # pass if exists
                pass

            param_ids = []
            # parameters
            # todo fetch
            for param in artist_params:
                try:
                    insert_query("parameter", [0, param, "art"])
                    param_ids.append(get_last_increment())
                except mysql.connector.IntegrityError:  # pass if exists
                    pass
            for param in track_params:
                try:
                    insert_query("parameter", [0, param, "tra"])
                    param_ids.append(get_last_increment())
                except mysql.connector.IntegrityError:  # pass if exists
                    pass
            for param in genre_params:
                try:
                    insert_query("parameter", [0, param, "gen"])
                    param_ids.append(get_last_increment())
                except mysql.connector.IntegrityError:  # pass if exists
                    pass
            # date_parameter
            for param_id in param_ids:
                try:
                    insert_query("date_parameter", [0, day, param_id])
                except mysql.connector.IntegrityError:  # pass if exists
                    pass

        # track_date
        insert_query("track_date", [0] + [track_obj["id"], day])
        # 1 second interval between each track addition
        # time.sleep(1)


load_dotenv()

cnx = mysql.connector.MySQLConnection(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_SCHEMA"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cursor = cnx.cursor()
