from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def cls():

    os.system('clear')


def get_token():

    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content_Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']

    return token


def get_auth_header(token):

    return {'Authorization': 'Bearer ' + token}


def search(token, query, type):

    url_base = 'https://api.spotify.com/v1/search'
    params = f'?q={query}&type={type}'
    url = url_base + params
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)[f'{type}s']['items']

    try:
        return json_result
    except IndexError:
        print('No result found')

    return None


# def item_search(token, type):

#     artist_prompt = input('Search: ')
#     print('')
#     search_query = search(token, artist_prompt, type)

#     items = []

#     for item in search_query:
#         if type == 'artist':
#             # do not show list if perfect hit
#             if item['name'].lower() == artist_prompt.lower():
#                 return (item['name'])
#             elif item['name'] not in items:
#                 items.append(item['name'])
#             else:
#                 search_query.remove(item)
#         else:
#             if item['name'] not in items:
#                 items.append(item['artists'][0]['name'] + item['name'])
#             else:
#                 search_query.remove(item)

#     # limit list
#     limit = {'artist': 5, 'track': 10}
#     for i, item in enumerate(search_query, 1):
#         if i <= limit[type]:
#             print(str(i) + '.', item['name'])

#     # print(search_query)
#     print('')
#     idx = input('Select: ')

#     object = search_query[int(idx) - 1]
#     artist_names = []
#     if type == 'track':
#         artist_names = [item['name'] for item in object['artists']]
#     ret = {
#         'artist': (object['id'], object['name']),
#         'track': (
#             object['id'], f'{", ".join(artist_names)} - {object["name"]}')
#     }

#     return ret[type]


def get_object(token, id, type):
    url = (
        f'https://api.spotify.com/v1/{type}s/{id}'
    )
    headers = get_auth_header(token)
    json_object = get(url, headers=headers)
    object = json.loads(json_object.content)
    return object


def get_audio_features(token, id):
    url = (
        f'https://api.spotify.com/v1/audio-features/{id}'
    )
    headers = get_auth_header(token)
    json_object = get(url, headers=headers)
    object = json.loads(json_object.content)
    return object


def print_track_info(token, track_id):

    # assign objects
    track = get_object(token, track_id, 'track')
    # album and track objects do not contain genre info
    album = get_object(token, track['album']['id'], 'album')
    artists = []
    for artist in track['artists']:
        artists.append(get_object(token, artist['id'], 'artist'))

    print('------')
    print('Track:')
    print('ID: ', track['id'])
    print('Name: ', track['name'])
    for i, artist in enumerate(artists, 1):
        if len(artists) > 1:
            print('')
            print(f' Artist {i}:')
        else:
            print('')
            print(' Artist:')
        print(' ID: ', artist['id'])
        print(' Name: ', artist['name'])
        print(' Genres: ', ', '.join(artist['genres']))
    print('')
    print(' Album:')
    print(' ID:', album['id'])
    print(' Name: ', album['name'])
    print(' Genres: ', ', '.join(album['genres']))
    print('------')


def get_songs_by_artist(token, artist_id):
    url = (
        f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=NO'
    )
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result


def get_recommendations(token, artists: str, genres: str, tracks: str):
    url_base = 'https://api.spotify.com/v1/recommendations'
    artists = f'?seed_artists={artists}'
    genres = f'&seed_genres={genres}'
    tracks = f'&seed_tracks={tracks}'
    limit = '&limit=30'
    market = '&market=NO'
    url = url_base + artists + genres + tracks + market + limit
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    lst = []
    for track in json_result:
        lst.append((track['id'], track['name']))
    return lst


def get_all_genres(token):
    url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return tuple(json_result['genres'])


def get_all_regions(token):
    url = 'https://api.spotify.com/v1/markets'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


token = get_token()
