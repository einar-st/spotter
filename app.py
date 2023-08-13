from flask import Flask, render_template
import db_func as dbf
from datetime import date, datetime, timedelta

app = Flask(__name__)


def get_artist_names_from_track(id):
    dbf.cursor.execute(
        f"\
        SELECT artist.name\
        FROM artist\
        INNER JOIN track_artist ON artist.artist_id = track_artist.artist_id\
        WHERE track_artist.track_id = '{id}';\
        "
    )
    artist_names = [item[0] for item in dbf.cursor.fetchall()]

    return ", ".join(artist_names)


def get_tracks_from_date(date_val):
    dbf.cursor.execute(
        f"\
        SELECT track_date.track_id, track.name\
        FROM track_date\
        INNER JOIN track ON track_date.track_id = track.track_id\
        WHERE track_date.date = '{date_val}';\
        "
    )

    tracks = dbf.cursor.fetchall()

    dbf.cnx.commit()

    lines = []

    # create list of artists connected to song
    for track in tracks:
        lines.append(
            get_artist_names_from_track(track[0])
            + " - "
            + str(track[1])
        )
        pass

    if lines == []:
        return ["No track recommendations for this date"]

    return lines


@app.route("/")
def front():
    return from_date(str(date.today()))


@app.route("/<sel_date>")
def from_date(sel_date):
    lines = []
    lines = get_tracks_from_date(sel_date)
    one_day = timedelta(1)
    today = datetime.strptime(str(date.today()), "%Y-%m-%d")
    current_day = datetime.strptime(sel_date, "%Y-%m-%d")
    if current_day == today:
        next_day = ""
    else:
        next_day = datetime.strftime(current_day + one_day, "%Y-%m-%d")
    return render_template(
        "index.html",
        header=sel_date,
        lines=lines,
        previous=datetime.strftime(current_day - one_day, "%Y-%m-%d"),
        next=next_day,
    )
