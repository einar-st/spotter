from dotenv import load_dotenv
import pypyodbc as odbc
import os


def get_db_values(table, column):

    cursor.execute(f'SELECT {column} FROM {schema}.{table}')
    return [item[0] for item in cursor.fetchall()]


# look for a value in a column
def exists(table: str, column: str, value: str):
    value = (value,)
    res = cursor.execute(
        f'SELECT {column} FROM [{schema}].[{table}] WHERE {column} = ?', value)
    row = res.fetchone()
    return bool(row)


def run_query(query, params):

    cursor.execute(query, params)
    cursor.commit()


def insert_query(table: str, values: list):

    # skip if no values
    if len(values) == 0:
        return

    q = ['?' for _ in values]
    query = f"INSERT INTO [{schema}].[{table}] VALUES ({', '.join(q)})"
    params = values

    print(", ".join(params), '->', table)

    # run_query(query, params)


def insert_track(track_obj: str, audio_features, album_obj: str,
                 artist_objs: list,
                 today: str, db_values: dict):

    result = {
        'artist_ids': [],
        'album_ids': [],
        'track_ids': [],
        'genres': []
    }

    # collect objects with API

    # album
    if album_obj['id'] not in db_values['album_ids']:
        insert_query(
            'album',
            [album_obj['id'],
                album_obj['name'],
                album_obj['release_date']]
        )
        result['album_ids'].append(album_obj['id'])
    else:
        print('Album exists')

    # track
    insert_query(
        'track',
        [track_obj['id'], track_obj['name'], album_obj['id'],
            str(track_obj['duration_ms']), str(track_obj['popularity']),
            str(track_obj['explicit']),
            str(round(audio_features['acousticness'], 3)),
            str(round(audio_features['danceability'], 3)),
            str(round(audio_features['energy'], 3)),
            str(round(audio_features['instrumentalness'], 3)),
            str(round(audio_features['liveness'], 3)),
            str(audio_features['mode']),
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
                        'genre', [genre])
                    # artist_genre
                    result['genres'].append(genre)
                insert_query(
                    'artist_genre', [artist_obj['id'], genre]
                )
        else:
            print(f'Artist "{artist_obj["name"]}" exists')

        # track-artist
        insert_query(
           'track_artist', [track_obj['id'], artist_obj['id']]
        )
        result['artist_ids'].append(artist_obj['id'])

    return result


load_dotenv()

# database schema
schema = 'sp'

# connection settings
con = odbc.connect(
    "DRIVER=" + 'FreeTDS'
    + ";SERVER=" + 'eqs.database.windows.net'
    + ";DATABASE=" + 'db'
    + ";UID=" + os.getenv('DB_USR')
    + ";PWD=" + os.getenv('DB_PWD')
    + ";PORT=1433"

)

cursor = con.cursor()
