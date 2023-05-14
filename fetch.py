import spot_func as spf
import db_func as dbf
import time

# todo
# - duplicate error catching

# select arguments manually
# arguments = spf.set_args(spf.token)

# load pre-existing values
db_values = {
    'artist_ids': dbf.get_db_values('artist', 'artist_id'),
    'album_ids': dbf.get_db_values('album', 'album_id'),
    'track_ids': dbf.get_db_values('track', 'track_id'),
    'genres': dbf.get_db_values('genre', 'genre')
}

for day_of_month in range(1, 32, 1):

    # set date value
    today = f'2023-01-{day_of_month:02}'
    arguments = ['5K4W6rqBFWDnAN6FQUkS6x,3nFkdlSjzX9mRTtwJOzDYB',
                 '0j2T0R9dR9qdJYsB7ciXhf', 'hip-hop']
    recommendations = spf.get_recommendations(
        spf.token, arguments[0], arguments[2], arguments[1]
    )

    # fetch track information for all recommendations

    for i, track in enumerate(recommendations):

        track_obj = spf.get_object(spf.token, track, 'track')

        # ignore tracks with names longer than 127 due to UTF bug on Linux
        # https://github.com/jiangwen365/pypyodbc/issues/27
        if len(track_obj['name']) < 128:
            artist_names = ', '.join(
                artist['name'] for artist in track_obj['artists'])
            print('')
            print(f"{artist_names} - {track_obj['name']}, {today}")
            print('==========')
            if track not in db_values['track_ids']:
                audio_features = spf.get_audio_features(spf.token, track)
                album_obj = spf.get_object(
                    spf.token, track_obj['album']['id'], 'album')
                artist_objs = []
                for artist_obj in track_obj['artists']:
                    artist_objs.append(
                        spf.get_object(spf.token, artist_obj['id'], 'artist'))
                new_values = dbf.insert_track(
                    track_obj, audio_features, album_obj, artist_objs, today,
                    db_values)

                for key in db_values.keys():
                    for key in db_values:
                        db_values[key].extend(new_values[key])
            else:
                print('Track exists')

            # insert date if it's the first track of the day
            if i == 0:
                dbf.insert_query(
                    'date', [today]
                )
            # track_date
            dbf.insert_query(
                'track_date',
                [track_obj['id'], today]
            )

            # avoid rate limit timeout
            time.sleep(1)
