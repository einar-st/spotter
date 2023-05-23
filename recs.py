import spot_func as spf

parameters = spf.select_args(spf.token)

# for type in parameters.values():
#     print(','.join(type))

recommendations = spf.get_recommendations(
    spf.token,
    ','.join(parameters['artist']),
    ','.join(parameters['track']),
    ','.join(parameters['genre'])
)

for i, item in enumerate(recommendations, 1):
    artist_list = []
    for artist in item['artists']:
        artist_list.append(artist['name'])
        artists = ', '.join(artist_list)

    print(f'{i}. {artists} - {item["name"]}')
