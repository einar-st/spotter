from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content_Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search(token, query, type):
    url_base = "https://api.spotify.com/v1/search"
    params = f"?q={query}&type={type}&limit=10"
    url = url_base + params
    headers = get_auth_header(token)
    json_object = get(url, headers=headers)
    result = json.loads(json_object.content)[f"{type}s"]["items"]

    try:
        return result
    except IndexError:
        print("No result found")

    return None


def select_args(token):
    def add_item(token, type):
        query = input("Enter search: ")
        search_obj = search(token, query, type)

        item_ids = []

        for i, item in enumerate(search_obj, 1):
            artist_name = ""
            if type == "track":
                artist_name = item["artists"][0]["name"] + " - "
            else:
                # for 'artist' return first hit if direct match
                if i == 1 and query.lower() == item["name"].lower():
                    return item["id"]
            print(f"{i}. {item['id']} {artist_name}{item['name']}")
            item_ids.append(item["id"])

        pick = int(input("Select item: "))

        return item_ids[pick - 1]

    result = {"artist": [], "track": [], "genre": []}
    genres = None

    while True:
        print("- Add parameter -")
        print("1. Artist 2. Track 3. Genre 4. Valid genres")
        add_type = int(input("Select : "))
        print("")

        s_type = {1: "artist", 2: "track"}
        if add_type in (1, 2):
            result[s_type[add_type]].append(add_item(token, s_type[add_type]))
        elif add_type == 3:
            genre = input("Enter genre: ")
            if genres is None:
                genres = get_all_genres(token)
            if genre in genres:
                result["genre"].append(genre)
            else:
                print(f"{genre} not a valid genre. Pick one of the following.")
                print(genres)
        elif add_type == 4:
            if genres is None:
                genres = get_all_genres(token)
            print(genres)
        elif add_type == 5:
            break

        print("")
        print(result)  # return tuple of artists, tracks, genres
        print("")

    return result


def get_object(token, id, type):
    url = f"https://api.spotify.com/v1/{type}s/{id}"
    headers = get_auth_header(token)
    json_object = get(url, headers=headers)
    object = json.loads(json_object.content)
    return object


def get_audio_features(token, id):
    url = f"https://api.spotify.com/v1/audio-features/{id}"
    headers = get_auth_header(token)
    json_object = get(url, headers=headers)
    object = json.loads(json_object.content)
    return object


def print_track_info(token, track_id):
    # assign objects
    track = get_object(token, track_id, "track")
    # album and track objects do not contain genre info
    album = get_object(token, track["album"]["id"], "album")
    artists = []
    for artist in track["artists"]:
        artists.append(get_object(token, artist["id"], "artist"))

    print("------")
    print("Track:")
    print("ID: ", track["id"])
    print("Name: ", track["name"])
    for i, artist in enumerate(artists, 1):
        if len(artists) > 1:
            print("")
            print(f" Artist {i}:")
        else:
            print("")
            print(" Artist:")
        print(" ID: ", artist["id"])
        print(" Name: ", artist["name"])
        print(" Genres: ", ", ".join(artist["genres"]))
    print("")
    print(" Album:")
    print(" ID:", album["id"])
    print(" Name: ", album["name"])
    print(" Genres: ", ", ".join(album["genres"]))
    print("------")


def get_songs_by_artist(token, artist_id):
    url = (
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=NO"
    )
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def get_recommendations(token, artists: str, genres: str, tracks: str):
    url_base = "https://api.spotify.com/v1/recommendations"
    artists = f"?seed_artists={artists}"
    genres = f"&seed_genres={genres}"
    tracks = f"&seed_tracks={tracks}"
    limit = "&limit=25"
    market = "&market=NO"
    url = url_base + artists + genres + tracks + market + limit
    headers = get_auth_header(token)
    json_object = get(url, headers=headers)
    result = json.loads(json_object.content)["tracks"]

    return result


def get_all_genres(token):
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return tuple(json_result["genres"])


def get_all_regions(token):
    url = "https://api.spotify.com/v1/markets"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


token = get_token()
