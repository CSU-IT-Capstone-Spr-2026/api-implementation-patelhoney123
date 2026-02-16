
"""
XKCD Comic Viewer - Starter Code + Features
Features implemented:
1) Navigation (Previous/Next)
2) Search by Comic Number
"""

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

XKCD_BASE_URL = "https://xkcd.com"


def get_latest_comic():
    """Fetch the most recent XKCD comic from the API and return dict or None."""
    try:
        response = requests.get(f"{XKCD_BASE_URL}/info.0.json", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None


def get_comic_by_number(comic_num):
    """Fetch a specific XKCD comic by its number and return dict or None."""
    try:
        response = requests.get(f"{XKCD_BASE_URL}/{comic_num}/info.0.json", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None


@app.route("/")
def index():
    # Home page: show latest comic
    latest = get_latest_comic()
    if latest:
        latest_num = latest.get("num", 1)
        return render_template("index.html", comic=latest, error=None, latest_num=latest_num)

    return render_template(
        "index.html",
        comic=None,
        error="Sorry, we couldn't fetch the latest comic right now. Please try again later.",
        latest_num=1
    )


@app.route("/comic/<int:comic_num>")
def show_comic(comic_num):
    # Always get latest num so we can validate and disable Next button
    latest = get_latest_comic()
    latest_num = latest.get("num", 1) if latest else 1

    # Validate comic number
    if comic_num < 1 or comic_num > latest_num:
        return render_template(
            "index.html",
            comic=None,
            error=f"Invalid comic number. Please enter a number between 1 and {latest_num}.",
            latest_num=latest_num
        )

    comic = get_comic_by_number(comic_num)

    if comic:
        return render_template("index.html", comic=comic, error=None, latest_num=latest_num)

    return render_template(
        "index.html",
        comic=None,
        error=f"Comic #{comic_num} could not be found. It may not exist (some numbers return 404).",
        latest_num=latest_num
    )


@app.route("/comic")
def search_comic():
    # Search form uses query string: /comic?comic_num=123
    comic_num = request.args.get("comic_num", "").strip()

    latest = get_latest_comic()
    latest_num = latest.get("num", 1) if latest else 1

    if not comic_num.isdigit():
        return render_template(
            "index.html",
            comic=latest if latest else None,
            error="Please enter a valid comic number (numbers only).",
            latest_num=latest_num
        )

    num = int(comic_num)

    if num < 1 or num > latest_num:
        return render_template(
            "index.html",
            comic=latest if latest else None,
            error=f"Invalid comic number. Please enter a number between 1 and {latest_num}.",
            latest_num=latest_num
        )

    # Reuse show_comic logic
    return show_comic(num)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
