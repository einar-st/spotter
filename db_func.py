from dotenv import load_dotenv
import mysql.connector
import os


def get_db_values(table, column):

    # cursor.execute(f'SELECT {column} FROM {schema}.{table}')
    cursor.execute(f'SELECT {column} FROM {table}')
    return [item[0] for item in cursor.fetchall()]


def insert_query(table: str, values: list):

    # skip if no values
    if len(values) == 0:
        return

    s_values = '%s, ' * len(values)
    query = f"INSERT INTO {table} VALUES ({s_values[:-2]})"
    # values_str = [str(value) for value in values]
    # print(", ".join(values_str), '->', table)

    cursor.execute(query, values)


def insert_track(track_obj: str, audio_features, album_obj: str,
                 artist_objs: list,
                 today: str, db_values: dict):

    result = {
        'artist_ids': [],
        'album_ids': [],
        'track_ids': [],
        'genres': []
    }

    # collect objects with Spotify API

    # album
    if album_obj['id'] not in db_values['album_ids']:
        album_vars = [
            album_obj['id'], album_obj['name'], album_obj['release_date'][:4]
        ]
        insert_query('album', album_vars)
        result['album_ids'].append(album_obj['id'])
    else:
        print('Album exists')

    # track
    insert_query(
        'track',
        [track_obj['id'], track_obj['name'], album_obj['id'],
            str(track_obj['duration_ms']), str(track_obj['popularity']),
            int(track_obj['explicit']),
            str(round(audio_features['acousticness'], 3)),
            str(round(audio_features['danceability'], 3)),
            str(round(audio_features['energy'], 3)),
            str(round(audio_features['instrumentalness'], 3)),
            str(round(audio_features['liveness'], 3)),
            int(audio_features['mode']),
            str(round(audio_features['time_signature'], 3)),
            str(round(audio_features['valence'], 3))])
    result['track_ids'].append(track_obj['id'])

    for artist_obj in artist_objs:
        if artist_obj['id'] not in db_values['artist_ids']:

            # artist
            insert_query(
                'artist',
                [artist_obj['id'], artist_obj['name'],
                    str(artist_obj['popularity'])]
            )
            # genre
            print('Genres:', ", ".join(artist_obj['genres']))
            for genre in artist_obj['genres']:
                if (genre not in db_values['genres']
                        and genre not in result['genres']):
                    insert_query(
                        'genre', [0] + [genre])
                    # artist_genre
                    result['genres'].append(genre)
                insert_query(
                    'artist_genre', [0] + [artist_obj['id'], genre]
                )
        else:
            print(f'Artist "{artist_obj["name"]}" exists')

        # track-artist
        insert_query(
           'track_artist', [0] + [track_obj['id'], artist_obj['id']]
        )
        result['artist_ids'].append(artist_obj['id'])

    return result


load_dotenv()

cnx = mysql.connector.MySQLConnection(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_DATABASE'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

cursor = cnx.cursor()
