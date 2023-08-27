import sys
from datetime import date, timedelta
import db_func as dbf

# original parameters (Jay-Z, Kanye, Bigger Stronger blabla)
# artist_params = ["5K4W6rqBFWDnAN6FQUkS6x", "3nFkdlSjzX9mRTtwJOzDYB"]
# track_params = ["0j2T0R9dR9qdJYsB7ciXhf"]
# genre_params = ["hip-hop"]

artist_params = ["1bgoHMYkNqVC9PTOrQECts", "7oPftvlwr6VrsViSDV7fJY"]
track_params = ["3EzFY9Rg0PpbADMth746zi", "2sIWM1FzNqLCccNwXuC4SA"]
genre_params = ["indie"]

today = date.today()

try:
    days = []
    for i in range(int(sys.argv[1])):
        day = today - timedelta(i)
        days.append(str(day))
        dbf.fetch_day(day, artist_params, track_params, genre_params)
    print(f"Songs for {', '.join(days)} successfully collected.")
except IndexError:
    dbf.fetch_day(today, artist_params, track_params, genre_params)
    print(f"Songs for {str(today)} successfully collected.")

dbf.cnx.commit()
dbf.cnx.close()
