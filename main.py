from pyyoutube import Api
api = Api(api_key="AIzaSyAzZR0LzXftjb_xh6fTwz9wZerWlEJO590")
import requests
from flask import Flask, render_template, request
import logging
import json
import urllib
import urllib.request
import urllib.error
import urllib.parse
import jinja2
import os


app = Flask(__name__)


def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print(url)
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print(url)
        print("Reason: ", e.reason)
    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/getresponse")
def data():
    checkbox = request.args.getlist("act_type")
    app.logger.info(f"This is the output: {checkbox}")
    activitylist = []
    name = request.args.get("username")
    for i in range(len(checkbox)):
        if checkbox[i] == "surpriseme":
            response = requests.get("http://www.boredapi.com/api/activity/").json()
            activity = "Activity: " + response['activity'] + " || Activity type: " + response['type']
            activitylist.append(activity)
        else:
            response = requests.get(f"http://www.boredapi.com/api/activity?type={checkbox[i]}").json()
            activity = "Activity: " + response['activity'] + " || Activity type: " + response['type']
            activitylist.append(activity)

    print(activitylist)
    return render_template("output.html", activitylist = activitylist, name = name)

@app.route("/getvideos")
def videos():
    query = request.args.get("playlist")
    listp = []
    r = api.search_by_keywords(q= query, search_type=["playlist"], count=5, limit=5)
    print(r.items)
    base_url = "https://www.youtube.com/embed/videoseries?list="
    for result in r.items:
        id = result.id.playlistId
        playlist_url = base_url + id
        listp.append(playlist_url)
        print(result.id.playlistId)
    app.logger.info(listp)
    return render_template("videos.html", lists=listp)
    # return listp


def main():
    r = api.search_by_keywords(q="surfing", search_type=["playlist"], count=5, limit=5)
    print(r.items)
    base_url = "https://www.youtube.com/playlist?list="
    for result in r.items:
        print(result.id.playlistId)
    for result in r.items:
        print(result.id.playlistId)

    # 1. Create search with q="key term", returns a list of search results
    # 2. For every search result, you can get the video ID by doing SearchResult.id.videoId
    # 3. Append video ID to base_url, and return that to user

# r.items is returned from r = api.search_by_keywords
# Video ID: r.items.id.videoID
# Playlist ID: r.items.id.playlistID


# Returns a link to a video in a playlist
# https://www.youtube.com/watch?v=VuNIsY6JdUw&list=PLdnEKz0ib5DD8X0JeJ9MgbTLKNESWNlRe
# Base url: https://www.youtube.com/watch?v=
# Video ID: VuNIsY6JdUw
# Combinor: &list=
# Playlist ID: PLdnEKz0ib5DD8X0JeJ9MgbTLKNESWNlRe

# Returns a link to a playlist, no video playing
# https://www.youtube.com/playlist?list=PLXDU_eVOJTx4vCcmQ5aqU78pyGCOK_tqY
# Base url: https://www.youtube.com/playlist?list=
# Playlist ID: PLXDU_eVOJTx4vCcmQ5aqU78pyGCOK_tqY

if __name__ == '__main__':
    main()
    app.run(host="localhost", port=8080, debug=True)
