import base64
import os.path

from werkzeug.utils import secure_filename
from flask import Blueprint, send_file, url_for, request, render_template, flash, redirect
from app.api.models import Music
from app.extensions import db
from flask_login import login_required

blueprint = Blueprint("api", __name__, url_prefix="/music")


@blueprint.route("/songlist")
def getAllSong():
    # get all song name and images name from database and send back
    song_list = []
    data = Music.query.all()
    for item in data:
        with open(f"./app/static/images/{item.image}", 'rb') as file:
            img = file.read()
        song_list.append(
            {
                "name": item.name,
                "artist": item.artist,
                "coverImg": str(base64.b64encode(img))
            }
        )
    return song_list

@blueprint.route("/<string:song_name>")
def getMusic(song_name):
    file_path = os.path.join("app", "static", "audios", song_name)
    file = os.path.isfile(file_path)
    print(file)
    if file:
        return send_file(f"./static/audios/{song_name}")
    else:
        return {"error": "File not found"}, 404

    # with open(f"./assets/{song_name}", "rb") as file:
    #     song = file.read()
    # return {
    #     "file": str(base64.b64encode(song))
    # }

@blueprint.route("/insert", methods=["POST"])
@login_required
def insertMusic():
    name = request.form.get("name")
    cover_image = request.files["cover_image"]
    song = request.files["song"]
    artist = request.form.get("artist")
    print(f"{name} | {cover_image.filename} | {song.filename}")
    if cover_image is None or song is None or name is None or artist is None:
        flash('Some field is empty')
        return redirect(url_for("user.home"))

    song_file_name = secure_filename(song.filename)
    cover_image_file_name = secure_filename(cover_image.filename)
    song.save(os.path.join("./app/static/audios", song_file_name))
    cover_image.save(os.path.join("./app/static/images", cover_image_file_name))

    new_music = Music(name=name, image=cover_image_file_name, song=song_file_name, artist=artist)
    db.session.add(new_music)
    db.session.commit()

    flash('Song insert success')
    return redirect(url_for("user.home"))




